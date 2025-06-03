# send_job.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_CHAT_ID = "-1002519195018"  # Replace with your real group ID

def send_message():
    text = "🕒 This is a scheduled message sent by a Render Cron Job."
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": GROUP_CHAT_ID,
        "text": text
    }
    requests.post(url, data=data)

if __name__ == "__main__":
    send_message()
