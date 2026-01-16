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
    
    def scrape_standings(self):
        """Puan durumunu çek"""
        log("Puan durumu çekiliyor...", "STEP")
        
        try:
            self.driver.get("https://www.google.com/search?q=süper+lig+puan+durumu&hl=tr")
            time.sleep(3)  # Sayfanın yüklenmesini bekle
            
            # Farklı selector'ları dene
            selectors = [
                "div[data-attrid='sports-bar'] table tr",
                "table.liveresults-sports-immersive__league-table tr",
                "div.imso_gs__tg tr",
                "g-scrolling-carousel table tr",
                "div[jscontroller] table tr"
            ]
            
            rows = []
            for selector in selectors:
                try:
                    rows = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if len(rows) > 5:
                        log(f"   Tablo bulundu: {len(rows)} satır", "INFO")
                        break
                except:
                    continue
            
            if not rows:
                # Alternatif: tüm tabloları bul
                tables = self.driver.find_elements(By.TAG_NAME, "table")
                for table in tables:
                    table_rows = table.find_elements(By.TAG_NAME, "tr")
                    if len(table_rows) >= 18:
                        rows = table_rows
                        log(f"   Alternatif tablo bulundu: {len(rows)} satır", "INFO")
                        break
            
            if not rows or len(rows) < 5:
                log("   Tablo bulunamadı, mevcut veriler korunacak", "WARNING")
                return False
            
            standings = []
            rank = 1
            
            for row in rows:
                try:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if len(cells) < 4:
                        continue
                    
                    # Takım adını bul
                    team_name = ""
                    for cell in cells:
                        text = cell.text.strip()
                        if text and not text.isdigit() and len(text) > 2:
                            team_name = text
                            break
                    
                    if not team_name:
                        continue
                    
                    # Sayısal değerleri topla
                    numbers = []
                    for cell in cells:
                        text = cell.text.strip()
                        if text.isdigit():
                            numbers.append(int(text))
                    
                    if len(numbers) >= 4:
                        team_data = {
                            'rank': rank,
                            'team_name': team_name,
                            'played': numbers[0] if len(numbers) > 0 else 0,
                            'wins': numbers[1] if len(numbers) > 1 else 0,
                            'draws': numbers[2] if len(numbers) > 2 else 0,
                            'losses': numbers[3] if len(numbers) > 3 else 0,
                            'goals_for': numbers[4] if len(numbers) > 4 else 0,
                            'goals_against': numbers[5] if len(numbers) > 5 else 0,
                            'points': numbers[-1] if numbers else 0,
                            'form': ["G", "G", "G", "G", "G"]
                        }
                        team_data['goal_diff'] = team_data['goals_for'] - team_data['goals_against']
                        standings.append(team_data)
                        log(f"   {rank}. {team_data['team_name']} - {team_data['points']} puan")
                        rank += 1
                        
                        if rank > 18:
                            break
                except Exception as e:
                    continue
            
            if standings:
                self.data['standings'] = standings
                log(f"{len(standings)} takım verisi alındı", "SUCCESS")
                return True
            else:
                log("Puan durumu verisi alınamadı, mevcut veriler korunacak", "WARNING")
                return False
            
        except Exception as e:
            log(f"Puan durumu hatası: {e}", "ERROR")
            return False
    
    def scrape_scorers(self):
        """Gol krallığını çek"""
        log("Gol Krallığı verileri çekiliyor...", "STEP")
        
        try:
            self.driver.get("https://www.google.com/search?q=süper+lig+gol+krallığı&hl=tr")
            time.sleep(2)
            
            scorers = []
            
            # Oyuncu kartlarını bul
            selectors = [
                "div[data-attrid*='player']",
                "div.kCrYT",
                "div.g-blk",
                "div[jscontroller] div[data-hveid]"
            ]
            
            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for el in elements[:10]:
                        text = el.text.strip()
                        if text and '\n' in text:
                            lines = text.split('\n')
                            name = lines[0] if lines else ""
                            team = lines[1] if len(lines) > 1 else ""
                            
                            # Gol sayısını bul
                            count = 0
                            for line in lines:
                                match = re.search(r'(\d+)\s*(gol|goal)?', line.lower())
                                if match:
                                    count = int(match.group(1))
                                    break
                            
                            if name and count > 0:
                                scorers.append({
                                    'name': name,
                                    'team': team,
                                    'count': count
                                })
                    
                    if scorers:
                        break
                except:
                    continue
            
            if scorers:
                self.data['scorers'] = scorers[:7]
                log(f"{len(self.data['scorers'])} gol kralı verisi alındı", "SUCCESS")
            else:
                log("Gol krallığı verisi alınamadı, mevcut veriler korunacak", "WARNING")
            
            return bool(scorers)
            
        except Exception as e:
            log(f"Gol krallığı hatası: {e}", "ERROR")
            return False
    
    def scrape_all(self):
        """Tüm verileri çek"""
        print("\n" + "=" * 50)
        log("VERİ ÇEKME İŞLEMİ BAŞLADI", "STEP")
        print("=" * 50)
        
        if not self.setup_driver():
            return False
        
        success_count = 0
        
        try:
            # Puan durumu
            if self.scrape_standings():
                success_count += 1
            
            # Gol krallığı
            if self.scrape_scorers():
                success_count += 1
            
            print("=" * 50)
            if success_count > 0:
                log(f"VERİ ÇEKME TAMAMLANDI ({success_count} başarılı)", "SUCCESS")
            else:
                log("VERİ ÇEKİLEMEDİ - Mevcut veriler korunacak", "WARNING")
            print("=" * 50 + "\n")
            
            return success_count > 0
            
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
            
            updated = False
            
            # Puan durumunu güncelle
            if self.data.get('standings') and len(self.data['standings']) >= 10:
                new_standings = self.generate_standings_js()
                content = re.sub(
                    r'const REAL_STANDINGS = \[[\s\S]*?\];',
                    new_standings,
                    content
                )
                log("   Puan durumu güncellendi", "SUCCESS")
                updated = True
            
            # Gol krallığını güncelle
            if self.data.get('scorers') and len(self.data['scorers']) >= 3:
                new_scorers = self.generate_stats_js('TOP_SCORERS', self.data['scorers'])
                content = re.sub(
                    r'const TOP_SCORERS = \[[\s\S]*?\];',
                    new_scorers,
                    content
                )
                log("   Gol krallığı güncellendi", "SUCCESS")
                updated = True
            
            if updated:
                with open(self.app_js_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                log("web/app.js başarıyla güncellendi", "SUCCESS")
            else:
                log("Güncelleme yapılmadı - Yeterli veri yok", "WARNING")
            
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
    scraper.scrape_all()
    
    # 2. Veri çekildiyse app.js güncelle
    if scraper.data.get('standings') or scraper.data.get('scorers'):
        updater = AppJSUpdater(scraper.data)
        updater.update_file()
    else:
        log("Veri çekilemedi - Manuel güncelleme gerekebilir", "WARNING")
    
    # 3. GitHub'a push (her durumda)
    git_push()
    
    print("\n" + "=" * 50)
    print("🏁 GÜNCELLEME TAMAMLANDI")
    print("🌐 Website: https://kaan482.github.io/Superlig360/")
    print("=" * 50 + "\n")

if __name__ == "__main__":
    main()
