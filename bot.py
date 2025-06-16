import telebot
from tinydb import TinyDB, Query

BOT_TOKEN = "8014434799:AAEbIAf7MXfJAFmEmnDH39Nt2fATkypfP_g"

bot = telebot.TeleBot(BOT_TOKEN)
db = TinyDB("database.json")
Admin = 836505188  # Sizning Telegram ID'ingiz

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🎬 Kodni yuboring, sizga kino chiqadi.")

@bot.message_handler(commands=['add'])
def add_code(message):
    if message.from_user.id != Admin:
        return bot.reply_to(message, "❌ Sizda ruxsat yo‘q.")
    try:
        parts = message.text.split(" ", 2)
        kod, kino = parts[1], parts[2]
        db.insert({'code': kod, 'film': kino})
        bot.reply_to(message, f"✅ Kod '{kod}' saqlandi.")
    except:
        bot.reply_to(message, "❗ Foydalanish: /add kod kino_nomi")

@bot.message_handler(commands=['del'])
def delete_code(message):
    if message.from_user.id != Admin:
        return bot.reply_to(message, "❌ Sizda ruxsat yo‘q.")
    try:
        kod = message.text.split(" ", 1)[1]
        db.remove(Query().code == kod)
        bot.reply_to(message, f"🗑️ Kod '{kod}' o‘chirildi.")
    except:
        bot.reply_to(message, "❗ Foydalanish: /del kod")

@bot.message_handler(func=lambda message: True)
def check_code(message):
    result = db.search(Query().code == message.text.strip())
    if result:
        bot.reply_to(message, f"🎥 Kino: {result[0]['film']}")
    else:
        bot.reply_to(message, "❌ Kod topilmadi.")

bot.polling()
