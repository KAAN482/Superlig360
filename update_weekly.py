"""
Süper Lig 360 - Otomatik Veri Güncelleme Scripti
================================================

Tek tuşla:
1. Google'dan güncel verileri çeker (Selenium)
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

# Proje dizini
PROJECT_DIR = Path(__file__).parent

# ============================================================
# LOGGING (Sadece Terminal)
# ============================================================

def log(message, level="INFO"):
    """Terminale log yaz"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    symbols = {
        "INFO": "ℹ️ ",
        "SUCCESS": "✅",
        "ERROR": "❌",
        "WARNING": "⚠️ ",
        "STEP": "📌"
    }
    symbol = symbols.get(level, "")
    print(f"[{timestamp}] {symbol} {message}")

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
        log("Chrome driver başlatılıyor...", "STEP")
        
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--lang=tr-TR')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            log("Chrome driver hazır", "SUCCESS")
            return True
        except Exception as e:
            log(f"Driver hatası: {e}", "ERROR")
            return False
    
    def scrape_standings(self):
        """Puan durumunu çek"""
        log("Puan durumu çekiliyor...", "STEP")
        
        try:
            self.driver.get("https://www.google.com/search?q=süper+lig+puan+durumu")
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table"))
            )
            
            rows = self.driver.find_elements(By.CSS_SELECTOR, "table tr")
            
            standings = []
            for i, row in enumerate(rows[1:19], 1):
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
                    log(f"   {i}. {team_data['team_name']} - {team_data['points']} puan")
            
            self.data['standings'] = standings
            log(f"{len(standings)} takım verisi alındı", "SUCCESS")
            return True
            
        except Exception as e:
            log(f"Puan durumu hatası: {e}", "ERROR")
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
        log(f"{stat_type} verileri çekiliyor...", "STEP")
        
        try:
            self.driver.get(f"https://www.google.com/search?q=süper+lig+{url_suffix}")
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div"))
            )
            
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
            
            log(f"{len(stats)} {stat_type} verisi alındı", "SUCCESS")
            return stats
            
        except Exception as e:
            log(f"{stat_type} hatası: {e}", "ERROR")
            return []
    
    def scrape_all(self):
        """Tüm verileri çek"""
        print("\n" + "=" * 50)
        log("VERİ ÇEKME İŞLEMİ BAŞLADI", "STEP")
        print("=" * 50)
        
        if not self.setup_driver():
            return False
        
        try:
            self.scrape_standings()
            self.data['scorers'] = self.scrape_stats("Gol Krallığı", "gol+krallığı", 7)
            self.data['assists'] = self.scrape_stats("Asist Krallığı", "asist+krallığı", 6)
            self.data['yellow_cards'] = self.scrape_stats("Sarı Kart", "sarı+kart+sıralaması", 5)
            self.data['red_cards'] = self.scrape_stats("Kırmızı Kart", "kırmızı+kart+sıralaması", 5)
            
            print("=" * 50)
            log("TÜM VERİLER ÇEKİLDİ", "SUCCESS")
            print("=" * 50 + "\n")
            return True
            
        except Exception as e:
            log(f"Genel hata: {e}", "ERROR")
            return False
        finally:
            if self.driver:
                self.driver.quit()
                log("Chrome driver kapatıldı")
    
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
        log("web/app.js güncelleniyor...", "STEP")
        
        try:
            with open(self.app_js_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if self.data.get('standings'):
                new_standings = self.generate_standings_js()
                content = re.sub(
                    r'const REAL_STANDINGS = \[[\s\S]*?\];',
                    new_standings,
                    content
                )
                log("   Puan durumu güncellendi", "SUCCESS")
            
            if self.data.get('scorers'):
                new_scorers = self.generate_stats_js('TOP_SCORERS', self.data['scorers'])
                content = re.sub(
                    r'const TOP_SCORERS = \[[\s\S]*?\];',
                    new_scorers,
                    content
                )
                log("   Gol krallığı güncellendi", "SUCCESS")
            
            with open(self.app_js_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            log("web/app.js başarıyla güncellendi", "SUCCESS")
            return True
            
        except Exception as e:
            log(f"Dosya güncelleme hatası: {e}", "ERROR")
            return False

# ============================================================
# GIT OPERATIONS
# ============================================================

def git_push():
    """Değişiklikleri GitHub'a gönder"""
    log("GitHub'a gönderiliyor...", "STEP")
    
    try:
        subprocess.run(["git", "add", "."], check=True, cwd=PROJECT_DIR)
        log("   Dosyalar eklendi", "SUCCESS")
        
        commit_msg = f"Otomatik güncelleme - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        result = subprocess.run(
            ["git", "commit", "-m", commit_msg],
            capture_output=True,
            text=True,
            cwd=PROJECT_DIR
        )
        
        if result.returncode == 0:
            log(f"   Commit: {commit_msg}", "SUCCESS")
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
# MAIN
# ============================================================

def main():
    """Ana fonksiyon"""
    print("\n" + "=" * 50)
    print("⚽ SÜPER LİG 360 - OTOMATİK GÜNCELLEME")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    if not SELENIUM_AVAILABLE:
        log("Selenium yüklü değil!", "WARNING")
        log("Yüklemek için: pip install selenium webdriver-manager", "INFO")
        print("\n" + "-" * 50)
        print("📋 MANUEL GÜNCELLEME MODU")
        print("-" * 50)
        print("""
1. Google'da ara: 'süper lig puan durumu'
2. web/app.js dosyasını güncelle
3. Bu scripti tekrar çalıştır
        """)
        git_push()
        return
    
    log("Otomatik scraping modu", "INFO")
    
    # 1. Verileri çek
    scraper = SuperLigScraper()
    if scraper.scrape_all():
        # 2. app.js güncelle
        updater = AppJSUpdater(scraper.data)
        if updater.update_file():
            # 3. GitHub'a push
            git_push()
    
    print("\n" + "=" * 50)
    print("🏁 GÜNCELLEME TAMAMLANDI")
    print("🌐 Website: https://kaan482.github.io/Superlig360/")
    print("=" * 50 + "\n")

if __name__ == "__main__":
    main()
