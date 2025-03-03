import os
import re
from pyrogram import Client, filters
from pyrogram.types import Message

# ✅ Bot Setup
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Client("rename_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ✅ Function to clean filename
def clean_filename(original_name):
    # Remove everything inside brackets [] (e.g., [Dual], [Fansub])
    original_name = re.sub(r".*?", "", original_name)

    # Extract only letters, numbers, episode numbers (E###), and quality (480p, 1080p)
    match = re.findall(r"[a-zA-Z]+|E\d{1,4}|[0-9]{3,4}p", original_name)

    if match:
        clean_name = " ".join(match)  # Join extracted parts with a space
        return f"[@Animes2u] {clean_name}"  # Add the prefix
    return f"[@Animes2u] Unknown_File"

# ✅ File Rename & Process
@bot.on_message(filters.document)
async def rename_file(client: Client, message: Message):
    file_path = await client.download_media(message)
    
    if not file_path:
        await message.reply_text("❌ Failed to download file.")
        return

    # Extract filename & clean it
    file_name, file_ext = os.path.splitext(message.document.file_name)
    new_filename = clean_filename(file_name) + file_ext
    new_file_path = os.path.join(os.path.dirname(file_path), new_filename)

    os.rename(file_path, new_file_path)

    try:
        await client.send_document(
            chat_id=message.chat.id,
            document=new_file_path,
            file_name=new_filename,
            caption=f"✅ Renamed: {new_filename}",
        )
        os.remove(new_file_path)  # ✅ Delete after sending
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

# ✅ Start Command
@bot.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    await message.reply_text(
        "👋 Hello! Send a file, and I'll rename it!"
    )

# ✅ Start the bot
bot.run()
