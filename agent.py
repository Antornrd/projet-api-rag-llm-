import os
import anthropic

def compter_occurrences(texte: str, mot: str) -> int:
    return texte.lower().count(mot.lower())

def calculer(expression: str) -> float:
    return eval(expression)

TEXTE = "Le SVM est performant. Le SVM atteint 61% de précision."

outils = [
    {
        "name": "compter_occurrences",
        "description": "Compte combien de fois un mot apparaît dans le texte de référence.",
        "input_schema": {
            "type": "object",
            "properties": {
                "mot": {"type": "string", "description": "Le mot à compter"}
            },
            "required": ["mot"]
        }
    },
    {
        "name": "calculer",
        "description": "Évalue une expression mathématique. Ex: '2+3*4'",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "L'expression à calculer"}
            },
            "required": ["expression"]
        }
    }
]

def executer_outil(nom: str, arguments: dict) -> str:
    if nom == "compter_occurrences":
        return str(compter_occurrences(TEXTE, arguments["mot"]))
    elif nom == "calculer":
        return str(calculer(arguments["expression"]))
    return "Outil inconnu"

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

question = "Dans le texte de référence, combien de fois apparaît SVM, et quel est ce nombre multiplié par 10 ?"

messages = [{"role": "user", "content": question}]

while True:
    reponse = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        tools=outils,
        messages=messages
    )

    print(f"\n--- Stop reason: {reponse.stop_reason} ---")

    if reponse.stop_reason == "tool_use":
        messages.append({"role": "assistant", "content": reponse.content})

        resultats_outils = []
        for bloc in reponse.content:
            if bloc.type == "tool_use":
                print(f"Claude veut appeler: {bloc.name}({bloc.input})")
                resultat = executer_outil(bloc.name, bloc.input)
                print(f"Résultat: {resultat}")
                resultats_outils.append({
                    "type": "tool_result",
                    "tool_use_id": bloc.id,
                    "content": resultat
                })
        messages.append({"role": "user", "content": resultats_outils})
    else:
        for bloc in reponse.content:
            if bloc.type == "text":
                print(f"\n=== RÉPONSE FINALE ===\n{bloc.text}")
        break