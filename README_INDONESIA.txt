═══════════════════════════════════════════════════════════
  NFT MONITOR - INSTALASI OTOMATIS (BAHASA INDONESIA)
═══════════════════════════════════════════════════════════


🚀 INSTALASI 1-KLIK (PALING MUDAH)
===================================

Semua file sudah digabung dalam 1 folder.
Instalasi 100% otomatis tanpa ketik manual!


📦 APA YANG SUDAH TERMASUK
============================

Folder ini berisi:
✅ Semua script Python (Basic & Enhanced)
✅ Dokumentasi lengkap (Bahasa Inggris & Indonesia)
✅ Installer otomatis (Linux/Mac & Windows)
✅ Test tool otomatis
✅ File konfigurasi template


🔧 CARA INSTALL (PILIH SESUAI OS)
===================================

UNTUK LINUX / MAC:
------------------
1. Buka Terminal
2. Masuk ke folder ini:
   cd /path/ke/nft-monitor

3. Jalankan installer:
   chmod +x install.sh
   ./install.sh

4. Ikuti instruksi di layar
5. Selesai!


UNTUK WINDOWS:
--------------
1. Buka Command Prompt atau PowerShell
2. Masuk ke folder ini:
   cd C:\path\ke\nft-monitor

3. Double-click: install.bat
   ATAU ketik: install.bat

4. Ikuti instruksi di layar
5. Selesai!


📋 APA YANG DILAKUKAN INSTALLER
=================================

Installer otomatis akan:

✓ Cek Python dan pip (install dulu jika belum ada)
✓ Install dependencies (requests, python-dotenv)
✓ Minta TOKEN Telegram Bot (dari @BotFather)
✓ Minta CHAT ID Telegram (dari @userinfobot)
✓ Buat file .env otomatis
✓ Test koneksi Telegram
✓ Kirim pesan test ke Telegram kamu
✓ Pilih versi bot (Basic atau Enhanced)
✓ Jalankan bot!

TOTAL WAKTU: 3-5 menit
KETIK MANUAL: Hanya TOKEN dan CHAT ID


🎯 PERSIAPAN SEBELUM INSTALL
==============================

Anda perlu 2 hal dari Telegram:

1️⃣ TOKEN BOT TELEGRAM
   Cara dapat:
   a. Buka Telegram
   b. Cari: @BotFather
   c. Kirim: /newbot
   d. Ikuti instruksi
   e. Copy TOKEN (seperti: 123456:ABCdef...)

2️⃣ CHAT ID TELEGRAM
   Cara dapat:
   a. Cari: @userinfobot di Telegram
   b. Kirim: /start
   c. Copy ID yang muncul (angka)


💻 REQUIREMENTS SISTEM
=======================

MINIMUM:
- Python 3.7 atau lebih baru
- pip (Python package manager)
- Koneksi internet
- Akun Telegram

RECOMMENDED:
- Python 3.9+
- 1GB RAM free
- 500MB disk space


📱 SETELAH INSTALASI
=====================

Bot akan otomatis:
✓ Monitoring platform NFT
✓ Kirim alert ke Telegram
✓ Tracking free mints
✓ Analisa pump potential (versi Enhanced)

Anda akan dapat alert seperti:

    🔥 FREE MINT ALERT - 🚀🚀🚀 VERY HIGH POTENTIAL
    
    Project: Amazing NFT
    Platform: Rarible (Polygon)
    Price: Free (+ gas $0.02)
    
    🎯 PUMP SCORE: 85/100
    
    📊 Metrics:
    • Volume 24h: $12,450
    • Holders: 342
    
    🔗 Link mint


🔄 MENJALANKAN BOT
===================

Setelah install, ada 3 cara jalankan:

1. FOREGROUND (terlihat):
   python3 nft_monitor_enhanced.py
   (Tekan Ctrl+C untuk stop)

2. BACKGROUND (Linux/Mac):
   screen -S nft-monitor
   python3 nft_monitor_enhanced.py
   # Tekan Ctrl+A lalu D untuk detach
   # Lihat lagi: screen -r nft-monitor

3. WINDOWS SERVICE:
   Buat scheduled task di Windows


⚙️ KONFIGURASI (OPSIONAL)
===========================

File .env sudah dibuat otomatis.
Bisa edit untuk custom settings:

Buka file .env, edit:

# Minimum score untuk alert (skip yang rendah)
MIN_PUMP_SCORE=60

