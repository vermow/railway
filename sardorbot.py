import logging
import os
import asyncio
import re
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, 
                           InlineKeyboardButton, CallbackQuery)
from aiogram.filters import Command, state
import mysql.connector
from aiogram.fsm.context import FSMContext
import uuid
from dotenv import load_dotenv
from aiogram.utils.keyboard import InlineKeyboardBuilder


# .env faylni yuklash
load_dotenv()

# MySQL sozlamalari
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
# Bot sozlamalari
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
print("Admin ID:", ADMIN_ID)
CHANNELS = ["@infoCryptouz"]

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot)
users = {}

COIN_XP_VALUES = {"$PAWS":30 ,"NOTCOIN": 50, "MEMEFI": 20, "TONCOIN": 10, "USDT": 10 , "$ZOO": 10, "$TAPS":10, "$PX":10, "$SOON":10, "MAJOR":10, "MEMEFI":10, "X EMPIRE":10, "$HAMSTER":10, "$DOGS":10, "$CATIZEN":10, "NOTCOIN":10, "TONCOIN":10, "💸USDT":10}
WALLET_ADDRESS = "UQB1NTMNh25eWKpSvhGq2LStBQ-PyiyJFMNr_nP5a2F8h32R"
ACCEPTED_COINS = ["$PAWS","$ZOO", "$TAPS", "$PX", "$SOON", "MAJOR", "MEMEFI", "X EMPIRE", "$HAMSTER", "$DOGS", "$CATIZEN", "NOTCOIN", "TONCOIN", "💸USDT"]

# Bonus code lar
BONUS_CODES = {
    "CODE1": 1.0,
    "CODE2": 1.0,
    "CODE3": 1.0,
    "CODE4": 1.0,
    "CODE5": 1.0,
    "CODE6": 1.0,
    "CODE7": 1.0,
    "CODE8": 1.0,
    "CODE9": 1.0,
    "CODE10": 1.0,
}

# MySQL ulanish funksiyasi
def get_db_connection():
    return mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)

# Kanal obunasini tekshirish
async def check_subscription(user_id):
    for channel in CHANNELS:
        try:
            user = await bot.get_chat_member(channel, user_id)
            if user.status in ["member", "administrator", "creator"]:
                return True
        except Exception as e:
            logging.warning(f"Obuna tekshirishda xatolik: {e}")
            return False
    return False

# Asosiy menyu
def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💰 Crypto Coin tanga sotish"), KeyboardButton(text="💰Referal tizimi")],
            [KeyboardButton(text="TG Premium olish"), KeyboardButton(text="TG Stars olish")],
            [KeyboardButton(text="Coin sotgan foydalanuvchilar statistikasi"), KeyboardButton(text="Walletim")],
            [KeyboardButton(text="Admin Panel"), KeyboardButton(text="Bonus code")]
        ],
        resize_keyboard=True
    )


# def import_backup_sql():
#     conn = None
#     cursor = None
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()

#         backup_file_path = "/app/backup.sql"
#         if not os.path.exists(backup_file_path):
#             print("backup.sql fayli topilmadi!")
#             return

#         with open(backup_file_path, 'r', encoding='utf-8') as file:
#             sql_script = file.read()

#         sql_commands = sql_script.split(';')

#         for command in sql_commands:
#             command = command.strip()
#             if command:
#                 cursor.execute(command)

#         conn.commit()
#         print("✅ backup.sql fayli muvaffaqiyatli import qilindi!")

#     except Exception as e:
#         print(f"❌ backup.sql import qilishda xatolik: {e}")

#     finally:
#         if cursor is not None:
#             cursor.close()
#         if conn is not None:
#             conn.close()


# Ortga qaytish tugmasi
def back_to_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="⬅️ Ortga qaytish")]],
        resize_keyboard=True
    )

@dp.message(lambda message: message.text == "⬅️ Ortga qaytish")
async def back_to_menu(message: types.Message):
    await message.answer("Asosiy menyu:", reply_markup=main_menu())

