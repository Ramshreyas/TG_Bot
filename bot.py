import logging
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from db import init_db, get_session, ChatType, Chat, User, Message, Update as DBUpdate, engine
from sqlmodel import Session

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_text(f'Hi {user.first_name}! I am a summarization bot. Add me to a group and use /summarize to get message summaries!')

async def summarize(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /summarize command."""
    logger.info("Received /summarize command")
    await update.message.reply_text("I received your summarize command! Args: " + (' '.join(context.args) if context.args else "no args"))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log all messages in groups."""
    if update.message:
        # Debug logging
        logger.info(f"Received update type: {update.message.chat.type}")
        logger.info(f"Message text: {update.message.text if update.message.text else '[non-text content]'}")
        
        if update.message.chat.type in ['group', 'supergroup']:
            chat_id = update.message.chat.id
            message_text = update.message.text if update.message.text else "[non-text content]"
            user = update.message.from_user
            username = user.username if user.username else user.first_name
            
            logger.info(f"Processing message from {username} in chat {chat_id}")
            
            # Store in database
            with Session(engine) as session:
                try:
                    logger.info("Starting database operations...")
                    
                    # Get or create chat type
                    chat_type = session.query(ChatType).filter_by(type_name=update.message.chat.type).first()
                    if not chat_type:
                        logger.info(f"Creating new chat type: {update.message.chat.type}")
                        chat_type = ChatType(type_name=update.message.chat.type)
                        session.add(chat_type)
                        session.flush()
                    
                    # Get or create chat
                    chat = session.query(Chat).filter_by(chat_id=chat_id).first()
                    if not chat:
                        logger.info(f"Creating new chat with ID: {chat_id}")
                        chat = Chat(
                            chat_id=chat_id,
                            title=update.message.chat.title,
                            type_id=chat_type.id
                        )
                        session.add(chat)
                        session.flush()

                    # Get or create user
                    db_user = session.query(User).filter_by(user_id=user.id).first()
                    if not db_user:
                        logger.info(f"Creating new user: {username}")
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

                    # Create message
                    logger.info("Creating new message")
                    message = Message(
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
                    session.add(message)
                    session.flush()
                    
                    # Create update record
                    logger.info("Creating update record")
                    db_update = DBUpdate(
                        update_id=update.update_id,
                        message_id=message.id
                    )
                    session.add(db_update)
                    session.commit()

                    logger.info("Database operations completed successfully")

                except Exception as e:
                    logger.error(f"Error storing message in database: {e}")
                    session.rollback()
                    raise  # Re-raise the exception for debugging
            
            log_message = f"Group: {update.message.chat.title} ({chat_id}) | User: {username} | Message: {message_text}"
            logger.info(log_message)
        else:
            logger.debug(f"Ignoring message from chat type: {update.message.chat.type}")

def get_messages_last_7_days(chat_id):
    with Session(engine) as session:
        seven_days_ago = datetime.now() - timedelta(days=7)
        messages = session.query(Message).filter_by(chat_id=chat_id).filter(Message.date > int(seven_days_ago.timestamp())).all()
        return messages

def main() -> None:
    """Start the bot."""
    # Initialize database
    init_db()
    
    # Set logging to DEBUG level
    logging.getLogger().setLevel(logging.DEBUG)
    
    # Create the Application and pass it your bot's token
    application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("summarize", summarize))
    
    # Add message handler specifically for group messages
    application.add_handler(MessageHandler(filters.ChatType.GROUPS & filters.TEXT, handle_message))

    # Start the Bot
    logger.info("Bot started and listening for messages...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
