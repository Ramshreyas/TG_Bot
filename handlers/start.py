# handlers/start.py
from telegram import Update
from telegram.ext import ContextTypes
from sqlmodel import Session, select
from db import engine, BotUser

def get_first_admin_username():
    with Session(engine) as session:
        admin_user = session.exec(select(BotUser).where(BotUser.is_admin == True)).first()
        if admin_user:
            return admin_user.username
    return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    first_admin = get_first_admin_username()
    if first_admin:
        admin_info = f"\nPlease contact {first_admin} to be added to the whitelist."
    else:
        admin_info = "\nCurrently, no admins are available."

    await update.message.reply_text(
        f"Hi {user.first_name}! I am a summarization bot. Add me to a group and use /summarize <group name> to get "
        f"message summaries from the last 3 days!{admin_info}"
    )
