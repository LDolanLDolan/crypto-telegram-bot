import os
import sqlite3
import requests
import logging
import asyncio
from datetime import datetime
from typing import Dict, List
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class SimpleCryptoBot:
    def __init__(self):
        self.db_path = "crypto_alerts.db"
        self.coingecko_url = "https://api.coingecko.com/api/v3/simple/price"
        
        # Supported cryptocurrencies
        self.coins = {
            'bitcoin': {'name': 'Bitcoin', 'symbol': 'BTC', 'emoji': '₿'},
            'ethereum': {'name': 'Ethereum', 'symbol': 'ETH', 'emoji': 'Ξ'},
            'solana': {'name': 'Solana', 'symbol': 'SOL', 'emoji': '☀️'},
            'ripple': {'name': 'XRP', 'symbol': 'XRP', 'emoji': '💧'},
            'cardano': {'name': 'Cardano', 'symbol': 'ADA', 'emoji': '₳'},
            'dogecoin': {'name': 'Dogecoin', 'symbol': 'DOGE', 'emoji': '🐕'},
            'polkadot': {'name': 'Polkadot', 'symbol': 'DOT', 'emoji': '⚫'},
            'chainlink': {'name': 'Chainlink', 'symbol': 'LINK', 'emoji': '🔗'},
            'polygon': {'name': 'Polygon', 'symbol': 'MATIC', 'emoji': '🔷'},
            'litecoin': {'name': 'Litecoin', 'symbol': 'LTC', 'emoji': 'Ł'}
        }
        
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                chat_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                coin_id TEXT,
                coin_symbol TEXT,
                alert_type TEXT,
                target_price REAL,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    
    def get_prices(self) -> Dict:
        """Fetch current crypto prices"""
        try:
            coin_ids = ','.join(self.coins.keys())
            url = f"{self.coingecko_url}?ids={coin_ids}&vs_currencies=usd"
            
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            prices = response.json()
            logger.info(f"Fetched prices for {len(prices)} coins")
            return prices
        except Exception as e:
            logger.error(f"Error fetching prices: {e}")
            return {}
    
    def add_user(self, user_id: int, username: str, chat_id: int):
        """Add user to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO users (user_id, username, chat_id)
            VALUES (?, ?, ?)
        ''', (user_id, username or "", chat_id))
        
        conn.commit()
        conn.close()
        logger.info(f"User {user_id} added/updated")
    
    def add_alert(self, user_id: int, coin_id: str, alert_type: str, target_price: float) -> bool:
        """Add price alert"""
        if coin_id not in self.coins:
            return False
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Remove existing alert of same type
        cursor.execute('''
            UPDATE alerts SET is_active = 0 
            WHERE user_id = ? AND coin_id = ? AND alert_type = ? AND is_active = 1
        ''', (user_id, coin_id, alert_type))
        
        # Add new alert
        cursor.execute('''
            INSERT INTO alerts (user_id, coin_id, coin_symbol, alert_type, target_price)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, coin_id, self.coins[coin_id]['symbol'], alert_type, target_price))
        
        conn.commit()
        conn.close()
        logger.info(f"Alert added: {user_id} - {coin_id} {alert_type} at {target_price}")
        return True
    
    def get_user_alerts(self, user_id: int) -> List[Dict]:
        """Get user's active alerts"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT coin_id, coin_symbol, alert_type, target_price
            FROM alerts 
            WHERE user_id = ? AND is_active = 1
            ORDER BY created_at DESC
        ''', (user_id,))
        
        alerts = []
        for row in cursor.fetchall():
            alerts.append({
                'coin_id': row[0],
                'coin_symbol': row[1],
                'alert_type': row[2],
                'target_price': row[3]
            })
        
        conn.close()
        return alerts
    
    def check_alerts(self, application) -> None:
        """Check alerts and send notifications"""
        prices = self.get_prices()
        if not prices:
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT a.id, a.user_id, u.chat_id, a.coin_id, a.coin_symbol, 
                   a.alert_type, a.target_price
            FROM alerts a
            JOIN users u ON a.user_id = u.user_id
            WHERE a.is_active = 1
        ''')
        
        triggered_alerts = []
        
        for row in cursor.fetchall():
            alert_id, user_id, chat_id, coin_id, coin_symbol, alert_type, target_price = row
            
            if coin_id not in prices:
                continue
            
            current_price = prices[coin_id]['usd']
            should_trigger = False
            
            if alert_type == 'buy' and current_price <= target_price:
                should_trigger = True
                message = f"🔔 *BUY ALERT!*\n\n"
                message += f"{self.coins[coin_id]['emoji']} *{coin_symbol}* has reached your buy target!\n"
                message += f"Current: `${current_price:,.2f}`\n"
                message += f"Target: `${target_price:,.2f}`\n\n"
                message += f"💡 Good opportunity to buy!"
            
            elif alert_type == 'sell' and current_price >= target_price:
                should_trigger = True
                message = f"🚨 *SELL ALERT!*\n\n"
                message += f"{self.coins[coin_id]['emoji']} *{coin_symbol}* has reached your sell target!\n"
                message += f"Current: `${current_price:,.2f}`\n"
                message += f"Target: `${target_price:,.2f}`\n\n"
                message += f"💰 Consider taking profits!"
            
            if should_trigger:
                triggered_alerts.append((alert_id, chat_id, message))
        
        # Send notifications
        for alert_id, chat_id, message in triggered_alerts:
            try:
                asyncio.create_task(
                    application.bot.send_message(
                        chat_id=chat_id,
                        text=message,
                        parse_mode='Markdown'
                    )
                )
                
                # Deactivate alert
                cursor.execute('UPDATE alerts SET is_active = 0 WHERE id = ?', (alert_id,))
                logger.info(f"Alert sent and deactivated: {alert_id}")
                
            except Exception as e:
                logger.error(f"Error sending alert {alert_id}: {e}")
        
        if triggered_alerts:
            conn.commit()
        conn.close()

