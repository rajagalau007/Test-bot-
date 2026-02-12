#!/data/data/com.termux/files/usr/bin/bash
#
# UNIFIED BOT - Termux Installer
# Installer khusus untuk Android (Termux)
#

# Warna
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

clear
echo -e "${BLUE}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   UNIFIED BOT - INSTALLER UNTUK TERMUX/ANDROID           ║
║     NFT Monitor + Degen Coin Hunter + Price Alerts       ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${GREEN}Installer untuk Termux (Android)${NC}"
echo "  ✓ Install Python & dependencies"
echo "  ✓ Setup NFT Monitor"
echo "  ✓ Setup Degen Coin Hunter"
echo "  ✓ Setup Price Alerts"
echo ""
echo -e "${YELLOW}Tekan ENTER untuk mulai...${NC}"
read

# Update & Upgrade
echo -e "\n${BLUE}[STEP 1/7]${NC} ${GREEN}Update Termux...${NC}\n"
pkg update -y && pkg upgrade -y
echo -e "${GREEN}✓ Termux updated${NC}"

# Install Python
echo -e "\n${BLUE}[STEP 2/7]${NC} ${GREEN}Install Python...${NC}\n"
pkg install python git wget -y
echo -e "${GREEN}✓ Python installed${NC}"

# Install dependencies
echo -e "\n${BLUE}[STEP 3/7]${NC} ${GREEN}Install dependencies...${NC}\n"
pip install requests python-dotenv --upgrade
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Setup Telegram
echo -e "\n${BLUE}[STEP 4/7]${NC} ${GREEN}Setup Telegram...${NC}\n"
echo "Buat bot di @BotFather, lalu masukkan TOKEN:"
read -r TOKEN
echo "Dapatkan ID dari @userinfobot, lalu masukkan CHAT ID:"
read -r CHATID

# Create .env
echo -e "\n${BLUE}[STEP 5/7]${NC} ${GREEN}Create config...${NC}\n"
cat > .env << ENVEOF
TELEGRAM_BOT_TOKEN=$TOKEN
TELEGRAM_CHAT_ID=$CHATID
ENABLE_NFT=true
ENABLE_DEGEN=true
NFT_CHECK_INTERVAL=5
DEGEN_CHECK_INTERVAL=3
MIN_PUMP_SCORE=50
MIN_DEGEN_SCORE=60
ENVEOF
echo -e "${GREEN}✓ Config created${NC}"

# Test
echo -e "\n${BLUE}[STEP 6/7]${NC} ${GREEN}Testing...${NC}\n"
python test_telegram.py
echo -e "${GREEN}✓ Test OK${NC}"

# Done
echo -e "\n${BLUE}[STEP 7/7]${NC} ${GREEN}Done!${NC}\n"
echo "Jalankan: python unified_bot.py"
