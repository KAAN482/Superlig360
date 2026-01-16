# Süper Lig 360 ⚽

Türkiye Süper Lig için modern ve kapsamlı bir analitik dashboard.

🌐 **Canlı Demo:** [https://kaan482.github.io/Superlig360/](https://kaan482.github.io/Superlig360/)

---

## ✨ Özellikler

### 📊 Puan Durumu
- 18 takımın güncel puan tablosu
- UEFA bölgeleri renk kodlu gösterim:
  - 🔵 Şampiyonlar Ligi (1. sıra)
  - 🟠 Avrupa Ligi (2-3. sıra)
  - 🟢 Konferans Ligi (4-5. sıra)
  - 🔴 Küme düşme (16-18. sıra)
- Son 5 maç formu (G/B/M rozetleri)

### 📈 İstatistikler
- **Gol Krallığı** - En çok gol atan oyuncular
- **Asist Krallığı** - En çok asist yapan oyuncular
- **Sarı Kartlar** - En çok sarı kart gören 5 oyuncu
- **Kırmızı Kartlar** - En çok kırmızı kart gören 5 oyuncu

### 📅 Fikstür
- Haftalık maç programı
- Takım formları görsel olarak
- 🤖 **AI Destekli Maç Tahminleri**

### 🎨 Dinamik Arayüz
- Her sekme için farklı arka plan görseli
- Modern glassmorphism tasarım
- Responsive mobil uyumlu tasarım

---

## 🔄 Haftalık Güncelleme Sistemi

Her hafta sonu verileri güncellemek için `update_weekly.py` scripti kullanılır.

### Komutlar

```bash
# Değişiklikleri GitHub'a gönder
python update_weekly.py

# Proje durumunu kontrol et
python update_weekly.py --check

# Güncelleme rehberini göster
python update_weekly.py --guide

# Yardım
python update_weekly.py --help
```

### Güncelleme Adımları

#### 1️⃣ Verileri Topla
Google'da şunları ara:
- `süper lig puan durumu`
- `süper lig gol krallığı`
- `süper lig asist krallığı`
- `süper lig 19. hafta maçları`

#### 2️⃣ web/app.js Dosyasını Güncelle

**Puan Durumu (REAL_STANDINGS):**
```javascript
const REAL_STANDINGS = [
    { 
        rank: 1, 
        team_name: "Galatasaray", 
        played: 17, 
        wins: 13, 
        draws: 3, 
        losses: 1, 
        goals_for: 39, 
        goals_against: 12, 
        goal_diff: 27, 
        points: 42, 
        form: ["G", "B", "G", "G", "G"]  // Son 5 maç
    },
    // ... diğer takımlar
];
```

**Gol Krallığı (TOP_SCORERS):**
```javascript
const TOP_SCORERS = [
    { name: "Oyuncu Adı", team: "Takım", count: 12 },
    // ...
];
```

**Asist Krallığı (TOP_ASSISTS):**
```javascript
const TOP_ASSISTS = [
    { name: "Oyuncu Adı", team: "Takım", count: 7 },
    // ...
];
```

**Kartlar (YELLOW_CARDS, RED_CARDS):**
```javascript
const YELLOW_CARDS = [
    { name: "Oyuncu Adı", team: "Takım", count: 7 },
    // ... (5 oyuncu)
];
```

**Fikstür (FIXTURES):**
```javascript
const FIXTURES = [
    { home: "Ev Sahibi", away: "Deplasman", date: "18 Ocak Paz", time: "20:00" },
    // ...
];
```

#### 3️⃣ Script'i Çalıştır
```bash
python update_weekly.py
```

Script otomatik olarak:
1. Değişiklikleri kontrol eder
2. Git commit oluşturur
3. GitHub'a push eder
4. GitHub Actions website'i günceller

---

## 🛠️ Teknolojiler

| Kategori | Teknoloji |
|----------|-----------|
| Frontend | HTML, CSS, JavaScript (Vanilla) |
| Styling | Modern CSS (Glassmorphism, Gradients) |
| Görseller | Unsplash (Ücretsiz) |
| Deployment | GitHub Pages + GitHub Actions |
| Data | Google'dan manuel veri çekimi |

---

## 📁 Proje Yapısı

```
Superlig360/
├── web/                      # Frontend dosyaları
│   ├── index.html            # Ana sayfa
│   ├── style.css             # Stiller
│   └── app.js                # JavaScript + Veriler
├── dashboard/                # Streamlit dashboard (opsiyonel)
├── scraper/                  # Veri çekme scriptleri
├── sql/                      # Veritabanı şemaları
├── superlig360_dbt/          # DBT modelleri
├── update_weekly.py          # 🔄 Tek tuşla güncelleme
├── .github/workflows/        # CI/CD (Otomatik deploy)
└── README.md                 # Bu dosya
```

---

## 🚀 Hızlı Başlangıç

```bash
# Projeyi klonla
git clone https://github.com/KAAN482/Superlig360.git
cd Superlig360

# Yerel olarak test et (web/index.html'i tarayıcıda aç)

# Güncelleme yap
python update_weekly.py --check  # Durumu kontrol et
python update_weekly.py          # Push et
```

---

## 📝 Lisans

MIT License

---

**Geliştirici:** KAAN482  
**Website:** [https://kaan482.github.io/Superlig360/](https://kaan482.github.io/Superlig360/)
