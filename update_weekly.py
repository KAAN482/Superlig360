"""
Süper Lig 360 - FotMob Veri Güncelleme Scripti
==============================================

Bu script Süper Lig verilerini FotMob'dan çeker ve projeyi günceller.
Kullanıcı isteği üzerine HEADLESS MOD KAPALI olarak çalışır (Tarayıcı açılır).

Kullanım:
  python update_weekly.py
"""

import os
import sys
import re
import json
import time
from datetime import datetime
from pathlib import Path
import subprocess

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
    "1933": "Başakşehir", "3061": "Galatasaray", "3057": "Fenerbahçe",
    "3058": "Beşiktaş", "3056": "Trabzonspor", "3060": "Göztepe",
    "3063": "Konyaspor", "3064": "Rizespor", "3065": "Alanyaspor",
    "3066": "Gaziantep FK", "3067": "Hatayspor", "3069": "Antalyaspor",
    "3073": "Kasımpaşa", "3074": "Samsunspor", "3075": "Kocaelispor",
    "3077": "Kayserispor", "3079": "Karagümrük", "1054": "Gençlerbirliği",
    "3059": "Eyüpspor", "7496": "Bodrum FK"
}

def log(mesaj, seviye="INFO"):
    """Terminale log yaz"""
    zaman = datetime.now().strftime('%H:%M:%S')
    semboller = {"INFO": "ℹ️ ", "SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️ ", "STEP": "📌"}
    print(f"[{zaman}] {semboller.get(seviye, '')} {mesaj}")

