#!/data/data/com.termux/files/usr/bin/bash
#
# ALL-IN-ONE INSTALLER
# One command to setup everything
#

set -e

clear
cat << "EOF"
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║    🚀 UNIFIED BOT - ALL-IN-ONE INSTALLER 🚀              ║
║    NFT + Degen + Telegram Control                        ║
║                                                           ║
║    Install EVERYTHING dengan 1 command!                  ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
EOF

echo ""
echo "Platform: $(uname -o 2>/dev/null || uname -s)"
echo ""
echo "Installer ini akan:"
echo "  ✓ Install Python & dependencies"
echo "  ✓ Setup folder structure"
echo "  ✓ Configure Telegram"
echo "  ✓ Install control bot"
echo "  ✓ Ready to run!"
echo ""
read -p "Lanjut? (y/n): " confirm

if [ "$confirm" != "y" ]; then
    echo "Installation cancelled"
    exit 0
fi

# Detect OS
if [ -d "/data/data/com.termux" ]; then
    OS="termux"
    PKG_MANAGER="pkg"
elif command -v apt-get &> /dev/null; then
    OS="debian"
    PKG_MANAGER="apt-get"
elif command -v yum &> /dev/null; then
    OS="redhat"
    PKG_MANAGER="yum"
else
    OS="unknown"
    PKG_MANAGER=""
fi

echo ""
echo "🔍 Detected: $OS"
echo ""

# Update & Install
echo "[1/5] Installing packages..."
if [ "$OS" = "termux" ]; then
    pkg update -y
    pkg install python git wget -y
else
    echo "Please install Python 3.7+ manually if not installed"
fi

echo "✓ Packages installed"

# Install Python packages
echo ""
echo "[2/5] Installing Python packages..."
pip install requests python-dotenv psutil --upgrade --quiet
echo "✓ Python packages installed"

# Setup directory
echo ""
echo "[3/5] Creating directory structure..."
INSTALL_DIR="$HOME/crypto-bot"
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"
echo "✓ Directory: $INSTALL_DIR"

# Get Telegram credentials
echo ""
echo "[4/5] Telegram Configuration"
echo ""
echo "Kamu perlu:"
echo "  1. BOT TOKEN (dari @BotFather)"
echo "  2. CHAT ID (dari @userinfobot)"
echo ""

read -p "BOT TOKEN: " TOKEN
read -p "CHAT ID: " CHATID

# Create .env
cat > .env << ENVEOF
TELEGRAM_BOT_TOKEN=$TOKEN
TELEGRAM_CHAT_ID=$CHATID
ENABLE_NFT=true
ENABLE_DEGEN=true
NFT_CHECK_INTERVAL=5
DEGEN_CHECK_INTERVAL=3
MIN_PUMP_SCORE=50
MIN_DEGEN_SCORE=60
PLATFORMS=rarible,opensea,magiceden
CHAINS=ethereum,polygon,solana
DEGEN_CHAINS=ethereum,bsc,polygon
DEFAULT_STOP_LOSS=-20
DEFAULT_TAKE_PROFIT=100
ENVEOF

echo "✓ Configuration created"

# Download/Create minimal bot files
echo ""
echo "[5/5] Setting up bot files..."

# Note: In real deployment, these would be downloaded
# For now, create placeholder
cat > README.txt << 'READMEEOF'
BOT FILES NEEDED:
- unified_bot.py
- nft_monitor_enhanced.py
- degen_hunter.py
- telegram_control.py

Place all bot files in this directory: ~/crypto-bot/

Then run:
python telegram_control.py &

Control via Telegram!
READMEEOF

echo "✓ Setup complete"

# Test Telegram
echo ""
echo "Testing Telegram connection..."

python3 - << 'PYEOF'
import os
from dotenv import load_dotenv

load_dotenv()

try:
    import requests
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    r = requests.post(url, json={
        'chat_id': chat_id,
        'text': '🎉 Setup Complete!\n\nBot ready di: ~/crypto-bot\n\nNext: Place bot files dan run!',
        'parse_mode': 'HTML'
    }, timeout=10)
    
    if r.status_code == 200:
        print("✓ Test message sent!")
    else:
        print("✗ Test failed")
except Exception as e:
    print(f"✗ Error: {e}")
PYEOF

echo ""
echo "╔═══════════════════════════════════════════════════════╗"
echo "║                                                       ║"
echo "║              ✅ INSTALLATION COMPLETE!               ║"
echo "║                                                       ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""
echo "📁 Install directory: $INSTALL_DIR"
echo "✅ Configuration: .env"
echo ""
echo "📥 NEXT STEPS:"
echo ""
echo "1. Place all bot files in: $INSTALL_DIR/"
echo "   Required files:"
echo "   - unified_bot.py"
echo "   - nft_monitor_enhanced.py"
echo "   - degen_hunter.py"
echo "   - telegram_control.py"
echo ""
echo "2. Run control bot:"
echo "   cd $INSTALL_DIR"
echo "   python telegram_control.py &"
echo ""
echo "3. Control via Telegram:"
echo "   /start - Start bot"
echo "   /status - Check status"
echo "   /help - Show commands"
echo ""
echo "✅ Check Telegram for test message!"
echo ""
