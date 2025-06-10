# 🌍 Smart Travel Assistant (Akıllı Seyahat Asistanı)

Hava durumuna göre kişiselleştirilmiş seyahat planları oluşturan akıllı web uygulaması.

## 📋 Proje Hakkında

Smart Travel Assistant, kullanıcıların belirttiği şehir ve gün sayısına göre hava durumu tahminlerini analiz ederek en uygun gezilecek yerleri öneren bir sistemdir. Uygulama, hava koşullarına göre kapalı/açık alan aktiviteleri önerir ve optimize edilmiş rotalar oluşturur.

## ✨ Özellikler

- **🌤️ Hava Durumu Tabanlı Planlama**: OpenWeatherMap API kullanarak 5 günlük hava tahminlerine göre aktivite önerileri
- **📍 Akıllı Mekan Önerileri**: Foursquare API ile şehirdeki gezilecek yerleri bulma
- **🗺️ İnteraktif Harita**: Leaflet.js ile önerilen rotayı harita üzerinde görüntüleme
- **⏰ 3 Saatlik Zaman Dilimleri**: Gün boyunca 3'er saatlik optimum aktivite planlaması
- **🚶‍♂️ Rota Optimizasyonu**: En kısa mesafe algoritması ile gezilecek yerleri sıralama
- **📱 Responsive Tasarım**: Mobil ve masaüstü uyumlu kullanıcı arayüzü
- **🎯 Dinamik Kategori Seçimi**: Hava durumu ve sıcaklığa göre uygun aktivite kategorileri

### Hava Durumu Bazlı Öneriler

- **☔ Yağışlı Havalar**: Müze, sanat galerisi, kütüphane, alışveriş merkezi
- **🥶 Soğuk Hava (< 10°C)**: Kafe, restoran, kapalı mekanlar
- **🔥 Sıcak Hava (> 30°C)**: Klimalı mekanlar, plaj, marina
- **🌤️ İdeal Hava (10-25°C)**: Park, tarihi mekan, açık alan aktiviteleri

## 🛠️ Kullanılan Teknolojiler

### Backend
- **Python 3.x**
- **Flask** - Web framework
- **Requests** - HTTP istekleri

### Frontend
- **HTML5 & CSS3**
- **Bootstrap 5** - UI framework
- **JavaScript (ES6+)**
- **Leaflet.js** - İnteraktif haritalar
- **Font Awesome** - İkonlar

### API'ler
- **OpenWeatherMap API** - Hava durumu verileri
- **Foursquare API** - Mekan verileri

## 📦 Kurulum

### 1. Projeyi İndirin
```bash
git clone https://github.com/kullaniciadi/smart-travel-assistant.git
cd smart-travel-assistant
```

### 2. Gerekli Paketleri Yükleyin
```bash
pip install flask requests
```

### 3. API Anahtarlarını Ayarlayın

`config/settings.py` dosyasında aşağıdaki API anahtarlarını güncelleyin:

```python
WEATHER_API_KEY = 'your_openweathermap_api_key'
PLACES_API_KEY = 'your_foursquare_api_key'
```

#### API Anahtarları Nasıl Alınır?

**OpenWeatherMap API:**
1. [OpenWeatherMap](https://openweathermap.org/api) adresine gidin
2. Ücretsiz hesap oluşturun
3. API key'inizi alın

**Foursquare API:**
1. [Foursquare Developers](https://developer.foursquare.com/) adresine gidin
2. Uygulama oluşturun
3. API key'inizi alın

### 4. Uygulamayı Çalıştırın

**Web Arayüzü:**
```bash
python app.py
```
Tarayıcınızda `http://localhost:5000` adresine gidin.

**Terminal Arayüzü:**
```bash
python main.py
```

## 🎮 Kullanım

### Web Arayüzü
1. Ana sayfada şehir ismini girin (örn: Istanbul, Berlin, Paris)
2. Gün sayısını seçin (1-5 gün arası)
3. "Plan Oluştur" butonuna tıklayın
4. Oluşturulan rotayı harita ve detaylı program listesinde görüntüleyin

### Terminal Arayüzü
1. Şehir ismini girin
2. Gün sayısını belirtin
3. Önerilen rotayı konsol çıktısında inceleyin

## 📁 Proje Yapısı

```
smart-travel-assistant/
│
├── app.py                    # Flask web uygulaması
├── main.py                   # Terminal tabanlı uygulama
├── requirements.txt          # Python bağımlılıkları
│
├── config/
│   └── settings.py          # API anahtarları ve ayarlar
│
├── services/
│   ├── weather_api.py       # OpenWeatherMap API servisi
│   ├── places_api.py        # Foursquare API servisi
│   └── recommendation.py    # Öneri algoritmaları
│
├── utils/
│   └── helpers.py           # Yardımcı fonksiyonlar
│
└── templates/
    └── index.html           # Ana web sayfası
```

## 🔧 Yapılandırma

### Şehir Koordinatları
`utils/helpers.py` dosyasında popüler şehirlerin koordinatları tanımlıdır. Yeni şehirler ekleyebilirsiniz:

```python
city_coords = {
    'yeni_sehir': (enlem, boylam),
    # ...
}
```

### Kategori Önerileri
`services/weather_api.py` dosyasında hava durumuna göre öneri kategorileri tanımlıdır. Foursquare kategori ID'leriyle yeni kategoriler ekleyebilirsiniz.

## 🌐 API Endpoints

- `GET /` - Ana sayfa
- `POST /create-plan` - Seyahat planı oluşturma
- `GET /health` - Sistem durumu kontrolü

## 🚀 Geliştirme Önerileri

- [ ] Kullanıcı hesap sistemi
- [ ] Plan kaydetme/paylaşma özelliği
- [ ] Daha fazla şehir desteği
- [ ] Mobil uygulama geliştirme
- [ ] AI tabanlı kişiselleştirilmiş öneriler
- [ ] Sosyal medya entegrasyonu
- [ ] Çoklu dil desteği

## 🐛 Bilinen Sorunlar

- Bazı şehirler için koordinat bilgisi bulunamayabilir
- API rate limit'lerine dikkat edilmeli
- Internet bağlantısı gereklidir

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/yeni-ozellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/yeni-ozellik`)
5. Pull Request oluşturun

## 📞 İletişim

- Proje Sahibi: Alperen Kurt
- E-posta: alpereenkurtt@gmail.com

