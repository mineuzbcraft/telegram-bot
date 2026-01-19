import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from flask import Flask, request, render_template_string
from threading import Thread
import os
import time

# ==================== TOKEN ====================
# Tokenni to'g'ri olish
BOT_TOKEN = "8194877107:AAFYZR8HbBD5B43WN3d871srclsOa7H6xwk"  # ⬅️ To'g'ridan-to'g'ri
# Yoki: BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    print("ERROR: UC sevice vaqtinchalik ishlamayapti")
    exit()

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# ==================== RENDER URL ====================
# BU YERGA O'Z RENDER URL'INGIZ
RENDER_URL = "https://telegram-bot-1-mr8u.onrender.com"

# ==================== HTML FORM (QISQACHA) ====================
html_form = """
<!DOCTYPE html>
<html>
<head><title>PUBG UC</title>
<style>body{background:#1a1a2e;color:white;padding:20px;}</style>
</head>
<body>
<h1>PUBG UC Sotib Olish</h1>
<form method="POST">
<input type="email" name="email" placeholder="Email" required><br><br>
<button type="submit">Buyurtma berish</button>
</form>
</body>
</html>
"""

# ==================== FLASK ROUTES ====================
@app.route("/form/<user_id>", methods=["GET", "POST"])
def form(user_id):
    if request.method == "POST":
        email = request.form.get("email")
        
        # Foydalanuvchiga xabar
        user_message = f"✅ Buyurtmangiz qabul qilindi!\nEmail: {email}"
        bot.send_message(user_id, user_message)
        
        # Admin ga xabar
        ADMIN_ID = 6948346741
        admin_message = f"🛒 YANGI BUYURTMA!\nUser ID: {user_id}\nEmail: {email}"
        bot.send_message(ADMIN_ID, admin_message)
        
        return "Buyurtma qabul qilindi!"

    return render_template_string(html_form)

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
    app.run(host="0.0.0.0", port=10000)  # Render uchun 10000 port

def run_bot():
    print("🤖 Bot ishga tushmoqda...")
    bot.polling(none_stop=True, interval=0, timeout=60)

if __name__ == "__main__":
    print(f"🌐 URL: {RENDER_URL}")
    
    # Flask ni threadda ishga tushirish
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Botni asosiy threadda ishga tushirish
    time.sleep(2)  # Flask ishga tushishi uchun kutish
    run_bot()
