#!/usr/bin/env python3
"""
DEGEN COIN HUNTER - Track New Launches & Pumps
Monitor DEX launches, detect pumps, send alerts with stop loss/take profit
SAFE: Read-only monitoring, NO auto-trading
"""

import os
import time
import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import sqlite3

class DegenCoinHunter:
    def __init__(self, telegram_token: str, telegram_chat_id: str):
        self.telegram_token = telegram_token
        self.telegram_chat_id = telegram_chat_id
        self.db_path = "degen_tracker.db"
        self.init_database()
        
        # API endpoints
        self.dexscreener_api = "https://api.dexscreener.com/latest/dex"
        self.dextools_api = "https://api.dextools.io/v1"
        self.coingecko_api = "https://api.coingecko.com/api/v3"
        
        # Tracking state
        self.tracked_tokens = {}  # {address: {price, entry_price, sl, tp}}
        
    def init_database(self):
        """Initialize database for tracking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # New launches table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS new_launches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                token_address TEXT UNIQUE,
                token_name TEXT,
                token_symbol TEXT,
                chain TEXT,
                dex TEXT,
                launch_time DATETIME,
                initial_liquidity REAL,
                initial_price REAL,
                pump_potential REAL,
                alerted BOOLEAN DEFAULT 0,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Pump detection table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pump_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                token_address TEXT,
                token_symbol TEXT,
                chain TEXT,
                price_change_5m REAL,
                price_change_1h REAL,
                volume_surge REAL,
                pump_score REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Price alerts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS price_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                token_address TEXT,
                token_symbol TEXT,
                entry_price REAL,
                current_price REAL,
                stop_loss REAL,
                take_profit REAL,
                alert_type TEXT,
                triggered BOOLEAN DEFAULT 0,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def calculate_degen_score(self, token_data: Dict) -> float:
        """
        Calculate degen/pump potential score (0-100)
        Higher = more likely to pump
        """
        score = 0.0
        
        # Liquidity check (0-20 points)
        liquidity = token_data.get('liquidity', 0)
        if liquidity > 100000:
            score += 20
        elif liquidity > 50000:
            score += 15
        elif liquidity > 10000:
            score += 10
        elif liquidity > 5000:
            score += 5
        
        # Volume/Liquidity ratio (0-20 points)
        volume = token_data.get('volume_24h', 0)
        if liquidity > 0:
            vol_liq_ratio = volume / liquidity
            if vol_liq_ratio > 10:
                score += 20
            elif vol_liq_ratio > 5:
                score += 15
            elif vol_liq_ratio > 2:
                score += 10
            elif vol_liq_ratio > 1:
                score += 5
        
        # Age (newer = higher score) (0-15 points)
        age_hours = token_data.get('age_hours', 999)
        if age_hours < 1:
            score += 15
        elif age_hours < 6:
            score += 12
        elif age_hours < 24:
            score += 8
        elif age_hours < 48:
            score += 4
        
        # Holder count (0-15 points)
        holders = token_data.get('holders', 0)
        if holders > 1000:
            score += 15
        elif holders > 500:
            score += 12
        elif holders > 100:
            score += 8
        elif holders > 50:
            score += 4
        
        # Price momentum (0-15 points)
        price_change_1h = token_data.get('price_change_1h', 0)
        if price_change_1h > 100:
            score += 15
        elif price_change_1h > 50:
            score += 12
        elif price_change_1h > 20:
            score += 8
        elif price_change_1h > 10:
            score += 4
        
        # Transaction activity (0-15 points)
        txns_5m = token_data.get('txns_5m', 0)
        if txns_5m > 50:
            score += 15
        elif txns_5m > 20:
            score += 10
        elif txns_5m > 10:
            score += 5
        
        return min(score, 100.0)
    
    def detect_pump(self, token_data: Dict) -> bool:
        """
        Detect if token is currently pumping
        """
        # Criteria for pump:
        # - Price up 20%+ in 5 minutes OR
        # - Price up 50%+ in 1 hour OR
        # - Volume surge 5x+ normal
        
        price_change_5m = token_data.get('price_change_5m', 0)
        price_change_1h = token_data.get('price_change_1h', 0)
        volume_surge = token_data.get('volume_surge', 1)
        
        is_pumping = (
            price_change_5m > 20 or
            price_change_1h > 50 or
            volume_surge > 5
        )
        
        return is_pumping
    
    def scan_new_launches(self, chain: str = "ethereum") -> List[Dict]:
        """
        Scan for new token launches on DEX
        """
        print(f"→ Scanning new launches on {chain}...")
        results = []
        
        try:
            # DexScreener API - new pairs
            url = f"{self.dexscreener_api}/search?q={chain}"
            response = requests.get(url, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                pairs = data.get('pairs', [])
                
                for pair in pairs[:20]:  # Check recent 20
                    # Check if recently launched (< 48 hours)
                    created_at = pair.get('pairCreatedAt', 0)
                    age_hours = (time.time() * 1000 - created_at) / (1000 * 3600) if created_at else 999
                    
                    if age_hours < 48:  # Less than 48 hours old
                        token_data = {
                            'address': pair.get('pairAddress', ''),
                            'name': pair.get('baseToken', {}).get('name', ''),
                            'symbol': pair.get('baseToken', {}).get('symbol', ''),
                            'chain': pair.get('chainId', chain),
                            'dex': pair.get('dexId', ''),
                            'price': float(pair.get('priceUsd', 0)),
                            'liquidity': float(pair.get('liquidity', {}).get('usd', 0)),
                            'volume_24h': float(pair.get('volume', {}).get('h24', 0)),
                            'price_change_5m': float(pair.get('priceChange', {}).get('m5', 0)),
                            'price_change_1h': float(pair.get('priceChange', {}).get('h1', 0)),
                            'txns_5m': pair.get('txns', {}).get('m5', {}).get('buys', 0) + pair.get('txns', {}).get('m5', {}).get('sells', 0),
                            'age_hours': age_hours,
                            'url': f"https://dexscreener.com/{chain}/{pair.get('pairAddress', '')}"
                        }
                        
                        # Calculate degen score
                        degen_score = self.calculate_degen_score(token_data)
                        token_data['degen_score'] = degen_score
                        
                        # Check if pumping
                        is_pumping = self.detect_pump(token_data)
                        token_data['is_pumping'] = is_pumping
                        
                        # Only alert if score > threshold
                        min_score = float(os.getenv('MIN_DEGEN_SCORE', '50'))
                        if degen_score >= min_score or is_pumping:
                            results.append(token_data)
                            
        except Exception as e:
            print(f"Error scanning {chain}: {e}")
        
        return results
    
    def check_price_alerts(self) -> List[Dict]:
        """
        Check tracked tokens for stop loss / take profit triggers
        """
        alerts = []
        
        for address, tracking in list(self.tracked_tokens.items()):
            try:
                # Get current price
                url = f"{self.dexscreener_api}/tokens/{address}"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    pairs = data.get('pairs', [])
                    
                    if pairs:
                        current_price = float(pairs[0].get('priceUsd', 0))
                        entry_price = tracking['entry_price']
                        stop_loss = tracking['stop_loss']
                        take_profit = tracking['take_profit']
                        
                        # Calculate profit/loss %
                        pnl_percent = ((current_price - entry_price) / entry_price) * 100
                        
                        # Check stop loss
                        if current_price <= stop_loss:
                            alerts.append({
                                'type': 'STOP_LOSS',
                                'address': address,
                                'symbol': tracking['symbol'],
                                'entry_price': entry_price,
                                'current_price': current_price,
                                'stop_loss': stop_loss,
                                'pnl_percent': pnl_percent,
                                'url': f"https://dexscreener.com/ethereum/{address}"
                            })
                            # Remove from tracking
                            del self.tracked_tokens[address]
                        
                        # Check take profit
                        elif current_price >= take_profit:
                            alerts.append({
                                'type': 'TAKE_PROFIT',
                                'address': address,
                                'symbol': tracking['symbol'],
                                'entry_price': entry_price,
                                'current_price': current_price,
                                'take_profit': take_profit,
                                'pnl_percent': pnl_percent,
                                'url': f"https://dexscreener.com/ethereum/{address}"
                            })
                            # Remove from tracking
                            del self.tracked_tokens[address]
                            
            except Exception as e:
                print(f"Error checking {address}: {e}")
        
        return alerts
    
    def add_price_alert(self, address: str, symbol: str, entry_price: float, 
                       stop_loss_percent: float = -20, take_profit_percent: float = 100):
        """
        Add token to price tracking
        """
        stop_loss = entry_price * (1 + stop_loss_percent / 100)
        take_profit = entry_price * (1 + take_profit_percent / 100)
        
        self.tracked_tokens[address] = {
            'symbol': symbol,
            'entry_price': entry_price,
            'stop_loss': stop_loss,
            'take_profit': take_profit
        }
        
        print(f"✓ Tracking {symbol}: Entry ${entry_price:.8f}, SL ${stop_loss:.8f}, TP ${take_profit:.8f}")
    
    def send_telegram_alert(self, message: str):
        """Send Telegram alert"""
        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        payload = {
            'chat_id': self.telegram_chat_id,
            'text': message,
            'parse_mode': 'HTML',
            'disable_web_page_preview': False
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Telegram error: {e}")
            return False
    
    def format_launch_alert(self, token: Dict) -> str:
        """Format new launch alert"""
        score = token.get('degen_score', 0)
        is_pumping = token.get('is_pumping', False)
        
        # Score emoji
        if score >= 80:
            score_emoji = "🚀🚀🚀"
            potential = "VERY HIGH"
        elif score >= 60:
            score_emoji = "🚀🚀"
            potential = "HIGH"
        elif score >= 40:
            score_emoji = "🚀"
            potential = "MODERATE"
        else:
            score_emoji = "⚡"
            potential = "LOW"
        
        pump_status = "🔥 PUMPING NOW!" if is_pumping else ""
        
        message = f"""
