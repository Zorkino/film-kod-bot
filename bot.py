import telebot
from tinydb import TinyDB, Query

BOT_TOKEN = "8014434799:AAEbIAf7MXfJAFmEmnDH39Nt2fATkypfP_g"
bot = telebot.TeleBot(BOT_TOKEN)
db = TinyDB("database.json")
table = db.table("films")
Admin = 836505188  # Sizning Telegram ID'ingiz

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🎬 Kodni yuboring, sizga kino chiqadi.")

@bot.message_handler(content_types=['video', 'document'])
def save_file(message):
    if message.from_user.id != Admin:
        return
    file_id = message.video.file_id if message.content_type == "video" else message.document.file_id
    bot.reply_to(message, f"✅ Fayl saqlandi.\nKod biriktirish uchun:\n/add kod {file_id}")

@bot.message_handler(commands=['add'])
def add_code(message):
    if message.from_user.id != Admin:
        return bot.reply_to(message, "❌ Sizda ruxsat yo‘q.")
    try:
        _, kod, file_id = message.text.split(" ", 2)
        table.insert({'code': kod, 'file_id': file_id})
        bot.reply_to(message, f"✅ Kod '{kod}' fayl bilan biriktirildi.")
    except:
        bot.reply_to(message, "❗ Foydalanish: /add kod file_id")

@bot.message_handler(commands=['del'])
def delete_code(message):
    if message.from_user.id != Admin:
        return bot.reply_to(message, "❌ Sizda ruxsat yo‘q.")
    try:
        kod = message.text.split(" ", 1)[1]
        table.remove(Query().code == kod)
        bot.reply_to(message, f"🗑️ Kod '{kod}' o‘chirildi.")
    except:
        bot.reply_to(message, "❗ Foydalanish: /del kod")

@bot.message_handler(func=lambda message: True)
def check_code(message):
    result = table.search(Query().code == message.text.strip())
    if result:
        bot.send_video(message.chat.id, result[0]['file_id'], caption="🎥 Mana kodingizga mos film.")
    else:
        bot.reply_to(message, "❌ Kod topilmadi.")

bot.polling()
