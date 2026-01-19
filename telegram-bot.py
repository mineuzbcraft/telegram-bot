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

# ==================== HTML (TO'LIQ, LEKIN PORT MUAMMOSIZ) ====================
html_form = """
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PUBG UC Sotib Olish</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        :root {
            --primary: #ff9900;
            --secondary: #1a1a2e;
            --accent: #00a8ff;
            --light: #f8f9fa;
            --dark: #16213e;
            --success: #2ecc71;
            --free: #2ecc71;
        }
        
        body {
            background: linear-gradient(135deg, var(--secondary), var(--dark));
            color: var(--light);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 600px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }
        
        .logo {
            font-size: 2.5rem;
            color: var(--primary);
            margin-bottom: 10px;
        }
        
        .header h1 {
            font-size: 1.8rem;
            background: linear-gradient(to right, var(--primary), var(--accent));
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }
        
        .header p {
            color: #ccc;
            margin-top: 10px;
        }

        .packages-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }
        
        .package-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 10px;
            padding: 20px 15px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: transform 0.3s ease;
        }

        .package-card:hover {
            transform: translateY(-5px);
        }
        
        .package-card.free {
            border-color: var(--free);
        }
        
        .package-icon {
            font-size: 2rem;
            margin-bottom: 10px;
        }
        
        .package-card.free .package-icon {
            color: var(--free);
        }
        
        .package-card.paid .package-icon {
            color: var(--primary);
        }
        
        .package-uc {
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 8px;
        }
        
        .package-card.free .package-uc {
            color: var(--free);
        }
        
        .package-card.paid .package-uc {
            color: var(--primary);
        }
        
        .package-price {
            font-size: 1rem;
            margin-bottom: 12px;
            color: var(--accent);
        }
        
        .package-card.free .package-price {
            color: var(--free);
        }
        
        .package-btn {
            width: 100%;
            padding: 10px;
            border: none;
            border-radius: 6px;
            color: white;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .package-card.free .package-btn {
            background: var(--free);
        }
        
        .package-card.paid .package-btn {
            background: linear-gradient(to right, var(--primary), var(--accent));
        }

        .package-btn:hover {
            transform: scale(1.05);
        }
        
        .free-badge {
            background: var(--free);
            color: white;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.7rem;
            margin-bottom: 8px;
            display: inline-block;
        }

        .popular-badge {
            background: var(--primary);
            color: white;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.7rem;
            margin-bottom: 8px;
            display: inline-block;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">
                <i class="fas fa-fire"></i>
            </div>
            <h1>PUBG UC MARKET</h1>
            <p>Eng arzon narxlarda UC sotib oling</p>
        </div>

        <div class="packages-grid">
            <div class="package-card free">
                <div class="free-badge">BEPUL</div>
                <div class="package-icon">
                    <i class="fas fa-gift"></i>
                </div>
                <div class="package-uc">60 UC</div>
                <div class="package-price">TEKIN</div>
                <button class="package-btn" onclick="alert('Bepul UC: Hisobingizga 60 UC yuklandi!')">Olish</button>
            </div>
            
            <div class="package-card paid">
                <div class="package-icon">
                    <i class="fas fa-star"></i>
                </div>
                <div class="package-uc">120 UC</div>
                <div class="package-price">39,000 UZS</div>
                <button class="package-btn" onclick="alert('120 UC tanlandi! To\'lov qilish uchun admin bilan bog\'laning.')">Sotib olish</button>
            </div>
            
            <div class="package-card paid">
                <div class="package-icon">
                    <i class="fas fa-crown"></i>
                </div>
                <div class="package-uc">355 UC</div>
                <div class="package-price">89,000 UZS</div>
                <button class="package-btn" onclick="alert('355 UC tanlandi! To\'lov qilish uchun admin bilan bog\'laning.')">Sotib olish</button>
            </div>

            <div class="package-card paid">
                <div class="popular-badge">POPULAR</div>
                <div class="package-icon">
                    <i class="fas fa-rocket"></i>
                </div>
                <div class="package-uc">720 UC</div>
                <div class="package-price">169,000 UZS</div>
                <button class="package-btn" onclick="alert('720 UC tanlandi! To\'lov qilish uchun admin bilan bog\'laning.')">Sotib olish</button>
            </div>

            <div class="package-card paid">
                <div class="package-icon">
                    <i class="fas fa-gem"></i>
                </div>
                <div class="package-uc">1,500 UC</div>
                <div class="package-price">319,000 UZS</div>
                <button class="package-btn" onclick="alert('1500 UC tanlandi! To\'lov qilish uchun admin bilan bog\'laning.')">Sotib olish</button>
            </div>

            <div class="package-card paid">
                <div class="package-icon">
                    <i class="fas fa-trophy"></i>
                </div>
                <div class="package-uc">3,000 UC</div>
                <div class="package-price">599,000 UZS</div>
                <button class="package-btn" onclick="alert('3000 UC tanlandi! To\'lov qilish uchun admin bilan bog\'laning.')">Sotib olish</button>
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 30px; color: #ccc;">
            <p>Buyurtma berish uchun: @msrfteam</p>
        </div>
    </div>
</body>
</html>
"""

# ==================== FLASK ROUTES ====================
@app.route("/")
def home():
    return "✅ Bot ishlayapti!"

@app.route("/form/<user_id>", methods=["GET", "POST"])
def form(user_id):
    if request.method == "POST":
        email = request.form.get("email")
        
        # Foydalanuvchi xabari
        user_message = f"✅ Buyurtmangiz qabul qilindi!\n\n"
        user_message += f"📧 Email: {email}\n"
        user_message += f"⏳ Yetkazish: 5-15 daqiqa\n\n"
        user_message += f"📞 Support: @msrfteam"
        
        # Admin xabari
        admin_message = f"🛒 YANGI BUYURTMA!\n\n"
        admin_message += f"👤 User ID: {user_id}\n"
        admin_message += f"📧 Email: {email}\n"
        
        # 1. FOYDALANUVCHIGA yuborish
        bot.send_message(user_id, user_message)
        
        # 2. ADMINGA yuborish
        ADMIN_ID = 6948346741
        bot.send_message(ADMIN_ID, admin_message)
        
        return "✅ Buyurtmangiz qabul qilindi! Telegramda xabaringizni tekshiring."

    return render_template_string(html_form)

# ==================== TELEGRAM BOT ====================
@bot.message_handler(commands=["start"])
def start(msg):
    bot.send_message(msg.chat.id, "Salom! bir kunlik aksiya PUBG UC olish uchun /link buyrug'ini yuboring.")

@bot.message_handler(commands=["link"])
def link(msg):
    user_id = msg.chat.id
    uniq = f"{RENDER_URL}/form/{user_id}"
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔗 UC Sotib Olish", url=uniq))
    
    bot.send_message(
        user_id,
        f"🔗 Sizning shaxsiy linkingiz:\n\n{uniq}\n\n"
        f"Ushbu link orqali PUBG UC paketlarini ko'rishingiz mumkin!",
        reply_markup=markup
    )

# ==================== RUN FUNCTIONS ====================
def run_flask():
    app.run(host="0.0.0.0", port=10000)  # PORT 10000 - Render uchun yaxshi

def run_bot():
    print("🤖 Bot ishga tushmoqda...")
    bot.polling(none_stop=True, interval=0, timeout=60)

if __name__ == "__main__":
    print("🚀 Dastur ishga tushmoqda...")
    
    # Flask ni alohida threadda ishga tushirish
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Botni ishga tushirish
    time.sleep(2)  # Flask ishga tushishi uchun kutish
    run_bot()
