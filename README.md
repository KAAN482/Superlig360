# Süper Lig 360 ⚽

<div align="center">

**Türkiye Süper Lig için Modern Analitik Dashboard**

[![Website](https://img.shields.io/badge/🌐_Website-Canlı_Demo-blue?style=for-the-badge)](https://kaan482.github.io/Superlig360/)
[![GitHub](https://img.shields.io/badge/📦_GitHub-Repo-black?style=for-the-badge)](https://github.com/KAAN482/Superlig360)

</div>

---

## 📸 Ekran Görüntüleri

| Puan Durumu | İstatistikler | Fikstür |
|-------------|---------------|---------|
| UEFA bölgeleri renk kodlu | Gol/Asist krallığı | AI maç tahminleri |
| Son 5 maç formu | Kart istatistikleri | Takım formları |

---

## ✨ Özellikler

### 🏆 Puan Durumu
- 18 takımın güncel sıralaması
- **UEFA Bölgeleri:**
  - 🔵 Şampiyonlar Ligi (1. sıra)
  - 🟠 Avrupa Ligi (2-3. sıra)
  - 🟢 Konferans Ligi (4-5. sıra)
  - 🔴 Küme düşme (16-18. sıra)
- Son 5 maç formu (G/B/M rozetleri)

### 📊 İstatistikler
- ⚽ **Gol Krallığı** - En golcü 7 oyuncu
- 🅰️ **Asist Krallığı** - En çok asist yapan 6 oyuncu
- 🟡 **Sarı Kartlar** - Top 5
- 🔴 **Kırmızı Kartlar** - Top 5

### 📅 Fikstür & AI Tahmin
- Haftalık maç programı
- Her takımın son 5 maç formu
- 🤖 **AI Destekli Tahminler:**
  - Puan durumu analizi
  - Form skoru hesaplama
  - Ev sahibi avantajı (%15)
  - Güven yüzdesi

### 🎨 Dinamik Tasarım
- Her sekme için farklı arka plan görseli
- Glassmorphism efektleri
- Responsive mobil tasarım
- Yumuşak geçiş animasyonları

---

## 🔄 Tek Tuşla Güncelleme

### Kurulum
```bash
pip install selenium webdriver-manager
```

### Çalıştırma
```bash
python update_weekly.py
```

### Terminal Çıktısı
```
==================================================
⚽ SÜPER LİG 360 - OTOMATİK GÜNCELLEME
📅 2026-01-17 00:00:00
==================================================

[00:00:01] 📌 Chrome driver başlatılıyor...
[00:00:03] ✅ Chrome driver hazır
[00:00:04] 📌 Puan durumu çekiliyor...
[00:00:05]    1. Galatasaray - 42 puan
[00:00:05]    2. Fenerbahçe - 39 puan
[00:00:05]    3. Trabzonspor - 35 puan
           ...
[00:00:10] ✅ 18 takım verisi alındı
[00:00:11] 📌 Gol Krallığı verileri çekiliyor...
[00:00:12] ✅ 7 Gol Krallığı verisi alındı
[00:00:13] 📌 Asist Krallığı verileri çekiliyor...
[00:00:14] ✅ 6 Asist Krallığı verisi alındı
[00:00:15] 📌 Sarı Kart verileri çekiliyor...
[00:00:16] ✅ 5 Sarı Kart verisi alındı
[00:00:17] 📌 Kırmızı Kart verileri çekiliyor...
[00:00:18] ✅ 5 Kırmızı Kart verisi alındı
==================================================
✅ TÜM VERİLER ÇEKİLDİ
==================================================

[00:00:19] 📌 web/app.js güncelleniyor...
[00:00:19] ✅ Puan durumu güncellendi
[00:00:19] ✅ Gol krallığı güncellendi
[00:00:20] ✅ web/app.js başarıyla güncellendi
[00:00:21] 📌 GitHub'a gönderiliyor...
[00:00:21] ✅ Dosyalar eklendi
[00:00:22] ✅ Commit: Otomatik güncelleme - 2026-01-17 00:00
[00:00:25] ✅ Push başarılı!

==================================================
🏁 GÜNCELLEME TAMAMLANDI
🌐 Website: https://kaan482.github.io/Superlig360/
==================================================
```

### Güncelleme Akışı

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Google'dan     │ ──▶ │   web/app.js    │ ──▶ │    GitHub       │
│  Veri Çek       │     │   Güncelle      │     │    Push         │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
   • Puan durumu           • REAL_STANDINGS       • Otomatik commit
   • Gol krallığı          • TOP_SCORERS          • GitHub Actions
   • Asist krallığı        • TOP_ASSISTS          • Website deploy
   • Kartlar               • YELLOW/RED_CARDS
```

---

## 🛠️ Teknoloji Stack

| Kategori | Teknoloji |
|----------|-----------|
| **Frontend** | HTML5, CSS3, JavaScript (ES6+) |
| **Styling** | Glassmorphism, CSS Grid, Flexbox |
| **Scraping** | Python 3, Selenium, webdriver-manager |
| **Database** | PostgreSQL (Docker) |
| **Data Transform** | dbt (Data Build Tool) |
| **Deployment** | GitHub Pages, GitHub Actions |
| **Görseller** | Unsplash (Ücretsiz) |

---

## 📁 Proje Yapısı

```
Superlig360/
│
├── 🌐 web/                      # Frontend (Canlı Website)
│   ├── index.html               # Ana sayfa
│   ├── style.css                # Tüm stiller (~800 satır)
│   ├── app.js                   # JavaScript + Veri (~280 satır)
│   ├── api.py                   # Flask API (opsiyonel)
│   └── requirements.txt
│
├── 📊 dashboard/                # Streamlit Dashboard (Opsiyonel)
│   ├── app.py                   # Dashboard uygulaması
│   └── requirements.txt
│
├── 🔍 scraper/                  # Veri Çekme Araçları
│   ├── main.py                  # Ana scraper
│   ├── google_scraper.py        # Google scraper
│   ├── Dockerfile               # Docker yapılandırması
│   └── requirements.txt
│
├── 🗄️ sql/                      # Veritabanı
│   ├── init.sql                 # Tablo oluşturma
│   ├── seed_data.sql            # Örnek veri
│   └── analysis.sql             # Analiz sorguları
│
├── 📈 superlig360_dbt/          # dbt Modelleri
│   ├── dbt_project.yml          # dbt yapılandırması
│   ├── profiles.yml             # Profil ayarları
│   ├── models/                  # Veri modelleri
│   │   └── staging/             # Staging modelleri
│   └── snapshots/               # Geçmiş verileri
│
├── ⚙️ .github/workflows/        # CI/CD
│   └── deploy.yml               # Otomatik deployment
│
├── 🔄 update_weekly.py          # TEK TUŞLA GÜNCELLEME
├── 📖 DOCUMENTATION.txt         # Detaylı dokümantasyon
├── 🐳 docker-compose.yml        # Docker yapılandırması
├── 📋 requirements.txt          # Python bağımlılıkları
└── 📄 README.md                 # Bu dosya
```

---

## 🚀 Kurulum

### Ön Gereksinimler

| Gereksinim | Versiyon | Kontrol Komutu |
|------------|----------|----------------|
| Python | 3.8+ | `python --version` |
| pip | Son sürüm | `pip --version` |
| Git | Son sürüm | `git --version` |
| Chrome | Son sürüm | Tarayıcı |

---

### 1️⃣ Projeyi İndir

```bash
# GitHub'dan klonla
git clone https://github.com/KAAN482/Superlig360.git

# Proje klasörüne gir
cd Superlig360
```

---

### 2️⃣ Requirements Dosyaları

Projede birden fazla `requirements.txt` dosyası var:

| Dosya | İçerik | Kullanım |
|-------|--------|----------|
| `requirements.txt` | Ana bağımlılıklar | `pip install -r requirements.txt` |
| `web/requirements.txt` | Flask API | Web API için |
| `dashboard/requirements.txt` | Streamlit | Dashboard için |
| `scraper/requirements.txt` | Selenium | Scraper için |

**Tüm bağımlılıkları yükle:**
```bash
# Ana bağımlılıklar
pip install -r requirements.txt

# Otomatik güncelleme için (Selenium)
pip install selenium webdriver-manager

# Dashboard için (opsiyonel)
pip install -r dashboard/requirements.txt

# Web API için (opsiyonel)
pip install -r web/requirements.txt
```

**Tek satırda tümü:**
```bash
pip install selenium webdriver-manager streamlit flask psycopg2-binary
```

---

### 3️⃣ Kullanım Senaryoları

#### A) Sadece Website Görüntüleme
```bash
# Tarayıcıda aç (kurulum gerektirmez)
start web/index.html      # Windows
open web/index.html       # Mac
xdg-open web/index.html   # Linux
```

#### B) Otomatik Veri Güncelleme
```bash
# 1. Selenium yükle
pip install selenium webdriver-manager

# 2. Script'i çalıştır
python update_weekly.py

# Bu işlem:
# - Google'dan verileri çeker
# - web/app.js dosyasını günceller
# - GitHub'a push eder
```

#### C) Streamlit Dashboard
```bash
# 1. Bağımlılıkları yükle
pip install -r dashboard/requirements.txt

# 2. Dashboard'u başlat
streamlit run dashboard/app.py

# Tarayıcıda: http://localhost:8501
```

#### D) Flask API
```bash
# 1. Bağımlılıkları yükle
pip install -r web/requirements.txt

# 2. API'yi başlat
python web/api.py

# API: http://localhost:5000
```

#### E) Full Stack (PostgreSQL + dbt)
```bash
# 1. Docker Desktop'ı başlat

# 2. Veritabanını başlat
docker-compose up -d

# 3. Veritabanı bağlantısını kontrol et
# Host: localhost, Port: 5432
# Database: superlig360, User: postgres

# 4. dbt kurulumu
pip install dbt-postgres
cd superlig360_dbt
dbt deps      # Paketleri indir
dbt run       # Modelleri çalıştır
dbt test      # Testleri çalıştır
```

---

### 4️⃣ Doğrulama

Kurulumu doğrula:
```bash
# Python sürümü
python --version

# Selenium yüklü mü?
python -c "import selenium; print('Selenium OK')"

# Chrome driver test
python -c "from selenium import webdriver; print('WebDriver OK')"
```

---

### 5️⃣ Hızlı Başlangıç (TL;DR)

```bash
# 1. Klonla
git clone https://github.com/KAAN482/Superlig360.git
cd Superlig360

# 2. Selenium yükle
pip install selenium webdriver-manager

# 3. Verileri güncelle
python update_weekly.py

# 4. Website'i aç
start web/index.html
```

---

## 🤖 AI Tahmin Sistemi

```
Tahmin Formülü:
─────────────────────────────────────────────

Ev Gücü = (PPG × 10 + Form Skoru + Averaj) × 1.15
Deplasman Gücü = PPG × 10 + Form Skoru + Averaj

PPG = Toplam Puan ÷ Oynanan Maç
Form Skoru = Son 5 maç (ağırlıklı)
Averaj = (Atılan - Yenilen) ÷ Oynanan Maç

Form Ağırlıkları: [1.0, 1.2, 1.4, 1.6, 2.0]
  Galibiyet = 3 puan × ağırlık
  Beraberlik = 1 puan × ağırlık
  Mağlubiyet = 0 puan

Karar:
  Fark > 4    → Ev sahibi (%60-85)
  Fark < -4   → Deplasman (%60-85)
  -4 < Fark < 4 → Beraberlik (%45)
```

---

## 📖 Dokümantasyon

Detaylı kullanım kılavuzu: [`DOCUMENTATION.txt`](DOCUMENTATION.txt)

İçerik:
- Proje hakkında
- Tüm özellikler
- Veri yapıları
- AI tahmin sistemi
- Sorun giderme
- Geliştirme rehberi

---

## 📝 Lisans

MIT License © 2026 KAAN482

---

<div align="center">

**⚽ Süper Lig 360**

[Website](https://kaan482.github.io/Superlig360/) • [GitHub](https://github.com/KAAN482/Superlig360) • [Dokümantasyon](DOCUMENTATION.txt)

</div>
