# handlers/user_management.py (modified)
from telegram import Update
from telegram.ext import ContextTypes
from sqlmodel import Session, select
from db import engine, BotUser

def is_admin(update: Update) -> bool:
    effective_username = update.effective_user.username
    if not effective_username:
        return False
    with Session(engine) as session:
        user = session.exec(select(BotUser).where(BotUser.username == effective_username)).first()
        if user and user.is_admin:
            return True
    return False

async def addadmin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        await update.message.reply_text("You are not authorized to perform this action.")
        return

    if not context.args:
        await update.message.reply_text("Please provide a username.")
        return

    username = context.args[0]
    with Session(engine) as session:
        user = session.exec(select(BotUser).where(BotUser.username == username)).first()
        if user:
            user.is_admin = True
        else:
            user = BotUser(username=username, is_admin=True)
            session.add(user)
        session.commit()
    await update.message.reply_text(f"{username} is now an admin.")

async def removeadmin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        await update.message.reply_text("You are not authorized to perform this action.")
        return

    if not context.args:
        await update.message.reply_text("Please provide a username.")
        return

    username = context.args[0]
    with Session(engine) as session:
        user = session.exec(select(BotUser).where(BotUser.username == username)).first()
        if not user:
            await update.message.reply_text("User not found.")
            return
        user.is_admin = False
        session.commit()
    await update.message.reply_text(f"{username} is no longer an admin.")

async def adduser(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        await update.message.reply_text("You are not authorized to perform this action.")
        return

    if not context.args:
        await update.message.reply_text("Please provide a username.")
        return

    username = context.args[0]
    with Session(engine) as session:
        user = session.exec(select(BotUser).where(BotUser.username == username)).first()
        if user:
            user.is_admin = False  # Ensure not admin
        else:
            user = BotUser(username=username, is_admin=False)
            session.add(user)
        session.commit()
    await update.message.reply_text(f"{username} has been added as a regular user.")

async def removeuser(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        await update.message.reply_text("You are not authorized to perform this action.")
        return

    if not context.args:
        await update.message.reply_text("Please provide a username.")
        return

    username = context.args[0]
    with Session(engine) as session:
        user = session.exec(select(BotUser).where(BotUser.username == username)).first()
        if not user:
            await update.message.reply_text("User not found.")
            return
        session.delete(user)
        session.commit()
    await update.message.reply_text(f"{username} has been removed.")
