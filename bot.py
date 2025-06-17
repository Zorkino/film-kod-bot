import telebot
from tinydb import TinyDB, Query

BOT_TOKEN = "8014434799:AAEbIAf7MXfJAFmEmnDH39Nt2fATkypfP_g"
bot = telebot.TeleBot(BOT_TOKEN)
db = TinyDB("database.json")
films = db.table("films")
Admin = 836505188  # O'Z TELEGRAM ID'ingiz (sizning)

# /start komandasi
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🎬 Kodni yuboring, sizga kino chiqadi.")

# Kino faylini yuklash
@bot.message_handler(content_types=['video', 'document'])
def save_film_file(message):
    if message.from_user.id != Admin:
        return bot.reply_to(message, "❌ Siz admin emassiz.")
    
    # Fayl ID sini aniqlash
    file_id = None
    if message.content_type == 'video':
        file_id = message.video.file_id
    elif message.content_type == 'document':
        file_id = message.document.file_id
    
    if file_id:
        bot.reply_to(message, f"✅ Fayl saqlandi.\nKod bog‘lash uchun buyrug‘ni yuboring:\n`/add kod {file_id}`", parse_mode='Markdown')
    else:
        bot.reply_to(message, "❗ Fayl ID aniqlanmadi.")

# Kod biriktirish
@bot.message_handler(commands=['add'])
def add_code(message):
    if message.from_user.id != Admin:
        return bot.reply_to(message, "❌ Siz admin emassiz.")
    try:
        _, code, file_id = message.text.split(" ", 2)
        films.insert({'code': code.strip(), 'file_id': file_id.strip()})
        bot.reply_to(message, f"✅ Kod `{code}` muvaffaqiyatli bog‘landi.", parse_mode='Markdown')
    except:
        bot.reply_to(message, "❗ Foydalanish: /add kod file_id")

# Kodni o‘chirish
@bot.message_handler(commands=['del'])
def delete_code(message):
    if message.from_user.id != Admin:
        return bot.reply_to(message, "❌ Siz admin emassiz.")
    try:
        code = message.text.split(" ", 1)[1].strip()
        films.remove(Query().code == code)
        bot.reply_to(message, f"🗑️ Kod `{code}` o‘chirildi.", parse_mode='Markdown')
    except:
        bot.reply_to(message, "❗ Foydalanish: /del kod")

# Oddiy kod yuborilganda tekshirish
@bot.message_handler(func=lambda message: True)
def check_code(message):
    code = message.text.strip()
    result = films.search(Query().code == code)
    if result:
        bot.send_video(message.chat.id, result[0]['file_id'], caption="🎥 Mana kodingizga mos kino:")
    else:
        bot.reply_to(message, "❌ Bunday kod topilmadi.")
        
# Botni ishga tushirish
bot.polling(non_stop=True)
