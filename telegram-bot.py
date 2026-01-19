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

# ==================== HTML (QISQA TEST) ====================
html_form = """
<!DOCTYPE html>
<html>
<head>
    <title>PUBG UC</title>
    <style>
        body { background: #1a1a2e; color: white; padding: 20px; }
        h1 { color: #ff9900; }
        button { background: #00a8ff; color: white; padding: 10px; border: none; margin: 5px; }
    </style>
</head>
<body>
    <h1>PUBG UC MARKET</h1>
    <p>Eng arzon narxlarda UC sotib oling</p>
    
    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px;">
        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;">
            <h3>60 UC</h3>
            <p>TEKIN</p>
            <button onclick="alert('60 UC tanlandi!')">Olish</button>
        </div>
        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;">
            <h3>120 UC</h3>
            <p>39,000 UZS</p>
            <button onclick="alert('120 UC tanlandi!')">Sotib olish</button>
        </div>
        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;">
            <h3>355 UC</h3>
            <p>89,000 UZS</p>
            <button onclick="alert('355 UC tanlandi!')">Sotib olish</button>
        </div>
        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;">
            <h3>720 UC</h3>
            <p>169,000 UZS</p>
            <button onclick="alert('720 UC tanlandi!')">Sotib olish</button>
        </div>
        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;">
            <h3>1,500 UC</h3>
            <p>319,000 UZS</p>
            <button onclick="alert('1500 UC tanlandi!')">Sotib olish</button>
        </div>
        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;">
            <h3>3,000 UC</h3>
            <p>599,000 UZS</p>
            <button onclick="alert('3000 UC tanlandi!')">Sotib olish</button>
        </div>
    </div>
    
    <form method="POST" style="margin-top: 20px;">
        <input type="email" name="email" placeholder="Email" required style="width: 100%; padding: 10px; margin: 10px 0;">
        <button type="submit" style="width: 100%;">Buyurtma berish</button>
    </form>
</body>
</html>
"""

# ==================== FLASK ROUTES ====================
@app.route("/")
def home():
    return "✅ Bot ishlayapti! /form/<user_id> yo'li orqali o'ting."

@app.route("/form/<user_id>", methods=["GET", "POST"])
def form(user_id):
    print(f"Form so'rovi: user_id = {user_id}")  # Log uchun
    
    if request.method == "POST":
        email = request.form.get("email")
        print(f"POST qabul qilindi: email = {email}")
        
        # Foydalanuvchi xabari
        user_message = f"✅ Buyurtmangiz qabul qilindi!\nEmail: {email}"
        
        # Admin xabari
        admin_message = f"🛒 YANGI BUYURTMA!\nUser ID: {user_id}\nEmail: {email}"
        
        try:
            # Xabarlarni yuborish
            bot.send_message(user_id, user_message)
            bot.send_message(6948346741, admin_message)
            print("Xabarlar yuborildi")
        except Exception as e:
            print(f"Xatolik: {e}")
        
        return "✅ Buyurtmangiz qabul qilindi! Telegramda xabaringizni tekshiring."

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
    print("🌐 Flask server ishga tushmoqda...")
    app.run(host="0.0.0.0", port=8080, debug=False)  # PORT 8080

def run_bot():
    print("🤖 Bot ishga tushmoqda...")
    try:
        bot.polling(none_stop=True, interval=0, timeout=30)
    except Exception as e:
        print(f"Bot xatosi: {e}")
        time.sleep(5)
        run_bot()  # Qayta urinish

if __name__ == "__main__":
    print("🚀 Dastur ishga tushmoqda...")
    print(f"🌐 RENDER_URL: {RENDER_URL}")
    print(f"🤖 TOKEN: {BOT_TOKEN[:10]}...")
    
    # Flask ni alohida threadda ishga tushirish
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Kutib, keyin botni ishga tushirish
    time.sleep(3)
    run_bot()
