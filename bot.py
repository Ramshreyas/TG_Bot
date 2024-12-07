# bot.py
import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from db import init_db
from handlers.start import start
from handlers.summarize import summarize
from handlers.message import handle_message

load_dotenv()

def main() -> None:
    init_db()
    application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("summarize", summarize))
    application.add_handler(MessageHandler(filters.ChatType.GROUPS & filters.TEXT, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()
