import os, asyncio, sys
from hydrogram import Client, filters

# محرك التشخيص والسرعة
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client(
    "black_hole",
    api_id=int(API_ID) if API_ID else 0,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.all)
async def debug_monitor(client, message):
    # 1. اختبار وصول الرسالة للبوت
    print(f"📡 [LOG] Received message from: {message.from_user.id if message.from_user else 'Unknown'}")
    print(f"📝 [LOG] Text: {message.text}")

    # 2. فحص كلمة "بوت"
    if message.text == "بوت":
        print("🎯 [CHECK] 'بوت' detected! Attempting to reply...")
        try:
            sent = await message.reply_text("⚡️")
            if sent:
                print("✅ [SUCCESS] Reply sent successfully!")
        except Exception as e:
            print(f"❌ [ERROR] Could not reply: {e}")

    # 3. فحص أمر "حظر"
    if message.text == "حظر":
        print("⚔️ [CHECK] 'حظر' detected!")
        if not message.reply_to_message:
            print("⚠️ [WARN] No reply detected for ban command.")
            return
            
        try:
            target = message.reply_to_message.from_user.id
            await client.ban_chat_member(message.chat.id, target)
            await message.reply_text("👤 Done.")
            print(f"✅ [SUCCESS] User {target} banned.")
        except Exception as e:
            print(f"❌ [ERROR] Ban failed: {e}")

async def start_system():
    print("🚀 --- Initializing High-Speed Engine ---")
    try:
        await app.start()
        me = await app.get_me()
        print(f"✅ --- Engine Online: @{me.username} ---")
        print(f"🆔 --- Bot ID: {me.id} ---")
    except Exception as e:
        print(f"‼️ --- CRITICAL STARTUP ERROR: {e} ---")
        return

    # تشغيل السيرفر الوهمي للتمويه
    port = int(os.environ.get("PORT", 10000))
    print(f"🌐 --- Web Stealth active on port {port} ---")
    os.system(f"python3 -m http.server {port}")

if __name__ == "__main__":
    asyncio.run(start_system())
