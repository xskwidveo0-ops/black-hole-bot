import telebot
import os
from threading import Thread

# جلب التوكن من إعدادات الرندر لضمان عدم التصادم
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN, threaded=True, num_threads=100)

@bot.message_handler(func=lambda m: m.text == 'حظر' and m.reply_to_message)
def black_hole(message):
    cid = message.chat.id
    uid = message.reply_to_message.from_user.id
    # تنفيذ الحظر فوراً في خيط معالجة مستقل للسرعة
    Thread(target=bot.ban_chat_member, args=(cid, uid)).start()

bot.infinity_polling(interval=0, timeout=10)
