import os
import time
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
EMAIL_USER = os.getenv("EMAIL_USER")  # Gmail SMTP login email
EMAIL_PASS = os.getenv("EMAIL_PASS")  # Gmail App Password

if not BOT_TOKEN or not GEMINI_API_KEY:
    print("❌ Missing BOT_TOKEN or GEMINI_API_KEY. Use export command.")
    exit()

TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

# store conversation for each chat
email_state = {}

# ---------------- Telegram API ----------------
def get_updates(offset=None):
    params = {'timeout': 100, 'offset': offset}
    response = requests.get(TELEGRAM_URL + "/getUpdates", params=params)
    return response.json()

def send_message(chat_id, text):
    data = {'chat_id': chat_id, 'text': text}
    requests.post(TELEGRAM_URL + "/sendMessage", data=data)

# ---------------- Gemini API ----------------
def ask_gemini(prompt):
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(GEMINI_URL, headers=headers, params=params, json=data)

    if response.status_code == 200:
        try:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except:
            return "⚠️ Gemini response error"
    else:
        return f"❌ Gemini API Error: {response.status_code}"

# ---------------- Email Sender ----------------
def send_email_dynamic(sender, receiver, subject, body):
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()
        return f"📩 Email sent successfully from {sender} to {receiver} 🚀"
    except Exception as e:
        return f"❌ Email send failed: {str(e)}"

# ---------------- Main Loop ----------------
def main():
    print("🤖 AI-Agent-Sara is now online...")
    offset = None

    while True:
        updates = get_updates(offset)
        if "result" in updates:
            for item in updates["result"]:
                offset = item["update_id"] + 1
                message = item.get("message")
                if not message:
                    continue

                chat_id = message["chat"]["id"]
                text = message.get("text", "").strip()

                print(f"📩 {chat_id}: {text}")

                # ---- EMAIL AUTOMATION FLOW ----
                if chat_id in email_state:
                    state = email_state[chat_id]

                    # Step 1 — Sender email
                    if state["step"] == 1:
                        state["sender"] = text
                        state["step"] = 2
                        send_message(chat_id, "📨 Enter receiver email:\nExample: receiver@gmail.com")
                        continue

                    # Step 2 — Receiver email
                    elif state["step"] == 2:
                        state["receiver"] = text
                        state["step"] = 3
                        send_message(chat_id, "📌 Enter email subject:")
                        continue

                    # Step 3 — Subject
                    elif state["step"] == 3:
                        state["subject"] = text
                        state["step"] = 4
                        send_message(chat_id, "✍️ Enter message body:")
                        continue

                    # Step 4 — Final body → send email
                    elif state["step"] == 4:
                        state["body"] = text
                        result = send_email_dynamic(
                            state["sender"],
                            state["receiver"],
                            state["subject"],
                            state["body"]
                        )
                        send_message(chat_id, result)
                        del email_state[chat_id]
                        continue

                # Start email automation
                if text.lower() == "/email":
                    send_message(chat_id,
                                 "📧 Enter your email (Sender):\nExample: user@gmail.com")
                    email_state[chat_id] = {"step": 1}
                    continue

                # Start bot
                if text.lower() == "/start":
                    send_message(
                        chat_id,
                        "👋 Hello, I'm Sara — Gemini AI Assistant.\n\n"
                        "💬 Just chat with me normally.\n"
                        "📧 To send an email → type /email\n"
                    )
                    continue

                # Default Gemini chat
                reply = ask_gemini(text)
                send_message(chat_id, reply)

        time.sleep(1)

if __name__ == "__main__":
    main()
