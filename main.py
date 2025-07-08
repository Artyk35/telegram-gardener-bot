import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from gpt_engine import get_or_generate_plant_info
from formatter import format_plant_info

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip().lower()
    await update.message.reply_text("🔍 Ищу информацию...")
    plant_info = get_or_generate_plant_info(query)
    response = format_plant_info(plant_info)
    await update.message.reply_text(response, parse_mode="Markdown")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Бот запущен")
    app.run_polling()
