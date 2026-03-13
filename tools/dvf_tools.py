"""
    L'utilisateur peut fournir plusieurs informations : 
    - une surface habitable souhaitée,
    - un ou plusieurs types de logement,
    - une ou plusieurs communes d'intérêt.

    surface_habitable_souhaitee est un dictionnaire contenant deux clés : 'min' et 'max'.
    Les cas possibles sont :
    - si l'utilisateur connaît uniquement une surface minimale : {'min': x, 'max': False}
    - si l'utilisateur connaît uniquement une surface maximale : {'min': False, 'max': x}
    - si l'utilisateur ne mentionne aucune surface : {'min': False, 'max': False}
    - si l'utilisateur donne une surface idéale unique : {'min': x - 1, 'max': x + 1}

    type_souhaite est une liste de chaînes de caractères. 
    Elle peut être vide ou contenir :
    - 'Local industriel, commercial ou assimilé'
    - 'Maison'
    - 'Dépendance'
    - 'Appartement'

    communes_souhaitees est une liste de codes postaux. Par exemple :
    - [45130, 45100, 45000]
    Si l'utilisateur fournit un nom de ville, tous les codes postaux associés doivent être ajoutés à la liste.
    (Les données sont limitées au département du Loiret.)

    Le résultat de cette fonction est une liste de dictionnaires.  
    Pour chaque commune, on obtient :
    - le code postal,
    - le prix minimum,
    - le prix maximum,
    - le prix moyen,
    - le coefficient de variation.

    Cette fonction permet d'estimer le prix moyen en fonction des caractéristiques fournies par l'utilisateur.
    """

# ---- imports des librairies nécessaires ----
import pandas as pd
import sys
from pathlib import Path
from langchain.tools import tool


# Ajouter le chemin du dossier parent au sys.path
current_dir = Path(__file__).resolve().parents[1]
docs_dir = current_dir / "docs"
sys.path.insert(0, str(docs_dir))
data_immo_path = docs_dir / "data_immobiliere_loiret.parquet"


# ---- function to calculate the average price of a property based on the habitable surface, type and location ----
@tool
def moyenne_prix_bien_selon_surface_habitable(surface_habitable_souhaite, type_souhaite, communes_souhaite) -> list[dict[str, float | int | str]]:  
    """
        Cette fonction permet de calculer le prix moyen d'un bien immobilier en fonction de la surface habitable souhaitée, du type de logement et des communes d'intérêt fournies par l'utilisateur.
        
        args: 
        - surface_habitable_souhaite : un dictionnaire contenant les clés 'min' et 'max' pour la surface habitable souhaitée.
        - type_souhaite : une liste de types de logement souhaités.
        - communes_souhaite : une liste de codes postaux des communes d'intérêt.

        returns:
        - une liste de dictionnaires contenant les statistiques pour chaque commune.
    """
    # ---- load data from data repository  ----
    df = pd.read_parquet(data_immo_path)

    # ---- gerer les cas où l'utilisateur ne fournit pas de surface habitable minimale ou maximale ----
    if not surface_habitable_souhaite['min']:
        surface_habitable_souhaite['min'] = 1 
    if not surface_habitable_souhaite['max']:
        surface_habitable_souhaite['max'] = 100000

    # ---- filtrer les données en fonction des critères de l'utilisateur et calculer les statistiques pour chaque commune ----
    results = []
    for commune in communes_souhaite:
        df_ = df[(df["Surface reelle bati"] > surface_habitable_souhaite['min']) & (df["Surface reelle bati"] < surface_habitable_souhaite['max'])]
        if len(type_souhaite) > 0:
            df_1 = df_[df_['Type local'].isin(values=type_souhaite)]
        else:
            df_1=df_
        df_2 = df_1[df_1['Code postal']== commune]
        df_2['Valeur fonciere'] = df_2['Valeur fonciere'].str.replace(',','.').astype(float)
        df_mean = df_2['Valeur fonciere'].mean()
        df_std = df_2['Valeur fonciere'].std()
        df_cv = df_std / df_mean * 100
        df_max = df_2['Valeur fonciere'].max()
        df_min = df_2['Valeur fonciere'].min()
    
        result = {
            'commune': commune,
            'max' : df_max,
            'min' : df_min,
            'mean': df_mean,
            'cv' : df_cv
        }
        results.append(result)
    return results



if __name__ == "__main__" :
    surface_habitable_souhaite = {'min': 50, 'max': 100}
    type_souhaite = ['Maison', 'Appartement']
    communes_souhaite = [45130, 45100, 45000]
    print(moyenne_prix_bien_selon_surface_habitable.invoke({'surface_habitable_souhaite': surface_habitable_souhaite, 'type_souhaite': type_souhaite, 'communes_souhaite': communes_souhaite}))