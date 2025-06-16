import telebot
from tinydb import TinyDB, Query

# 🔐 TOKEN
BOT_TOKEN = "8014434799:AAEbIAf7MXfJAFmEmnDH39Nt2fATkypfP_g"

bot = telebot.TeleBot(BOT_TOKEN)

# 🗂 DATABASE
db = TinyDB("database.json")
table = db.table("codes")  # 👈 MUHIM O‘ZGARISH

# 👤 ADMIN ID
Admin = 836505188  # O‘zingizning ID'ingiz

# 🔰 START komandasi
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🎬 Kodni yuboring, sizga kino chiqadi.")

# ➕ Kod qo‘shish
@bot.message_handler(commands=['add'])
def add_code(message):
    if message.from_user.id != Admin:
        return bot.reply_to(message, "❌ Sizda ruxsat yo‘q.")
    try:
        parts = message.text.split(" ", 2)
        kod, kino = parts[1], parts[2]
        table.insert({'code': kod, 'film': kino})  # 👈 table ishlatyapmiz
        bot.reply_to(message, f"✅ Kod '{kod}' saqlandi.")
    except:
        bot.reply_to(message, "❗ Foydalanish: /add kod kino_nomi")

# ❌ Kod o‘chirish
@bot.message_handler(commands=['del'])
def delete_code(message):
    if message.from_user.id != Admin:
        return bot.reply_to(message, "❌ Sizda ruxsat yo‘q.")
    try:
        kod = message.text.split(" ", 1)[1]
        table.remove(Query().code == kod)  # 👈 table orqali
        bot.reply_to(message, f"🗑️ Kod '{kod}' o‘chirildi.")
    except:
        bot.reply_to(message, "❗ Foydalanish: /del kod")

# 🔍 Kod tekshirish
@bot.message_handler(func=lambda message: True)
def check_code(message):
    kod = message.text.strip()
    result = table.search(Query().code == kod)  # 👈 table bilan ishlayapti
    if result:
        bot.reply_to(message, f"🎥 Kino: {result[0]['film']}")
    else:
        bot.reply_to(message, "❌ Kod topilmadi.")

# 🚀 Botni ishga tushirish
bot.polling()
