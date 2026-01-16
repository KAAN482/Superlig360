"""
Süper Lig 360 - Tek Tuşla Haftalık Güncelleme Scripti
=====================================================

Bu script her hafta sonu çalıştırılarak website'i günceller.

KULLANIM:
  python update_weekly.py              # Sadece GitHub'a push
  python update_weekly.py --check      # Durum kontrolü
  python update_weekly.py --help       # Yardım

NE YAPAR:
  1. Mevcut değişiklikleri kontrol eder
  2. Değişiklik varsa commit oluşturur
  3. GitHub'a push eder
  4. GitHub Actions otomatik olarak website'i günceller

HAFTALIK GÜNCELLEME ADIMLARI:
  1. Google'da 'süper lig puan durumu' ara
  2. Puan tablosundaki verileri web/app.js'e kopyala
  3. İstatistikleri güncelle (gol, asist, kartlar)
  4. Bu scripti çalıştır: python update_weekly.py
"""

import subprocess
import sys
import os
from datetime import datetime

# Proje dizini
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

def print_header():
    print("\n" + "=" * 60)
    print("⚽ Süper Lig 360 - Haftalık Güncelleme")
    print(f"📅 Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

def check_git_status():
    """Git durumunu kontrol et"""
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
        cwd=PROJECT_DIR
    )
    return result.stdout.strip()

def get_current_branch():
    """Mevcut branch'i al"""
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        capture_output=True,
        text=True,
        cwd=PROJECT_DIR
    )
    return result.stdout.strip()

def show_status():
    """Proje durumunu göster"""
    print_header()
    
    # Git durumu
    changes = check_git_status()
    branch = get_current_branch()
    
    print(f"\n� Proje Dizini: {PROJECT_DIR}")
    print(f"🌿 Branch: {branch}")
    
    if changes:
        print("\n📝 Bekleyen Değişiklikler:")
        for line in changes.split('\n'):
            if line:
                status = line[:2]
                filename = line[3:]
                if 'M' in status:
                    print(f"   ✏️  Değiştirildi: {filename}")
                elif 'A' in status:
                    print(f"   ➕ Eklendi: {filename}")
                elif '?' in status:
                    print(f"   ❓ Yeni dosya: {filename}")
                else:
                    print(f"   📄 {filename}")
    else:
        print("\n✅ Bekleyen değişiklik yok.")
    
    print("\n" + "-" * 60)
    print("📋 Güncelleme Talimatları:")
    print("-" * 60)
    print("""
1. Google'da 'süper lig puan durumu' ara
2. Puan tablosundan verileri al:
   - Takım sıralamaları ve puanlar
   - Galibiyet, beraberlik, mağlubiyet sayıları
   - Averaj ve son 5 maç formu

3. web/app.js dosyasını aç ve şu bölümleri güncelle:
   - REAL_STANDINGS (puan durumu)
   - TOP_SCORERS (gol krallığı)
   - TOP_ASSISTS (asist krallığı)
   - YELLOW_CARDS (sarı kartlar)
   - RED_CARDS (kırmızı kartlar)
   - FIXTURES (sonraki hafta maçları)

4. Bu scripti tekrar çalıştır:
   python update_weekly.py
""")

def run_update():
    """Değişiklikleri GitHub'a gönder"""
    print_header()
    
    # Değişiklikleri kontrol et
    print("\n� Adım 1: Değişiklikler kontrol ediliyor...")
    changes = check_git_status()
    
    if not changes:
        print("   ℹ️  Commit edilecek değişiklik yok.")
        print("   💡 Önce web/app.js dosyasını güncelleyin.")
        show_update_guide()
        return
    
    print(f"   ✅ {len(changes.split(chr(10)))} dosyada değişiklik bulundu.")
    
    # Git add
    print("\n📦 Adım 2: Dosyalar hazırlanıyor...")
    try:
        subprocess.run(
            ["git", "add", "."],
            check=True,
            cwd=PROJECT_DIR
        )
        print("   ✅ Tüm dosyalar eklendi.")
    except subprocess.CalledProcessError:
        print("   ❌ Dosyalar eklenirken hata oluştu.")
        return
    
    # Git commit
    print("\n💾 Adım 3: Commit oluşturuluyor...")
    commit_msg = f"Haftalık güncelleme - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    try:
        subprocess.run(
            ["git", "commit", "-m", commit_msg],
            check=True,
            cwd=PROJECT_DIR
        )
        print(f"   ✅ Commit: {commit_msg}")
    except subprocess.CalledProcessError:
        print("   ℹ️  Commit edilecek yeni değişiklik yok.")
        return
    
    # Git push
    print("\n🚀 Adım 4: GitHub'a gönderiliyor...")
    try:
        subprocess.run(
            ["git", "push", "origin", "main"],
            check=True,
            cwd=PROJECT_DIR
        )
        print("   ✅ Push başarılı!")
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Push hatası: {e}")
        return
    
    # Başarı mesajı
    print("\n" + "=" * 60)
    print("🎉 GÜNCELLEME TAMAMLANDI!")
    print("=" * 60)
    print("""
📌 Sonraki adımlar:
   1. GitHub Actions otomatik olarak çalışacak
   2. ~2 dakika içinde website güncellenecek
   
🌐 Website: https://kaan482.github.io/Superlig360/
📊 Actions:  https://github.com/KAAN482/Superlig360/actions
""")

def show_update_guide():
    """Güncelleme rehberini göster"""
    print("\n" + "-" * 60)
    print("📋 VERİ GÜNCELLEME REHBERİ")
    print("-" * 60)
    print("""
🔍 ADIM 1: Google'da Ara
   → 'süper lig puan durumu'
   → 'süper lig gol krallığı'
   → 'süper lig 19. hafta maçları'

✏️  ADIM 2: web/app.js Dosyasını Güncelle

   REAL_STANDINGS dizisindeki her takım için:
   - rank: Sıralama (1-18)
   - team_name: Takım adı
   - played: Oynanan maç
   - wins, draws, losses: G, B, M
   - goals_for, goals_against: Atılan, yenilen
   - goal_diff: Averaj
   - points: Puan
   - form: Son 5 maç ["G","B","M","G","G"]

   Aynı şekilde:
   - TOP_SCORERS: Gol kralları
   - TOP_ASSISTS: Asist kralları
   - YELLOW_CARDS: Sarı kartlar (5 oyuncu)
   - RED_CARDS: Kırmızı kartlar (5 oyuncu)
   - FIXTURES: Sonraki hafta maçları

🚀 ADIM 3: Bu Scripti Çalıştır
   python update_weekly.py
""")

def show_help():
    """Yardım mesajını göster"""
    print("""
⚽ Süper Lig 360 - Haftalık Güncelleme Scripti

KULLANIM:
  python update_weekly.py              Değişiklikleri GitHub'a gönder
  python update_weekly.py --check      Proje durumunu kontrol et
  python update_weekly.py --guide      Güncelleme rehberini göster
  python update_weekly.py --help       Bu yardım mesajını göster

ÖNEMLİ:
  Bu script web/app.js dosyasındaki verileri OTOMATİK güncellemez.
  Önce verileri manuel olarak güncelleyip, sonra bu scripti çalıştırın.
  Script sadece değişiklikleri GitHub'a push eder.
""")

if __name__ == "__main__":
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    
    if "--help" in args or "-h" in args:
        show_help()
    elif "--check" in args or "-c" in args:
        show_status()
    elif "--guide" in args or "-g" in args:
        show_update_guide()
    else:
        run_update()
