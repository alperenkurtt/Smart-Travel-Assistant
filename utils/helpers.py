from math import radians, cos, sin, asin, sqrt
from config.settings import PLACES_API_KEY
import requests

def haversine(lon1, lat1, lon2, lat2):
    """
    İki enlem-boylam arasındaki mesafeyi kilometre cinsinden hesaplar.
    """
    # Dereceden radyana dönüşüm
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    km = 6371 * c
    return km

def build_route(places, start_lat, start_lon):
    """
    Verilen yer listesini, başlangıç konumuna göre en yakın olandan başlayarak sıralar.
    """
    remaining = places.copy()
    route = []
    current_lat = start_lat
    current_lon = start_lon

    while remaining:
        closest = min(
            remaining,
            key=lambda place: haversine(
                current_lon,
                current_lat,
                place['geocodes']['main']['longitude'],
                place['geocodes']['main']['latitude']
            )
        )
        route.append(closest)
        current_lat = closest['geocodes']['main']['latitude']
        current_lon = closest['geocodes']['main']['longitude']
        remaining.remove(closest)

    return route

def get_city_coordinates_old(city):
    """Şehir koordinatlarını tahmin eder"""
    city_coords = {
        'istanbul': (41.0082, 28.9784),
        'berlin': (52.5200, 13.4050),
        'paris': (48.8566, 2.3522),
        'london': (51.5074, -0.1278),
        'rome': (41.9028, 12.4964),
        'madrid': (40.4168, -3.7038),
        'amsterdam': (52.3676, 4.9041),
        'vienna': (48.2082, 16.3738),
        'prague': (50.0755, 14.4378),
        'barcelona': (41.3851, 2.1734),
        'athens': (37.9755, 23.7348),
        'budapest': (47.4979, 19.0402),
        'venice': (45.4408, 12.3155),
        'florence': (43.7696, 11.2558),
        'lisbon': (38.7223, -9.1393),
        'moscow': (55.7558, 37.6176),
        'stockholm': (59.3293, 18.0686),
    }

    city_lower = city.lower()
    return city_coords.get(city_lower, (41.0082, 28.9784))


def get_city_coordinates(city):
    url = "https://api.foursquare.com/v3/places/search"
    headers = {
        "accept": "application/json",
        "Authorization": PLACES_API_KEY
    }
    params = {
        "near": city,
        "categories": "16014",
        "limit": 1
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        if data.get("results") and len(data["results"]) > 0:
            place = data["results"][0]
            if 'geocodes' in place and 'main' in place['geocodes']:
                lat = place['geocodes']['main']['latitude']
                lng = place['geocodes']['main']['longitude']
                return (lat, lng)
    except:
        pass

    city_coords = {
        'istanbul': (41.0082, 28.9784),
        'berlin': (52.5200, 13.4050),
        'paris': (48.8566, 2.3522),
        'london': (51.5074, -0.1278),
        'rome': (41.9028, 12.4964),
        'madrid': (40.4168, -3.7038),
        'amsterdam': (52.3676, 4.9041),
        'vienna': (48.2082, 16.3738),
        'prague': (50.0755, 14.4378),
        'barcelona': (41.3851, 2.1734),
        'athens': (37.9755, 23.7348),
        'budapest': (47.4979, 19.0402),
        'venice': (45.4408, 12.3155),
        'florence': (43.7696, 11.2558),
        'lisbon': (38.7223, -9.1393),
        'moscow': (55.7558, 37.6176),
        'stockholm': (59.3293, 18.0686),
    }

    city_lower = city.lower()
    return city_coords.get(city_lower, (41.0082, 28.9784))