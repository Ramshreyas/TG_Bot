import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from sqlmodel import Session, select
from db import init_db, get_session, ChatType, Chat, User, Message, Update as DBUpdate, engine

# Load environment variables
load_dotenv()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(f'Hi {user.first_name}! I am a summarization bot. Add me to a group and use /summarize to get message summaries!')

async def summarize(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    messages = get_messages_last_7_days(chat_id)
    if not messages:
        await context.bot.send_message(chat_id=chat_id, text="No messages found in the last 7 days.")
    else:
        response = "Messages from the last 7 days:\n"
        for msg in messages:
            response += f"- {msg.text}\n"
        await context.bot.send_message(chat_id=chat_id, text=response)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message and update.message.chat.type in ['group', 'supergroup']:
        chat_id = update.message.chat.id
        message_text = update.message.text if update.message.text else "[non-text content]"
        user = update.message.from_user
        username = user.username if user.username else user.first_name

        with Session(engine) as session:
            try:
                chat_type = session.exec(select(ChatType).where(ChatType.type_name == update.message.chat.type)).first()
                if not chat_type:
                    chat_type = ChatType(type_name=update.message.chat.type)
                    session.add(chat_type)
                    session.flush()

                chat = session.exec(select(Chat).where(Chat.chat_id == chat_id)).first()
                if not chat:
                    chat = Chat(
                        chat_id=chat_id,
                        title=update.message.chat.title,
                        type_id=chat_type.id
                    )
                    session.add(chat)
                    session.flush()

                db_user = session.exec(select(User).where(User.user_id == user.id)).first()
                if not db_user:
                    db_user = User(
                        user_id=user.id,
                        first_name=user.first_name,
                        last_name=user.last_name,
                        is_bot=user.is_bot,
                        language_code=user.language_code,
                        username=user.username
                    )
                    session.add(db_user)
                    session.flush()

                msg = Message(
                    message_id=update.message.message_id,
                    channel_chat_created=update.message.channel_chat_created,
                    chat_id=chat.id,
                    date=int(update.message.date.timestamp()),
                    delete_chat_photo=update.message.delete_chat_photo,
                    from_user_id=db_user.id,
                    group_chat_created=update.message.group_chat_created,
                    supergroup_chat_created=update.message.supergroup_chat_created,
                    text=message_text
                )
                session.add(msg)
                session.flush()

                db_update = DBUpdate(
                    update_id=update.update_id,
                    message_id=msg.id
                )
                session.add(db_update)
                session.commit()

            except Exception:
                session.rollback()
                raise

def get_messages_last_7_days(chat_id):
    with Session(engine) as session:
        seven_days_ago = datetime.now() - timedelta(days=7)
        statement = (
            select(Message)
            .where(Message.chat_id == chat_id)
            .where(Message.date > int(seven_days_ago.timestamp()))
        )
        return session.exec(statement).all()

def main() -> None:
    init_db()
    application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("summarize", summarize))
    application.add_handler(MessageHandler(filters.ChatType.GROUPS & filters.TEXT, handle_message))
    application.run_polling()

if __name__ == '__main__':
    main()
