import os
import asyncio
from hydrogram import Client, filters
from hydrogram.types import Message

# جلب المتغيرات
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# تعريف البوت مع تجاهل الأخطاء البرمجية للمكتبة
class BlackHole(Client):
    def __init__(self):
        super().__init__(
            "black_hole",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=None
        )

    async def start(self):
        await super().start()
        print("⚡️ [Black Hole] البوت استيقظ الآن وهو جاهز للحظر!")

app = BlackHole()

# أمر الفحص
@app.on_message(filters.command("بوت", "") & filters.me)
async def bot_check(client, message: Message):
    try:
        await message.reply_text("⚡️")
    except:
        pass

# أمر الحظر السريع
@app.on_message(filters.command("حظر", "") & filters.me)
async def ban_user(client, message: Message):
    try:
        if message.reply_to_message:
            await client.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
            await message.reply_text("👤 تم طرده إلى الثقب الأسود!")
    except Exception as e:
        print(f"Error during ban: {e}")

async def run_all():
    # تشغيل البوت
    try:
        await app.start()
    except Exception as e:
        print(f"Login Error: {e}")
    
    # تشغيل سيرفر الويب للتمويه ومنع النوم
    port = int(os.environ.get("PORT", 10000))
    os.system(f"python3 -m http.server {port}")

if __name__ == "__main__":
    asyncio.run(run_all())
