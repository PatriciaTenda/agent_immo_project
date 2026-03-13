# Imports des librairies nécessaires
from fastapi import FastAPI
from pathlib import Path
from agent.agent_servive import agent_run
from typing import Any
from .schemas.agent_schemas import AgentResponse, AgentRequest
from langchain_core.messages import AIMessage
import sys

# configuration du chemin vers le point d'entrée de l'application
root_path = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root_path))

# création de l'application FastAPI
app = FastAPI()

# Route de base pour vérifier l'application
@app.get("/")
def home():
    return { "message": "Bienvenue dans l'API de l'agent immobilier!"}


@app.post("/agent", response_model = AgentResponse)
def run_agent_endpoint(payload: AgentRequest)-> AgentResponse:
    """
        Endpoint pour exécuter l'agent immobilier avec une requête utilisateur.

        Args:
        user_query (str): Question ou demande de l'utilisateur adressée à l'agent.

        Returns:
        dict: Réponse générée par l'agent contenant l'historique des messages
        et la réponse finale du modèle.    
    """
    response = agent_run(payload.content)
    messages: list[Any]  = response.get("messages") or response.get("input") or []
    answer = ""
    for message in reversed(messages):
        if isinstance(message, AIMessage):
            answer = getattr(message, "content", "")
            break
    
    return AgentResponse(response = answer)


