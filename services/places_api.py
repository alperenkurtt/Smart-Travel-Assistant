# Foursquare
from config.settings import PLACES_API_KEY, DEFAULT_CITY
import requests

def get_place_data(query):
    # 1. Arama yap
    search_url = "https://api.foursquare.com/v3/places/search"
    headers = {
        "accept": "application/json",
        "Authorization": PLACES_API_KEY
    }
    params = {
        "query": query,
        "limit": 1
    }

    response = requests.get(search_url, headers=headers, params=params)
    data = response.json()

    if not data.get("results"):
        print("Yer bulunamadı.")
        return None

    # 2. fsq_id al ve detayları çek
    fsq_id = data["results"][0]["fsq_id"]
    detail_url = f"https://api.foursquare.com/v3/places/{fsq_id}"
    detail_response = requests.get(detail_url, headers=headers)
    detail_data = detail_response.json()

    return detail_data

def search_places_by_categories(query, category_ids, limit=10):
    """
    Şehir ismine göre, belirli kategorilerde gezilecek yerleri Foursquare'dan getirir.
    """
    url = "https://api.foursquare.com/v3/places/search"
    headers = {
        "accept": "application/json",
        "Authorization": PLACES_API_KEY
    }

    params = {
        "near": query,
        "categories": ",".join(category_ids),
        "limit": limit,
        "sort": "RELEVANCE"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        results = response.json()
        return results.get("results", [])
    else:
        print("API hatası:", response.status_code, response.text)
        return []

