# noqa
# Import des librairies
import os
from typing import Any, Sequence, Callable
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.tools import BaseTool
from tools.estimate_surface_tools import estimate_surface
from tools.geocode_tools import geocode_address
from llm.llm_service import llm_model, PROMPT_SYSTEM
from tools.dvf_tools import moyenne_prix_bien_selon_surface_habitable

# ----- Charger les variables d'environnement à partir du fichier .env -----
load_dotenv()

# ----- enable automated tracing of your model calls, set the LangSmith API key ------
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
if "LANGSMITH_API_KEY" not in os.environ:
   raise ValueError("La variable d'environnement LANGSMITH_API_KEY est introuvable.")
os.environ["LANGSMITH_TRACING"] = "true"

# ---- define tools for agent-----
tools: Sequence[BaseTool | Callable[..., Any] | dict[str, Any]] = [estimate_surface, geocode_address, moyenne_prix_bien_selon_surface_habitable]

# ----- agent ------
agent = create_agent(
    model = llm_model,
    tools= tools,
    system_prompt=PROMPT_SYSTEM
)

# -------- Fonction d'exécution de l'agent IA  framework langchain--------
def agent_run(user_query:str)->dict[str, Any]:
    """
        Invoque l'agent LangChain avec une requête utilisateur.

    Args:
        user_query (str): Question ou demande de l'utilisateur adressée à l'agent.

    Returns:
        dict: Réponse générée par l'agent contenant l'historique des messages
        et la réponse finale du modèle.
    
    """
    try:
            response = agent.invoke(
                {
                    "messages": [
                        {"role" : "user",
                        "content" : user_query,
                        }
                    ]
                }
            )
        
            return response
    except Exception as e:
            return {"error" : e}
        
if __name__ == "__main__":
    question = """
        Tu dois obligatoirement utiliser les 3 tools suivants dans cet ordre, sans en sauter aucun :

        geocode_address
        estimate_surface
        moyenne_prix_bien_selon_surface_habitable
        Contexte utilisateur :

        Budget : 250000 euros
        Adresse à géocoder : 10 rue de Rivoli, Paris
        Frais inclus : true
        Prix moyen au m2 à utiliser pour l'estimation : 9800
        Paramètres imposés pour le tool DVF :

        surface_habitable_souhaite = {"min": 20, "max": 30}
        type_souhaite = ["Appartement", "Maison"]
        communes_souhaite = [45000, 45100, 45130]
        Consignes de sortie :

        Section 1 : résultat géocodage (coordonnées + statut)
        Section 2 : surface estimée avec la formule utilisée
        Section 3 : résultat DVF par commune (min, max, mean, cv)
        Section 4 : conclusion conseil immobilier synthétique
        Important :

        N'invente aucun résultat tool.
        Si un tool échoue, affiche clairement l'erreur mais continue avec les autres tools si possible.
    """
    result = agent_run(question)
    print(result)

    