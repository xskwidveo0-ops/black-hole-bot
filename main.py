from hydrogram import Client, filters
import os

# سحب البيانات من إعدادات Render (عشان الأمان والسرعة)
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("black_hole", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- [1] أمر الرد اللحظي (لقياس السرعة) ---
@app.on_message(filters.regex("^(بوت|فحص)$"))
async def speed_test(client, message):
    # الرد هنا "Direct" بدون أي معالجة نصوص لتقليل التأخير
    await message.reply_text("⚡️| أنا الأسرع في الوجود.")

# --- [2] أمر الحظر الإجرامي (القناص) ---
@app.on_message(filters.regex("^حظر$") & filters.reply & filters.group)
async def black_hole_ban(client, message):
    # الحظر يتم في "خلفية" البرنامج لضمان عدم تأخير أي عملية ثانية
    await client.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)

print("🚀 نظام بلاك هول في وضع الاستعداد.. تحدَّ أي بوت الآن!")
app.run()
