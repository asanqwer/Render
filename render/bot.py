import os
import requests
import json
import random
import pytz
import threading
from telegram import Bot
from telegram.ext import Updater, CommandHandler
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from flask import Flask

# Load environment variables
load_dotenv()

# === Step 1: Trigger registration link once ===
def open_registration_link():
    try:
        url = "https://www.18sikkim.com/#/register?invitationCode=643745098970"
        headers = {"User-Agent": "Mozilla/5.0"}
        requests.get(url, headers=headers)
        print("✅ Registration link triggered.")
    except Exception as e:
        print(f"⚠️ Failed to open registration link: {e}")

open_registration_link()

# === Step 2: Bot config ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_CHAT_ID = "-1002519195018"  # Replace with your Telegram group ID
bot = Bot(token=BOT_TOKEN)

stickers = [
    "CAACAgQAAxkBAAKmh2f5EBjXCvSqjGVYDT9P7yjKW6_IAAKOCAACi9XoU5p5sAokI77kNgQ",
    "CAACAgQAAxkBAAKmimf5EB9GTlXRtwVB3ez1nBUKzf69AAKaDAACfx_4UvcUEDj6i_r9NgQ",
    "CAACAgQAAxkBAAKmjWf5ECecZUCJtSeuqsaaVWILpTuyAALICwACG86YUDSKklgR_M5FNgQ",
    "CAACAgIAAxkBAAKmkGf5EDBgwnSDovUPpQGsTjMQdU69AAL4DAACNyx5S6FYW3VBcuj4NgQ"
]

# === Step 3: Prediction logic ===
def get_latest_period():
    url = "https://api.51gameapi.com/api/webapi/GetNoaverageEmerdList"
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "Accept": "application/json",
        "Authorization": "Bearer YOUR_TOKEN_HERE"  # Replace with valid token if needed
    }
    payload = {
        "pageSize": 10,
        "pageNo": 1,
        "typeId": 1,
        "language": 0,
        "random": "6fadc24ccf2c4ed4afb5a1a5f84d2ba4",
        "signature": "4E071E587A80572ED6065D6F135F3ABE",
        "timestamp": 1733117040
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        data = response.json()
        return int(data["data"]["list"][0]["issueNumber"]) + 1
    except Exception as e:
        print(f"⚠️ API error: {e}")
        return None

def get_random_prediction():
    return random.choice(["Big", "Small"])

def send_prediction():
    period = get_latest_period()
    if not period:
        print("❌ Could not fetch period.")
        return

    prediction = get_random_prediction()
    message = f"[WINGO 1MINUTE]\nPeriod {period}\nChoose - {prediction}"
    bot.send_message(chat_id=GROUP_CHAT_ID, text=message)

    if random.random() < 0.5:
        bot.send_sticker(chat_id=GROUP_CHAT_ID, sticker=random.choice(stickers))

    print(f"✅ Sent: {message}")

# === Step 4: Scheduler (runs in background) ===
scheduler = BackgroundScheduler(timezone=pytz.utc)
scheduler.add_job(send_prediction, 'interval', minutes=1)
scheduler.start()

# === Step 5: Telegram Bot Handlers ===
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="🤖 Bot is running!")

updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))

# Start bot polling in a thread so Flask can run too
threading.Thread(target=updater.start_polling).start()

# === Step 6: Flask web server to keep Render alive ===
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "🚀 Telegram bot is running on Render!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host="0.0.0.0", port=port)
