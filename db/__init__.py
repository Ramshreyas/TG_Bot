# db/__init__.py
import os
from sqlmodel import SQLModel, create_engine
from .models import ChatType, Chat, User, Message, Update, Summary, BotUser
from .database import init_db, get_session, engine


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")

engine = create_engine(DATABASE_URL, echo=False)

def init_db():
    SQLModel.metadata.create_all(engine)


__all__ = ['ChatType', 'Chat', 'User', 'Message', 'Update', 'Summary', 'BotUser','init_db', 'get_session', 'engine']
