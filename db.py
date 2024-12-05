from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, List
from sqlmodel import Field, SQLModel, create_engine, Session, Relationship

class ChatType(str, Enum):
    PRIVATE = "private"
    GROUP = "group"
    SUPERGROUP = "supergroup"
    CHANNEL = "channel"

class Chat(SQLModel, table=True):
    id: int = Field(primary_key=True)
    chat_id: int
    type_id: int
    title: Optional[str] = None
    all_members_are_administrators: Optional[bool] = None

class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_bot: bool = False
    language_code: Optional[str] = None

class Message(SQLModel, table=True):
    id: int = Field(primary_key=True, autoincrement=True)
    message_id: int
    chat_id: int = Field(foreign_key="chat.id")
    from_user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    date: int
    text: Optional[str] = None
    reply_to_message_id: Optional[int] = None
    channel_chat_created: bool = False
    delete_chat_photo: bool = False
    group_chat_created: bool = False
    supergroup_chat_created: bool = False

# Database setup
DATABASE_URL = "sqlite:///./messages.db"
engine = create_engine(DATABASE_URL)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)

def get_messages_last_7_days(chat_id: int) -> List[Message]:
    """Fetch messages from the last 7 days for a specific chat."""
    with Session(engine) as session:
        seven_days_ago = int((datetime.now() - timedelta(days=7)).timestamp())
        messages = (
            session.query(Message)
            .filter(
                Message.chat_id == chat_id,
                Message.date > seven_days_ago
            )
            .order_by(Message.date)
            .all()
        )
        return messages
