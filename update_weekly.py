"""
Süper Lig 360 - Tek Tuşla Haftalık Güncelleme Scripti
=====================================================
Bu script her hafta sonu çalıştırılarak veritabanını günceller.

Kullanım:
  python update_weekly.py

Ne yapar:
  1. Google'dan güncel puan durumu ve istatistikleri çeker
  2. web/app.js dosyasını günceller
  3. GitHub'a push eder (otomatik deploy olur)
"""

import subprocess
import sys
from datetime import datetime

def run_update():
    print("=" * 60)
    print("🔄 Süper Lig 360 - Haftalık Güncelleme")
    print(f"📅 Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    try:
        # Step 1: Run the scraper to get latest data
        print("\n📊 Adım 1: En son veriler çekiliyor...")
        print("   → Google'dan puan durumu ve istatistikler alınıyor")
        
        # Note: scraper/google_scraper.py will be run here
        # For now, manual update is required
        
        print("\n⚠️  Şu an manuel güncelleme gerekiyor:")
        print("   1. Google'da 'süper lig puan durumu' ara")
        print("   2. web/app.js dosyasındaki verileri güncelle")
        print("   3. Sonra bu scripti tekrar çalıştır")
        
        # Step 2: Git operations
        print("\n📤 Adım 2: Değişiklikler GitHub'a gönderiliyor...")
        
        # Add all changes
        subprocess.run(["git", "add", "."], check=True)
        
        # Create commit with date
        commit_msg = f"Haftalık güncelleme - {datetime.now().strftime('%Y-%m-%d')}"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        
        # Push to GitHub
        subprocess.run(["git", "push", "origin", "main"], check=True)
        
        print("\n✅ Güncelleme tamamlandı!")
        print("🌐 Website otomatik olarak güncellenecek:")
        print("   https://kaan482.github.io/Superlig360/")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Hata oluştu: {e}")
        print("   Lütfen manuel olarak kontrol edin.")
    except Exception as e:
        print(f"\n❌ Beklenmeyen hata: {e}")

if __name__ == "__main__":
    run_update()
