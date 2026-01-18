# Süper Lig 360 ⚽

<div align="center">

**Türkiye Süper Lig için Modern Analitik Dashboard**

[![Website](https://img.shields.io/badge/🌐_Website-Canlı_Demo-blue?style=for-the-badge)](https://kaan482.github.io/Superlig360/)
[![GitHub](https://img.shields.io/badge/📦_GitHub-Repo-black?style=for-the-badge)](https://github.com/KAAN482/Superlig360)

</div>

---

## ✨ Özellikler

### 🏆 Puan Durumu
- 18 takımın güncel sıralaması
- **UEFA Bölgeleri** renk kodlu
- Son 5 maç formu (G/B/M rozetleri)

### 📊 İstatistikler (6 Kategori - FotMob)
| Kategori | Açıklama |
|----------|----------|
| ⚽ **Gol Krallığı** | En çok gol atan 5 oyuncu |
| 🅰️ **Asist Krallığı** | En çok asist yapan 5 oyuncu |
| ⭐ **Rating** | En yüksek FotMob puanı |
| 🧤 **Gol Yemeden** | Kalesini gole kapatan kaleciler |
| 🟡 **Sarı Kartlar** | En çok sarı kart gören 5 oyuncu |
| 🔴 **Kırmızı Kartlar** | En çok kırmızı kart gören 5 oyuncu |

### 📅 Fikstür & AI Tahmin
- Haftalık maç programı
- **Oynanan Maçlar**: Skor görüntülenir (örn: "2 - 1")
- **Oynanacak Maçlar**: Tarih, saat ve AI tahmini
- 🤖 AI destekli maç tahminleri (form ve puan analizine dayalı)

### 🎨 Dinamik Tasarım
- Her sekme için farklı arka plan görseli
- Mobil uyumlu responsive tasarım

---

## 🔄 Otomatik Güncelleme (FotMob)

### Kurulum
```bash
pip install -r requirements.txt
```

### Kullanım
```bash
python update_weekly.py
```

### Veri Kaynakları (FotMob Türkçe)

| Veri | URL |
|------|-----|
| Puan Durumu | fotmob.com/tr/leagues/71/table/super-lig |
| Gol Krallığı | fotmob.com/.../players/goals/super-lig |
| Asist | fotmob.com/.../players/goal_assist/super-lig |
| Rating | fotmob.com/.../players/rating/super-lig |
| Gol Yemeden | fotmob.com/.../players/clean_sheet/super-lig |
| Sarı Kart | fotmob.com/.../players/yellow_card/super-lig |
| Kırmızı Kart | fotmob.com/.../players/red_card/super-lig |

### Terminal Çıktısı
```
==================================================
⚽ SÜPER LİG 360 - OTOMATİK GÜNCELLEME
📅 2026-01-17 01:08:56
📊 Veri Kaynağı: FotMob (Türkçe)
==================================================
[01:08:56] ℹ️  Otomatik scraping modu (FotMob)

==================================================
[01:08:56] 📌 VERİ ÇEKME İŞLEMİ BAŞLADI (FotMob)
==================================================
[01:08:56] 📌 Chrome driver başlatılıyor...
[01:09:03] ✅ Chrome driver hazır
[01:09:03] 📌 Puan durumu çekiliyor...
[01:09:08] ✅ 18 takım verisi alındı
[01:09:08] 📌 Gol Krallığı verileri çekiliyor...
[01:09:12] ✅ 5 Gol Krallığı verisi alındı
...
==================================================
[01:10:30] ✅ VERİ ÇEKME TAMAMLANDI (9/9 başarılı)
==================================================

[01:10:30] 📌 web/app.js güncelleniyor...
[01:10:30] ✅ web/app.js başarıyla güncellendi
[01:10:31] 📌 GitHub'a gönderiliyor...
[01:10:35] ✅ Push başarılı!

==================================================
🏁 GÜNCELLEME TAMAMLANDI
🌐 Website: https://kaan482.github.io/Superlig360/
==================================================
```

---

## 📁 Proje Yapısı

```
Superlig360/
├── web/                      # Frontend
│   ├── index.html            # Ana sayfa
│   ├── style.css             # Stiller
│   └── app.js                # JavaScript + Veri
├── update_weekly.py          # 🔄 FotMob Scraper
├── DOCUMENTATION.txt         # 📖 Detaylı dokümantasyon
├── README.md                 # Bu dosya
└── .github/workflows/        # CI/CD
```

---

## 🚀 Hızlı Başlangıç

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

## 📖 Dokümantasyon

Detaylı kullanım: [`DOCUMENTATION.txt`](DOCUMENTATION.txt)

---

**Geliştirici:** KAAN482  
**Lisans:** MIT  
**Veri Kaynağı:** [FotMob](https://www.fotmob.com)