class FotMobScraper:
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
        log("Chrome driver başlatılıyor (GÖRÜNÜR MOD)...", "STEP")
        options = Options()
        # options.add_argument('--headless=new') # Headless KAPALI
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1600,900')
        options.add_argument('--lang=tr-TR')
        
        # Anti-detection
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        
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
        return TAKIM_SOZLUGU.get(str(takim_id), f"Takım {takim_id}")

    def puan_durumu_cek(self):
        log("Puan durumu çekiliyor...", "STEP")
        try:
            self.driver.get(FOTMOB_URLS['tablo'])
            
            # Tablonun yüklenmesini bekle
            try:
                WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/teams/']"))
                )
                time.sleep(3) 
            except TimeoutException:
                log("   Tablo yüklenemedi (Zaman aşımı)", "ERROR")
                return False

            script = """
            return Array.from(document.querySelectorAll('a[href*="/teams/"]')).map(a => {
                const match = a.href.match(/\\/teams\\/(\\d+)\\//);
                const name = a.innerText.trim();
                const row = a.closest('tr') || a.closest('div[role="row"]') || a.closest('div[class*="TableRowCSS"]');
                
                let stats = [];
                let form = [];
                
                if (row) {
                    // Satırdaki tüm metinleri al
                    stats = Array.from(row.querySelectorAll('td, span, div[class*="TableCell"]')).map(el => el.innerText.trim());
                    
                    // Form bilgisini çek (G/B/M)
                    const formIcons = row.querySelectorAll('[class*="team-form__win"], [class*="team-form__draw"], [class*="team-form__loss"]');
                    if (formIcons.length > 0) {
                        form = Array.from(formIcons).map(icon => {
                            const text = icon.innerText.trim();
                            if (text === "G" || text === "W") return "G";
                            if (text === "B" || text === "D") return "B";
                            if (text === "M" || text === "L") return "M";
                            return null;
                        }).filter(f => f !== null).slice(-5); // Son 5 maç
                    }
                }
                
                if (match && name && name.length > 2) {
                    return { id: match[1], name: name, stats: stats, form: form };
                }
                return null;
            }).filter(t => t !== null);
            """
            
            takimlar = self.driver.execute_script(script)
            
            puan_durumu = []
            sira = 1
            goruldu = set()
            
            for takim in takimlar:
                if takim['name'] in goruldu: continue
                goruldu.add(takim['name'])
                
                # İstatistikleri temizle (sadece sayıları al)
                stats = takim.get('stats', [])
                sayilar = []
                for s in stats:
                    # Negatif sayıları ve normal sayıları yakala
                    temiz = s.replace(',', '').replace('.', '').strip()
                    if temiz.lstrip('-').isdigit():
                        sayilar.append(int(temiz))
                
                # FotMob sırası: Rank(#), Oynanan(O), G, B, M, Goller(AG), Yenilen(YG), Averaj(Av), Puan(P)
                # Genellikle 9 sayı döner. [Rank, Played, Win, Draw, Loss, GF, GA, GD, Pts]
                
                start_idx = 0
                if len(sayilar) == 9:
                    start_idx = 1 # Rank'i atla
                
                if len(sayilar) >= 8:
                    try:
                        puan_durumu.append({
                            'sira': sira,
                            'takim_adi': takim['name'],
                            'oynanan': sayilar[start_idx],
                            'galibiyet': sayilar[start_idx+1],
                            'beraberlik': sayilar[start_idx+2],
                            'maglubiyet': sayilar[start_idx+3],
                            'atilan_gol': sayilar[start_idx+4],
                            'yenilen_gol': sayilar[start_idx+5],
                            'averaj': sayilar[start_idx+6], # GD
                            'puan': sayilar[-1],
                            'form': takim.get('form', ["?"]*5) # Çekilen form verisi
                        })
                        
                        form_str = "-".join(takim.get('form', []))
                        log(f"   {sira}. {takim['name']} - {sayilar[-1]}p ({form_str})")
                        sira += 1
                        if sira > 18: break
                    except Exception:
                        continue

            if puan_durumu:
                self.veri['puan_durumu'] = puan_durumu
                log(f"{len(puan_durumu)} takım verisi alındı", "SUCCESS")
                return True
            return False
            
        except Exception as e:
            log(f"Puan durumu hatası: {e}", "ERROR")
            return False

    def istatistik_cek(self, kategori, url_anahtar, turkce_adi):
        log(f"{turkce_adi} verileri çekiliyor...", "STEP")
        try:
            self.driver.get(FOTMOB_URLS[url_anahtar])
            
            try:
                WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/players/']"))
                )
                time.sleep(3)
            except TimeoutException:
                log(f"   {turkce_adi} yüklenemedi", "ERROR")
                return False
            
            script = """
            return Array.from(document.querySelectorAll('a[href*="/players/"]')).slice(0, 20).map(a => {
                const row = a.closest('tr') || a.closest('div[class*="row"]') || a.closest('div[class*="Row"]');
                if (!row) return null;
                
                const name = a.innerText.split('\\n')[0].trim();
                const stat = row.querySelector('[class*="StatValue"], [class*="stat"], [class*="Stat"]');
                
                const teamImg = row.querySelector('img[src*="teamlogo"]');
                let teamId = null;
                if (teamImg) {
                    const match = teamImg.src.match(/teamlogo\\/(\\d+)/);
                    if (match) teamId = match[1];
                }
                
                return {
                    name: name,
                    stat: stat ? stat.innerText.trim() : null,
                    teamId: teamId
                };
            }).filter(p => p && p.name && p.stat);
            """
            
            oyuncular = self.driver.execute_script(script)
            
            istatistikler = []
            goruldu = set()
            
            for oyuncu in oyuncular:
                if oyuncu['name'] in goruldu or len(istatistikler) >= 5: continue
                goruldu.add(oyuncu['name'])
                
                try:
                    stat_str = oyuncu['stat'].replace(',', '.')
                    sayi = float(stat_str) if '.' in stat_str else int(stat_str)
                except:
                    continue
                
                takim = self.takim_adi_bul(oyuncu['teamId']) if oyuncu['teamId'] else "Bilinmiyor"
                
                istatistikler.append({
                    'oyuncu': oyuncu['name'],
                    'takim': takim,
                    'sayi': sayi
                })
                log(f"   {len(istatistikler)}. {oyuncu['name']} ({takim}) - {sayi}")
            
            if istatistikler:
                self.veri[kategori] = istatistikler
                log(f"{len(istatistikler)} veri alındı", "SUCCESS")
                return True
            return False
            
        except Exception as e:
            log(f"{turkce_adi} hatası: {e}", "ERROR")
            return False

    def fikstur_cek(self):
        log("Fikstür verileri çekiliyor...", "STEP")
        try:
            self.driver.get(FOTMOB_URLS['fikstur'])
            
            try:
                # Maç wrapper'larını bekle
                WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "a[class*='MatchWrapper']"))
                )
                time.sleep(3)
            except TimeoutException:
                # Alternatif selector
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/matches/']"))
                    )
                except:
                    log("   Fikstür yüklenemedi", "ERROR")
                    return False
            
            script = """
            return Array.from(document.querySelectorAll('a[class*="MatchWrapper"], a[href*="/matches/"]')).slice(0, 15).map(a => {
                // Takım isimlerini bul (genellikle 2 tane olur)
                const teams = Array.from(a.querySelectorAll('span[class*="TeamName"], span[class*="name"]'));
                const time = a.querySelector('[class*="time"], [class*="Time"]');
                const date = a.closest('div').querySelector('[class*="DateHeader"], [class*="date"]') || a.querySelector('[class*="Date"]');
                
                if (teams.length < 2) return null;
                
                return {
                    home: teams[0].innerText.trim(),
                    away: teams[1].innerText.trim(),
                    date: date ? date.innerText.trim() : 'Yakında',
                    time: time ? time.innerText.trim() : '--:--'
                };
            }).filter(m => m !== null);
            """
            
            maclar = self.driver.execute_script(script)
            
            fikstur = []
            for mac in maclar[:9]: # İlk 9 maç
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
        print("\n" + "=" * 50)
        log("FOTMOB VERİ ÇEKME BAŞLADI", "STEP")
        print("=" * 50)
        
        if not self.driver_baslat(): return False
        
        try:
            self.puan_durumu_cek()
            self.istatistik_cek('gol_kralligi', 'goller', 'Gol Krallığı')
            self.istatistik_cek('asist_kralligi', 'asistler', 'Asist Krallığı')
            self.istatistik_cek('en_iyi_rating', 'rating', 'En İyi Rating')
            self.istatistik_cek('kacirilan_firsatlar', 'kacirilan', 'Kaçırılan Fırsatlar')
            self.istatistik_cek('gol_yemeden', 'gol_yemeden', 'Gol Yemeden')
            self.istatistik_cek('sari_kartlar', 'sari_kart', 'Sarı Kartlar')
            self.istatistik_cek('kirmizi_kartlar', 'kirmizi_kart', 'Kırmızı Kartlar')
            self.fikstur_cek()
            
            print("=" * 50)
            return True
        finally:
            if self.driver:
                self.driver.quit()
                log("Tarayıcı kapatıldı")

