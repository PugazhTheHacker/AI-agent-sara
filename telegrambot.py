"""
Telegram + Gemini AI Chatbot
Author  : Pugazhenthi J
AI Agent: Sara
"""

import os
import time
import requests
from google import genai

# === CONFIG ===
BOT_TOKEN = "YOUR_TOKEN"
GEMINI_API_KEY = "YOUR_TOKEN"
if not BOT_TOKEN or not GEMINI_API_KEY:
    print("❌ Missing BOT_TOKEN or GEMINI_API_KEY environment variables.")
    print("👉 Example:")
    print('export BOT_TOKEN="your_telegram_bot_token"')
    print('export GEMINI_API_KEY="your_gemini_api_key"')
    exit()

# === TELEGRAM URL ===
TG_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# === GEMINI CLIENT ===
client = genai.Client(api_key=GEMINI_API_KEY)

# === TELEGRAM FUNCTIONS ===
def get_updates(offset=None):
    """Fetch new messages from Telegram."""
    params = {"timeout": 100, "offset": offset}
    res = requests.get(f"{TG_URL}/getUpdates", params=params)
    return res.json()

def send_message(chat_id, text):
    """Send a text message back to the user."""
    data = {"chat_id": chat_id, "text": text}
    requests.post(f"{TG_URL}/sendMessage", data=data)

# === GEMINI AI FUNCTION ===
def ask_sara(prompt):
    """Ask Sara (Gemini AI) for a response."""
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"You are Sara, an AI assistant created by Pugazhenthi J. {prompt}"
        )
        return response.text or "⚠️ Sara didn’t respond this time."
    except Exception as e:
        return f"⚠️ Sara error: {e}"

# === MAIN BOT LOOP ===
def main():
    print("🤖 Sara (Gemini AI) Telegram Bot is running...")
    offset = None

    while True:
        updates = get_updates(offset)
        if "result" in updates:
            for item in updates["result"]:
                offset = item["update_id"] + 1
                message = item.get("message", {})
                chat_id = message.get("chat", {}).get("id")
                text = message.get("text", "")

                if not text or not chat_id:
                    continue

                print(f"📩 From {chat_id}: {text}")

                if text.lower() == "/start":
                    send_message(chat_id, "👋 Hi! I’m *Sara*, an AI assistant created by *Pugazhenthi J*. How can I help you today?")
                else:
                    reply = ask_sara(text)
                    send_message(chat_id, reply)

        time.sleep(1)

if __name__ == "__main__":
    main()
