from sqlmodel import SQLModel, Session, create_engine
from typing import Generator
import os
from .models import ChatType, Chat, User, Message, Update, Subscriber

# Create SQLite database URL
DATABASE_URL = "sqlite:///telegram_bot.db"

# Create SQLite engine
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False},
    echo=True  # Set to False in production
)

def init_db(drop_tables=False) -> None:
    """Initialize the database and create tables."""
    if drop_tables:
        SQLModel.metadata.drop_all(engine)
    
    # Create tables if they don't exist
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """Get a database session."""
    with Session(engine) as session:
        yield session
