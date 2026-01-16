"""
Süper Lig 360 - FotMob Veri Güncelleme Scripti
==============================================

Tek tuşla:
1. FotMob'dan güncel verileri çeker (Selenium)
2. web/app.js dosyasını otomatik günceller
3. GitHub'a push eder

Kullanım:
  python update_weekly.py

Gereksinimler:
  pip install selenium webdriver-manager
"""

import os
import sys
import re
import json
import time
from datetime import datetime
from pathlib import Path

# Selenium imports
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

import subprocess

# Proje dizini
PROJECT_DIR = Path(__file__).parent

# FotMob URL'leri (Türkçe)
FOTMOB_BASE = "https://www.fotmob.com/tr/leagues/71"
FOTMOB_URLS = {
    'tablo': f"{FOTMOB_BASE}/table/super-lig",
    'fikstur': f"{FOTMOB_BASE}/fixtures/super-lig?group=by-round",
    'stats': f"{FOTMOB_BASE}/stats/super-lig",
    # Detaylı istatistik sayfaları
    'goller': f"{FOTMOB_BASE}/stats/season/27244/players/goals/super-lig",
    'asistler': f"{FOTMOB_BASE}/stats/season/27244/players/goal_assist/super-lig",
    'rating': f"{FOTMOB_BASE}/stats/season/27244/players/rating/super-lig",
    'kacirilan': f"{FOTMOB_BASE}/stats/season/27244/players/big_chance_missed/super-lig",
    'gol_yemeden': f"{FOTMOB_BASE}/stats/season/27244/players/clean_sheet/super-lig",
    'sari_kart': f"{FOTMOB_BASE}/stats/season/27244/players/yellow_card/super-lig",
    'kirmizi_kart': f"{FOTMOB_BASE}/stats/season/27244/players/red_card/super-lig"
}

# Takım ID -> Türkçe İsim eşleştirmesi
TAKIM_SOZLUGU = {
    "1933": "Başakşehir",
    "3061": "Galatasaray",
    "3057": "Fenerbahçe",
    "3058": "Beşiktaş",
    "3056": "Trabzonspor",
    "3060": "Göztepe",
    "3063": "Konyaspor",
    "3064": "Rizespor",
    "3065": "Alanyaspor",
    "3066": "Gaziantep FK",
    "3067": "Hatayspor",
    "3069": "Antalyaspor",
    "3073": "Kasımpaşa",
    "3074": "Samsunspor",
    "3075": "Kocaelispor",
    "3077": "Kayserispor",
    "3079": "Karagümrük",
    "1054": "Gençlerbirliği",
    "3059": "Eyüpspor",
    "7496": "Bodrum FK"
}

# ============================================================
# LOGGING (Sadece Terminal - Türkçe)
# ============================================================

def log(mesaj, seviye="INFO"):
    """Terminale log yaz"""
    zaman = datetime.now().strftime('%H:%M:%S')
    semboller = {
        "INFO": "ℹ️ ",
        "SUCCESS": "✅",
        "ERROR": "❌",
        "WARNING": "⚠️ ",
        "STEP": "📌"
    }
    sembol = semboller.get(seviye, "")
    print(f"[{zaman}] {sembol} {mesaj}")

# ============================================================
# FOTMOB SCRAPER
# ============================================================

