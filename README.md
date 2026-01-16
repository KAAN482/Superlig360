# Süper Lig 360 ⚽

Türkiye Süper Lig verilerini görselleştiren modern bir web uygulaması.

## 🚀 Özellikler

- **Puan Durumu**: 18 takımın güncel lig sıralaması
- **İstatistikler**: 
  - ⚽ Gol Krallığı
  - 🅰️ Asist Sıralaması
  - 🟡 Sarı Kart İstatistikleri
  - 🔴 Kırmızı Kart İstatistikleri

## 📦 Teknolojiler

- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Python Flask API
- **Database**: PostgreSQL (Docker)
- **Data Transform**: dbt (Data Build Tool)

## 🛠️ Kurulum

### Gereksinimler
- Docker & Docker Compose
- Python 3.9+
- Node.js (opsiyonel)

### Adımlar

1. **Projeyi klonlayın**
```bash
git clone https://github.com/your-repo/superlig360.git
cd superlig360
```

2. **Docker ile veritabanını başlatın**
```bash
docker-compose up -d
```

3. **Python bağımlılıklarını yükleyin**
```bash
pip install -r requirements.txt
```

4. **Veritabanını başlatın**
```bash
python populate_real_data.py
```

5. **dbt modellerini çalıştırın**
```bash
cd superlig360_dbt
dbt run --profiles-dir .
```

6. **Flask API'yi başlatın**
```bash
python web/api.py
```

7. **Dashboard'u açın**
```
web/index.html dosyasını tarayıcınızda açın
```

## 📁 Proje Yapısı

```
Süperlig360/
├── web/                  # Frontend dosyaları
│   ├── index.html       # Ana dashboard
│   ├── app.js           # JavaScript logic & data
│   ├── style.css        # Stil dosyası
│   └── api.py           # Flask REST API
├── superlig360_dbt/      # dbt projesi
│   └── models/          # SQL modelleri
├── sql/                  # SQL dosyaları
├── scraper/              # Veri çekme scriptleri
├── docker-compose.yml    # Docker config
└── requirements.txt      # Python bağımlılıkları
```

## 📊 Veri Kaynağı

Veriler Google'dan çekilen Trendyol Süper Lig 2025-26 sezonu 17. hafta istatistiklerini içermektedir.

## 📝 Lisans

MIT License

---

**Süper Lig 360** - Türk Futbolunu Verilerle Keşfet ⚽🇹🇷
