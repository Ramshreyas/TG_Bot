# handlers/start.py
from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(
        f'Hi {user.first_name}! I am a summarization bot. Add me to a group and use /summarize <group name> to get message summaries from the last 3 days!'
    )