# Platform yang dimonitor
PLATFORMS=rarible,opensea,magiceden,zora

# Blockchain yang dimonitor
CHAINS=polygon,solana,zora

# Interval cek (menit)
CHECK_INTERVAL=5


📚 DOKUMENTASI
===============

FILE PENTING (BACA INI):

1. START_HERE_ENHANCED.txt
   → Mulai dari sini!
   → Penjelasan fitur Enhanced

2. SECURITY_GUIDE.txt
   → WAJIB BACA sebelum mint NFT!
   → Cara aman mint NFT
   → Hindari scam

3. PUMP_ANALYSIS_GUIDE.txt
   → Cara kerja Pump Score
   → Interpretasi skor 0-100

4. PLATFORM_GUIDE.txt
   → Perbandingan 7 platform
   → Mana yang terbaik

5. WHATS_NEW.txt
   → Fitur baru Enhanced version
   → Update terbaru


🆘 TROUBLESHOOTING
===================

Problem: Python tidak ditemukan
Solusi: 
  - Install Python dari python.org
  - Checklist "Add to PATH" saat install
  - Restart terminal/cmd

Problem: pip tidak ditemukan
Solusi:
  - Install: python -m ensurepip
  - Atau reinstall Python

Problem: Installer error
Solusi:
  - Pastikan Python 3.7+
  - Pastikan koneksi internet
  - Cek TOKEN dan CHAT_ID benar

Problem: Bot tidak kirim alert
Solusi:
  - Cek bot running (tidak crash)
  - Cek .env file (TOKEN dan CHAT_ID)
  - Free mint memang jarang (sabar)
  - Turunkan MIN_PUMP_SCORE ke 30

Problem: Terlalu banyak alert
Solusi:
  - Naikkan MIN_PUMP_SCORE ke 70
  - Pilih platform spesifik
  - Filter chain tertentu


🔒 KEAMANAN
============

Bot ini 100% AMAN karena:

✅ TIDAK menyimpan private key
✅ TIDAK otomatis mint NFT
✅ TIDAK execute transaksi blockchain
✅ Hanya monitoring dan kirim alert

Anda tetap harus:
⚠️ Verifikasi contract di Etherscan
⚠️ Cek Twitter/Discord project
⚠️ Pakai burner wallet
⚠️ Jangan share private key


💡 TIPS PENGGUNAAN
===================

1. MULAI DENGAN ENHANCED VERSION
   - Lebih banyak platform
   - Pump score analysis
   - Alert lebih detail

2. SET MIN_PUMP_SCORE=60
   - Quality over quantity
   - Lebih sedikit alert
   - Lebih tinggi success rate

3. FOKUS LOW GAS CHAINS
   - Polygon: $0.01-0.50
   - Solana: $0.001
   - Zora Network: FREE!

4. TRACKING RESULTS
   - Catat score vs hasil
   - Pelajari pattern
   - Improve strategi

5. VERIFIKASI SELALU
   - Jangan percaya score 100%
   - Cek contract
   - Research team


🎓 BELAJAR LEBIH LANJUT
========================

Setelah install, baca:

Hari 1:
- START_HERE_ENHANCED.txt (20 menit)
- SECURITY_GUIDE.txt (30 menit)

Hari 2:
- PUMP_ANALYSIS_GUIDE.txt (20 menit)
- PLATFORM_GUIDE.txt (15 menit)

Hari 3:
- Mulai mint!
- Tracking hasil
- Optimize settings


📞 BANTUAN
===========

Jika ada masalah:

1. Baca dokumentasi (90% masalah solved)
2. Cek file TROUBLESHOOTING.txt
3. Test ulang dengan: python3 test_telegram.py
4. Reinstall jika perlu


🎯 KESIMPULAN
==============

Dengan installer otomatis ini:

✅ Install < 5 menit
✅ Tanpa ketik manual (kecuali TOKEN/ID)
✅ Langsung jalan
✅ Monitoring 7+ platform
✅ Pump score analysis
✅ 100% aman

Siap cari NFT free mint yang akan pump! 🚀


═══════════════════════════════════════════════════════════
           INSTALASI OTOMATIS - TANPA RIBET!
═══════════════════════════════════════════════════════════

Linux/Mac:  chmod +x install.sh && ./install.sh
Windows:    install.bat

Selesai dalam 3-5 menit! 🎉
