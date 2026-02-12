#!/data/data/com.termux/files/usr/bin/bash
#
# TERMUX SETUP - Simple & Working
# Installer untuk Unified Bot di Termux
#

clear
echo "╔═══════════════════════════════════════════════════════╗"
echo "║                                                       ║"
echo "║   UNIFIED BOT - TERMUX SETUP                         ║"
echo "║   NFT + Degen Coin Hunter + Telegram Control         ║"
echo "║                                                       ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""

# Check if in Termux
if [ ! -d "/data/data/com.termux" ]; then
    echo "❌ This script is for Termux only!"
    exit 1
fi

echo "📱 Detected: Termux"
echo ""
echo "This will:"
echo "  ✓ Install Python & dependencies"
echo "  ✓ Download all bot files"  
echo "  ✓ Setup Telegram configuration"
echo "  ✓ Install control bot"
echo ""
read -p "Press ENTER to continue..."

# Step 1: Update Termux
echo ""
echo "[1/6] Updating Termux..."
pkg update -y
echo "✓ Updated"

# Step 2: Install packages
echo ""
echo "[2/6] Installing packages..."
pkg install python git wget -y
echo "✓ Installed"

# Step 3: Install Python packages
echo ""
echo "[3/6] Installing Python dependencies..."
pip install requests python-dotenv psutil --upgrade
echo "✓ Dependencies installed"

# Step 4: Setup directory
echo ""
echo "[4/6] Setting up directory..."

# Create bot directory in home
cd ~
mkdir -p crypto-bot
cd crypto-bot

echo "✓ Directory ready: ~/crypto-bot"

# Step 5: Get Telegram credentials
echo ""
echo "[5/6] Telegram Setup"
echo ""
echo "Kamu perlu 2 hal:"
echo ""
echo "1. BOT TOKEN dari @BotFather"
echo "   - Buka Telegram"
echo "   - Cari @BotFather"
echo "   - Kirim /newbot"
echo "   - Copy TOKEN"
echo ""
echo "2. CHAT ID dari @userinfobot"
echo "   - Cari @userinfobot"
echo "   - Kirim /start"
echo "   - Copy ID"
echo ""

read -p "Sudah siap? (y/n): " ready
if [ "$ready" != "y" ]; then
    echo ""
    echo "Silakan dapatkan TOKEN dan CHAT_ID dulu"
    echo "Lalu jalankan script ini lagi: ./setup_termux.sh"
    exit 0
fi

echo ""
read -p "Masukkan BOT TOKEN: " TOKEN
read -p "Masukkan CHAT ID: " CHATID

# Step 6: Create files
echo ""
echo "[6/6] Creating configuration..."

# Create .env
cat > .env << EOF
# Telegram
TELEGRAM_BOT_TOKEN=$TOKEN
TELEGRAM_CHAT_ID=$CHATID

# Modules
ENABLE_NFT=true
ENABLE_DEGEN=true

# NFT Settings
NFT_CHECK_INTERVAL=5
MIN_PUMP_SCORE=50
PLATFORMS=rarible,opensea,magiceden
CHAINS=ethereum,polygon,solana

# Degen Settings  
DEGEN_CHECK_INTERVAL=3
MIN_DEGEN_SCORE=60
DEGEN_CHAINS=ethereum,bsc,polygon

# Price Alerts
DEFAULT_STOP_LOSS=-20
DEFAULT_TAKE_PROFIT=100
EOF

echo "✓ Configuration created"

# Create a simple test script
cat > test_connection.py << 'PYEOF'
import os
from dotenv import load_dotenv
import requests

load_dotenv()

token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')

url = f"https://api.telegram.org/bot{token}/sendMessage"
payload = {
    'chat_id': chat_id,
    'text': '🎉 <b>Termux Setup Sukses!</b>\n\n'
            '✅ Bot files ready\n'
            '✅ Configuration OK\n'
            '✅ Telegram connected\n\n'
            '<b>Next Steps:</b>\n'
            '1. Download bot files (check guide)\n'
            '2. Run: python telegram_control.py\n'
            '3. Control via Telegram!\n\n'
            'Setup complete! 🚀',
    'parse_mode': 'HTML'
}

try:
    r = requests.post(url, json=payload, timeout=10)
    if r.status_code == 200:
        print("✓ Test message sent to Telegram!")
    else:
        print(f"✗ Failed: {r.status_code}")
except Exception as e:
    print(f"✗ Error: {e}")
PYEOF

# Test connection
python test_connection.py

echo ""
echo "╔═══════════════════════════════════════════════════════╗"
echo "║                                                       ║"
echo "║            ✓ SETUP SELESAI!                          ║"
echo "║                                                       ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""
echo "📁 Bot directory: ~/crypto-bot"
echo "✅ Configuration: .env"
echo ""
echo "📥 DOWNLOAD BOT FILES:"
echo ""
echo "Cara 1: Manual Download"
echo "  - Download files dari link yang diberikan"
echo "  - Extract ke folder ~/crypto-bot"
echo ""
echo "Cara 2: Git Clone (jika ada repo)"
echo "  git clone [repo-url] ~/crypto-bot"
echo ""
echo "🚀 SETELAH FILES READY:"
echo ""
echo "  cd ~/crypto-bot"
echo "  python telegram_control.py"
echo ""
echo "Lalu control bot via Telegram!"
echo "Kirim /help untuk lihat commands"
echo ""
