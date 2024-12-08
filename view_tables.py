from sqlmodel import Session, select
from db import engine, Chat, User, Message, ChatType, Summary

def view_tables():
    with Session(engine) as session:
        # View Chats
        print("\n=== Chats ===")
        chats = session.exec(select(Chat)).all()
        for chat in chats:
            print(f"ID: {chat.id}, Chat ID: {chat.chat_id}, Title: {chat.title}, Type ID: {chat.type_id}")

        # View Messages
        print("\n=== Messages ===")
        messages = session.exec(select(Message)).all()
        for msg in messages:
            print(f"ID: {msg.id}, Message ID: {msg.message_id}, Text: {msg.text[:50]}...")

        # View Users
        print("\n=== Users ===")
        users = session.exec(select(User)).all()
        for user in users:
            print(f"ID: {user.id}, Username: {user.username}, First Name: {user.first_name}")

        # View Summaries
        print("\n=== Summaries ===")
        summaries = session.exec(select(Summary)).all()
        for summary in summaries:
            print(f"ID: {summary.id}, Chat ID: {summary.chat_id}, Summary: {summary.summary_text[:50]}...")

def get_chat_names():
    """Get a list of all chat titles/names with their IDs."""
    with Session(engine) as session:
        chats = session.exec(select(Chat)).all()
        return [(chat.chat_id, chat.title or f"Chat {chat.chat_id}") for chat in chats]

if __name__ == "__main__":
    # Print all tables
    view_tables()
    
    # Print just chat names
    print("\n=== Chat Names ===")
    for chat_id, name in get_chat_names():
        print(f"Chat ID: {chat_id}, Name: {name}")