class FotMobScraper:
    """FotMob'dan Süper Lig verilerini çeken scraper"""
    
    def __init__(self):
        self.driver = None
        self.takim_eslestirme = {}
        self.veri = {
            'puan_durumu': [],
            'gol_kralligi': [],
            'asist_kralligi': [],
            'en_iyi_rating': [],
            'kacirilan_firsatlar': [],
            'gol_yemeden': [],
            'sari_kartlar': [],
            'kirmizi_kartlar': [],
            'fikstur': []
        }
    
    def driver_baslat(self):
        """Chrome driver'ı başlat"""
        log("Chrome driver başlatılıyor...", "STEP")
        
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--lang=tr-TR')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            log("Chrome driver hazır", "SUCCESS")
            return True
        except Exception as e:
            log(f"Driver hatası: {e}", "ERROR")
            return False
    
    def takim_adi_bul(self, takim_id):
        """Takım ID'sinden Türkçe isim bul"""
        return TAKIM_SOZLUGU.get(str(takim_id), f"Takım {takim_id}")
    
    def puan_durumu_cek(self):
        """FotMob'dan puan durumunu çek"""
        log("Puan durumu çekiliyor...", "STEP")
        
        try:
            self.driver.get(FOTMOB_URLS['tablo'])
            time.sleep(3)
            
            # JavaScript ile veri çek
            script = """
            return Array.from(document.querySelectorAll('a[href*="/teams/"]')).map(a => {
                const match = a.href.match(/\\/teams\\/(\\d+)\\//);
                const name = a.innerText.trim();
                const row = a.closest('tr') || a.closest('div[class*="row"]');
                let stats = [];
                if (row) {
                    stats = Array.from(row.querySelectorAll('td, span')).map(el => el.innerText.trim());
                }
                if (match && name && !name.includes('\\n') && name.length > 1) {
                    return { id: match[1], name: name, stats: stats };
                }
                return null;
            }).filter(t => t !== null);
            """
            
            takimlar = self.driver.execute_script(script)
            
            puan_durumu = []
            sira = 1
            goruldu = set()
            
            for takim in takimlar:
                if takim['name'] in goruldu:
                    continue
                goruldu.add(takim['name'])
                
                # Stats dizisinden verileri çıkar
                stats = takim.get('stats', [])
                sayilar = [int(s) for s in stats if s.isdigit()]
                
                if len(sayilar) >= 7:
                    puan_durumu.append({
                        'sira': sira,
                        'takim_adi': takim['name'],
                        'oynanan': sayilar[0],
                        'galibiyet': sayilar[1],
                        'beraberlik': sayilar[2],
                        'maglubiyet': sayilar[3],
                        'atilan_gol': sayilar[4] if len(sayilar) > 4 else 0,
                        'yenilen_gol': sayilar[5] if len(sayilar) > 5 else 0,
                        'averaj': sayilar[4] - sayilar[5] if len(sayilar) > 5 else 0,
                        'puan': sayilar[-1],
                        'form': ["G", "G", "G", "G", "G"]
                    })
                    log(f"   {sira}. {takim['name']} - {sayilar[-1]} puan")
                    sira += 1
                    
                    if sira > 18:
                        break
            
            if puan_durumu:
                self.veri['puan_durumu'] = puan_durumu
                log(f"{len(puan_durumu)} takım verisi alındı", "SUCCESS")
                return True
            else:
                log("Puan durumu verisi alınamadı", "WARNING")
                return False
            
        except Exception as e:
            log(f"Puan durumu hatası: {e}", "ERROR")
            return False
    
    def istatistik_cek(self, kategori, url_anahtar, turkce_adi):
        """FotMob'dan istatistik çek (ilk 5)"""
        log(f"{turkce_adi} verileri çekiliyor...", "STEP")
        
        try:
            self.driver.get(FOTMOB_URLS[url_anahtar])
            time.sleep(3)
            
            # JavaScript ile oyuncu verilerini çek
            script = """
            return Array.from(document.querySelectorAll('a[href*="/players/"]')).slice(0, 20).map(a => {
                const name = a.querySelector('[class*="PlayerName"], [class*="TeamOrPlayerName"]');
                const stat = a.closest('div').querySelector('[class*="StatValue"], [class*="stat"]');
                const teamImg = a.closest('div').querySelector('img[src*="teamlogo"]');
                
                let teamId = null;
                if (teamImg) {
                    const match = teamImg.src.match(/teamlogo\\/(\\d+)/);
                    if (match) teamId = match[1];
                }
                
                return {
                    name: name ? name.innerText.trim() : a.innerText.split('\\n')[0].trim(),
                    stat: stat ? stat.innerText.trim() : null,
                    teamId: teamId
                };
            }).filter(p => p.name && p.stat);
            """
            
            oyuncular = self.driver.execute_script(script)
            
            istatistikler = []
            goruldu = set()
            
            for oyuncu in oyuncular:
                if oyuncu['name'] in goruldu or len(istatistikler) >= 5:
                    continue
                goruldu.add(oyuncu['name'])
                
                # Stat değerini parse et
                try:
                    stat_str = oyuncu['stat'].replace(',', '.')
                    sayi = float(stat_str) if '.' in stat_str else int(stat_str)
                except:
                    continue
                
                # Takım adını bul
                takim = self.takim_adi_bul(oyuncu['teamId']) if oyuncu['teamId'] else "Bilinmiyor"
                
                istatistikler.append({
                    'oyuncu': oyuncu['name'],
                    'takim': takim,
                    'sayi': sayi
                })
                log(f"   {len(istatistikler)}. {oyuncu['name']} ({takim}) - {sayi}")
            
            if istatistikler:
                self.veri[kategori] = istatistikler
                log(f"{len(istatistikler)} {turkce_adi} verisi alındı", "SUCCESS")
                return True
            else:
                log(f"{turkce_adi} verisi alınamadı", "WARNING")
                return False
            
        except Exception as e:
            log(f"{turkce_adi} hatası: {e}", "ERROR")
            return False
    
    def fikstur_cek(self):
        """FotMob'dan fikstür çek"""
        log("Fikstür verileri çekiliyor...", "STEP")
        
        try:
            self.driver.get(FOTMOB_URLS['fikstur'])
            time.sleep(3)
            
            script = """
            return Array.from(document.querySelectorAll('a[href*="/matches/"]')).slice(0, 9).map(a => {
                const teams = a.querySelectorAll('[class*="team"], [class*="Team"]');
                const time = a.querySelector('[class*="time"], [class*="Time"]');
                const date = a.querySelector('[class*="date"], [class*="Date"]');
                
                let home = '', away = '';
                if (teams.length >= 2) {
                    home = teams[0].innerText.trim();
                    away = teams[1].innerText.trim();
                }
                
                return {
                    home: home,
                    away: away,
                    date: date ? date.innerText.trim() : 'Yakında',
                    time: time ? time.innerText.trim() : '--:--'
                };
            }).filter(m => m.home && m.away);
            """
            
            maclar = self.driver.execute_script(script)
            
            fikstur = []
            for mac in maclar[:9]:
                fikstur.append({
                    'ev_sahibi': mac['home'],
                    'deplasman': mac['away'],
                    'tarih': mac['date'],
                    'saat': mac['time']
                })
                log(f"   {mac['home']} vs {mac['away']}")
            
            if fikstur:
                self.veri['fikstur'] = fikstur
                log(f"{len(fikstur)} maç verisi alındı", "SUCCESS")
                return True
            
            return False
            
        except Exception as e:
            log(f"Fikstür hatası: {e}", "ERROR")
            return False
    
    def tum_verileri_cek(self):
        """Tüm verileri çek"""
        print("\n" + "=" * 50)
        log("VERİ ÇEKME İŞLEMİ BAŞLADI (FotMob)", "STEP")
        print("=" * 50)
        
        if not self.driver_baslat():
            return False
        
        basarili = 0
        
        try:
            # Puan durumu
            if self.puan_durumu_cek():
                basarili += 1
            
            # İstatistikler
            if self.istatistik_cek('gol_kralligi', 'goller', 'Gol Krallığı'):
                basarili += 1
            
            if self.istatistik_cek('asist_kralligi', 'asistler', 'Asist Krallığı'):
                basarili += 1
            
            if self.istatistik_cek('en_iyi_rating', 'rating', 'En İyi Rating'):
                basarili += 1
            
            if self.istatistik_cek('kacirilan_firsatlar', 'kacirilan', 'Kaçırılan Fırsatlar'):
                basarili += 1
            
            if self.istatistik_cek('gol_yemeden', 'gol_yemeden', 'Gol Yemeden'):
                basarili += 1
            
            if self.istatistik_cek('sari_kartlar', 'sari_kart', 'Sarı Kartlar'):
                basarili += 1
            
            if self.istatistik_cek('kirmizi_kartlar', 'kirmizi_kart', 'Kırmızı Kartlar'):
                basarili += 1
            
            # Fikstür
            if self.fikstur_cek():
                basarili += 1
            
            print("=" * 50)
            if basarili > 0:
                log(f"VERİ ÇEKME TAMAMLANDI ({basarili}/9 başarılı)", "SUCCESS")
            else:
                log("VERİ ÇEKİLEMEDİ - Mevcut veriler korunacak", "WARNING")
            print("=" * 50 + "\n")
            
            return basarili > 0
            
        except Exception as e:
            log(f"Genel hata: {e}", "ERROR")
            return False
        finally:
            if self.driver:
                self.driver.quit()
                log("Chrome driver kapatıldı")

