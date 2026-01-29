import os
import threading
import uvloop
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
from hydrogram import Client, filters, idle
from hydrogram.types import ChatPermissions
from motor.motor_asyncio import AsyncIOMotorClient

# 1. تفعيل المحرك النووي
uvloop.install()

# 2. إعدادات قاعدة البيانات (ضع رابطك هنا أو في متغيرات رندر)
MONGO_URL = os.environ.get("MONGO_URL", "رابط_قاعدتك_هنا")
db_client = AsyncIOMotorClient(MONGO_URL)
db = db_client["black_hole_db"]
sudo_collection = db["sudo_users"]

OWNER_ID = 778171393  # آيديك الخاص

async def run_ultimate_bot():
    # --- سيرفر التمويه ---
    def run_web_server():
        port = int(os.environ.get("PORT", 8080))
        server = HTTPServer(("0.0.0.0", port), type('H', (BaseHTTPRequestHandler,), {
            'do_GET': lambda s: (s.send_response(200), s.end_headers()),
            'log_message': lambda *a: None
        }))
        server.serve_forever()
    threading.Thread(target=run_web_server, daemon=True).start()

    # --- إعدادات البوت ---
    app = Client("black_hole_pro", api_id=int(os.environ.get("API_ID")), 
                 api_hash=os.environ.get("API_HASH"), bot_token=os.environ.get("BOT_TOKEN"),
                 workers=100, in_memory=True)

    # --- نظام الصلاحيات بالاعتماد على القاعدة ---
    async def is_admin(client, message):
        user_id = message.from_user.id
        if user_id == OWNER_ID: return True
        # التحقق من قاعدة البيانات
        is_sudo = await sudo_collection.find_one({"user_id": user_id})
        if is_sudo: return True
        # التحقق من رتبة المشرف في التلجرام
        check = await client.get_chat_member(message.chat.id, user_id)
        return check.status in ("administrator", "creator")

    # --- الأوامر ---

    @app.on_message(filters.regex("^رفع مميز$") & filters.reply)
    async def promote(client, message):
        if not await is_admin(client, message): return
        target_id = message.reply_to_message.from_user.id
        await sudo_collection.update_one({"user_id": target_id}, {"$set": {"user_id": target_id}}, upsert=True)
        await message.reply_text(f"✅ تم حفظ المستخدم في الذاكرة الدائمة.")

    @app.on_message(filters.regex("^تنزيل مميز$") & filters.reply)
    async def demote(client, message):
        if not await is_admin(client, message): return
        target_id = message.reply_to_message.from_user.id
        await sudo_collection.delete_one({"user_id": target_id})
        await message.reply_text(f"❌ تم حذفه من الذاكرة الدائمة.")

    @app.on_message(filters.regex(r"^مسح (\d+)$"))
    async def purge_msgs(client, message):
        if not await is_admin(client, message): return
        count = int(message.matches[0].group(1))
        chat_id = message.chat.id
        msgs_to_delete = []

        if message.reply_to_message:
            target_user = message.reply_to_message.from_user.id
            async for m in client.get_chat_history(chat_id, limit=1000):
                if m.from_user and m.from_user.id == target_user:
                    msgs_to_delete.append(m.id)
                if len(msgs_to_delete) >= count: break
        else:
            async for m in client.get_chat_history(chat_id, limit=count + 1):
                msgs_to_delete.append(m.id)

        if msgs_to_delete:
            # تقسيم الحذف لمجموعات (للسرعة القصوى وتجنب حظر التلجرام)
            for i in range(0, len(msgs_to_delete), 100):
                await client.delete_messages(chat_id, msgs_to_delete[i:i+100])
            info = await message.reply_text(f"🧹 تم تطهير {len(msgs_to_delete)} رسالة بنجاح.")
            await asyncio.sleep(3)
            await info.delete()

    print("🚀 NUCLEAR SYSTEM WITH CLOUD MEMORY LIVE...")
    await app.start()
    await idle()

if __name__ == "__main__":
    asyncio.run(run_ultimate_bot())
