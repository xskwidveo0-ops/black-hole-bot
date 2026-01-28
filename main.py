import os
import threading
import uvloop
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
from hydrogram import Client, filters

# 1. تثبيت المحرك الفضائي في النظام
uvloop.install()

# 2. إعدادات البوت (الرام فقط لسرعة البرق)
app = Client(
    "black_hole_turbo",
    api_id=int(os.environ.get("API_ID")),
    api_hash=os.environ.get("API_HASH"),
    bot_token=os.environ.get("BOT_TOKEN"),
    workers=32,
    in_memory=True
)

# 3. دوال الرد السريع
@app.on_message(filters.regex("بوت"))
async def speed_test(client, message):
    await message.reply_text("⚡️")

@app.on_message(filters.regex("حظر") & filters.reply)
async def ban_hammer(client, message):
    try:
        await client.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        await message.reply_text("👤 Done.")
    except:
        pass

# 4. سيرفر التمويه (يعمل في Thread منفصل)
class SilentHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
    def log_message(self, format, *args): pass

def start_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), SilentHandler)
    server.serve_forever()

# 5. الوظيفة الرئيسية للتشغيل الصحيح
async def start_all():
    # تشغيل السيرفر في الخلفية
    threading.Thread(target=start_web_server, daemon=True).start()
    
    print("🚀 ACTIVATING NUCLEAR ENGINE...")
    await app.start()
    print("✅ SYSTEM LIVE & HYPER-FAST")
    
    # ابقاء البوت حياً
    from hydrogram.methods.utilities.idle import idle
    await idle()
    await app.stop()

if __name__ == "__main__":
    # الطريقة الصحيحة لتشغيل uvloop بدون أخطاء RuntimeError
    asyncio.run(start_all())
