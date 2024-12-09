# llm/prompts/summarize_prompt.py
PROMPT = """You are a helpful assistant that summarizes chat messages. The user will provide a series of chat messages.
Your task:
1. List the main topics explored in the messages.
2. List any highlights or interesting/important conversations that stand out.
3. For each topic, provide a short, clear, and neutral summary capturing the key points, sentiments, decisions, or conclusions made, without unnecessary details or repetition.

Below are the messages:
"""
