import telebot
import os

# سحب التوكن من إعدادات Render
TOKEN = os.getenv('BOT_TOKEN')

# تشغيل 100 خيط معالجة للسرعة القصوى
bot = telebot.TeleBot(TOKEN, threaded=True, num_threads=100)

# 1. أوامر الرد المختصرة جداً (سرعة جنونية)
@bot.message_handler(func=lambda message: message.text in ['بوت', 'هلا', 'فحص'])
def fast_reply(message):
    bot.reply_to(message, "هلا")

# 2. أمر الحظر المختصر
@bot.message_handler(func=lambda message: message.text == 'حظر' and message.reply_to_message)
def ban_user(message):
    try:
        bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        bot.reply_to(message, "تم")
    except:
        pass # تجاهل الخطأ لزيادة السرعة

# تشغيل البوت
if __name__ == "__main__":
    bot.infinity_polling()