# Global bot instance
bot = SimpleCryptoBot()

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    bot.add_user(user.id, user.username, chat_id)
    
    message = "🤖 *Welcome to Crypto Alert Bot!*\n\n"
    message += "I'll help you track cryptocurrency prices.\n\n"
    message += "*Commands:*\n"
    message += "📊 `/prices` - Current prices\n"
    message += "⚡ `/buy coin price` - Set buy alert\n"
    message += "💰 `/sell coin price` - Set sell alert\n"
    message += "📋 `/alerts` - Your alerts\n\n"
    message += "*Example:* `/buy bitcoin 30000`"
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def prices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /prices command"""
    price_data = bot.get_prices()
    
    if not price_data:
        await update.message.reply_text("❌ Couldn't fetch prices. Try again later.")
        return
    
    message = "📊 *Current Crypto Prices:*\n\n"
    
    for coin_id, coin_info in bot.coins.items():
        if coin_id in price_data:
            price = price_data[coin_id]['usd']
            message += f"{coin_info['emoji']} *{coin_info['symbol']}*: `${price:,.2f}`\n"
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def buy_alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /buy command"""
    if len(context.args) != 2:
        await update.message.reply_text("Usage: `/buy <coin> <price>`\nExample: `/buy bitcoin 30000`", parse_mode='Markdown')
        return
    
    coin_name = context.args[0].lower()
    try:
        target_price = float(context.args[1])
    except ValueError:
        await update.message.reply_text("❌ Invalid price. Please enter a number.")
        return
    
    # Find coin
    coin_id = None
    for cid, cinfo in bot.coins.items():
        if coin_name in [cid, cinfo['symbol'].lower(), cinfo['name'].lower()]:
            coin_id = cid
            break
    
    if not coin_id:
        supported = ", ".join([info['symbol'] for info in bot.coins.values()])
        await update.message.reply_text(f"❌ Coin not supported. Available: {supported}")
        return
    
    success = bot.add_alert(update.effective_user.id, coin_id, 'buy', target_price)
    
    if success:
        coin_info = bot.coins[coin_id]
        message = f"✅ *Buy alert set!*\n\n{coin_info['emoji']} {coin_info['symbol']} at `${target_price:,.2f}`"
        await update.message.reply_text(message, parse_mode='Markdown')

