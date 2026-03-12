# noqa
# Import des librairies
import sys
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# ajouter la racine du projet au path
root_path = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root_path))

from langchain_mistralai import ChatMistralAI

# ---- define a system prompt-----
PROMPT_SYSTEM = """
    Tu es un assistant spécialisé en conseil immobilier.
    Tu aides les agents immobiliers à analyser les demandes de leurs clients.

    Tu peux utiliser les outils disponibles pour estimer une surface, récupérer
    des informations de marché ou compléter ton analyse.

    Consignes :
    - Réponds de manière claire, structurée et professionnelle.
    - Si des informations sont manquantes, signale-le explicitement.
    - Utilise les tools seulement lorsqu'ils sont pertinents.
    - Donne une réponse utile pour la prise de décision immobilière.
"""


# instantiate our model object and generate chat completions
llm_model =ChatMistralAI(
    name="mistral-large-latest",
    temperature=0,
    max_retries=2
)
