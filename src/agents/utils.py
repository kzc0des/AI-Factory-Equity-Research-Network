import os
from pydantic import SecretStr
from langchain_openai import ChatOpenAI

def get_llm(model: str = "gpt-4o", temperature: float = 0) -> ChatOpenAI:
    """
    Returns a configured ChatOpenAI instance.
    """
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        api_key=SecretStr(os.environ.get("OPENAI_API_KEY", "dummy_key"))
    )

def is_demo_mode() -> bool:
    """
    Returns True if DEMO_MODE is set to 'True' (case-insensitive) in the environment.
    """
    return os.environ.get("DEMO_MODE", "False").strip().lower() == "true"

