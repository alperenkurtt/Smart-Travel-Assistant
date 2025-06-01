from math import radians, cos, sin, asin, sqrt

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
        # En yakın yeri bul
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
