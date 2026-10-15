from openai import OpenAI
from ..config import settings
from .prompt_service import load_prompt

client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None


def generate_reply(conversation_history: list[dict]) -> str:
    system_prompt = load_prompt("system_prompt.txt")
    assistant_rules = load_prompt("assistant_rules.txt")

    if client is None:
        return (
            "Mira is running in demo mode because no OPENAI_API_KEY was found. "
            "Add your API key in backend/.env to enable live AI replies."
        )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "system", "content": assistant_rules},
        *conversation_history,
    ]

    response = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=messages,
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()