💎 <b>NEW DEGEN COIN ALERT</b> {score_emoji} {pump_status}

<b>Token:</b> {token.get('name', 'Unknown')} (${token.get('symbol', '???')})
<b>Chain:</b> {token.get('chain', 'Unknown').upper()}
<b>DEX:</b> {token.get('dex', 'Unknown').upper()}

<b>🎯 DEGEN SCORE: {score:.0f}/100 ({potential} POTENTIAL)</b>

<b>💰 Stats:</b>
• Price: ${token.get('price', 0):.10f}
• Liquidity: ${token.get('liquidity', 0):,.0f}
• Volume 24h: ${token.get('volume_24h', 0):,.0f}
• Age: {token.get('age_hours', 0):.1f} hours

<b>📊 Price Action:</b>
• 5m: {token.get('price_change_5m', 0):+.1f}%
• 1h: {token.get('price_change_1h', 0):+.1f}%
• Txns (5m): {token.get('txns_5m', 0)}

<b>🔗 Trade:</b>
{token.get('url', 'Not available')}

<b>⚠️ DEGEN WARNING:</b>
✅ Check contract on scanner
✅ Verify liquidity locked
✅ Check holder distribution
✅ Use SMALL position size
✅ Set stop loss -20%
✅ Never invest more than you can lose

