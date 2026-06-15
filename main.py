from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

app = FastAPI()

@app.get("/")

def racine():
    return{"message": "Mon API tourne"}

# PATH PARAMETER : le prénom est DANS l'URL
# Ex : /salut/Antoine → {"message": "Salut Antoine"}
@app.get("/salut/{prenom}")
def saluer(prenom: str):
    return {"message":f"Salut {prenom}"}


# QUERY PARAMETERS : les valeurs passent APRÈS un ?
# Ex : /addition?a=3&b=7 → {"resultat": 10}
@app.get("/addition")
def additionner(a: int, b: int):
    return{"resultat":a+b}

class Utilisateur(BaseModel):
    nom: str
    age: int

@app.post("/Utilisateur")
def creer_utilisateur(user: Utilisateur):
    return {"message": f"{user.nom} ({user.age} ans) créé"}

class Produit(BaseModel):
    nom: str
    prix: int
    en_stock: bool

@app.post("/Produit")
def creer_produit(product: Produit):
    return {"message": f"{product.nom} ({product.prix} euros, dispo : {product.en_stock}) "}

class Article(BaseModel):
    name: str
    quantity: int
    priority:str

articles=[]

@app.post("/articles")
def ajouter_articles(article: Article):
    articles.append(article)
    return {"message": f"{article.name} a été ajouté quantité ({article.quantity} ) "}

@app.delete("/articles/{index}")
def supp_articles(index: int):
    if index < len(articles):
        article=articles.pop(index)
        return {"message": f"l'article : {article.name }a été supprimé "}
    raise HTTPException(status_code=404, detail=f"Aucun article à l'index {index}")


@app.get("/articles")
def lister_articles(priority: str = None):
    if priority:
        resultat=[a for a in articles if a.priority == priority]
        return {"liste de courses": resultat}
    return{"liste de courses":articles}

@app.get("/articles/{index}")
def lire_article(index: int):
    if index < len(articles):
        return {"articles":articles[index]}
    raise HTTPException(status_code=404, detail=f"Aucun article à l'index {index}")
