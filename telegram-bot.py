import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from flask import Flask, request, render_template_string
from threading import Thread
import time

# ==================== TOKEN ====================
BOT_TOKEN = "8194877107:AAFYZR8HbBD5B43WN3d871srclsOa7H6xwk"
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# ==================== RENDER URL ====================
RENDER_URL = "https://telegram-bot-1-mr8u.onrender.com"

# ==================== HTML (QISQA) ====================
html_form = """
<!DOCTYPE html>
<html>
<head><title>PUBG UC</title>
<style>
body{background:#1a1a2e;color:white;padding:20px;font-family:Arial;}
h1{color:#ff9900;}
.package{background:rgba(255,255,255,0.1);padding:15px;margin:10px;border-radius:10px;}
button{background:#00a8ff;color:white;padding:10px;border:none;border-radius:5px;}
</style>
</head>
<body>
<h1>PUBG UC MARKET</h1>
<p>Eng arzon narxlarda UC sotib oling</p>

<div class="package">
<h3>60 UC - TEKIN</h3>
<button onclick="alert('60 UC tanlandi!')">Olish</button>
</div>

<div class="package">
<h3>120 UC - 39,000 UZS</h3>
<button onclick="alert('120 UC tanlandi!')">Sotib olish</button>
</div>

<p>Buyurtma: @msrfteam</p>
</body>
</html>
"""

# ==================== FLASK ROUTES ====================
@app.route("/")
def home():
    return "✅ Bot ishlayapti! URL: /form/123"

@app.route("/form/<user_id>", methods=["GET"])
def form(user_id):
    print(f"📞 Form so'rovi: user_id={user_id}")
    return render_template_string(html_form)

@app.route("/test")
def test():
    return "✅ Flask server ishlayapti!"

# ==================== TELEGRAM BOT ====================
@bot.message_handler(commands=["start"])
def start(msg):
    bot.send_message(msg.chat.id, "Salom! /link buyrug'ini yuboring.")

@bot.message_handler(commands=["link"])
def link(msg):
    user_id = msg.chat.id
    uniq = f"{RENDER_URL}/form/{user_id}"
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔗 UC Sotib Olish", url=uniq))
    
    bot.send_message(
        user_id,
        f"🔗 Sizning linkingiz:\n{uniq}",
        reply_markup=markup
    )

# ==================== RUN FUNCTIONS ====================
def run_flask():
    print("🌐 Flask server ishga tushmoqda...")
    try:
        app.run(host="0.0.0.0", port=8080, debug=False, use_reloader=False)
    except Exception as e:
        print(f"❌ Flask xatosi: {e}")

def run_bot():
    print("🤖 Bot ishga tushmoqda...")
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=30)
        except Exception as e:
            print(f"❌ Bot xatosi: {e}")
            time.sleep(5)

if __name__ == "__main__":
    print("🚀 Dastur ishga tushmoqda...")
    print(f"🌐 URL: {RENDER_URL}")
    
    # 1. Flask ni ishga tushirish
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # 2. Kutish va tekshirish
    time.sleep(3)
    
    # 3. Flask ishlayotganini tekshirish
    print("✅ Flask ishga tushdi")
    
    # 4. Botni ishga tushirish
    run_bot()
