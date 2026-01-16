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

Veri Kaynakları:
  - Puan Durumu: https://www.fotmob.com/leagues/71/table/super-lig
  - Fikstür: https://www.fotmob.com/leagues/71/fixtures/super-lig?group=by-round
  - İstatistikler: https://www.fotmob.com/leagues/71/stats/super-lig
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

# FotMob URL'leri
FOTMOB_URLS = {
    'table': 'https://www.fotmob.com/leagues/71/table/super-lig',
    'fixtures': 'https://www.fotmob.com/leagues/71/fixtures/super-lig?group=by-round',
    'stats': 'https://www.fotmob.com/leagues/71/stats/super-lig'
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
    
    def puan_durumu_cek(self):
        """FotMob'dan puan durumunu çek"""
        log("Puan durumu çekiliyor (FotMob)...", "STEP")
        
        try:
            self.driver.get(FOTMOB_URLS['table'])
            time.sleep(4)
            
            # Tablodaki satırları bul
            rows = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/teams/']")
            
            if not rows:
                # Alternatif selector
                rows = self.driver.find_elements(By.CSS_SELECTOR, "div[class*='TableRow'], tr[class*='row']")
            
            puan_durumu = []
            
            # Sayfa kaynağından veri çıkar
            page_source = self.driver.page_source
            
            # Takım isimlerini bul
            team_pattern = r'"name":"([^"]+)".*?"played":(\d+).*?"wins":(\d+).*?"draws":(\d+).*?"losses":(\d+).*?"scoresStr":"(\d+)-(\d+)".*?"pts":(\d+)'
            matches = re.findall(team_pattern, page_source)
            
            if matches:
                for i, match in enumerate(matches[:18], 1):
                    takim = {
                        'sira': i,
                        'takim_adi': match[0],
                        'oynanan': int(match[1]),
                        'galibiyet': int(match[2]),
                        'beraberlik': int(match[3]),
                        'maglubiyet': int(match[4]),
                        'atilan_gol': int(match[5]),
                        'yenilen_gol': int(match[6]),
                        'averaj': int(match[5]) - int(match[6]),
                        'puan': int(match[7]),
                        'form': ["G", "G", "G", "G", "G"]  # Varsayılan
                    }
                    puan_durumu.append(takim)
                    log(f"   {i}. {takim['takim_adi']} - {takim['puan']} puan")
            
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
    
    def istatistik_cek(self, kategori, fotmob_adi, turkce_adi):
        """FotMob'dan istatistik çek"""
        log(f"{turkce_adi} verileri çekiliyor...", "STEP")
        
        try:
            # Stats sayfasına git (ilk kez gidiyorsa)
            current_url = self.driver.current_url
            if 'stats' not in current_url:
                self.driver.get(FOTMOB_URLS['stats'])
                time.sleep(3)
            
            # "See all" veya "Show all" butonunu bul ve tıkla
            try:
                # Farklı olası selektorlar
                see_all_selectors = [
                    "button:contains('See all')",
                    "button:contains('Show all')",
                    "a:contains('See all')",
                    "[data-testid='see-all']",
                    ".see-all-button",
                    "button[class*='see']",
                    "button[class*='show']"
                ]
                
                for selector in see_all_selectors:
                    try:
                        # Tüm "See all" butonlarını bul
                        buttons = self.driver.find_elements(By.CSS_SELECTOR, "button, a")
                        for button in buttons:
                            if any(text in button.text.lower() for text in ['see all', 'show all', 'tümünü gör']):
                                try:
                                    self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                                    time.sleep(0.5)
                                    button.click()
                                    time.sleep(2)
                                    log(f"   'See all' butonuna tıklandı", "SUCCESS")
                                    break
                                except:
                                    continue
                        break
                    except:
                        continue
            except:
                pass
            
            # Sayfa kaynağından oyuncu verilerini çıkar
            page_source = self.driver.page_source
            
            # JSON datayı bul
            istatistikler = []
            
            # Farklı regex patternleri dene
            patterns = [
                r'"name":"([^"]+)"[^}]*?"teamName":"([^"]+)"[^}]*?"' + fotmob_adi + r'"[:\s]+(\d+\.?\d*)',
                r'"participantName":"([^"]+)"[^}]*?"teamName":"([^"]+)"[^}]*?"' + fotmob_adi + r'"[:\s]+(\d+\.?\d*)',
                r'{"name":"([^"]+)"[^}]*?"team[^"]*?":"([^"]+)"[^}]*?"' + fotmob_adi + r'"[:\s]+(\d+\.?\d*)'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, page_source)
                if matches and len(matches) >= 3:
                    # İlk 5'i al
                    for match in matches[:5]:
                        try:
                            sayi = float(match[2]) if '.' in match[2] else int(match[2])
                            istatistikler.append({
                                'oyuncu': match[0],
                                'takim': match[1],
                                'sayi': sayi
                            })
                            log(f"   {match[0]} - {sayi}", "INFO")
                        except:
                            continue
                    break
            
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
            self.driver.get(FOTMOB_URLS['fixtures'])
            time.sleep(3)
            
            page_source = self.driver.page_source
            
            # Maç verilerini çıkar
            match_pattern = r'"home":\{"name":"([^"]+)".*?"away":\{"name":"([^"]+)"'
            matches = re.findall(match_pattern, page_source)
            
            fikstur = []
            for i, match in enumerate(matches[:9]):
                fikstur.append({
                    'ev_sahibi': match[0],
                    'deplasman': match[1],
                    'tarih': 'Yakında',
                    'saat': '--:--'
                })
            
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
            
            # Fikstür
            if self.fikstur_cek():
                basarili += 1
            
            # İstatistikler - Gol Krallığı
            if self.istatistik_cek('gol_kralligi', 'goals', 'Gol Krallığı'):
                basarili += 1
            
            print("=" * 50)
            if basarili > 0:
                log(f"VERİ ÇEKME TAMAMLANDI ({basarili} başarılı)", "SUCCESS")
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
    
    def kapat(self):
        if self.driver:
            self.driver.quit()

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
            
            # Puan durumunu güncelle
            if self.veri.get('puan_durumu') and len(self.veri['puan_durumu']) >= 10:
                yeni_puan = self.puan_durumu_js_olustur()
                icerik = re.sub(
                    r'const REAL_STANDINGS = \[[\s\S]*?\];',
                    yeni_puan,
                    icerik
                )
                log("   Puan durumu güncellendi", "SUCCESS")
                guncellendi = True
            
            # Gol krallığını güncelle
            if self.veri.get('gol_kralligi') and len(self.veri['gol_kralligi']) >= 3:
                yeni_goller = self.istatistik_js_olustur('TOP_SCORERS', self.veri['gol_kralligi'])
                icerik = re.sub(
                    r'const TOP_SCORERS = \[[\s\S]*?\];',
                    yeni_goller,
                    icerik
                )
                log("   Gol krallığı güncellendi", "SUCCESS")
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
    print("📊 Veri Kaynağı: FotMob")
    print("=" * 50)
    
    if not SELENIUM_AVAILABLE:
        log("Selenium yüklü değil!", "WARNING")
        log("Yüklemek için: pip install selenium webdriver-manager", "INFO")
        print("\n" + "-" * 50)
        print("📋 MANUEL GÜNCELLEME MODU")
        print("-" * 50)
        print("""
1. FotMob'a git: https://www.fotmob.com/leagues/71/table/super-lig
2. web/app.js dosyasını güncelle
3. Bu scripti tekrar çalıştır
        """)
        git_gonder()
        return
    
    log("Otomatik scraping modu (FotMob)", "INFO")
    
    # 1. Verileri çek
    scraper = FotMobScraper()
    scraper.tum_verileri_cek()
    
    # 2. Veri çekildiyse app.js güncelle
    if scraper.veri.get('puan_durumu') or scraper.veri.get('gol_kralligi'):
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
