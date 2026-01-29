import os
import threading
import uvloop
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
from hydrogram import Client, filters, idle
from motor.motor_asyncio import AsyncIOMotorClient

# 1. تفعيل المحرك النووي
uvloop.install()

# 2. إعدادات الذاكرة
MONGO_URL = os.environ.get("MONGO_URL")
db_client = AsyncIOMotorClient(MONGO_URL)
db = db_client["black_hole_db"]
sudo_collection = db["sudo_users"]

# آيديك الخاص
OWNER_ID = 778171393

async def run_ultimate_bot():
    def run_web_server():
        port = int(os.environ.get("PORT", 8080))
        server = HTTPServer(("0.0.0.0", port), type('H', (BaseHTTPRequestHandler,), {
            'do_GET': lambda s: (s.send_response(200), s.end_headers()),
            'log_message': lambda *a: None
        }))
        server.serve_forever()
    threading.Thread(target=run_web_server, daemon=True).start()

    app = Client(
        "black_hole_ultimate",
        api_id=int(os.environ.get("API_ID")),
        api_hash=os.environ.get("API_HASH"),
        bot_token=os.environ.get("BOT_TOKEN"),
        workers=100, 
        in_memory=True
    )

    async def is_admin(client, message):
        user_id = message.from_user.id
        if user_id == OWNER_ID: return True
        is_sudo = await sudo_collection.find_one({"user_id": user_id})
        return True if is_sudo else False

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

    @app.on_message(filters.regex("^رفع مميز$") & filters.reply)
    async def promote(client, message):
        if message.from_user.id != OWNER_ID: return
        target_id = message.reply_to_message.from_user.id
        await sudo_collection.update_one({"user_id": target_id}, {"$set": {"user_id": target_id}}, upsert=True)
        await message.reply_text("✅ تم الحفظ في الذاكرة.")

    @app.on_message(filters.regex("^تنزيل مميز$") & filters.reply)
    async def demote(client, message):
        if message.from_user.id != OWNER_ID: return
        target_id = message.reply_to_message.from_user.id
        await sudo_collection.delete_one({"user_id": target_id})
        await message.reply_text("❌ تم الحذف من الذاكرة.")

    # --- أمر المسح الخارق (المطور) ---
    @app.on_message(filters.regex(r"^مسح\s+(\d+)$"))
    async def purge_msgs(client, message):
        if not await is_admin(client, message): return
        
        count = int(message.matches[0].group(1))
        chat_id = message.chat.id
        msgs_to_delete = []
        
        try:
            # حالة المسح لشخص معين (بالرد)
            if message.reply_to_message:
                target_user = message.reply_to_message.from_user.id
                # نبحث في آخر 1000 رسالة لنجد رسائل هذا الشخص
                async for m in client.get_chat_history(chat_id, limit=1000):
                    if m.from_user and m.from_user.id == target_user:
                        msgs_to_delete.append(m.id)
                    if len(msgs_to_delete) >= count: break
            # حالة المسح العام
            else:
                async for m in client.get_chat_history(chat_id, limit=count):
                    msgs_to_delete.append(m.id)
            
            # تنفيذ المسح على دفعات (كل دفعة 100 رسالة للسرعة وتجنب الحظر)
            if msgs_to_delete:
                for i in range(0, len(msgs_to_delete), 100):
                    batch = msgs_to_delete[i:i+100]
                    await client.delete_messages(chat_id, batch)
                
                status = await message.reply_text(f"🧹 تم تطهير {len(msgs_to_delete)} رسالة.")
                await asyncio.sleep(2)
                await status.delete()
                
        except Exception as e:
            # إذا فشل البحث في التاريخ (مثل مشكلة 400)، نستخدم تكنيك الحذف المباشر كخطة بديلة
            current_id = message.id
            backup_ids = [current_id - i for i in range(count + 1)]
            await client.delete_messages(chat_id, backup_ids)

    print("🚀 NUCLEAR ENGINE IS LIVE & SMART...")
    await app.start()
    await idle()

if __name__ == "__main__":
    asyncio.run(run_ultimate_bot())
