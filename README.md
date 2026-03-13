# agent_immo_project
Le projet consiste à développer une  solution d’intelligence artificielle basée sur un agent capable d’interagir avec des outils externes(API, Bases de données, outils spécialisés) afin d’aider les agents immobiliers à faire du conseil immobilier pertinent, rapide et basées sur des données.


# Configuration de l'environnement du projet
 ````bash
    python3.1.. -m venv env
    env/Scripts/activate   
 ````

# Installation des dépendances
 ```bash
    pip freeze > requirements.txt # Fichier requirements.txt à créer avec les dépendances nécessaires
    pip install --upgrade huggingface_hub # librairie pour interagir avec HuggingFace
    pip install fastapi[all] # pour l'API REST ou uvicorn[standard] si vous préférez utiliser uvicorn directement
    pip install fastapi[uvicorn standard] # pour l'API REST
    pip install python-dotenv # pour gérer les variables d'environnement
    pip install -U sentence-transformers # pour la recherche sémantique
    pip install pandas # pour la manipulation des données      
    pip install -U langchain langchain-huggingface huggingface_hub
    pip install -qU langchain-mistralai
    pip install flake8 black   
```