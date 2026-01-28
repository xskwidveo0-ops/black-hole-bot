import os
import asyncio
from hydrogram import Client, filters
from hydrogram.types import Message

# جلب المتغيرات من إعدادات رندر
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# تعريف البوت
app = Client("black_hole", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("بوت", "") & filters.me)
async def bot_check(client: Client, message: Message):
    await message.reply_text("⚡️")

@app.on_message(filters.command("حظر", "") & filters.me)
async def ban_user(client: Client, message: Message):
    if message.reply_to_message:
        await client.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        await message.reply_text("👤 تم الحظر بنجاح!")

async def start_services():
    print("--- محاولة تشغيل البوت ---")
    try:
        await app.start()
        print("✅ تم تشغيل البوت بنجاح واتصل بتلجرام!")
    except Exception as e:
        print(f"❌ خطأ كارثي في الاتصال: {e}")
    
    # تشغيل سيرفر الويب للتمويه
    port = int(os.environ.get("PORT", 10000))
    print(f"🌐 تشغيل سيرفر التمويه على المنفذ: {port}")
    os.system(f"python3 -m http.server {port}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_services())
