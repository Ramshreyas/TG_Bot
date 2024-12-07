# handlers/message.py
from telegram import Update
from telegram.ext import ContextTypes
from sqlmodel import Session, select
from db import engine, ChatType, Chat, User, Message, Update as DBUpdate

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
