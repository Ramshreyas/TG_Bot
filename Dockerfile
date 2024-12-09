# Dockerfile
FROM python:3.11.4-slim

# Set work directory
WORKDIR /app

# Install system dependencies needed for psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt /app/requirements.txt

# Install dependencies (including psycopg2)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot code
COPY . /app

# Set environment variables
ENV DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/postgres

# Run the bot
CMD ["python", "bot.py"]