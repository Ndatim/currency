import logging
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests
import threading

# Setup Flask app
app = Flask(__name__)

# Logging for debugging purposes
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

API_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"  # Replace with your bot's token
EXCHANGE_API_URL = "https://api.exchangerate-api.com/v4/latest/"
CURRENCY_NAMES = {
    "USD": "US Dollars", "EUR": "Euros", "GBP": "British Pounds", 
    "RWF": "Rwandan Franc", "KES": "Kenyan Shillings", 
    "INR": "Indian Rupees", "JPY": "Japanese Yen", 
    "AUD": "Australian Dollars", "CAD": "Canadian Dollars", "CHF": "Swiss Francs"
}

answer_count = 0

# Telegram bot function
async def convert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global answer_count
    if not context.args:
        await update.message.reply_text("🚨 CONVERT TO ANY CURRENCY 🚨\n\n💬 How to use (Type):\n1️⃣ /convert 269 USD to EUR  (OR)\n2️⃣ /convert 269 USD EUR\n\n🔗 Use one best format for you.\n🔗 Currency can be both capital/lower case")
        return

    try:
        parts = ' '.join(context.args).split()
        amount, currency_from, currency_to = (float(parts[0]), parts[1].upper(), parts[3].upper()) if "to" in parts and len(parts) == 4 else (float(parts[0]), parts[1].upper(), parts[2].upper())

        processing_message = await update.message.reply_text("🔄 Processing...")
        data = requests.get(f"{EXCHANGE_API_URL}{currency_from}").json()

        if currency_to not in data.get("rates", {}):
            await processing_message.edit_text("❌ Error: Invalid currency")
            return

        converted_amount = amount * data["rates"][currency_to]
        result_message = f"✅ {amount} {currency_from} = {converted_amount:.2f} {currency_to}.\n\n💰 {currency_from} ({CURRENCY_NAMES.get(currency_from, currency_from)})\n💰 {currency_to} ({CURRENCY_NAMES.get(currency_to, currency_to)})\n\n"

        answer_count += 1
        if answer_count >= 4:
            result_message += "👉 Click to share this bot to your friend: https://t.me/share/url?url=https://t.me/Manyservicebot&text=Check%20out%20Multi%20Service%20Bot"
            answer_count = 0

        await processing_message.edit_text(result_message)

    except (ValueError, IndexError):
        await update.message.reply_text("❌ Invalid format. Use:\n1️⃣ /convert 269 USD to EUR  (OR)\n2️⃣ /convert 269 USD EUR")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

# Flask route for health check or any other API endpoints you want to use
@app.route('/')
def index():
    return "Your Flask API is running!"

# Function to run the Telegram bot in a separate thread
def run_bot():
    app = Application.builder().token(API_TOKEN).build()
    app.add_handler(CommandHandler("convert", convert))
    app.run_polling()

# Run the Telegram bot in a separate thread so it can work alongside Flask
if __name__ == '__main__':
    # Start the Flask app in a separate thread
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000)).start()
    # Run the bot in the main thread
    run_bot()