# Referal statistikasini saqlash uchun jadval yaratish
def create_referal_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS referals (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id BIGINT NOT NULL,
            referal_id BIGINT NOT NULL,
            xp INT DEFAULT 0,
            ton DECIMAL(10, 8) DEFAULT 0,
            UNIQUE(user_id, referal_id)
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# Referal statistikasini olish
def get_referal_stats(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(referal_id) as referal_count, SUM(xp) as total_xp, SUM(ton) as total_ton FROM referals WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result or (0, 0, 0)

# Referal tizimi tugmasini bosganda
@dp.message(lambda message: message.text == "💰Referal tizimi")
async def referal_system(message: types.Message):
    user_id = message.from_user.id
    bot_info = await bot.get_me()
    referal_link = f"https://t.me/{bot_info.username}?start={user_id}"
    referal_count, total_xp, total_ton = get_referal_stats(user_id)

    text = (
        f"📎 Sizning referal havolangiz:\n"
        f"{referal_link}\n\n"
        f"👥 Siz chaqirgan do'stlaringiz soni: {referal_count}\n"
        f"🏆 Sizning jami XP: {total_xp}\n"
        f"💰 Sizning jami TON: {total_ton if total_ton is not None else 0:.3f}\n\n"
        f"Har bir do'stingiz uchun 10 XP va 0.008 TON olasiz!"
    )
    await message.answer(text, reply_markup=back_to_main_menu())

# Start bosganda referal linkni tekshirish
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.full_name

    if not await check_subscription(user_id):
        await message.answer("Iltimos, kanalga obuna bo'ling!")
        return

    referal_id = None
    if len(message.text.split()) > 1:
        try:
            referal_id = int(message.text.split()[1])
        except ValueError:
            pass

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Foydalanuvchini bazaga qo'shish (agar bo‘lmasa)
        cursor.execute(
            "INSERT INTO users (user_id, username) VALUES (%s, %s) "
            "ON DUPLICATE KEY UPDATE username = VALUES(username)",
            (user_id, username)
        )

        if referal_id and referal_id != user_id:
            # Foydalanuvchi ilgari referal sifatida qo‘shilganmi, tekshiramiz
            cursor.execute(
                "SELECT COUNT(*) FROM referals WHERE referal_id = %s", (user_id,)
            )
            already_referred = cursor.fetchone()[0] > 0  # Agar mavjud bo‘lsa, True qaytadi

            if not already_referred:
                # Referalni ro‘yxatga olish va XP/TON berish
                cursor.execute(
                    "INSERT INTO referals (user_id, referal_id, xp, ton) "
                    "VALUES (%s, %s, %s, %s)",
                    (referal_id, user_id, 10, 0.008)
                )
                
                cursor.execute(
                    "UPDATE users SET xp = xp + 10, ton = ton + 0.008 "
                    "WHERE user_id = %s", (referal_id,)
                )

                await bot.send_message(
                    referal_id,
                    f"🎉 Yangi referal qo'shildi!\n"
                    f"Sizning chaqirgan do'stingiz: {username}\n"
                    f"10 XP va 0.008 TON qo'shildi."
                )

        conn.commit()
        await message.answer("Xush kelibsiz! Tanlang:", reply_markup=main_menu())

    except Exception as e:
        logging.error(f"Database error: {e}")
        await message.answer("Xatolik yuz berdi! Iltimos qayta urinib ko'ring.")
    finally:
        cursor.close()
        conn.close()

# TG Premium olish
@dp.message(lambda message: message.text == "TG Premium olish")
async def tg_premium(message: types.Message):
    text = (
        "TG Premium olib berish narxlari:\n"
        "⭐️1oylik - 49.900(kirib)\n"
        "⭐️3oylik- 189.000🎁\n"
        "⭐️6oylik- 249.000🎁\n"
        "⭐️12oylik - 309.000(kirib)\n\n"
        "Olish uchun adminga yozing: @sardortete"
    )
    await message.answer(text, reply_markup=back_to_main_menu())

# TG Stars olish
@dp.message(lambda message: message.text == "TG Stars olish")
async def tg_stars(message: types.Message):
    text = (
        "TG Stars olib berish narxlari:\n"
        "⭐100 - 29.000 uzs ⭐️\n"
        "⭐250 - 69.000 uzs ⭐️\n"
        "⭐500 - 129.000 uzs ⭐️\n"
        "⭐1000 - 249.000 uzs ⭐️\n"
        "⭐2000 - 449.000 uzs ⭐️\n\n"
        "Ko'proq olganlarga bonuslar bor!!!\n"
        "Hammasi halol ishonchli!!!\n"
        "Olish uchun adminga murojaat qiling: @sardortete"
    )
    await message.answer(text, reply_markup=back_to_main_menu())

# Coin sotgan foydalanuvchilar statistikasi
@dp.message(lambda message: message.text == "Coin sotgan foydalanuvchilar statistikasi")
async def coin_statistics(message: types.Message):
    user_id = message.from_user.id
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) as total_coins, SUM(xp) as total_xp FROM transactions WHERE telegram_id = %s", (user_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    total_coins = result[0] if result[0] else 0
    total_xp = result[1] if result[1] else 0

    referal_count, referal_xp, total_ton = get_referal_stats(user_id)

    text = (
        "Sizning statistkangiz:\n"
        "Coin sotish bo'limidan statistkangiz:\n"
        f"Coin miqdori: {total_coins} \n"
        f"Olgan XP: {total_xp} XP\n\n"
        "Referal tizimidagi statistka:\n"
        f"TON: {total_ton if total_ton is not None else 0:.3f}\n"
        f"XP: {referal_xp or 0} XP\n\n"
        f"JAMI XP: {total_xp + (referal_xp or 0)} XP\n\n"
        "Eng ko'p XP to'plagan foydalanuvchilar ro'yxati:\n"
        "1. username - XP; 2. username - XP; 3. username - XP\n\n"
        "Har hafta yutuqli uyinga qatnashing!!!\n"
        "Ko'p XP to'plang TOP-3 ga kirgan foydalanuvchilarga har hafta Yutuq TON beriladi!!!"
    )
    await message.answer(text, reply_markup=back_to_main_menu())

# Bonus code
@dp.message(lambda message: message.text == "Bonus code")
async def bonus_code(message: types.Message):
    await message.answer("Bonus code kiriting:", reply_markup=back_to_main_menu())

@dp.message(lambda message: message.text in BONUS_CODES)
async def handle_bonus_code(message: types.Message):
    user_id = message.from_user.id
    code = message.text

    conn = get_db_connection()
    cursor = conn.cursor()

    # Code ni tekshirish
    cursor.execute("SELECT * FROM users WHERE user_id = %s AND bonus_codes LIKE %s", (user_id, f"%{code}%"))
    if cursor.fetchone():
        await message.answer("⚠️ Bu code allaqachon ishlatilgan!", reply_markup=back_to_main_menu())
    else:
        # Bonusni qo'shish
        bonus_amount = BONUS_CODES[code]
        cursor.execute("UPDATE users SET bonus_token = bonus_token + %s WHERE user_id = %s", (bonus_amount, user_id))
        cursor.execute("UPDATE users SET bonus_codes = CONCAT(bonus_codes, %s) WHERE user_id = %s", (f"{code},", user_id))
        conn.commit()

        await message.answer(f"🎉 Tabriklaymiz! Sizga {bonus_amount} TON bonus berildi!", reply_markup=back_to_main_menu())

    cursor.close()
    conn.close()



@dp.message(lambda message: message.text == "💰 Crypto Coin tanga sotish")
async def crypto_coin_selling(message: types.Message):
    text = "Bu yerda Airdrop coinlaringizni qulay va ishonchli tarzda sota olasiz."
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=coin)] for coin in COIN_XP_VALUES.keys()] + [[KeyboardButton(text="⬅️ Ortga qaytish")]],
        resize_keyboard=True
    )
    await message.answer(text, reply_markup=keyboard)

