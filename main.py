import os
import threading
import uvloop
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
from hydrogram import Client, filters, idle
from motor.motor_asyncio import AsyncIOMotorClient

# 1. تفعيل المحرك النووي (السرعة القصوى)
uvloop.install()

# 2. إعدادات الذاكرة الدائمة (MongoDB)
MONGO_URL = os.environ.get("MONGO_URL")
db_client = AsyncIOMotorClient(MONGO_URL)
db = db_client["black_hole_db"]
sudo_collection = db["sudo_users"]

# آيديك الخاص
OWNER_ID = 778171393

async def run_ultimate_bot():
    # --- سيرفر التمويه لـ Render ---
    def run_web_server():
        port = int(os.environ.get("PORT", 8080))
        server = HTTPServer(("0.0.0.0", port), type('H', (BaseHTTPRequestHandler,), {
            'do_GET': lambda s: (s.send_response(200), s.end_headers()),
            'log_message': lambda *a: None
        }))
        server.serve_forever()
    threading.Thread(target=run_web_server, daemon=True).start()

    # --- إعدادات البوت الاحترافية ---
    app = Client(
        "black_hole_ultimate",
        api_id=int(os.environ.get("API_ID")),
        api_hash=os.environ.get("API_HASH"),
        bot_token=os.environ.get("BOT_TOKEN"),
        workers=100, 
        in_memory=True
    )

    # --- نظام التحقق من الصلاحيات ---
    async def is_admin(client, message):
        user_id = message.from_user.id
        if user_id == OWNER_ID: return True
        is_sudo = await sudo_collection.find_one({"user_id": user_id})
        if is_sudo: return True
        return False

    # --- [أوامر كود أمس - السرعة] ---

    @app.on_message(filters.regex("^بوت$"))
    async def fast_reply(client, message):
        await message.reply_text("⚡️")

    @app.on_message(filters.regex("^حظر$") & filters.reply)
    async def fast_ban(client, message):
        if not await is_admin(client, message): return
        try:
            await client.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
            await message.reply_text("👤 Done.")
        except: pass

    # --- [أوامر اليوم - الذاكرة والمسح] ---

    @app.on_message(filters.regex("^رفع مميز$") & filters.reply)
    async def promote(client, message):
        if message.from_user.id != OWNER_ID: return
        target_id = message.reply_to_message.from_user.id
        await sudo_collection.update_one({"user_id": target_id}, {"$set": {"user_id": target_id}}, upsert=True)
        await message.reply_text(f"✅ تم الحفظ في الذاكرة الدائمة.")

    @app.on_message(filters.regex("^تنزيل مميز$") & filters.reply)
    async def demote(client, message):
        if message.from_user.id != OWNER_ID: return
        target_id = message.reply_to_message.from_user.id
        await sudo_collection.delete_one({"user_id": target_id})
        await message.reply_text(f"❌ تم الحذف من الذاكرة.")

    @app.on_message(filters.regex(r"^مسح\s+(\d+)$"))
    async def purge_msgs(client, message):
        if not await is_admin(client, message): return
        try:
            count = int(message.matches[0].group(1))
            chat_id = message.chat.id
            current_id = message.id
            
            if message.reply_to_message:
                target_id = message.reply_to_message.id
                await client.delete_messages(chat_id, [target_id, current_id])
            else:
                to_delete = [current_id - i for i in range(count + 1)]
                await client.delete_messages(chat_id, to_delete)
                res = await client.send_message(chat_id, f"🧹 تم تنظيف {count} رسالة بنجاح.")
                await asyncio.sleep(2)
                await res.delete()
        except Exception as e:
            print(f"Error in Purge: {e}")

    print("🚀 THE NUCLEAR ENGINE IS LIVE WITH MEMORY...")
    await app.start()
    await idle()

if __name__ == "__main__":
    asyncio.run(run_ultimate_bot())
