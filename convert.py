from flask import Flask, request
import logging
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

TOKEN = "7551381595:AAHW7Chk4-8OLIwM6D4FQJUZMDLpH5SeFbQ"
bot = Bot(TOKEN)

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

async def reply_hello(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello")

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    application.update_queue.put_nowait(update)
    return "OK", 200

def main():
    global application
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_hello))

if __name__ == "__main__":
    main()