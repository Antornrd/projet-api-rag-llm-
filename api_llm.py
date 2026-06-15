from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import anthropic
import os
app = FastAPI()

client=anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

#1 le modele pydantic - qu'est ce que le client envoie ?
class Question(BaseModel):
    question: str
    role: str = "Tu es un assistant qui répond en une phrase maximum."


#2 la route post
@app.post("/ask")
def poser_question(q: Question):
    message = client.messages.create(
     model="claude-haiku-4-5-20251001",
    max_tokens=200,
    system=q.role,
    messages=[
        {"role": "user", "content": q.question}
    ]
)
    reponse=message.content[0].text
    return {"reponse": reponse}