@dp.message(lambda message: message.text in COIN_XP_VALUES.keys())
async def coin_info(message: types.Message):
    user_id = message.from_user.id
    coin = message.text
    sdelka_id = str(uuid.uuid4())[:8]  # 8 ta belgidan iborat unique ID

    # Foydalanuvchi ma'lumotlarini saqlash
    if user_id not in users:
        users[user_id] = {}  # Foydalanuvchi lug'atga qo'shiladi

    users[user_id].update({"coin": coin, "sdelka_id": sdelka_id, "status": "open"})  # Sdelka holatini saqlaymiz

    await message.answer(f"Nechta {coin} sotmoqchisiz? Miqdorni yozing.", reply_markup=back_to_main_menu())
    
@dp.message(lambda message: message.text and message.text.isdigit() and message.from_user.id in users and users[message.from_user.id].get("status") == "open")
async def ask_for_receipt(message: types.Message):
    user_id = message.from_user.id
    amount = int(message.text)
    transaction_id = str(uuid.uuid4())[:8]  # 8 ta belgidan iborat random ID
    users[user_id]["amount"] = amount
    users[user_id]["status"] = "waiting_receipt"
    users[user_id]["transaction_id"] = transaction_id  # ID ni saqlaymiz

    coin = users[user_id]["coin"]
    xp = amount * COIN_XP_VALUES.get(coin, 0)

    await message.answer(
        f"✅ {amount} {coin} sotmoqchisiz.\n"
        f"🏆 Sizga {xp} XP beriladi.\n"
        f"📌 Tranzaksiya ID: #{transaction_id}\n\n"
        f"📌 Endi {WALLET_ADDRESS} hamyonga {coin} yuboring va chekni tashlang!"
    )
    await message.answer("Chekni tashlang:", reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="⬅️ Ortga qaytish")]], resize_keyboard=True))

