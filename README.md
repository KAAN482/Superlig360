# Süper Lig 360 ⚽

Türkiye Süper Lig için modern ve kapsamlı bir analitik dashboard.

🌐 **Canlı Demo:** [https://kaan482.github.io/Superlig360/](https://kaan482.github.io/Superlig360/)

## ✨ Özellikler

### 📊 Puan Durumu
- 18 takımın güncel puan tablosu
- UEFA bölgeleri renk kodlu gösterim (Şampiyonlar Ligi, Avrupa Ligi, Konferans Ligi)
- Küme düşme bölgesi gösterimi
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
  - Puan durumuna göre
  - Son 5 maç performansına göre
  - Averaj ve ev sahibi avantajı hesabı

### 🎨 Dinamik Arayüz
- Her sekme için farklı arka plan gradyanları
- Modern glassmorphism tasarım
- Responsive mobil uyumlu tasarım

## 🚀 Haftalık Güncelleme

Her hafta sonu verileri güncellemek için:

```bash
python update_weekly.py
```

Bu script:
1. Değişiklikleri commit eder
2. GitHub'a push eder
3. Website otomatik olarak güncellenir

## 🛠️ Teknolojiler

- **Frontend:** HTML, CSS, JavaScript (Vanilla)
- **Styling:** Modern CSS (Glassmorphism, Gradients)
- **Deployment:** GitHub Pages + GitHub Actions
- **Data:** Google'dan manuel veri çekimi

## 📁 Proje Yapısı

```
Superlig360/
├── web/                  # Frontend dosyaları
│   ├── index.html        # Ana sayfa
│   ├── style.css         # Stiller
│   └── app.js            # JavaScript
├── dashboard/            # Streamlit dashboard
├── scraper/              # Veri çekme scriptleri
├── sql/                  # Veritabanı şemaları
├── superlig360_dbt/      # DBT modelleri
├── update_weekly.py      # Tek tuşla güncelleme
└── .github/workflows/    # CI/CD
```

## 📝 Lisans

MIT License
