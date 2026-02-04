import os
from datetime import datetime
from openai import AsyncOpenAI

async def extract_task_from_text(text: str):
    """
    Extract task information from natural language using Groq AI
    """
    client = AsyncOpenAI(
        api_key=os.getenv("GROQ_API_KEY"),
        base_url=os.getenv("GROQ_BASE_URL")
    )
    
    response = await client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You extract structured todo tasks from user messages. Return ONLY valid JSON, no markdown, no explanations."
            },
            {
                "role": "user",
                "content": f"""Convert this into JSON with fields: title (string), description (string, optional)

User message: {text}

Return format: {{"title": "...", "description": "..."}}"""
            }
        ],
        temperature=0.2
    )
    
    content = response.choices[0].message.content.strip()
    
    # Clean markdown code blocks if AI adds them
    if content.startswith("```"):
        lines = content.split("\n")
        content = "\n".join(lines[1:-1])
        if content.startswith("json"):
            content = content[4:].strip()
    
    # Parse and return JSON
    import json
    return json.loads(content)
