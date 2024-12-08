# add_admin.py
import sys
import os
from dotenv import load_dotenv
from sqlmodel import Session, select
from db import engine, BotUser

def main():
    load_dotenv()
    if len(sys.argv) < 2:
        print("Usage: python add_admin.py <username>")
        sys.exit(1)

    username = sys.argv[1]

    with Session(engine) as session:
        user = session.exec(select(BotUser).where(BotUser.username == username)).first()
        if user:
            user.is_admin = True
        else:
            user = BotUser(username=username, is_admin=True)
            session.add(user)
        session.commit()
    print(f"{username} is now an admin.")

if __name__ == "__main__":
    main()
