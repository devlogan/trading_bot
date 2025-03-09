import requests
from utils.constants import TELEGRAM_CHAT_ID, TELEGRAM_BOT_TOKEN

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print(f"❌ Error sending message: {response.text}")
    else:
        print(f"✅ Sent message: {message}")
