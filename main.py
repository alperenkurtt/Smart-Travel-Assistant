import requests
from config.settings import PLACES_API_KEY, WEATHER_API_KEY
from services.places_api import get_place_data, search_places_by_categories
from services.weather_api import  get_weather_condition, get_recommended_places
from utils.helpers import build_route, haversine

city = "Berlin"

# 1. Hava durumunu al (örnek veriyoruz burada)
weather_data = {"weather": [{"main": "Clear"}]}

# 2. Kategorileri belirle
categories = get_recommended_places(weather_data)

# 3. Foursquare'dan uygun yerleri çek
places = search_places_by_categories(city, categories, limit=10)

# 4. Başlangıç konumu (örneğin şehir merkezi)
start_lat = 41.0082  # Sultanahmet civarı
start_lon = 28.9784

# 5. Rota oluştur
route = build_route(places, start_lat, start_lon)

# 6. Rota yazdır
for i, place in enumerate(route):
    name = place["name"]
    address = place["location"]["formatted_address"]
    print(f"{i+1}. {name} - {address}")