# @dp.message(lambda message: message.text == "📨 Chekni yuborish")
# async def request_receipt(message: types.Message):
#     user_id = message.from_user.id
#     if user_id in users and users[user_id]["status"] == "waiting_receipt":
#         await message.answer("Iltimos, chekni rasm yoki skrinshot shaklida yuboring.", reply_markup=back_to_main_menu())
#         users[user_id]["status"] = "receipt_sent"  # Holatni yangilash
#     else:
#         await message.answer("Iltimos, avval miqdorni kiriting.", reply_markup=back_to_main_menu())

@dp.callback_query(lambda call: call.data.startswith("confirm_"))
async def confirm_transaction(call: CallbackQuery):
    user_id = int(call.data.split("_")[1])

    if user_id in users and users[user_id]["status"] == "receipt_sent":  # Holatni to'g'ri tekshirish
        await bot.send_message(user_id, "✅ Chek tasdiqlandi! Endi kartangizni yuboring.", reply_markup=back_to_main_menu())
        users[user_id]["status"] = "waiting_card"  # Holatni yangilash
        await call.message.answer("✅ Tasdiqlandi. Endi foydalanuvchi kartasini yuborishini kuting.")
    else:
        await call.answer("⚠️ Xatolik: Foydalanuvchi topilmadi yoki sdelka yopilgan.", show_alert=True)

@dp.message(lambda message: message.text and message.from_user.id in users and users[message.from_user.id].get("status") == "waiting_card")
async def receive_card(message: types.Message):
    user_id = message.from_user.id
    users[user_id]["card"] = message.text

    # Admin uchun karta ma'lumoti
    text = (
        f"💳 *Yangi karta ma'lumoti!* \n"
        f"👤 *Foydalanuvchi:* {message.from_user.full_name} \n"
        f"🆔 *ID:* {user_id} \n"
        f"💰 *Coin:* {users[user_id]['coin']} \n"
        f"🔢 *Miqdor:* {users[user_id]['amount']} \n"
        f"🏆 *XP:* {users[user_id]['amount'] * COIN_XP_VALUES[users[user_id]['coin']]} \n\n"
        f"💳 *Karta raqami:* {message.text} \n\n"
        f"✅ Pulni tashlaganingizdan so‘ng tasdiqlash tugmasini bosing!"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="✅ Pul tashlandi", callback_data=f"paid_{user_id}")]]
    )

    await bot.send_message(ADMIN_ID, text, reply_markup=keyboard, parse_mode="Markdown")
    await message.answer("✅ Kartangiz adminga yuborildi. Pul tushishini kuting!", reply_markup=back_to_main_menu())

