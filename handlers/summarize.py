# handlers/summarize.py
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes
from sqlmodel import Session, select
from db import engine, Chat, Message
from llm.summarizer import summarize_messages

async def summarize(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide a group name.")
        return

    group_name = " ".join(context.args)

    with Session(engine) as session:
        chat = session.exec(select(Chat).where(Chat.title == group_name)).first()
        if not chat:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="No messages found for that group.")
            return

        messages = get_messages_last_3_days(chat.id)

    if not messages:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="No messages found in the last 3 days for that group.")
    else:
        summary = summarize_messages(messages)
        response = f"Summary for '{group_name}':\n{summary}"
        max_length = 4000
        chunks = [response[i:i+max_length] for i in range(0, len(response), max_length)]
        for chunk in chunks:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=chunk)

def get_messages_last_3_days(chat_id):
    with Session(engine) as session:
        three_days_ago = datetime.utcnow() - timedelta(days=3)
        statement = (
            select(Message)
            .where(Message.chat_id == chat_id)
            .where(Message.date > int(three_days_ago.timestamp()))
        )
        return session.exec(statement).all()
