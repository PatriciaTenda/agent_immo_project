import pandas as pd

df = pd.read_parquet("data_immobiliere_loiret.parquet")



def moyenne_prix_bien_selon_surface_habitable(surface_habitable_souhaite, type_souhaite, communes_souhaite):  
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

    type_souhaite est une liste de chaînes de caractères. Elle peut être vide ou contenir :
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
    df = pd.read_parquet("data_immobiliere_loiret.parquet")

    if surface_habitable_souhaite['min'] == False:
        surface_habitable_souhaite['min'] = 1 
    if surface_habitable_souhaite['max'] == False:
        surface_habitable_souhaite['max'] = 100000

    results = []
    for commune in communes_souhaite:
        df_ = df[(df["Surface reelle bati"] > surface_habitable_souhaite['min']) & (df["Surface reelle bati"] < surface_habitable_souhaite['max'])]
        if len(type_souhaite) > 0:
            df_1 = df_[df['Type local'].isin(values=type_souhaite)]
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



