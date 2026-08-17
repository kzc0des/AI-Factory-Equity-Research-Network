import os
from pydantic import SecretStr
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables from a local .env file if it exists
load_dotenv()

def get_llm(model: str = "gpt-4o", temperature: float = 0) -> ChatOpenAI:
    """
    Returns a configured ChatOpenAI instance, supporting either OpenAI or Gemini.
    """
    gemini_key = os.environ.get("GEMINI_API_KEY")
    api_key = gemini_key or os.environ.get("OPENAI_API_KEY", "dummy_key")
    model_name = ("gemini-1.5-pro" if "4" in model else "gemini-1.5-flash") if gemini_key else model

    kwargs = {
        "model": model_name,
        "temperature": temperature,
        "api_key": SecretStr(api_key),
    }
    if gemini_key:
        kwargs["base_url"] = "https://generativelanguage.googleapis.com/v1beta/openai/"

    return ChatOpenAI(**kwargs)



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

