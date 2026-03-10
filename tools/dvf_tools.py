# Importer les librairies nécessaires
from pathlib import Path
import sys
from langchain.tools import tool

# configuration du chemin vers le module des tools
root_path = Path(__file__).resolve().parents[0]
print(root_path)
sys.path.insert(0,str(root_path))

# ------- fonction d'estimation de la surface d'un bien------
@tool
def estimate_surface(budget: float, include_fees: bool, price_per_m2: float)-> float:

    """
            Calcule la surface estimée d'un bien immobilier en fonction du budget et du prix moyen au m².

    Args:
        budget (float): Budget total disponible pour l'achat.
        include_fees (bool): Indique si les frais d'acquisition doivent être pris en compte.
        price_per_m2 (float): Prix moyen au mètre carré du marché immobilier.

    Returns:
        dict: Un dictionnaire contenant :
            - budget (float): Budget initial.
            - include_fees (bool): Indique si les frais ont été appliqués.
            - price_per_m2 (float): Prix moyen au m² utilisé pour le calcul.
            - estimated_surface (float): Surface estimée du bien en m².
    
    """

    fee_coefficient = 0.92

    if price_per_m2<=0 or budget<=0:
        raise ValueError("Le budget et le prix au mètre carré doit être supérieur à 0")
    
    effective_budget = budget * fee_coefficient if include_fees else budget

    surface = effective_budget/price_per_m2

    return round(surface, 2)
    
    

    




    