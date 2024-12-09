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

## Deployment with Docker

### Requirements
- Docker
- Docker Compose

### Steps

1. **Set Up Environment Variables**:
   Create a `.env` file:

``` bash
TELEGRAM_BOT_TOKEN=your_telegram_bot_token 
OPENAI_API_KEY=your_openai_api_key
```

2. **Build and Run the Containers**:
Use `docker-compose` to build and run the bot and the Postgres database:

```bash
docker-compose up --build
```

This command will:
- Build the Docker image for the bot.
- Start a Postgres database container.
- Wait for the database to become healthy.
- Start the bot container, which connects to the database and initializes it.

3. **Persisting Data**:
   The `docker-compose.yml` file includes a named volume `pgdata` to store Postgres data. This ensures that your data (chats, messages, summaries, and user information) is preserved even if the containers are stopped or removed.
   
   To further ensure data safety:
   - Regularly back up the `pgdata` volume using `docker cp` or `pg_dump`.
   - For production environments, consider off-site backups or replication for disaster recovery.

4. **Adding the First Admin**:
Once the containers are running, you can create your first admin user by executing:
```bash
  docker-compose exec bot python add_admin.py <username>
```

Using the Bot:

- Start a conversation with your Telegram bot using /start
- Ask the admin shown in the /start response to add you as a user
- Now you can request summaries with /summarize <group name>