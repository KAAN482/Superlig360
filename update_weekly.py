"""
Süper Lig 360 - Otomatik Veri Güncelleme Scripti
================================================

Bu script tek tuşla:
1. Google'dan güncel verileri çeker (Selenium)
2. web/app.js dosyasını otomatik günceller
3. GitHub'a push eder
4. Her aşamayı loglar

Kullanım:
  python update_weekly.py

Gereksinimler:
  pip install selenium webdriver-manager
"""

import os
import sys
import re
import json
import logging
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
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

import subprocess

# ============================================================
# LOGGING SETUP
# ============================================================

# Proje dizini
PROJECT_DIR = Path(__file__).parent
LOG_DIR = PROJECT_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Log dosyası
log_filename = LOG_DIR / f"update_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

# Logger setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(log_filename, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# ============================================================
# SCRAPER CLASS
# ============================================================

class SuperLigScraper:
    """Google'dan Süper Lig verilerini çeken scraper"""
    
    def __init__(self):
        self.driver = None
        self.data = {
            'standings': [],
            'scorers': [],
            'assists': [],
            'yellow_cards': [],
            'red_cards': [],
            'fixtures': []
        }
    
    def setup_driver(self):
        """Chrome driver'ı başlat"""
        logger.info("🌐 Chrome driver başlatılıyor...")
        
        options = Options()
        options.add_argument('--headless')  # Görünmez mod
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--lang=tr-TR')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            logger.info("✅ Chrome driver hazır")
            return True
        except Exception as e:
            logger.error(f"❌ Driver hatası: {e}")
            return False
    
    def scrape_standings(self):
        """Puan durumunu çek"""
        logger.info("📊 Puan durumu çekiliyor...")
        
        try:
            self.driver.get("https://www.google.com/search?q=süper+lig+puan+durumu")
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table"))
            )
            
            # Tablo verilerini çek
            rows = self.driver.find_elements(By.CSS_SELECTOR, "table tr")
            
            standings = []
            for i, row in enumerate(rows[1:19], 1):  # İlk 18 takım
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) >= 8:
                    team_data = {
                        'rank': i,
                        'team_name': cells[1].text.strip(),
                        'played': int(cells[2].text or 0),
                        'wins': int(cells[3].text or 0),
                        'draws': int(cells[4].text or 0),
                        'losses': int(cells[5].text or 0),
                        'goals_for': int(cells[6].text.split('-')[0] if '-' in cells[6].text else cells[6].text or 0),
                        'goals_against': int(cells[6].text.split('-')[1] if '-' in cells[6].text else 0),
                        'points': int(cells[7].text or 0),
                        'form': self.get_form(row)
                    }
                    team_data['goal_diff'] = team_data['goals_for'] - team_data['goals_against']
                    standings.append(team_data)
                    logger.info(f"   {i}. {team_data['team_name']} - {team_data['points']} puan")
            
            self.data['standings'] = standings
            logger.info(f"✅ {len(standings)} takım verisi alındı")
            return True
            
        except Exception as e:
            logger.error(f"❌ Puan durumu hatası: {e}")
            return False
    
    def get_form(self, row):
        """Son 5 maç formunu al"""
        try:
            form_elements = row.find_elements(By.CSS_SELECTOR, "[data-tooltip]")
            form = []
            for el in form_elements[-5:]:
                tooltip = el.get_attribute("data-tooltip") or ""
                if "kazandı" in tooltip.lower() or "galibiyet" in tooltip.lower():
                    form.append("G")
                elif "kaybetti" in tooltip.lower() or "mağlubiyet" in tooltip.lower():
                    form.append("M")
                else:
                    form.append("B")
            return form if form else ["G", "G", "G", "G", "G"]
        except:
            return ["G", "G", "G", "G", "G"]
    
    def scrape_stats(self, stat_type, url_suffix, limit=7):
        """İstatistik verilerini çek"""
        logger.info(f"📈 {stat_type} verileri çekiliyor...")
        
        try:
            self.driver.get(f"https://www.google.com/search?q=süper+lig+{url_suffix}")
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div"))
            )
            
            # Oyuncu listesini bul
            stats = []
            player_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-attrid*='player'], .kCrYT")
            
            for el in player_elements[:limit]:
                text = el.text.strip()
                if text and len(text) > 3:
                    parts = text.split('\n')
                    if len(parts) >= 2:
                        stats.append({
                            'name': parts[0],
                            'team': parts[1] if len(parts) > 1 else "Bilinmiyor",
                            'count': int(re.search(r'\d+', parts[-1]).group()) if re.search(r'\d+', parts[-1]) else 0
                        })
            
            logger.info(f"✅ {len(stats)} {stat_type} verisi alındı")
            return stats
            
        except Exception as e:
            logger.error(f"❌ {stat_type} hatası: {e}")
            return []
    
    def scrape_all(self):
        """Tüm verileri çek"""
        logger.info("=" * 60)
        logger.info("🚀 VERİ ÇEKME İŞLEMİ BAŞLADI")
        logger.info("=" * 60)
        
        if not self.setup_driver():
            return False
        
        try:
            # Puan durumu
            self.scrape_standings()
            
            # Gol krallığı
            self.data['scorers'] = self.scrape_stats("Gol Krallığı", "gol+krallığı", 7)
            
            # Asist krallığı
            self.data['assists'] = self.scrape_stats("Asist Krallığı", "asist+krallığı", 6)
            
            # Sarı kartlar
            self.data['yellow_cards'] = self.scrape_stats("Sarı Kart", "sarı+kart+sıralaması", 5)
            
            # Kırmızı kartlar
            self.data['red_cards'] = self.scrape_stats("Kırmızı Kart", "kırmızı+kart+sıralaması", 5)
            
            logger.info("=" * 60)
            logger.info("✅ TÜM VERİLER ÇEKİLDİ")
            logger.info("=" * 60)
            return True
            
        except Exception as e:
            logger.error(f"❌ Genel hata: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()
                logger.info("🔒 Chrome driver kapatıldı")
    
    def close(self):
        if self.driver:
            self.driver.quit()

# ============================================================
# APP.JS UPDATER
# ============================================================

class AppJSUpdater:
    """web/app.js dosyasını günceller"""
    
    def __init__(self, data):
        self.data = data
        self.app_js_path = PROJECT_DIR / "web" / "app.js"
    
    def generate_standings_js(self):
        """Puan durumu JavaScript kodu"""
        lines = ["const REAL_STANDINGS = ["]
        for team in self.data.get('standings', []):
            form_str = json.dumps(team.get('form', ['G','G','G','G','G']))
            lines.append(f'    {{ rank: {team["rank"]}, team_name: "{team["team_name"]}", played: {team["played"]}, wins: {team["wins"]}, draws: {team["draws"]}, losses: {team["losses"]}, goals_for: {team["goals_for"]}, goals_against: {team["goals_against"]}, goal_diff: {team["goal_diff"]}, points: {team["points"]}, form: {form_str} }},')
        lines.append("];")
        return '\n'.join(lines)
    
    def generate_stats_js(self, var_name, data):
        """İstatistik JavaScript kodu"""
        lines = [f"const {var_name} = ["]
        for item in data:
            lines.append(f'    {{ name: "{item["name"]}", team: "{item["team"]}", count: {item["count"]} }},')
        lines.append("];")
        return '\n'.join(lines)
    
    def update_file(self):
        """app.js dosyasını güncelle"""
        logger.info("📝 web/app.js güncelleniyor...")
        
        try:
            with open(self.app_js_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Puan durumunu güncelle
            if self.data.get('standings'):
                new_standings = self.generate_standings_js()
                content = re.sub(
                    r'const REAL_STANDINGS = \[[\s\S]*?\];',
                    new_standings,
                    content
                )
                logger.info("   ✅ Puan durumu güncellendi")
            
            # Gol krallığını güncelle
            if self.data.get('scorers'):
                new_scorers = self.generate_stats_js('TOP_SCORERS', self.data['scorers'])
                content = re.sub(
                    r'const TOP_SCORERS = \[[\s\S]*?\];',
                    new_scorers,
                    content
                )
                logger.info("   ✅ Gol krallığı güncellendi")
            
            # Dosyayı kaydet
            with open(self.app_js_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info("✅ web/app.js başarıyla güncellendi")
            return True
            
        except Exception as e:
            logger.error(f"❌ Dosya güncelleme hatası: {e}")
            return False

# ============================================================
# GIT OPERATIONS
# ============================================================

def git_push():
    """Değişiklikleri GitHub'a gönder"""
    logger.info("📤 GitHub'a gönderiliyor...")
    
    try:
        # Git add
        subprocess.run(["git", "add", "."], check=True, cwd=PROJECT_DIR)
        logger.info("   ✅ Dosyalar eklendi")
        
        # Git commit
        commit_msg = f"Otomatik güncelleme - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        result = subprocess.run(
            ["git", "commit", "-m", commit_msg],
            capture_output=True,
            text=True,
            cwd=PROJECT_DIR
        )
        
        if result.returncode == 0:
            logger.info(f"   ✅ Commit: {commit_msg}")
        else:
            logger.info("   ℹ️ Commit edilecek değişiklik yok")
            return True
        
        # Git push
        subprocess.run(["git", "push", "origin", "main"], check=True, cwd=PROJECT_DIR)
        logger.info("   ✅ Push başarılı!")
        
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Git hatası: {e}")
        return False

# ============================================================
# MAIN
# ============================================================

def main():
    """Ana fonksiyon"""
    print("\n" + "=" * 60)
    print("⚽ SÜPER LİG 360 - OTOMATİK GÜNCELLEME")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60 + "\n")
    
    logger.info("🎯 Güncelleme başlatıldı")
    logger.info(f"📁 Log dosyası: {log_filename}")
    
    # Selenium kontrolü
    if not SELENIUM_AVAILABLE:
        logger.warning("⚠️ Selenium yüklü değil!")
        logger.info("📦 Yüklemek için: pip install selenium webdriver-manager")
        logger.info("📝 Manuel güncelleme modu aktif...")
        
        # Manuel mod - sadece git push
        print("\n" + "-" * 60)
        print("📋 MANUEL GÜNCELLEME MODU")
        print("-" * 60)
        print("""
1. Google'da ara: 'süper lig puan durumu'
2. web/app.js dosyasını aç ve verileri güncelle
3. Bu scripti tekrar çalıştır

Değişiklik varsa GitHub'a gönderilecek.
        """)
        
        git_push()
        return
    
    # Otomatik scraping
    logger.info("🤖 Otomatik scraping modu")
    
    # 1. Verileri çek
    scraper = SuperLigScraper()
    if scraper.scrape_all():
        
        # 2. app.js güncelle
        updater = AppJSUpdater(scraper.data)
        if updater.update_file():
            
            # 3. GitHub'a push
            git_push()
    
    # Özet
    print("\n" + "=" * 60)
    print("📊 GÜNCELLEME ÖZETİ")
    print("=" * 60)
    print(f"📁 Log dosyası: {log_filename}")
    print(f"🌐 Website: https://kaan482.github.io/Superlig360/")
    print("=" * 60 + "\n")
    
    logger.info("🏁 Güncelleme tamamlandı")

if __name__ == "__main__":
    main()
