# noqa
# Import des librairies
import sys
import os
from typing import Any
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


# ajouter la racine du projet au path
root_path = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root_path))

from langchain.agents import create_agent
from tools.dvf_tools import estimate_surface
from tools.geocode_tools import geocode_address
from llm.llm_service import llm_model, PROMPT_SYSTEM


# ----- enable automated tracing of your model calls, set the LangSmith API key ------
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
if "LANGSMITH_API_KEY" not in os.environ:
   raise ValueError("La variable d'environnement LANGSMITH_API_KEY est introuvable.")
os.environ["LANGSMITH_TRACING"] = "true"

# ---- define tools for agent-----
tools = [estimate_surface, geocode_address]

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
    question = "Voici un bien à 250 000 euros situé au 10 rue de Rivoli à Paris, peux-tu localiser l'adresse avant l'analyse et estimer la surface d'un bien à ce prix là dans la meme zone ?"
    result = agent_run(question)
    print(result)