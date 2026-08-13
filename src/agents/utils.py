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
