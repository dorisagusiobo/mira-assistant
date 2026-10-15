from openai import OpenAI, OpenAIError
from ..config import settings
from .prompt_service import load_prompt

client = (
    OpenAI(api_key=settings.OPENAI_API_KEY, base_url=settings.OPENAI_BASE_URL or None, timeout=30)
    if settings.OPENAI_API_KEY
    else None
)


class LLMUnavailableError(Exception):
    """The AI provider could not return a usable reply."""


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

    try:
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
            temperature=0.7,
        )
    except OpenAIError as error:
        raise LLMUnavailableError(str(error)) from error

    content = response.choices[0].message.content if response.choices else None
    if not content or not content.strip():
        raise LLMUnavailableError("The AI provider returned an empty reply")
    return content.strip()
