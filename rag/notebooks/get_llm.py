import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Prefer the dedicated package; fallback keeps compatibility with older installs.
try:
    from langchain_ollama import ChatOllama
except ImportError:
    from langchain_community.chat_models import ChatOllama


load_dotenv()


def get_llm(provider: str = "openai"):
    provider = provider.strip().lower()

    if provider == "openai":
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError(
                "OPENAI_API_KEY not found. Add it to your .env before using provider='openai'."
            )
        return ChatOpenAI(model="gpt-4o-mini", temperature=0)

    if provider == "ollama":
        return ChatOllama(model="gemma2:2b", temperature=0)

    raise ValueError("Unsupported provider. Use 'openai' or 'ollama'.")