<i>This is extremely high risk. Most degen coins go to zero.</i>
"""
        return message.strip()
    
    def format_pump_alert(self, token: Dict) -> str:
        """Format pump detection alert"""
        message = f"""
🔥🔥🔥 <b>PUMP DETECTED!</b> 🔥🔥🔥

<b>Token:</b> ${token.get('symbol', '???')}
<b>Chain:</b> {token.get('chain', 'Unknown').upper()}

<b>📈 PUMP METRICS:</b>
• 5m: <b>{token.get('price_change_5m', 0):+.1f}%</b>
• 1h: <b>{token.get('price_change_1h', 0):+.1f}%</b>
• Volume Surge: <b>{token.get('volume_surge', 1):.1f}x</b>

<b>💰 Current Price:</b> ${token.get('price', 0):.10f}

<b>🔗 Trade:</b>
{token.get('url', 'Not available')}

<b>⚠️ PUMP WARNING:</b>
• Pumps can dump INSTANTLY
• Take profits on the way up
• Don't FOMO at peak
• Use stop loss
• High risk of rug pull
"""
        return message.strip()
    
    def format_price_alert(self, alert: Dict) -> str:
        """Format stop loss / take profit alert"""
        alert_type = alert['type']
        pnl = alert['pnl_percent']
        
        if alert_type == 'STOP_LOSS':
            emoji = "🛑"
            title = "STOP LOSS TRIGGERED"
            color = "RED"
        else:
            emoji = "✅"
            title = "TAKE PROFIT TRIGGERED"
            color = "GREEN"
        
        message = f"""
{emoji} <b>{title}</b> {emoji}

