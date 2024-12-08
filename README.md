# Telegram Summarization Bot

This project is a Telegram bot that summarizes messages from groups. It uses OpenAI's GPT models to generate concise summaries of recent messages. It also includes access control for which users can generate summaries.

## Features

- **Start Command**:  
  `/start` - Introduces the bot and informs the user how to generate summaries and how to contact the first admin for whitelist access.

- **Summarize Command**:  
  `/summarize <group name>` - Generates a summary of the last 3 days of messages for the specified group. If a summary was created in the last 30 minutes, it returns the cached summary from the database. Otherwise, it generates a new summary via OpenAI’s API and stores it in the database.

- **Access Control**:  
  The bot uses a whitelist system to determine which users can run the `/summarize` command. Only users in the `BotUser` table are allowed to generate summaries. Admin users can add or remove other admins and regular users.

- **User Management Commands** (Admin only):
  - `/addadmin <username>`
  - `/removeadmin <username>`
  - `/adduser <username>`
  - `/removeuser <username>`

- **Database Integration**:  
  Uses `sqlmodel` to store chats, messages, summaries, and bot users. Summaries are persisted with timestamps, and messages are logged to maintain a history.

- **OpenAI Integration**:  
  Uses OpenAI's GPT models to summarize chat messages. The model is accessed via the OpenAI API, and the prompt is stored separately. The summarizer includes usernames alongside messages to improve summary quality.

## Project Structure

- **bot.py**  
  Entry point of the application. Sets up the Telegram handlers and runs the bot.

- **handlers/**  
  Contains various handler files for different commands and logic:
  - `start.py`: Handles the `/start` command. Informs the user about the bot and how to contact the first admin to get whitelisted.
  - `summarize.py`: Handles the `/summarize` command. Checks for recent summaries in the DB and generates new summaries if needed.
  - `message.py`: Handles incoming group messages and stores them in the DB.
  - `user_management.py`: Handles `/addadmin`, `/removeadmin`, `/adduser`, and `/removeuser` commands, restricted to admin users.

- **llm/**  
  Contains code related to the Large Language Model (LLM) usage:
  - `summarizer.py`: Implements `summarize_messages` which queries the OpenAI API to summarize chat messages.
  - `prompts/summarize_prompt.py`: Defines the `PROMPT` constant for the summarizer.

- **db/**  
  Contains database initialization and model definitions:
  - `models.py`: Defines `Chat`, `Message`, `Summary`, `BotUser`, `ChatType`, `User`, `Update`, and `Subscriber`.

- **add_admin.py**  
  A command-line utility to add an admin user to the system without using Telegram commands.

- **.env**  
  Contains environment variables such as `TELEGRAM_BOT_TOKEN` and `OPENAI_API_KEY`.

## Setup

1. **Clone the repository**:  
   `git clone https://github.com/yourusername/telegram-summarization-bot.git`  
   `cd telegram-summarization-bot`

2. **Create and activate a virtual environment**:  
   `python3 -m venv venv`  
   `source venv/bin/activate`

3. **Install dependencies**:  
   `pip install -r requirements.txt`

4. **Set up environment variables**:  
   Create a `.env` file:  

    TELEGRAM_BOT_TOKEN=your_telegram_bot_token 
    OPENAI_API_KEY=your_openai_api_key

5. **Initialize the Database**:  
Ensure your database URL is configured in the code or environment. Run the bot once to create tables (assuming `init_db()` sets up the schema):  
`python bot.py`

After this, use:  
`python add_admin.py <username>`  
to add your first admin user.

## Usage

1. **Run the bot**:  
`python bot.py`

2. **In Telegram**:
- Start a conversation with the bot using `/start`.
- Have an admin add you as a user with `/adduser <yourusername>`.
- Use `/summarize <group name>` to get summaries of recent messages.

3. **User Management** (Admin only):
- `/addadmin <username>`
- `/removeadmin <username>`
- `/adduser <username>`
- `/removeuser <username>`

4. **Summarizing Messages**:
- When you run `/summarize <group name>`, the bot checks if it has summarized this group in the last 30 minutes.
- If yes, it returns the cached summary.
- If not, it fetches the last 3 days of messages, calls the OpenAI API to summarize them, stores the summary in the DB, and returns it.

## Notes

- Make sure your bot is configured to read group messages if needed. If the bot doesn't receive messages in groups, disable privacy mode via BotFather.
- The summarization depends on a working OpenAI API key and internet access.
- Adjust the OpenAI model, prompt, tokens, and temperature as needed.

## Contributing

- Pull requests and feature requests are welcome.
- Please ensure code quality and consistency before submitting a PR.

## License

This project is licensed under the MIT License. See `LICENSE` for more details.

