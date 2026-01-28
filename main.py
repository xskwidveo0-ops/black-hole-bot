import os
import asyncio
import threading
import uvloop
from http.server import HTTPServer, BaseHTTPRequestHandler
from hydrogram import Client, filters, idle

# 1. تفعيل المحرك الفضائي (استبدال قلب بايثون)
uvloop.install()

# 2. إعدادات البوت القصوى
# نستخدم workers بعدد المعالجات المتاحة لضمان عدم توقف أي رسالة
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client(
    "black_hole_turbo",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=min(32, (os.cpu_count() or 1) + 4), # ذكاء اصطناعي لتحديد عدد العمال
    in_memory=True, # عدم الكتابة على الهارد ديسك لسرعة خرافية (RAM only)
    ipv6=False # تعطيل IPV6 لتجنب تأخير الاتصال في بعض السيرفرات
)

# 3. دوال الرد السريع (بدون أي تأخير)
@app.on_message(filters.regex("بوت"))
async def speed_test(client, message):
    # الرد المباشر
    await message.reply_text("⚡️")

@app.on_message(filters.regex("حظر") & filters.reply)
async def ban_hammer(client, message):
    try:
        # الطرد بأقصى سرعة ممكنة
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        await client.ban_chat_member(chat_id, user_id)
        await message.reply_text("👤 Done.")
    except Exception as e:
        print(f"Error: {e}")

# 4. سيرفر التمويه (خفيف جداً ولا يستهلك موارد)
class SilentHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
    def log_message(self, format, *args):
        pass # إسكات اللوجز الخاصة بالسيرفر لتوفير الموارد

def start_stealth_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), SilentHandler)
    server.serve_forever()

# 5. التشغيل
if __name__ == "__main__":
    print("🚀 ACTIVATING NUCLEAR ENGINE WITH UVLOOP...")
    
    # تشغيل سيرفر الويب في مسار منفصل (الحل الهندسي الذي نجح معنا)
    server_thread = threading.Thread(target=start_stealth_server, daemon=True)
    server_thread.start()
    
    # تشغيل البوت
    app.start()
    print(f"✅ SYSTEM OPTIMIZED & READY. Speed: MAX")
    idle()
    app.stop()