<b>Token:</b> ${alert['symbol']}

<b>📊 Trade Summary:</b>
• Entry: ${alert['entry_price']:.10f}
• Current: ${alert['current_price']:.10f}
• Target: ${alert.get('stop_loss' if alert_type == 'STOP_LOSS' else 'take_profit', 0):.10f}

<b>💰 P/L: {pnl:+.2f}%</b>

<b>🔗 Trade:</b>
{alert.get('url', '')}

<b>{'🛑 Consider selling to limit losses' if alert_type == 'STOP_LOSS' else '✅ Consider taking profits'}</b>
"""
        return message.strip()
    
    def run_monitoring_cycle(self):
        """Run one monitoring cycle"""
        print(f"\n{'='*70}")
        print(f"💎 DEGEN COIN HUNTER - Cycle Started")
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}")
        
        # Scan chains
        chains = os.getenv('DEGEN_CHAINS', 'ethereum,bsc,polygon').split(',')
        
        all_launches = []
        for chain in chains:
            launches = self.scan_new_launches(chain.strip())
            all_launches.extend(launches)
        
        # Send alerts for new launches
        new_alerts = 0
        for launch in all_launches:
            message = self.format_launch_alert(launch)
            if self.send_telegram_alert(message):
                new_alerts += 1
                time.sleep(2)
        
        # Check price alerts
        price_alerts = self.check_price_alerts()
        for alert in price_alerts:
            message = self.format_price_alert(alert)
            self.send_telegram_alert(message)
            time.sleep(1)
        
        print(f"\n📊 Cycle Summary:")
        print(f"   New launches found: {len(all_launches)}")
        print(f"   Alerts sent: {new_alerts}")
        print(f"   Price alerts: {len(price_alerts)}")
        print(f"{'='*70}\n")
    
    def run_continuous(self, interval_minutes: int = 5):
        """Run continuous monitoring"""
        print(f"""
╔══════════════════════════════════════════════════════════════════╗
║          DEGEN COIN HUNTER - ACTIVATED                           ║
║                                                                  ║
║  💎 Hunting: New launches, Pumps, Price alerts                  ║
║  📱 Alerts: Telegram with stop loss / take profit                ║
║  ⏱️  Interval: {interval_minutes} minutes                                        ║
║  🔒 Safe: Read-only, NO auto-trading                            ║
╚══════════════════════════════════════════════════════════════════╝
""")
        
        self.send_telegram_alert(
            "💎 <b>Degen Coin Hunter Started!</b>\n\n"
            f"✓ Monitoring every {interval_minutes} minutes\n"
            "✓ Scanning: New launches & pumps\n"
            "✓ Tracking: Price alerts (SL/TP)\n\n"
            "⚠️ <b>HIGH RISK WARNING:</b>\n"
            "Degen coins are EXTREMELY risky!\n"
            "Only use money you can afford to lose!\n\n"
            "Stay safe and DYOR! 💎"
        )
        
        while True:
            try:
                self.run_monitoring_cycle()
                print(f"💤 Sleeping {interval_minutes} minutes...\n")
                time.sleep(interval_minutes * 60)
                
            except KeyboardInterrupt:
                print("\n\n🛑 Hunter stopped")
                self.send_telegram_alert("🛑 <b>Degen Coin Hunter Stopped</b>")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                time.sleep(60)


def main():
    """Main entry point"""
    from dotenv import load_dotenv
    load_dotenv()
    
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN', '')
    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID', '')
    
    if not telegram_token or not telegram_chat_id:
        print("❌ Missing Telegram configuration!")
        return
    
    hunter = DegenCoinHunter(telegram_token, telegram_chat_id)
    interval = int(os.getenv('CHECK_INTERVAL', '5'))
    hunter.run_continuous(interval_minutes=interval)


if __name__ == "__main__":
    main()