# ============================================================
# APP.JS GÜNCELLEYICI
# ============================================================

class AppJSGuncelleyici:
    """web/app.js dosyasını günceller"""
    
    def __init__(self, veri):
        self.veri = veri
        self.app_js_yolu = PROJECT_DIR / "web" / "app.js"
    
    def puan_durumu_js_olustur(self):
        """Puan durumu JavaScript kodu"""
        satirlar = ["const REAL_STANDINGS = ["]
        for takim in self.veri.get('puan_durumu', []):
            form_str = json.dumps(takim.get('form', ['G','G','G','G','G']))
            satirlar.append(f'    {{ rank: {takim["sira"]}, team_name: "{takim["takim_adi"]}", played: {takim["oynanan"]}, wins: {takim["galibiyet"]}, draws: {takim["beraberlik"]}, losses: {takim["maglubiyet"]}, goals_for: {takim["atilan_gol"]}, goals_against: {takim["yenilen_gol"]}, goal_diff: {takim["averaj"]}, points: {takim["puan"]}, form: {form_str} }},')
        satirlar.append("];")
        return '\n'.join(satirlar)
    
    def istatistik_js_olustur(self, degisken_adi, veri):
        """İstatistik JavaScript kodu"""
        satirlar = [f"const {degisken_adi} = ["]
        for oyuncu in veri:
            satirlar.append(f'    {{ name: "{oyuncu["oyuncu"]}", team: "{oyuncu["takim"]}", count: {oyuncu["sayi"]} }},')
        satirlar.append("];")
        return '\n'.join(satirlar)
    
    def dosya_guncelle(self):
        """app.js dosyasını güncelle"""
        log("web/app.js güncelleniyor...", "STEP")
        
        try:
            with open(self.app_js_yolu, 'r', encoding='utf-8') as f:
                icerik = f.read()
            
            guncellendi = False
            
            # Puan durumu
            if self.veri.get('puan_durumu') and len(self.veri['puan_durumu']) >= 10:
                yeni = self.puan_durumu_js_olustur()
                icerik = re.sub(r'const REAL_STANDINGS = \[[\s\S]*?\];', yeni, icerik)
                log("   Puan durumu güncellendi", "SUCCESS")
                guncellendi = True
            
            # İstatistikler eşleştirmesi
            eslesme = {
                'gol_kralligi': 'TOP_SCORERS',
                'asist_kralligi': 'TOP_ASSISTS',
                'en_iyi_rating': 'TOP_RATING',
                'kacirilan_firsatlar': 'MISSED_CHANCES',
                'gol_yemeden': 'CLEAN_SHEETS',
                'sari_kartlar': 'YELLOW_CARDS',
                'kirmizi_kartlar': 'RED_CARDS'
            }
            
            for kategori, js_degisken in eslesme.items():
                if self.veri.get(kategori) and len(self.veri[kategori]) >= 3:
                    yeni = self.istatistik_js_olustur(js_degisken, self.veri[kategori])
                    pattern = rf'const {js_degisken} = \[[\s\S]*?\];'
                    icerik = re.sub(pattern, yeni, icerik)
                    log(f"   {js_degisken} güncellendi", "SUCCESS")
                    guncellendi = True
            
            if guncellendi:
                with open(self.app_js_yolu, 'w', encoding='utf-8') as f:
                    f.write(icerik)
                log("web/app.js başarıyla güncellendi", "SUCCESS")
            else:
                log("Güncelleme yapılmadı - Yeterli veri yok", "WARNING")
            
            return True
            
        except Exception as e:
            log(f"Dosya güncelleme hatası: {e}", "ERROR")
            return False

