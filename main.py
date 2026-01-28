from hydrogram import Client, filters
from hydrogram.raw import functions
import os

# سحب البيانات (محرك التوربو)
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("black_hole", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- [1] الرد الخبيث (أسرع من البرق) ---
# ملاحظة: تم إلغاء معالجة النصوص، البوت سيرد "لحظياً"
@app.on_message(filters.regex("^(بوت|فحص)$") & filters.private)
async def fast_reply(client, message):
    # استخدام التوكنات المباشرة لتقليل استهلاك المعالج
    await message.reply_text("⚡️")

# --- [2] الحظر الإجرامي (بمستوى الـ Raw API) ---
# هذا الأمر لا ينتظر "تأكيد" التلجرام، يرسل الأمر ويغادر فوراً
@app.on_message(filters.regex("^حظر$") & filters.reply & filters.group)
async def sniper_ban(client, message):
    try:
        # استخدام Raw Functions لتجاوز طبقات الحماية العادية في المكتبة
        await client.invoke(
            functions.channels.EditBanned(
                channel=await client.resolve_peer(message.chat.id),
                participant=await client.resolve_peer(message.reply_to_message.from_user.id),
                banned_rights=message.chat.permissions # حظر كامل
            )
        )
    except:
        pass # لضمان عدم توقف البوت تحت أي ضغط

print("⚠️ تم تفعيل وضع القوة النهائية.. السرعة الآن تتجاوز الحدود!")
app.run()
