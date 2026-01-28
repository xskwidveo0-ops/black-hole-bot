import os
import threading
import uvloop
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
from hydrogram import Client, filters, idle

# 1. تفعيل محرك uvloop (أسرع بـ 4 أضعاف من بايثون العادي)
uvloop.install()

async def run_ultimate_bot():
    # 2. تشغيل سيرفر "التمويه" داخل الكود لضمان عدم حدوث تضارب
    def run_web_server():
        port = int(os.environ.get("PORT", 8080))
        server = HTTPServer(("0.0.0.0", port), type('H', (BaseHTTPRequestHandler,), {
            'do_GET': lambda s: (s.send_response(200), s.end_headers()),
            'log_message': lambda *a: None
        }))
        server.serve_forever()

    threading.Thread(target=run_web_server, daemon=True).start()

    # 3. إعدادات البوت "داخل" الدالة لضمان التوافق مع uvloop
    # workers=100 يعني قدرة هائلة على معالجة مئات الرسائل في ثانية واحدة
    app = Client(
        "black_hole_ultimate",
        api_id=int(os.environ.get("API_ID")),
        api_hash=os.environ.get("API_HASH"),
        bot_token=os.environ.get("BOT_TOKEN"),
        workers=100, 
        in_memory=True
    )

    @app.on_message(filters.regex("بوت"))
    async def fast_reply(client, message):
        await message.reply_text("⚡️")

    @app.on_message(filters.regex("حظر") & filters.reply)
    async def fast_ban(client, message):
        try:
            await client.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
            await message.reply_text("👤 Done.")
        except: pass

    print("🚀 THE NUCLEAR ENGINE IS LIVE...")
    await app.start()
    await idle() # ابقاء البوت حياً بأقل استهلاك للموارد
    await app.stop()

if __name__ == "__main__":
    # تشغيل كل شيء في مسار واحد نظيف وسريع جداً
    asyncio.run(run_ultimate_bot())