# ============================================================
# GIT İŞLEMLERİ
# ============================================================

def git_gonder():
    """Değişiklikleri GitHub'a gönder"""
    log("GitHub'a gönderiliyor...", "STEP")
    
    try:
        subprocess.run(["git", "add", "."], check=True, cwd=PROJECT_DIR)
        log("   Dosyalar eklendi", "SUCCESS")
        
        commit_mesaji = f"Otomatik güncelleme - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        sonuc = subprocess.run(
            ["git", "commit", "-m", commit_mesaji],
            capture_output=True,
            text=True,
            cwd=PROJECT_DIR
        )
        
        if sonuc.returncode == 0:
            log(f"   Commit: {commit_mesaji}", "SUCCESS")
        else:
            log("   Commit edilecek değişiklik yok", "INFO")
            return True
        
        subprocess.run(["git", "push", "origin", "main"], check=True, cwd=PROJECT_DIR)
        log("   Push başarılı!", "SUCCESS")
        
        return True
        
    except subprocess.CalledProcessError as e:
        log(f"Git hatası: {e}", "ERROR")
        return False

# ============================================================
# ANA FONKSİYON
# ============================================================

def ana():
    """Ana fonksiyon"""
    print("\n" + "=" * 50)
    print("⚽ SÜPER LİG 360 - OTOMATİK GÜNCELLEME")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("📊 Veri Kaynağı: FotMob (Türkçe)")
    print("=" * 50)
    
    if not SELENIUM_AVAILABLE:
        log("Selenium yüklü değil!", "WARNING")
        log("Yüklemek için: pip install selenium webdriver-manager", "INFO")
        git_gonder()
        return
    
    log("Otomatik scraping modu (FotMob)", "INFO")
    
    # 1. Verileri çek
    scraper = FotMobScraper()
    scraper.tum_verileri_cek()
    
    # 2. app.js güncelle
    if any(scraper.veri.values()):
        guncelleyici = AppJSGuncelleyici(scraper.veri)
        guncelleyici.dosya_guncelle()
    else:
        log("Veri çekilemedi - Manuel güncelleme gerekebilir", "WARNING")
    
    # 3. GitHub'a push
    git_gonder()
    
    print("\n" + "=" * 50)
    print("🏁 GÜNCELLEME TAMAMLANDI")
    print("🌐 Website: https://kaan482.github.io/Superlig360/")
    print("=" * 50 + "\n")

if __name__ == "__main__":
    ana()
