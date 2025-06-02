import requests
from services.weather_api import create_3hour_schedule, get_weather_condition
from services.places_api import search_places_by_categories
from utils.helpers import build_route, get_city_coordinates


def main():
    city = input("Hangi şehri gezmek istiyorsunuz? (örn: Istanbul, Berlin, Paris): ").strip()

    if not city:
        print("Lütfen geçerli bir şehir ismi girin.")
        return

    while True:
        try:
            days = int(input("Kaç günlük plan istiyorsunuz? (1-5): "))
            if 1 <= days <= 5:
                break
            else:
                print("Lütfen 1-5 arasında bir sayı girin.")
        except ValueError:
            print("Lütfen geçerli bir sayı girin.")

    print(f"\n🌍 {city} için {days} günlük akıllı gezi planı hazırlanıyor...\n")

    start_lat, start_lon = get_city_coordinates(city)
    print(f"📍 Başlangıç koordinatları: {start_lat}, {start_lon}\n")

    schedule = create_3hour_schedule(city, days=days)

    if not schedule:
        print("❌ Hava durumu bilgisi alınamadı.")
        return

    all_places = []
    used_place_ids = set()

    for slot in schedule:
        print(f"⏰ {slot['time_display']} | 🌡️ {slot['temperature']}°C | ☁️ {slot['weather']}")

        places = search_places_by_categories(
            city,
            slot['recommended_categories'],
            limit=10,
            coordinates=(start_lat, start_lon)
        )

        if places:
            selected_place = None

            for place in places:
                place_id = f"{place.get('name', '')}-{place.get('location', {}).get('formatted_address', '')}"

                if place_id not in used_place_ids:
                    selected_place = place
                    used_place_ids.add(place_id)
                    break

            if selected_place:
                slot['places'] = [selected_place]
                all_places.append(selected_place)

                name = selected_place.get('name', 'Bilinmeyen Yer')
                address = selected_place.get('location', {}).get('formatted_address', 'Adres yok')

                print(f"  📍 {name}")
                print(f"     📍 {address}")

                if 'geocodes' in selected_place and 'main' in selected_place['geocodes']:
                    lat = selected_place['geocodes']['main'].get('latitude')
                    lng = selected_place['geocodes']['main'].get('longitude')
                    if lat and lng:
                        print(f"     🌐 {lat:.4f}, {lng:.4f}")

                if 'rating' in selected_place:
                    print(f"     ⭐ {selected_place['rating']}")

                if 'categories' in selected_place and selected_place['categories']:
                    category_name = selected_place['categories'][0].get('name', '')
                    if category_name:
                        print(f"     🏷️ {category_name}")
            else:
                print(f"  ❌ Bu zaman dilimi için yeni yer bulunamadı (tümü zaten seçilmiş).")

        else:
            print(f"  ❌ Bu zaman dilimi için yer bulunamadı.")

        print()

    if all_places:
        print("\n🗺️ GENEL ROTA ÖZETİ:")
        print("=" * 50)

        print(f"📍 Başlangıç konumu: {city} ({start_lat}, {start_lon})\n")

        try:
            route = build_route(all_places, start_lat, start_lon)

            for i, place in enumerate(route):
                name = place.get('name', 'Bilinmeyen Yer')
                address = place.get('location', {}).get('formatted_address', 'Adres yok')

                print(f"{i + 1}. {name}")
                print(f"   📍 {address}")

                if 'geocodes' in place and 'main' in place['geocodes']:
                    lat = place['geocodes']['main'].get('latitude')
                    lng = place['geocodes']['main'].get('longitude')
                    if lat and lng:
                        print(f"   🌐 {lat:.4f}, {lng:.4f}")

                if 'rating' in place:
                    print(f"   ⭐ {place['rating']}")

                if 'categories' in place and place['categories']:
                    category_name = place['categories'][0].get('name', '')
                    if category_name:
                        print(f"   🏷️ {category_name}")
                print()
        except Exception as e:
            print(f"❌ Rota oluşturulurken hata: {e}")
            print("Basit liste halinde:")
            for i, place in enumerate(all_places):
                name = place.get('name', 'Bilinmeyen Yer')
                print(f"{i + 1}. {name}")
    else:
        print("❌ Hiç mekan bulunamadı.")

    print("✨ İyi geziler!")


if __name__ == "__main__":
    main()