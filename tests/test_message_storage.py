import os
import pytest
from sqlmodel import Session, select
from dotenv import load_dotenv
from telegram import Bot
import asyncio
from db.models import Message, Chat, User, ChatType
from db.database import engine, init_db
import time
from config import BOT_TOKEN, TEST_GROUP_ID

# Load environment variables
load_dotenv()

def pytest_addoption(parser):
    parser.addoption("--test-code", action="store", default="TEST_MESSAGE_123",
                    help="Test code to search for in messages")
    parser.addoption("--drop-tables", action="store_true", default=False,
                    help="Drop and recreate all tables before testing")

@pytest.fixture
def test_code(request):
    return request.config.getoption("--test-code")

@pytest.fixture(scope="module")
def setup_database(request):
    """Initialize the database before tests"""
    drop_tables = request.config.getoption("--drop-tables", default=False)
    init_db(drop_tables=drop_tables)
    yield

@pytest.mark.asyncio
async def test_message_storage(setup_database, test_code):
    """Test that messages are correctly stored in the database"""
    
    print("\n")
    print("="*80)
    print(f"Checking for message with code: {test_code}")
    print("="*80)
    print("\n")
    
    # Wait for message to be processed
    max_wait = 30  # Maximum wait time in seconds
    start_time = time.time()
    message_found = False
    
    print("Checking database for message...")
    
    while time.time() - start_time < max_wait and not message_found:
        # Query the database
        with Session(engine) as session:
            # Query for the message
            statement = select(Message).where(Message.text == test_code)
            db_message = session.exec(statement).first()
            
            if db_message is not None:
                message_found = True
                print(f"\nMessage found in database!")
                break
                
        # Wait a bit before next check
        print(".", end="", flush=True)
        await asyncio.sleep(2)
    
    # Assert message was found
    assert message_found, f"Message with code {test_code} was not found in database after {max_wait} seconds"
    
    # Initialize bot
    bot = Bot(token=BOT_TOKEN)
    
    try:
        # Query the database
        with Session(engine) as session:
            # Query for the message
            statement = select(Message).where(Message.text == test_code)
            db_message = session.exec(statement).first()
            
            # Assert message was stored
            assert db_message is not None
            assert db_message.text == test_code
            
            # Check related chat was stored
            chat = session.get(Chat, db_message.chat_id)
            assert chat is not None
            assert chat.chat_id == TEST_GROUP_ID
            
            # Check user was stored
            user = session.get(User, db_message.from_user_id)
            assert user is not None
            assert user.is_bot is False  # Since message was sent by user
            
    finally:
        await bot.close()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
