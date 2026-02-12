#!/usr/bin/env python3
"""
TELEGRAM CONTROL BOT
Control unified bot through Telegram commands
Start/Stop monitoring, Check status, Configure settings
"""

import os
import sys
import time
import subprocess
import psutil
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class TelegramControlBot:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN', '')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID', '')
        
        if not self.token or not self.chat_id:
            print("❌ Missing Telegram credentials!")
            sys.exit(1)
        
        self.bot_process = None
        self.last_update_id = 0
        
    def send_message(self, text: str, parse_mode: str = "HTML"):
        """Send message to Telegram"""
        import requests
        
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {
            'chat_id': self.chat_id,
            'text': text,
            'parse_mode': parse_mode
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def get_updates(self):
        """Get updates from Telegram"""
        import requests
        
        url = f"https://api.telegram.org/bot{self.token}/getUpdates"
        params = {
            'offset': self.last_update_id + 1,
            'timeout': 30
        }
        
        try:
            response = requests.get(url, params=params, timeout=35)
            if response.status_code == 200:
                data = response.json()
                return data.get('result', [])
        except:
            pass
        
        return []
    
    def is_bot_running(self):
        """Check if unified bot is running"""
        for proc in psutil.process_iter(['name', 'cmdline']):
            try:
                cmdline = ' '.join(proc.info['cmdline'] or [])
                if 'unified_bot.py' in cmdline or 'nft_monitor' in cmdline or 'degen_hunter' in cmdline:
                    return True, proc.pid
            except:
                pass
        return False, None
    
    def start_bot(self, mode: str = "unified"):
        """Start monitoring bot"""
        running, pid = self.is_bot_running()
        if running:
            return f"❌ Bot already running (PID: {pid})"
        
        try:
            if mode == "unified":
                script = "unified_bot.py"
            elif mode == "nft":
                script = "nft_monitor_enhanced.py"
            elif mode == "degen":
                script = "degen_hunter.py"
            else:
                return "❌ Invalid mode! Use: unified, nft, or degen"
            
            # Check if script exists
            if not os.path.exists(script):
                return f"❌ {script} not found! Make sure you're in the correct directory."
            
            # Start in background
            self.bot_process = subprocess.Popen(
                [sys.executable, script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                start_new_session=True
            )
            
            time.sleep(2)
            
            # Verify it started
            running, pid = self.is_bot_running()
            if running:
                return f"✅ Bot started successfully!\n📍 Mode: {mode}\n🆔 PID: {pid}"
            else:
                return "❌ Bot failed to start. Check logs."
                
        except Exception as e:
            return f"❌ Error starting bot: {e}"
    
    def stop_bot(self):
        """Stop monitoring bot"""
        running, pid = self.is_bot_running()
        if not running:
            return "❌ Bot is not running"
        
        try:
            # Kill process
            proc = psutil.Process(pid)
            proc.terminate()
            time.sleep(1)
            
            # Force kill if still running
            if proc.is_running():
                proc.kill()
            
            return f"✅ Bot stopped (PID: {pid})"
        except Exception as e:
            return f"❌ Error stopping bot: {e}"
    
    def get_status(self):
        """Get bot status"""
        running, pid = self.is_bot_running()
        
        if running:
            try:
                proc = psutil.Process(pid)
                cpu = proc.cpu_percent(interval=1)
                mem = proc.memory_info().rss / 1024 / 1024  # MB
                uptime = time.time() - proc.create_time()
                uptime_str = self.format_uptime(uptime)
                
                status = f"""
🟢 <b>Bot Status: RUNNING</b>

🆔 PID: {pid}
⏱️ Uptime: {uptime_str}
💾 Memory: {mem:.1f} MB
⚡ CPU: {cpu:.1f}%

📊 Config:
• NFT: {os.getenv('ENABLE_NFT', 'true')}
• DEGEN: {os.getenv('ENABLE_DEGEN', 'true')}
• NFT Interval: {os.getenv('NFT_CHECK_INTERVAL', '5')}m
• DEGEN Interval: {os.getenv('DEGEN_CHECK_INTERVAL', '3')}m
"""
            except:
                status = f"🟢 <b>Bot Status: RUNNING</b>\n\n🆔 PID: {pid}"
        else:
            status = "🔴 <b>Bot Status: STOPPED</b>"
        
        return status
    
    def format_uptime(self, seconds):
        """Format uptime"""
        days = int(seconds // 86400)
        hours = int((seconds % 86400) // 3600)
        minutes = int((seconds % 3600) // 60)
        
        parts = []
        if days > 0:
            parts.append(f"{days}d")
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes}m")
        
        return " ".join(parts) if parts else "<1m"
    
    def get_config(self):
        """Get current configuration"""
        config = f"""
⚙️ <b>Current Configuration</b>

<b>Modules:</b>
• NFT Monitor: {os.getenv('ENABLE_NFT', 'true')}
• Degen Hunter: {os.getenv('ENABLE_DEGEN', 'true')}

<b>NFT Settings:</b>
• Check Interval: {os.getenv('NFT_CHECK_INTERVAL', '5')} min
• Min Pump Score: {os.getenv('MIN_PUMP_SCORE', '50')}
• Platforms: {os.getenv('PLATFORMS', 'N/A')}
• Chains: {os.getenv('CHAINS', 'N/A')}

<b>Degen Settings:</b>
• Check Interval: {os.getenv('DEGEN_CHECK_INTERVAL', '3')} min
• Min Degen Score: {os.getenv('MIN_DEGEN_SCORE', '60')}
• Chains: {os.getenv('DEGEN_CHAINS', 'N/A')}

<b>Price Alerts:</b>
• Stop Loss: {os.getenv('DEFAULT_STOP_LOSS', '-20')}%
• Take Profit: {os.getenv('DEFAULT_TAKE_PROFIT', '100')}%
"""
        return config
    
    def get_help(self):
        """Get help message"""
        return """
🤖 <b>Telegram Control Bot - Commands</b>

<b>Bot Control:</b>
/start - Start unified bot (NFT + Degen)
/start_nft - Start NFT monitor only
/start_degen - Start degen hunter only
/stop - Stop bot
/restart - Restart bot
/status - Check bot status

<b>Information:</b>
/config - View configuration
/help - Show this help

<b>Quick Actions:</b>
Just send:
• "start" - Start bot
• "stop" - Stop bot
• "status" - Check status
• "restart" - Restart bot

<b>Tips:</b>
• Bot runs in background
• Safe to close Termux
• Use /status to check if running
"""
    
    def handle_command(self, command: str):
        """Handle command from Telegram"""
        command = command.lower().strip()
        
        if command in ['/start', 'start']:
            return self.start_bot('unified')
        
        elif command in ['/start_nft', 'start nft']:
            return self.start_bot('nft')
        
        elif command in ['/start_degen', 'start degen']:
            return self.start_bot('degen')
        
        elif command in ['/stop', 'stop']:
            return self.stop_bot()
        
        elif command in ['/restart', 'restart']:
            stop_msg = self.stop_bot()
            time.sleep(2)
            start_msg = self.start_bot('unified')
            return f"{stop_msg}\n\n{start_msg}"
        
        elif command in ['/status', 'status']:
            return self.get_status()
        
        elif command in ['/config', 'config']:
            return self.get_config()
        
        elif command in ['/help', 'help']:
            return self.get_help()
        
        else:
            return "❌ Unknown command. Send /help for available commands."
    
    def run(self):
        """Run control bot"""
        print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║       TELEGRAM CONTROL BOT - ACTIVATED                    ║
║          Control your bot via Telegram!                   ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
""")
        
        # Send startup message
        self.send_message(
            "🤖 <b>Telegram Control Bot Started!</b>\n\n"
            "Send /help to see available commands.\n\n"
            "You can now control the monitoring bot through Telegram!"
        )
        
        print("✅ Control bot running...")
        print("📱 Send commands via Telegram")
        print("⌨️  Press Ctrl+C to stop\n")
        
        # Main loop
        while True:
            try:
                updates = self.get_updates()
                
                for update in updates:
                    self.last_update_id = update['update_id']
                    
                    # Get message
                    message = update.get('message', {})
                    text = message.get('text', '')
                    from_id = str(message.get('chat', {}).get('id', ''))
                    
                    # Only respond to authorized user
                    if from_id == self.chat_id and text:
                        print(f"📨 Received: {text}")
                        
                        # Handle command
                        response = self.handle_command(text)
                        self.send_message(response)
                        
                        print(f"📤 Sent response")
                
                time.sleep(1)
                
            except KeyboardInterrupt:
                print("\n\n🛑 Control bot stopped")
                self.send_message("🛑 <b>Control Bot Stopped</b>")
                break
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(5)


def main():
    """Main entry point"""
    try:
        import requests
        import psutil
    except ImportError:
        print("Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "psutil", "python-dotenv"])
        print("✅ Packages installed. Please run again.")
        sys.exit(0)
    
    bot = TelegramControlBot()
    bot.run()


if __name__ == "__main__":
    main()
