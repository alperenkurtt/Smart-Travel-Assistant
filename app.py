from flask import Flask, request, render_template, jsonify
from services.weather_api import create_3hour_schedule
from services.places_api import search_places_by_categories
from utils.helpers import build_route, get_city_coordinates
import traceback

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create-plan', methods=['POST'])
def create_plan():
    try:
        data = request.get_json()
        city = data.get('city', '').strip()
        days = int(data.get('days', 2))

        if not city:
            return jsonify({'error': 'Şehir ismi gerekli'}), 400

        if not (1 <= days <= 5):
            return jsonify({'error': 'Gün sayısı 1-5 arasında olmalı'}), 400

        start_lat, start_lon = get_city_coordinates(city)
        print(f"🌍 {city} koordinatları: {start_lat}, {start_lon}")

        schedule = create_3hour_schedule(city, days=days)

        if not schedule:
            return jsonify({'error': 'Hava durumu bilgisi alınamadı'}), 500

        enhanced_schedule = []
        all_places = []
        used_place_ids = set()

        for slot in schedule:
            places = search_places_by_categories(
                city,
                slot['recommended_categories'],
                limit=15,
                coordinates=(start_lat, start_lon)
            )

            print(f"Slot {slot.get('time_display', '')}: {len(places)} mekan bulundu")
            if places:
                print(f"İlk mekanın geocodes bilgisi: {places[0].get('geocodes', 'YOK')}")

            selected_place = None
            if places:
                for place in places:
                    place_id = f"{place.get('name', '')}-{place.get('location', {}).get('formatted_address', '')}"

                    if place_id not in used_place_ids:
                        selected_place = place
                        used_place_ids.add(place_id)
                        break

                if selected_place:
                    lat, lng = None, None

                    if 'geocodes' in selected_place:
                        geocodes = selected_place['geocodes']
                        if 'main' in geocodes:
                            lat = geocodes['main'].get('latitude')
                            lng = geocodes['main'].get('longitude')

                    if lat is not None and lng is not None:
                        selected_place['lat'] = lat
                        selected_place['lng'] = lng
                        slot['place'] = selected_place
                        all_places.append(selected_place)
                        print(f"✅ Seçilen mekan: {selected_place.get('name', 'Bilinmeyen')} ({lat}, {lng})")
                    else:
                        print(f"UYARI: {selected_place.get('name', 'Bilinmeyen')} için koordinat bulunamadı")

            enhanced_schedule.append(slot)

        if all_places:
            try:
                route = build_route(all_places, start_lat, start_lon)
                print(f"🗺️ Rota oluşturuldu: {len(route)} mekan")
            except Exception as e:
                print(f"Rota oluşturma hatası: {e}")
        else:
            route = []

        map_data = {
            'city': city,
            'center': {
                'lat': start_lat,
                'lng': start_lon
            },
            'places': [],
            'route_line': []
        }

        map_data['route_line'].append([start_lat, start_lon])

        for i, place in enumerate(route):
            if 'lat' in place and 'lng' in place:
                place_info = {
                    'id': i + 1,
                    'name': place.get('name', 'Bilinmeyen Yer'),
                    'address': place.get('location', {}).get('formatted_address', ''),
                    'lat': place['lat'],
                    'lng': place['lng'],
                    'category': place.get('categories', [{}])[0].get('name', 'Genel') if place.get(
                        'categories') else 'Genel',
                    'rating': place.get('rating', 0),
                    'order': i + 1
                }
                map_data['places'].append(place_info)
                map_data['route_line'].append([place['lat'], place['lng']])

        print(f"📊 Sonuç: {len(all_places)} mekan bulundu, {len(map_data['places'])} haritada gösteriliyor")

        return jsonify({
            'success': True,
            'city': city,
            'days': days,
            'schedule': enhanced_schedule,
            'map_data': map_data,
            'total_places': len(all_places)
        })

    except Exception as e:
        print(f"Error: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': f'Bir hata oluştu: {str(e)}'}), 500


@app.route('/health')
def health():
    return jsonify({'status': 'OK', 'message': 'Smart Travel Assistant is running!'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)