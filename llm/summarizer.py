# llm/summarizer.py (modified)
import os
import openai
from llm.prompts.summarize_prompt import PROMPT

def summarize_messages(messages):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Include the username or first_name along with the message text
    messages_text = "\n".join(
        f"{(msg.from_user.username or msg.from_user.first_name)}: {msg.text}"
        for msg in messages if msg.text
    )

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": messages_text}
        ],
        max_tokens=300,
        temperature=0.7
    )

    summary = response.choices[0].message.content.strip()
    return summary
