# openweathermap
from config.settings import WEATHER_API_KEY, DEFAULT_CITY
import requests

current_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={DEFAULT_CITY}&units=metric&APPID={WEATHER_API_KEY}")
forecast_data = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={DEFAULT_CITY}&units=metric&appid={WEATHER_API_KEY}")

def get_weather_condition(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&APPID={WEATHER_API_KEY}"
    response = requests.get(url)
    data = response.json()

    condition = data['weather'][0]['main'].lower()  # örn: "Clear", "Rain", "Clouds"
    return condition

def get_recommended_places(weather_data):
    # Hava durumunu al (örneğin: 'Clear', 'Rain', 'Snow', vs.)
    weather_main = weather_data['weather'][0]['main'].lower()

    # Açık hava kategorileri (güzel havada gezilir)
    outdoor_categories = [
        "16014",  # Park
        "11025",  # Historical Landmark
        "10034",  # Outdoor Museum
        "16013",  # Botanical Garden
        "16032",  # Beach / Marina
    ]

    # Kapalı mekanlar (yağmur, kar vs.)
    indoor_categories = [
        "10027",  # Museum
        "10032",  # Art Gallery
        "10033",  # Science Museum
        "12001",  # Aquarium
        "11025",  # Historical Site (kapalı olabilir)
    ]

    # Karar ver
    if weather_main in ["rain", "thunderstorm", "drizzle", "snow"]:
        return indoor_categories
    else:
        return outdoor_categories