async def sell_alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /sell command"""
    if len(context.args) != 2:
        await update.message.reply_text("Usage: `/sell <coin> <price>`\nExample: `/sell ethereum 2500`", parse_mode='Markdown')
        return
    
    coin_name = context.args[0].lower()
    try:
        target_price = float(context.args[1])
    except ValueError:
        await update.message.reply_text("❌ Invalid price. Please enter a number.")
        return
    
    # Find coin
    coin_id = None
    for cid, cinfo in bot.coins.items():
        if coin_name in [cid, cinfo['symbol'].lower(), cinfo['name'].lower()]:
            coin_id = cid
            break
    
    if not coin_id:
        supported = ", ".join([info['symbol'] for info in bot.coins.values()])
        await update.message.reply_text(f"❌ Coin not supported. Available: {supported}")
        return
    
    success = bot.add_alert(update.effective_user.id, coin_id, 'sell', target_price)
    
    if success:
        coin_info = bot.coins[coin_id]
        message = f"✅ *Sell alert set!*\n\n{coin_info['emoji']} {coin_info['symbol']} at `${target_price:,.2f}`"
        await update.message.reply_text(message, parse_mode='Markdown')

async def alerts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /alerts command"""
    user_alerts = bot.get_user_alerts(update.effective_user.id)
    
    if not user_alerts:
        await update.message.reply_text("📭 You don't have any active alerts.")
        return
    
    message = "📋 *Your Active Alerts:*\n\n"
    
    for alert in user_alerts:
        coin_info = bot.coins[alert['coin_id']]
        alert_emoji = "🔻" if alert['alert_type'] == 'buy' else "🔺"
        message += f"{coin_info['emoji']} *{alert['coin_symbol']}* {alert_emoji}\n"
        message += f"   {alert['alert_type'].title()} at `${alert['target_price']:,.2f}`\n\n"
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    message = "🤖 *Crypto Alert Bot Help*\n\n"
    message += "*Commands:*\n"
    message += "📊 `/prices` - Current prices\n"
    message += "⚡ `/buy <coin> <price>` - Set buy alert\n"
    message += "💰 `/sell <coin> <price>` - Set sell alert\n"
    message += "📋 `/alerts` - Your alerts\n\n"
    message += "*Supported Coins:*\n"
    
    for coin_info in bot.coins.values():
        message += f"{coin_info['emoji']} {coin_info['symbol']} "
    
    message += "\n\n*Examples:*\n"
    message += "`/buy bitcoin 30000`\n"
    message += "`/sell eth 2500`"
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def price_check_job(context: ContextTypes.DEFAULT_TYPE):
    """Background job to check prices"""
    bot.check_alerts(context.application)

def main():
    """Main function"""
    # Get token
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        print("❌ TELEGRAM_BOT_TOKEN not set!")
        return
    
    print("🚀 Starting Crypto Alert Bot...")
    
    # Create application
    application = Application.builder().token(token).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("prices", prices))
    application.add_handler(CommandHandler("buy", buy_alert))
    application.add_handler(CommandHandler("sell", sell_alert))
    application.add_handler(CommandHandler("alerts", alerts))
    application.add_handler(CommandHandler("help", help_command))
    
    # Add background job
    application.job_queue.run_repeating(price_check_job, interval=30, first=10)
    
    print("✅ Bot started successfully!")
    print("💡 Try /start in your Telegram bot")
    
    # Start polling
    application.run_polling()

if __name__ == '__main__':
    main()