import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from flask import Flask, request, render_template_string
import os
import time

# ==================== TOKEN VA URL ====================
BOT_TOKEN = "8194877107:AAFYZR8HbBD5B43WN3d871srclsOa7H6xwk"
RENDER_URL = "https://telegram-bot-sdhp.onrender.com"  # ⬅️ YANGI URL!

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# ==================== HTML (SIZNING TO'LIQ HTML) ====================
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
                <button class="package-btn" onclick="alert('60 UC - BEPUL!')">Olish</button>
            </div>
            
            <div class="package-card paid">
                <div class="package-icon">
                    <i class="fas fa-star"></i>
                </div>
                <div class="package-uc">120 UC</div>
                <div class="package-price">39,000 UZS</div>
                <button class="package-btn" onclick="alert('120 UC - 39,000 UZS')">Sotib olish</button>
            </div>
            
            <div class="package-card paid">
                <div class="package-icon">
                    <i class="fas fa-crown"></i>
                </div>
                <div class="package-uc">355 UC</div>
                <div class="package-price">89,000 UZS</div>
                <button class="package-btn" onclick="alert('355 UC - 89,000 UZS')">Sotib olish</button>
            </div>

            <div class="package-card paid">
                <div class="popular-badge">POPULAR</div>
                <div class="package-icon">
                    <i class="fas fa-rocket"></i>
                </div>
                <div class="package-uc">720 UC</div>
                <div class="package-price">169,000 UZS</div>
                <button class="package-btn" onclick="alert('720 UC - 169,000 UZS')">Sotib olish</button>
            </div>

            <div class="package-card paid">
                <div class="package-icon">
                    <i class="fas fa-gem"></i>
                </div>
                <div class="package-uc">1,500 UC</div>
                <div class="package-price">319,000 UZS</div>
                <button class="package-btn" onclick="alert('1500 UC - 319,000 UZS')">Sotib olish</button>
            </div>

            <div class="package-card paid">
                <div class="package-icon">
                    <i class="fas fa-trophy"></i>
                </div>
                <div class="package-uc">3,000 UC</div>
                <div class="package-price">599,000 UZS</div>
                <button class="package-btn" onclick="alert('3000 UC - 599,000 UZS')">Sotib olish</button>
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
    return "✅ Bot ishlayapti! URL: /form/123"

@app.route("/form/<user_id>", methods=["GET"])
def form(user_id):
    return render_template_string(html_form)

# ==================== WEBHOOK (POLLING EMAS!) ====================
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/setwebhook")
def set_webhook():
    webhook_url = f"{RENDER_URL}/{BOT_TOKEN}"
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(url=webhook_url)
    return f"Webhook set to: {webhook_url}"

# ==================== TELEGRAM BOT HANDLERS ====================
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

# ==================== MAIN ====================
if __name__ == "__main__":
    print("🚀 Bot WEBHOOK bilan ishga tushmoqda...")
    print(f"🌐 URL: {RENDER_URL}")
    print(f"🤖 Webhook: {RENDER_URL}/{BOT_TOKEN}")
    
    # Webhook ni sozlash
    webhook_url = f"{RENDER_URL}/{BOT_TOKEN}"
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(url=webhook_url)
    
    print("✅ Webhook sozlandi!")
    print("✅ Bot faqat WEBHOOK orqali ishlaydi (polling emas!)")
    
    # Flask ni ishga tushirish
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
