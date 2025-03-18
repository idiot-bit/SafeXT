import logging
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import random
import os

# Telegram Bot Token
TOKEN = "7832607410:AAHBFdT8-pds_XQMG1_UiXb5vNcKFKYl4Qk"

# Owner ID (Only You Can Use the Bot)
OWNER_ID = 7832607410

# Key Storage (Last 10 Keys)
key_history = []

# Setup Logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# 📌 Step 1: Random Startup Messages
startup_messages = [
    "🔥 Welcome Back, Master! Ready to Roll? 🔥",
    "⚡ Bot Activated! Let’s Get Things Done! ⚡",
    "🚀 Powering Up! Your Command is My Mission! 🚀",
    "👑 Welcome, Boss! Your Bot is Online. 👑"
]

async def start(update: Update, context: CallbackContext) -> None:
    if update.effective_user.id != OWNER_ID:
        return  # Ignore if not owner
    startup_message = random.choice(startup_messages)
    await update.message.reply_text(startup_message)

# 📌 Step 2: Update Key Command
async def update_key(update: Update, context: CallbackContext) -> None:
    if update.effective_user.id != OWNER_ID:
        return

    # Extract new key
    new_key = " ".join(context.args)
    if not new_key:
        await update.message.reply_text("❌ Please provide a new key. Example: /updatekey NEW_KEY")
        return

    # Store only last 10 keys
    key_history.append(new_key)
    if len(key_history) > 10:
        key_history.pop(0)  # Remove the oldest key

    # Updated Message with New Key
    updated_message = f"""♻️Esᴘ - ❕
♻️Tᴏᴜᴄʜ-Aɪᴍʙᴏᴛ Bʀᴜᴛᴛᴛᴀʟ - 👽
♻️Nᴏ ʀᴇᴄᴏɪʟ - ⭕️
♻️Iɢɴᴏʀᴇ Kɴᴏᴄᴋᴇᴅ / Vɪsɪʙɪʟɪᴛʏ Cʜᴇᴄᴋ⚠️
♻️Oɴʟɪɴᴇ Bʏᴘᴀss Sʏsᴛᴇᴍ - 🌀

Key - `{new_key}`

𝗗𝗶𝗿𝗲𝗰𝘁 𝗟𝗼𝗴𝗶𝗻 𝗠𝗮𝗶𝗻 𝗔𝗰𝗰𝗼𝘂𝗻𝘁 ☠

𝗝𝗼𝗶𝗻 𝗦𝗵𝗮𝗿𝗲 & 𝗦𝘂𝗽𝗽𝗼𝗿𝘁 🤩
https://t.me/SafeXT
https://t.me/SafeXT

𝗡𝗼𝘁𝗲 : 
    𝗢𝗻𝗹𝘆 𝗦𝗮𝗳𝗲 𝗛𝗮𝗰𝗸𝘀 𝗣𝗿𝗼𝘃𝗶𝗱𝗶𝗻𝗴 ✅
      𝗨𝘀𝗲𝗹𝗲𝘀𝘀 𝗹𝗼𝗮𝗱𝗲𝗿 𝗼𝗿 𝗠𝗼𝗱𝘀🚫
         𝗜𝗮𝗺 𝗡𝗼𝘁 𝗣𝗿𝗼𝘃𝗶𝗱𝗶𝗻𝗴 ❎

   𝗪𝗮𝗻𝘁 𝗕𝘂𝘆 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 ❕
     @LocalxCheats 👽
"""
    await update.message.reply_text(updated_message, parse_mode="Markdown")

    # Step 3: Ask for APK
    await update.message.reply_text("📌 Send The Apk (Max 30MB)")

# 📌 Step 3: Handle APK Upload
async def handle_apk(update: Update, context: CallbackContext) -> None:
    if update.effective_user.id != OWNER_ID:
        return

    document = update.message.document
    if not document.mime_type.startswith("application/vnd.android.package-archive"):
        await update.message.reply_text("❌ Please send a valid APK file.")
        return

    if document.file_size > 30 * 1024 * 1024:
        await update.message.reply_text("❌ APK size is too large! Max 30MB allowed.")
        return

    # Download the APK
    file_path = f"{document.file_name}"
    file = await context.bot.get_file(document.file_id)
    await file.download_to_drive(file_path)

    # Send Updated Message + APK
    await update.message.reply_document(
        document=InputFile(file_path),
        caption=f"✅ **Updated Key & APK**\n\n🔑 **Key:** `{key_history[-1]}`\n📂 **APK:** {document.file_name}",
        parse_mode="Markdown"
    )

    # Delete file after sending
    os.remove(file_path)

# 📌 Bot Main Function
def main():
    app = Application.builder().token(TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("updatekey", update_key))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_apk))

    # Run Bot
    app.run_polling()

if __name__ == "__main__":
    main()