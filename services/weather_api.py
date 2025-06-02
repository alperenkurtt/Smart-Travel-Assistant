# openweathermap
import requests
from config.settings import WEATHER_API_KEY, DEFAULT_CITY

current_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={DEFAULT_CITY}&units=metric&APPID={WEATHER_API_KEY}")
forecast_data = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={DEFAULT_CITY}&units=metric&appid={WEATHER_API_KEY}")


def get_weather_condition(city):
    """Anlık hava durumu"""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&APPID={WEATHER_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Hava durumu API hatası: {e}")
        return None


def get_weather_forecast(city):
    """5 günlük tahmin (3'er saatlik)"""
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={WEATHER_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Hava tahmini API hatası: {e}")
        return None


def get_recommended_places_by_weather_and_temp(weather_main, temperature):

    outdoor_categories = [
        "16014",  # Park
        "11025",  # Historical Landmark
        "16013",  # Botanical Garden
        "16032",  # Beach / Marina
        "13065",  # Scenic Lookout
        "16019",  # Plaza
        "16027",  # Sculpture Garden
        "16003",  # Bridge
        "16011",  # Monument
    ]

    indoor_categories = [
        "10027",  # Museum
        "10032",  # Art Gallery
        "10033",  # Science Museum
        "12001",  # Aquarium
        "12012",  # Library
        "17069",  # Shopping Mall
        "12040",  # Convention Center
        "10003",  # Art Museum
        "10019",  # History Museum
    ]

    food_categories = [
        "13003",  # Café
        "13031",  # Restaurant
        "13002",  # Bakery
        "13040",  # Fast Food
        "13035",  # Ice Cream Shop
        "13008",  # Brewery
    ]

    cool_weather_categories = food_categories + indoor_categories[:4]
    hot_weather_categories = indoor_categories + ["16032"]

    if weather_main.lower() in ["rain", "thunderstorm", "drizzle", "snow"]:
        return indoor_categories[:6]

    elif temperature < 10:
        return cool_weather_categories[:6]

    elif temperature > 30:
        return hot_weather_categories[:6]

    elif 10 <= temperature <= 25:
        mixed = outdoor_categories[:3] + indoor_categories[:2] + food_categories[:2]
        return mixed

    else:
        return outdoor_categories[:5] + food_categories[:2]


def create_3hour_schedule(city, days=2):
    forecast_data = get_weather_forecast(city)
    if not forecast_data:
        return None

    schedule = []
    slot_number = 1

    for forecast in forecast_data['list']:
        datetime_str = forecast['dt_txt']
        hour = int(datetime_str.split(' ')[1].split(':')[0])

        if not (9 <= hour <= 21):
            continue

        if slot_number > days * 5:
            break

        weather_main = forecast['weather'][0]['main']
        temperature = forecast['main']['temp']

        categories = get_recommended_places_by_weather_and_temp(weather_main, temperature)

        time_display = f"{hour:02d}:00 - {(hour + 3):02d}:00"

        schedule.append({
            'time_slot': datetime_str,
            'time_display': time_display,
            'weather': weather_main,
            'temperature': temperature,
            'recommended_categories': categories,
            'slot_number': slot_number,
            'hour': hour
        })

        slot_number += 1

    return schedule