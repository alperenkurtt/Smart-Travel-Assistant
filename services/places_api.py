# Foursquare
from config.settings import PLACES_API_KEY, DEFAULT_CITY
import requests


def get_place_data(query):
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

    fsq_id = data["results"][0]["fsq_id"]
    detail_url = f"https://api.foursquare.com/v3/places/{fsq_id}"
    detail_response = requests.get(detail_url, headers=headers)
    detail_data = detail_response.json()

    return detail_data


def search_places_by_categories(query, category_ids, limit=10, coordinates=None):
    """
    Şehir ismine veya koordinatlara göre, belirli kategorilerde gezilecek yerleri Foursquare'dan getirir.
    Mekanların açık/kapalı saatleri bilgisini de ekler.

    Args:
        query: Şehir ismi
        category_ids: Kategori ID'leri listesi
        limit: Maksimum sonuç sayısı
        coordinates: (lat, lng) tuple - Eğer verilirse koordinat kullanılır, yoksa şehir ismi
    """
    url = "https://api.foursquare.com/v3/places/search"
    headers = {
        "accept": "application/json",
        "Authorization": PLACES_API_KEY
    }

    if coordinates and len(coordinates) == 2:
        near_param = f"{coordinates[0]},{coordinates[1]}"
        print(f"🔍 Koordinat ile arama yapılıyor: {near_param}")
    else:
        near_param = query
        print(f"🔍 Şehir ismi ile arama yapılıyor: {near_param}")

    params = {
        "near": near_param,
        "categories": ",".join(category_ids),
        "limit": limit,
        "sort": "RELEVANCE"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        results = response.json()
        places = results.get("results", [])

        return places

    except requests.exceptions.RequestException as e:
        print(f"API hatası: {e}")
        return []


def get_place_details_with_hours(fsq_id):
    """
    Belirli bir mekanın detaylı bilgilerini (özellikle açık/kapalı saatleri) getirir.
    """
    url = f"https://api.foursquare.com/v3/places/{fsq_id}"
    headers = {
        "accept": "application/json",
        "Authorization": PLACES_API_KEY
    }

    params = {
        "fields": "name,location,geocodes,hours,categories,rating,description"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Mekan detay hatası ({fsq_id}): {e}")
        return None


def is_place_open_at_hour(place_hours, target_hour):
    """
    Mekanın belirli saatte açık olup olmadığını kontrol eder.

    Args:
        place_hours: Foursquare'dan gelen hours bilgisi
        target_hour: Kontrol edilmek istenen saat (0-23)

    Returns:
        bool: Açıksa True, kapalıysa False, bilgi yoksa None
    """
    if not place_hours or 'regular' not in place_hours:
        return None  # Saat bilgisi yok

    # Güncel günün hangi gün olduğunu bul (0=Pazartesi, 6=Pazar)
    from datetime import datetime
    today = datetime.now().weekday()  # 0=Monday, 6=Sunday

    # Foursquare format: 1=Monday, 7=Sunday
    foursquare_day = today + 1 if today < 6 else 7

    regular_hours = place_hours.get('regular', [])

    for day_hours in regular_hours:
        if day_hours.get('day') == foursquare_day:
            if 'open' not in day_hours or 'close' not in day_hours:
                return None

            open_time = day_hours['open']
            close_time = day_hours['close']

            # "0900" -> 9
            open_hour = int(open_time[:2])
            close_hour = int(close_time[:2])

            if close_hour < open_hour:
                return target_hour >= open_hour or target_hour <= close_hour
            else:
                return open_hour <= target_hour <= close_hour

    return None


def filter_places_by_time(places, target_hour):
    """
    Verilen saatte açık olan mekanları filtreler.
    """
    open_places = []

    for place in places:
        hours_info = place.get('hours', {})
        is_open = is_place_open_at_hour(hours_info, target_hour)

        if is_open is True or is_open is None:
            # Mekanın açık olup olmadığı bilgisini ekle
            place['is_open_at_target_time'] = is_open
            place['target_hour'] = target_hour
            open_places.append(place)

    return open_places