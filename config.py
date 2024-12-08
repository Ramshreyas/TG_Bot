import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get bot token from environment
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
