# Projet API RAG LLM

Portfolio AI Engineer : API REST, intégration LLM (Anthropic Claude), et système RAG (Retrieval Augmented Generation).

## Contenu

- **`main.py`** — API REST complète (CRUD liste de courses) construite avec FastAPI et Pydantic.
- **`api_llm.py`** — Endpoint POST qui expose Claude via API, avec system prompt personnalisable.
- **`api_rag.py`** — Système RAG complet : indexation d'un document, recherche par embeddings (ChromaDB + sentence-transformers), génération de réponses sourcées via Claude.

## Stack technique

- Python 3.11
- FastAPI / Pydantic
- Anthropic Claude API
- ChromaDB (base vectorielle)
- sentence-transformers (embeddings)

## Lancer le projet

```bash
# Installer les dépendances
pip install fastapi uvicorn anthropic chromadb sentence-transformers

# Définir la clé API Anthropic
export ANTHROPIC_API_KEY="votre-cle-api"

# Lancer une des APIs
uvicorn api_rag:app --reload
```

Accéder à la documentation interactive sur `http://127.0.0.1:8000/docs`.

## Auteur

Antoine Renouard
