# AI-agent-sara


#🤖 AI-Agent-Sara — Gemini Powered Telegram Bot

AI-Agent-Sara is an intelligent Telegram chatbot built with Python.
It connects Google Gemini AI API with the Telegram Bot API, letting you chat with a powerful AI directly inside Telegram — like having your own personal AI assistant on your phone.

#🌟 Features

✅ Chat with Google’s Gemini AI directly in Telegram
✅ Fully written in Python using only requests
✅ Works on Linux, Windows, or cloud hosting (Render, Replit, VPS)
✅ Secure with environment variables (no hard-coded keys)
✅ Easy to extend for tools like nmap, weather, or news

#🧠 How It Works

Telegram Bot receives your message using Telegram Bot API.
The Python program forwards that message text to Gemini AI API.
Gemini processes the text using its large language model (LLM).

#🚀 Hosting on Render (Free 24/7)
Create a GitHub repo:
```
AI-Agent-Sara/
├── ai_agent_sara.py
├── requirements.txt
└── Procfile
```
#Install python pakages
```
pip3 install requirements.txt
```
#How to run this file 
```
python3 telegrambot.py
```

#API_TOKEN How to use 
```
BOT_TOKEN = your_telegram_bot_token
GEMINI_API_KEY = your_gemini_api_key
```
#💬 Example Questions to Test
Try chatting with Sara on Telegram:
```
/start
Hello Sara!
What is AI?
Explain cloud computing.
Write a short Tamil poem.
Who created Python?
Generate a funny quote about hackers.
```

#🧩 Future Ideas
You can extend AI-Agent-Sara easily:
🌦️ Add live weather info
🔍 Integrate Linux tools like nmap, ping, or whois
🧮 Add calculator or translator mode
📊 Connect it to databases for chat memory

#🛡️ Security Notes
Always store API keys in environment variables, not in the code.
Never share your tokens publicly.
Use .gitignore to hide local config files before pushing to GitHub.



#✨ Credits

Project: AI-Agent-Sara
Author: Pugazhenthi J
Built with:
🧠 Google Gemini API
💬 Telegram Bot API
🐍 Python 3
☁️ Render (for hosting)