class AppJSGuncelleyici:
    def __init__(self, veri):
        self.veri = veri
        self.app_js_yolu = PROJECT_DIR / "web" / "app.js"
    
    def puan_durumu_js(self):
        lines = ["const REAL_STANDINGS = ["]
        for t in self.veri.get('puan_durumu', []):
            form = json.dumps(t.get('form', ["G"]*5))
            lines.append(f'    {{ rank: {t["sira"]}, team_name: "{t["takim_adi"]}", played: {t["oynanan"]}, wins: {t["galibiyet"]}, draws: {t["beraberlik"]}, losses: {t["maglubiyet"]}, goals_for: {t["atilan_gol"]}, goals_against: {t["yenilen_gol"]}, goal_diff: {t["averaj"]}, points: {t["puan"]}, form: {form} }},')
        lines.append("];")
        return '\n'.join(lines)
    
    def istatistik_js(self, var_name, data):
        lines = [f"const {var_name} = ["]
        for p in data:
            lines.append(f'    {{ name: "{p["oyuncu"]}", team: "{p["takim"]}", count: {p["sayi"]} }},')
        lines.append("];")
        return '\n'.join(lines)
    
    def fikstur_js(self):
        lines = ["const FIXTURES = ["]
        for m in self.veri.get('fikstur', []):
            lines.append(f'    {{ home: "{m["ev_sahibi"]}", away: "{m["deplasman"]}", date: "{m["tarih"]}", time: "{m["saat"]}" }},')
        lines.append("];")
        return '\n'.join(lines)

    def guncelle(self):
        log("web/app.js güncelleniyor...", "STEP")
        try:
            with open(self.app_js_yolu, 'r', encoding='utf-8') as f: content = f.read()
            
            if self.veri.get('puan_durumu'):
                content = re.sub(r'const REAL_STANDINGS = \[[\s\S]*?\];', self.puan_durumu_js(), content)
                log("   Puan durumu güncellendi", "SUCCESS")
            
            map_stats = {
                'gol_kralligi': 'TOP_SCORERS', 'asist_kralligi': 'TOP_ASSISTS',
                'en_iyi_rating': 'TOP_RATING', 'kacirilan_firsatlar': 'MISSED_CHANCES',
                'gol_yemeden': 'CLEAN_SHEETS', 'sari_kartlar': 'YELLOW_CARDS',
                'kirmizi_kartlar': 'RED_CARDS'
            }
            for key, var in map_stats.items():
                if self.veri.get(key):
                    content = re.sub(rf'const {var} = \[[\s\S]*?\];', self.istatistik_js(var, self.veri[key]), content)
                    log(f"   {var} güncellendi", "SUCCESS")
            
            if self.veri.get('fikstur'):
                content = re.sub(r'const FIXTURES = \[[\s\S]*?\];', self.fikstur_js(), content)
                log("   Fikstür güncellendi", "SUCCESS")
            
            with open(self.app_js_yolu, 'w', encoding='utf-8') as f: f.write(content)
            return True
        except Exception as e:
            log(f"Dosya güncelleme hatası: {e}", "ERROR")
            return False

def git_push():
    log("GitHub'a gönderiliyor...", "STEP")
    try:
        subprocess.run(["git", "add", "."], check=True, cwd=PROJECT_DIR)
        msg = f"Otomatik guncelleme {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        subprocess.run(["git", "commit", "-m", msg], capture_output=True, cwd=PROJECT_DIR)
        subprocess.run(["git", "push", "origin", "main"], check=True, cwd=PROJECT_DIR)
        log("Push başarılı", "SUCCESS")
    except Exception as e:
        log(f"Git hatası: {e}", "ERROR")

if __name__ == "__main__":
    if not SELENIUM_AVAILABLE:
        print("Lütfen gereksinimleri yükleyin: pip install selenium webdriver-manager")
        sys.exit(1)
        
    scraper = FotMobScraper()
    scraper.tum_verileri_cek()
    
    if any(scraper.veri.values()):
        updater = AppJSGuncelleyici(scraper.veri)
        updater.guncelle()
        git_push()
    else:
        log("Veri çekilemediği için güncelleme yapılmadı.", "WARNING")