import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from hydrogram import Client, filters

# 1. إعداد البوت
app = Client(
    "black_hole",
    api_id=int(os.environ.get("API_ID")),
    api_hash=os.environ.get("API_HASH"),
    bot_token=os.environ.get("BOT_TOKEN")
)

# 2. وظائف الرد (المنطق)
@app.on_message(filters.regex("بوت"))
async def ping(client, message):
    print(f"⚡️ Received PING from {message.chat.id}")
    await message.reply_text("⚡️")

@app.on_message(filters.regex("حظر") & filters.reply)
async def ban(client, message):
    try:
        await client.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        await message.reply_text("👤 Done.")
    except Exception as e:
        print(f"Error: {e}")

# 3. سيرفر وهمي خفيف جداً (لإسكات Render)
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is Running")

def start_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), DummyHandler)
    print(f"🌐 Web Server running on port {port}")
    server.serve_forever()

# 4. التشغيل المتوازي (Multithreading)
if __name__ == "__main__":
    # تشغيل السيرفر الوهمي في مسار منفصل (Background Thread)
    t = threading.Thread(target=start_web_server)
    t.daemon = True
    t.start()
    
    # تشغيل البوت في المسار الرئيسي
    print("🚀 Bot Engine Starting...")
    app.run()
