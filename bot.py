import os
from dotenv import load_dotenv
from telegram import Update, Message
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

user_message_map = {}

async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    user_message_map[user.id] = user

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📩 New message from {user.full_name} (ID: {user.id}):\n\n{text}"
    )

    # Auto-reply to user
    # await update.message.reply_text("📨We will get back to you shortly.")

async def handle_admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return 

    if not context.args or len(context.args) < 2:
        await update.message.reply_text("❌ Usage: /reply <user_id> <message>")
        return

    try:
        user_id = int(context.args[0])
        message = " ".join(context.args[1:])
        await context.bot.send_message(chat_id=user_id, text=f"{message}")
        await update.message.reply_text("✅ Message sent to user.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reply", handle_admin_reply))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message))
    print("🤖 Support bot is running...")
    app.run_polling()