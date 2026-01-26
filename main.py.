import telebot
from threading import Thread

TOKEN = '7779349165:AAEt9SPMABYx9PN2NWRILyge0x8A3A5EgRo'
bot = telebot.TeleBot(TOKEN, threaded=True, num_threads=100)

@bot.message_handler(func=lambda m: m.text == 'حظر' and m.reply_to_message)
def black_hole(message):
    cid = message.chat.id
    uid = message.reply_to_message.from_user.id
    # طرد فوري بدون ردود لضمان سبق الجميع
    Thread(target=bot.ban_chat_member, args=(cid, uid)).start()

bot.infinity_polling(interval=0, timeout=10)