@dp.callback_query(lambda call: call.data.startswith("paid_"))
async def payment_done(call: CallbackQuery):
    user_id = int(call.data.split("_")[1])

    if user_id in users and users[user_id]["status"] == "waiting_card":  # Holatni to'g'ri tekshirish
        coin = users[user_id]["coin"]
        amount = users[user_id]["amount"]
        xp = amount * COIN_XP_VALUES.get(coin, 0)
        username = users[user_id].get("username", "Noma'lum foydalanuvchi")  # Agar username bo'lmasa, "Noma'lum foydalanuvchi" deb saqlaymiz

        # Ma'lumotni bazaga kiritish
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO transactions (telegram_id, username, coin, amount, xp, confirmed) VALUES (%s, %s, %s, %s, %s, TRUE)",
                       (user_id, username, coin, amount, xp))
        conn.commit()
        cursor.close()
        conn.close()

        await bot.send_message(
            user_id,
            f"✅ Pulingiz tushdi!\n"
            f"Bizning servicemizdan foydalanganingiz uchun rahmat!\n"
            f"Pul kartangizga tushdi.\n"
            f"Muammo bo‘lsa, adminga yozing: @sardortete\n\n"
            f"💰 Coin miqdori: {amount}\n"
            f"🏆 XP berildi: {xp}\n"
            f"📊 Statistikangizdan ko‘rishingiz mumkin!",
            reply_markup=back_to_main_menu()
        )
        await call.message.answer("✅ Pul tashlandi va foydalanuvchi xabardor qilindi!")
        
        # Sdelka yopiladi
        users[user_id]["status"] = "closed"
    else:
        await call.answer("⚠️ Xatolik: Foydalanuvchi topilmadi yoki sdelka yopilgan.", show_alert=True)


@dp.message(lambda message: message.photo or message.document)
async def handle_receipt(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.full_name
    file_id = message.photo[-1].file_id if message.photo else message.document.file_id

    if user_id in users and "amount" in users[user_id] and users[user_id]["status"] == "waiting_receipt":
        coin = users[user_id]["coin"]
        amount = users[user_id]["amount"]
        xp = amount * COIN_XP_VALUES.get(coin, 0)

        users[user_id]["file_id"] = file_id

        # Chekni adminga yuboramiz
        text = (
            f"📩 *Yangi chek!* \n"
            f"👤 *Foydalanuvchi:* {username} \n"
            f"🆔 *ID:* {user_id} \n"
            f"💰 *Coin:* {coin} \n"
            f"🔢 *Miqdor:* {amount} \n"
            f"🏆 *XP:* {xp} \n\n"
            f"✅ Tasdiqlash uchun pastdagi tugmani bosing!"
        )

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"confirm_{user_id}")]]
        )

        if message.photo:
            await bot.send_photo(ADMIN_ID, file_id, caption=text, reply_markup=keyboard, parse_mode="Markdown")
        else:
            await bot.send_document(ADMIN_ID, file_id, caption=text, reply_markup=keyboard, parse_mode="Markdown")

        await message.answer("✅ Chek adminga yuborildi. Tasdiqlashni kuting!", reply_markup=back_to_main_menu())
        users[user_id]["status"] = "receipt_sent"  # Holatni yangilash
    else:
        await message.answer("Iltimos, avval miqdorni kiriting yoki chekni yuboring.", reply_markup=back_to_main_menu())



# Walletim bo'limi
@dp.message(lambda message: message.text == "Walletim")
async def wallet(message: types.Message):
    user_id = message.from_user.id
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ton, bonus_token, wallet_address FROM users WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    ton = result[0] if result[0] else 0
    bonus_token = result[1] if result[1] else 0
    wallet_address = result[2] if result[2] else None

    text = (
        "Walletim:\n"
        f"TON: {ton:.3f}\n"
        f"BONUS token: {bonus_token}\n"
        f"Wallet address: {wallet_address if wallet_address else 'Ulangan manzil yoq'}\n\n"
        "Tanlang:"
    )

    if wallet_address:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Pul chiqarish")],
                [KeyboardButton(text="Adress o'zgartirish")],
                [KeyboardButton(text="⬅️ Ortga qaytish")]
            ],
            resize_keyboard=True
        )
    else:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Adress ulash")],
                [KeyboardButton(text="⬅️ Ortga qaytish")]
            ],
            resize_keyboard=True
        )

    await message.answer(text, reply_markup=keyboard)

