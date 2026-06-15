from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import anthropic
import os
import chromadb
from sentence_transformers import SentenceTransformer

app = FastAPI()


#charger le doc
with open("documents/prediction_foot.txt", "r") as f:
    text=f.read()
#decouper en chunks
#on decoupe par paragraphes (double saut de ligne)

# 2. DÉCOUPER en chunks (tous les 500 caractères)
taille = 500
chunks = [text[i:i+taille] for i in range(0, len(text), taille)]
chunks = [c.strip() for c in chunks if len(c.strip()) > 50]
print(f"{len(chunks)} chunks créés")
#creer les embeddings et stocker dans ChromaDB
embedder= SentenceTransformer("all-MiniLM-L6-v2")
db=chromadb.Client()


collection= db.create_collection("football")
collection.add(
    documents=chunks,
    ids=[f"chunk_{i}"for i in range(len(chunks))]
)

client_llm= anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
#1 le modele pydantic - qu'est ce que le client envoie ?
class Question(BaseModel):
    question: str
    role: str = "tu réponds uniquement en te basant sur le contexte fourni. Si l'information n'est pas dans le contexte, dis-le."

#2 la route post
@app.post("/ask")
def poser_question(q: Question):
    #chercher les chunks pertinents

    resultats= collection.query(
    query_texts=[q.question],
    n_results=3
)
    contexte= "\n\n".join(resultats["documents"][0])
    message = client_llm.messages.create(
     model="claude-haiku-4-5-20251001",
    max_tokens=200,
    system=q.role,
    messages=[
        {"role": "user", "content": f"Contexte:\n{contexte}\n\nQuestion :{q.question}" }
    ]
)
    reponse=message.content[0].text
    return {"reponse": reponse}
