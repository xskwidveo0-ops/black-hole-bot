import os, asyncio
from hydrogram import Client, filters

# variables are in English for maximum stability
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client(
    "black_hole",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Arabic commands for you, English logic for the server
@app.on_message(filters.command("بوت", ""))
async def bot_ping(client, message):
    await message.reply_text("⚡️")

@app.on_message(filters.command("حظر", ""))
async def bot_ban(client, message):
    if message.reply_to_message:
        try:
            await client.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
            await message.reply_text("👤 Done.")
        except Exception:
            pass

async def main():
    print("--- Starting Engine ---")
    await app.start()
    print("--- Engine Online ---")
    # Stealth mode for Render
    port = int(os.environ.get("PORT", 10000))
    os.system(f"python3 -m http.server {port}")

if __name__ == "__main__":
    asyncio.run(main())