@dp.message(lambda message: message.text == "Pul chiqarish")
async def withdraw_funds(message: types.Message):
    await message.answer("Qaysi manbadan pul chiqarmoqchisiz?", reply_markup=ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="REFERAL TIZIMDAN")],
            [KeyboardButton(text="BONUS TOKEN")],
            [KeyboardButton(text="⬅️ Ortga qaytish")]
        ],
        resize_keyboard=True
    ))
def get_user_balance(user_id):
    """Foydalanuvchining TON va BONUS token balansini olish"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ton, bonus_token FROM users WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if result:
        return {"ton": result[0], "bonus_token": result[1]}
    return {"ton": 0, "bonus_token": 0}  # Agar user bo'lmasa 0 qaytarish


@dp.message(lambda message: message.text in ["REFERAL TIZIMDAN", "BONUS TOKEN"])
async def handle_withdraw_source(message: types.Message):
    user_id = message.from_user.id
    source = message.text

    # Balansni bazadan olish
    balance_data = get_user_balance(user_id)

    # Foydalanuvchini users lug‘atiga qo‘shish
    if user_id not in users:
        users[user_id] = {}

    users[user_id].update(balance_data)  # Balans ma’lumotlarini qo‘shish
    users[user_id]["withdraw_source"] = source  # Qaysi manbadan chiqarishni saqlash
    users[user_id]["status"] = "pending"  # Yangi status qo‘shish

    # Foydalanuvchi tanlagan manbaga qarab balansni ko'rsatish
    balance = balance_data["ton"] if source == "REFERAL TIZIMDAN" else balance_data["bonus_token"]

    await message.answer(f"Miqdorni kiriting (mavjud: {balance}):", reply_markup=back_to_main_menu())


from aiogram.fsm.context import FSMContext  # ✅ FSM holati boshqarish uchun

@dp.message(lambda message: message.text and message.from_user.id in users and "withdraw_source" in users[message.from_user.id])
async def handle_withdraw_amount(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    source = users[user_id]["withdraw_source"]

    # Balansni olish
    balance_data = get_user_balance(user_id)
    balance = balance_data["ton"] if source == "REFERAL TIZIMDAN" else balance_data["bonus_token"]

    try:
        amount = float(message.text)
    except ValueError:
        await message.answer("❌ Iltimos, faqat raqam kiriting.", reply_markup=back_to_main_menu())
        return

    if amount <= 0 or amount > balance:
        await message.answer("❌ Xatolik: Siz mavjud bo‘lgan summadan ko‘proq yoki noto‘g‘ri miqdor kiritdingiz.", reply_markup=back_to_main_menu())
        return

    request_id = str(uuid.uuid4())[:8]

    # Userning wallet_addressini olish
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT wallet_address FROM users WHERE user_id = %s", (user_id,))
    wallet_result = cursor.fetchone()
    wallet_address = wallet_result[0] if wallet_result and wallet_result[0] else "NOMA‘LUM"

    # Zayavkani bazaga yozish
    cursor.execute(
        "INSERT INTO withdrawal_requests (request_id, user_id, amount, source, address, status) VALUES (%s, %s, %s, %s, %s, 'pending')",
        (request_id, user_id, amount, source, wallet_address)
    )
    conn.commit()
    cursor.close()
    conn.close()

    await state.clear()
    await message.answer(
        f"✅ Zayavka qabul qilindi. ID - #{request_id}\n12 soat ichida pulingiz tushadi.", 
        reply_markup=back_to_main_menu()
    )


@dp.message(lambda message: message.text == "Adress ulash")
async def connect_address(message: types.Message):
    await message.answer("Iltimos, TON SPACE hamyondi adresini yozing:", reply_markup=back_to_main_menu())

@dp.message(lambda message: message.text and message.text.startswith("UQ"))
async def handle_address(message: types.Message):
    user_id = message.from_user.id
    address = message.text
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET wallet_address = %s WHERE user_id = %s", (address, user_id))
    conn.commit()
    cursor.close()
    conn.close()

    await message.answer("Adress muvaffaqiyatli ulandi!", reply_markup=ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Pul chiqarish")],
            [KeyboardButton(text="Adress o'zgartirish")],
            [KeyboardButton(text="⬅️ Ortga qaytish")]
        ],
        resize_keyboard=True
    ))

# Adminning har qanday yozuviga javob bermaslik
# @dp.message(lambda message: message.from_user.id == ADMIN_ID and message.text != "Admin Panel")
# async def handle_admin_message(message: types.Message):
#     return  # Admin faqat "Admin Panel" ni yozsa, ishlayveradi


# Foydalanuvchi miqdor kiritganda
@dp.message(lambda message: message.text and message.text.split()[0] in ACCEPTED_COINS)
async def create_trade(message: types.Message):
    user_id = message.from_user.id
    text_parts = message.text.split()
    coin = text_parts[0]
    
    if len(text_parts) < 2 or not text_parts[1].isdigit():
        await message.answer("❌ Iltimos, to‘g‘ri formatda yozing: COIN MIQDOR (masalan: TONCOIN 100)")
        return
    
    amount = int(text_parts[1])
    status = "pending"
    transaction_id = str(uuid.uuid4())[:8]

    print(f"💾 Savdo yozilmoqda: ID={transaction_id}, User={user_id}, Coin={coin}, Amount={amount}")

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO trades (id, user_id, coin, amount, xp, status) VALUES (%s, %s, %s, %s, %s, %s)",
            (transaction_id, user_id, coin, amount, amount * 10, status)
        )
        conn.commit()
        print(f"✅ Savdo bazaga yozildi: ID={transaction_id}")
        await message.answer(f"✅ Savdo ochildi! ID: {transaction_id} Miqdor: {amount} {coin}")
    except Exception as e:
        logging.error(f"Savdoni yaratishda xatolik: {e}")
        print(f"❌ Xatolik: {e}")  # Xatolikni chiqarish
        await message.answer("❌ Xatolik yuz berdi.")
    finally:
        cursor.close()
        conn.close()









@dp.message(lambda message: message.text == "Admin Panel")
async def admin_panel(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Aktual Savdo"), KeyboardButton(text="Yopilgan Savdo")],
                [KeyboardButton(text="Pul chiqarish zayavkalari")],
                [KeyboardButton(text="⬅️ Ortga qaytish")]
            ],
            resize_keyboard=True
        )
        await message.answer("Admin paneliga xush kelibsiz!", reply_markup=keyboard)
    else:
        await message.answer("Siz admin emassiz!", reply_markup=main_menu())

@dp.message(lambda message: message.text == "Aktual Savdo")
async def list_active_trades(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ Siz admin emassiz!")
        return
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, user_id, coin, amount, xp FROM trades WHERE status='pending'")
    trades = cursor.fetchall()
    cursor.close()
    conn.close()
    
    if trades:
        for trade in trades:
            trade_id, user_id, coin, amount, xp = trade
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"approve_trade:{trade_id}")]]
            )
            await message.answer(
                f"📌 **Aktual Savdo**\n"
                f"🆔 **ID**: {trade_id}\n"
                f"👤 **Foydalanuvchi**: {user_id}\n"
                f"💰 **Coin**: {coin}\n"
                f"🔢 **Miqdor**: {amount}\n"
                f"🏆 **XP**: {xp}\n"
                f"📍 **Holati**: Tasdiqlanmagan",
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
    else:
        await message.answer("📌 Hozircha **Aktual Savdo** yo‘q.")


@dp.callback_query(lambda call: call.data.startswith("approve_trade:"))
async def approve_trade(call: CallbackQuery):
    trade_id = call.data.split(":")[1]
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE trades SET status='approved' WHERE id=%s", (trade_id,))
    conn.commit()
    cursor.close()
    conn.close()
    await call.message.edit_text(f"✅ Savdo tasdiqlandi! ID: {trade_id}")


@dp.message(lambda message: message.text == "Yopilgan Savdo")
async def closed_trades(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("Siz admin emassiz!")
        return
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, user_id, coin, amount, xp FROM trades WHERE status='approved'")
    trades = cursor.fetchall()
    cursor.close()
    conn.close()
    
    if trades:
        text = "📌 Yopilgan savdolar:\n"
        for trade in trades:
            trade_id, user_id, coin, amount, xp = trade
            text += f"ID: {trade_id}, User: {user_id}, Coin: {coin}, Miqdor: {amount}, XP: {xp}\n"
        await message.answer(text)
    else:
        await message.answer("Yopilgan savdolar mavjud emas.")

# @dp.message(lambda message: message.text == "Umumiy Savdo")
# async def all_transactions(message: types.Message):
#     if message.from_user.id == ADMIN_ID:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute("SELECT transaction_id, user_id, coin, amount, created_at, status FROM transactions")
#         transactions = cursor.fetchall()
#         cursor.close()
#         conn.close()

#         if transactions:
#             text = "Barcha savdolar ro'yxati:\n"
#             for idx, transaction in enumerate(transactions, start=1):
#                 status = "Yopilgan" if transaction[5] == "closed" else "Ochiq"
#                 text += f"{idx}. ID - #{transaction[0]} ({status})\n"
#             await message.answer(text, reply_markup=back_to_main_menu())
#         else:
#             await message.answer("Savdolar mavjud emas.", reply_markup=back_to_main_menu())
#     else:
#         await message.answer("Siz admin emassiz!", reply_markup=main_menu())

@dp.message(lambda message: message.text == "Pul chiqarish zayavkalari")
async def withdrawal_requests(message: types.Message):
    if message.from_user.id == ADMIN_ID:  # ✅ Admin tekshirilsin
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT request_id, user_id, amount, address, status FROM withdrawal_requests WHERE status = 'pending'")
        requests = cursor.fetchall()
        cursor.close()
        conn.close()

        if requests:
            for request in requests:
                request_id, user_id, amount, wallet_address, status = request
                text = (f"💰 *Pul chiqarish so‘rovi:*\n"
                        f"👤 *User ID:* `{user_id}`\n"
                        f"💸 *Miqdor:* `{amount} TON`\n"
                        f"🏦 *Wallet:* `{wallet_address}`\n"
                        f"📌 *Holat:* `Tasdiqlanmagan`\n")
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text=f"✅ Tasdiqlash {amount} TON", callback_data=f"approve_withdrawal:{request_id}")]
                ])
                await message.answer(text, reply_markup=keyboard, parse_mode="MarkdownV2")
        else:
            await message.answer("📭 Hozirda hech qanday pul chiqarish so'rovi mavjud emas.", reply_markup=back_to_main_menu())
    else:
        await message.answer("❌ Siz admin emassiz!", reply_markup=main_menu())  # ✅ Admin tekshiruvi qayta qo‘shildi



@dp.callback_query(lambda call: call.data.startswith("approve_withdrawal:"))
async def approve_withdrawal(call: CallbackQuery):
    if call.from_user.id == ADMIN_ID:
        request_id = call.data.split(":")[1]  # ✅ To‘g‘ri ajratish
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT user_id, amount FROM withdrawal_requests WHERE request_id = %s", (request_id,))          
        result = cursor.fetchone()
        if not result:
            await call.answer("❌ Xatolik: Bunday zayavka topilmadi!", show_alert=True)
            return
        
        user_id, amount = result

        cursor.execute("SELECT status FROM withdrawal_requests WHERE request_id = %s", (request_id,))
        status_result = cursor.fetchone()
        if status_result and status_result[0] == "completed":
            await call.answer("⚠️ Bu zayavka allaqachon tasdiqlangan!", show_alert=True)
            return

        cursor.execute("UPDATE users SET ton = ton - %s WHERE user_id = %s", (amount, user_id))  # ✅ TO‘G‘RI
        cursor.execute("UPDATE withdrawal_requests SET status = 'completed' WHERE request_id = %s", (request_id,))
        conn.commit()
        cursor.close()
        conn.close()

        await call.message.edit_text(f"✅ Pul chiqarish so‘rovi \\#{request_id} tasdiqlandi\\! ✅", parse_mode="MarkdownV2")

        def escape_markdown(text: str) -> str:
            escape_chars = r'_*[\]()~`>#+-=|{}.!'
            return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

        message = "💰 *Pul chiqarish so‘rovingiz tasdiqlandi!* ✅ Hisobingizga tushdi."
        escaped_message = escape_markdown(message)

        await bot.send_message(user_id, escaped_message, parse_mode="MarkdownV2")    
    else:
        await call.answer("❌ Siz admin emassiz!", show_alert=True)
                
async def main():
    # import_backup_sql()  # Yangi qator
    create_referal_table()  
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())