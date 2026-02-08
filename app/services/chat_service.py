import os
from openai import AsyncOpenAI

client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")  # groq/qwen compatible
)

MODEL = os.getenv("OPENAI_MODEL", "llama-3.1-8b-instant")

async def chat_with_ai(user_message: str) -> str:
    response = await client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful Todo AI assistant."},
            {"role": "user", "content": user_message}
        ]
    )

    return response.choices[0].message.content
