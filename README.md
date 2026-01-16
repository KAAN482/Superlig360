# Süper Lig 360 ⚽

Türkiye Süper Lig için modern ve kapsamlı bir analitik dashboard.

🌐 **Canlı Demo:** [https://kaan482.github.io/Superlig360/](https://kaan482.github.io/Superlig360/)

---

## ✨ Özellikler

| Özellik | Açıklama |
|---------|----------|
| 📊 **Puan Durumu** | 18 takımın güncel sıralaması, UEFA bölgeleri renk kodlu |
| 📈 **İstatistikler** | Gol/Asist krallığı, Sarı/Kırmızı kart sıralaması |
| 📅 **Fikstür** | Haftalık maç programı + AI tahminleri |
| 🎨 **Dinamik Tasarım** | Her sekme için farklı arka plan görseli |
| 🤖 **AI Tahmin** | Form ve puana dayalı maç tahminleri |

---

## 🔄 Otomatik Güncelleme Sistemi

### Kurulum

```bash
# Selenium ve webdriver-manager yükle
pip install selenium webdriver-manager
```

### Kullanım

```bash
python update_weekly.py
```

### Script Ne Yapar?

```
[00:00:01] 📌 Chrome driver başlatılıyor...
[00:00:03] ✅ Chrome driver hazır
[00:00:04] 📌 Puan durumu çekiliyor...
[00:00:05]    1. Galatasaray - 42 puan
[00:00:05]    2. Fenerbahçe - 39 puan
           ...
[00:00:10] ✅ 18 takım verisi alındı
[00:00:11] 📌 Gol Krallığı verileri çekiliyor...
[00:00:12] ✅ 7 Gol Krallığı verisi alındı
           ...
[00:00:20] 📌 web/app.js güncelleniyor...
[00:00:20] ✅ Puan durumu güncellendi
[00:00:20] ✅ Gol krallığı güncellendi
[00:00:21] 📌 GitHub'a gönderiliyor...
[00:00:22] ✅ Push başarılı!

🏁 GÜNCELLEME TAMAMLANDI
🌐 Website: https://kaan482.github.io/Superlig360/
```

### Çekilen Veriler

| Veri | Kaynak | Güncellenen Dosya |
|------|--------|-------------------|
| Puan durumu | Google | `web/app.js` → `REAL_STANDINGS` |
| Gol krallığı | Google | `web/app.js` → `TOP_SCORERS` |
| Asist krallığı | Google | `web/app.js` → `TOP_ASSISTS` |
| Sarı kartlar | Google | `web/app.js` → `YELLOW_CARDS` |
| Kırmızı kartlar | Google | `web/app.js` → `RED_CARDS` |

---

## 🛠️ Teknolojiler

| Kategori | Teknoloji |
|----------|-----------|
| Frontend | HTML, CSS, JavaScript |
| Scraping | Python, Selenium |
| Deployment | GitHub Pages, GitHub Actions |
| Görseller | Unsplash |

---

## 📁 Proje Yapısı

```
Superlig360/
├── web/
│   ├── index.html          # Ana sayfa
│   ├── style.css           # Stiller
│   └── app.js              # JavaScript + Veriler
├── update_weekly.py        # 🔄 Otomatik güncelleme scripti
├── DOCUMENTATION.txt       # 📖 Detaylı dokümantasyon
├── .github/workflows/      # CI/CD
└── README.md
```

---

## 🚀 Hızlı Başlangıç

```bash
# 1. Klonla
git clone https://github.com/KAAN482/Superlig360.git
cd Superlig360

# 2. Bağımlılıkları yükle (opsiyonel, scraping için)
pip install selenium webdriver-manager

# 3. Güncelle ve deploy et
python update_weekly.py
```

---

## 📖 Dokümantasyon

Detaylı dokümantasyon için: [`DOCUMENTATION.txt`](DOCUMENTATION.txt)

---

**Geliştirici:** KAAN482  
**Lisans:** MIT
