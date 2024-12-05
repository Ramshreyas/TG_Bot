# Telegram Group Summarization Bot

A Telegram bot that summarizes group chat messages using local AI model (Ollama).

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file and add your Telegram bot token:
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

3. Run the bot:
```bash
python bot.py
```

## Features

- `/start` - Introduces the bot
- `/summarize` - Summarizes last 7 days of messages in the group (coming soon)

## Usage

1. Add the bot to your Telegram group
2. Grant necessary permissions
3. Use `/summarize` command to get message summaries
