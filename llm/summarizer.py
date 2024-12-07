# llm/summarizer.py (modified)
import os
import openai
from llm.prompts.summarize_prompt import PROMPT

def summarize_messages(messages):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    messages_text = "\n".join(msg.text for msg in messages if msg.text)

    # Use ChatCompletion with the latest openai client version
    response = openai.chat.completions.create(
        model="gpt-4",  # Assuming 'o1' is a valid model name
        messages=[
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": messages_text}
        ],
        max_tokens=300,
        temperature=0.7
    )

    summary = response.choices[0].message.content.strip()
    return summary
