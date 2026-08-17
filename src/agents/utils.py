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

import json
from typing import Dict, Any, Optional

def load_cached_llm_profile(ticker: str) -> Optional[Dict[str, Any]]:
    """
    Loads the pre-saved LLM cache profile for a ticker if it exists.
    """
    cache_path = os.path.join("data", "llm_cache", f"{ticker}.json")
    if os.path.exists(cache_path):
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return None

