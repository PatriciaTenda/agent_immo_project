# Importer les librairies nécessires
from langchain.tools import tool
from dataclasses import dataclass
import requests

# ------ format des données en entrée----
@dataclass
class Bien():
    surface: float
    address: str
    type: str


# -------- fonction de geolocalisation-----
@tool
def geocode_address(address: str)->dict:
    """
    Geocode the address of a property and return its coordinates.

    :param bien: Property description containing at least the address.
    :return: Coordinates [longitude, latitude] and HTTP status code.
    """

    url = "https://data.geopf.fr/geocodage/search"
   
    params: dict[str, str] = {
        "q": address,
        "limit": "2",
        "autocomplete": "1",
    }

    try:
        res = requests.get(
            url,
            params,
            timeout=10
        )
        res.raise_for_status

        data = res.json()
        features = data.get("features", [])
        if not features:
            return {
               "coordinates" : None,
               "status_code" : res.status_code,
               "error" : "Acun résultat trouvé pour cet adresse" 
            }
        
        coordinates = res.json().get('features')[0].get('geometry').get('coordinates')
        return {
            "coordinates" : coordinates,
            "status_code" : res.status_code
        }
    
    except requests.RequestException as e:
        return {
               "coordinates" : None,
               "status_code" : None,
               "error" : str(e)
        }