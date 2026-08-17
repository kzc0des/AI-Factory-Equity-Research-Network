from typing import Any, Dict, Optional
import logging
import os
import json
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import yfinance as yf # type: ignore

logger = logging.getLogger(__name__)

from src.schema.company import CompanyProfile
from src.agents.utils import is_demo_mode

class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = kwargs.pop("timeout", 10)
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        kwargs.setdefault("timeout", self.timeout)
        return super().send(request, **kwargs)

def get_resilient_session() -> requests.Session:
    """
    Creates a requests session with retries, custom user-agent headers, and a default timeout.
    """
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    })
    # Retry on rate limiting (429) and standard server errors with exponential backoff
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        raise_on_status=False
    )
    adapter = TimeoutHTTPAdapter(timeout=10, max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

def normalize_margin_score(margin: float) -> int:
    """
    Normalizes the operating margin to a 1-5 score.
    
    Mapping based on PROJECT_SPEC.md:
    > 40% : 5
    30% - 40% : 4
    20% - 30% : 3
    10% - 20% : 2
    < 10% : 1
    """
    if margin > 40:
        return 5
    elif margin >= 30:
        return 4
    elif margin >= 20:
        return 3
    elif margin >= 10:
        return 2
    else:
        return 1

def fetch_operating_margin(ticker: str) -> Optional[float]:
    """
    Fetches the TTM operating margin for a given ticker.
    If DEMO_MODE is True, loads from the local cached file (data/financials.json).
    Otherwise, queries yfinance using a resilient HTTP session.
    
    Returns the margin as a percentage (e.g., 25.5 for 25.5%).
    Returns None if the data is unavailable.
    """
    if is_demo_mode():
        cache_path = os.path.join("data", "financials.json")
        if os.path.exists(cache_path):
            try:
                with open(cache_path, "r") as f:
                    data = json.load(f)
                margin = data.get(ticker)
                if margin is not None:
                    return float(margin)
            except Exception as e:
                logger.error(f"Error reading financials cache for {ticker}: {e}")
        return None

    try:
        session = get_resilient_session()
        stock = yf.Ticker(ticker, session=session)
        # yfinance typically returns operatingMargins as a decimal (e.g. 0.255)
        margin_decimal = stock.info.get("operatingMargins")
        
        if margin_decimal is not None:
            return margin_decimal * 100.0
            
    except Exception as e:
        logger.error(f"Error fetching operating margin for {ticker}: {e}")
        
    return None

def margin_analysis_node(state: CompanyProfile) -> Dict[str, Any]:
    """
    LangGraph node to fetch and score the operating margin for a company.
    
    Args:
        state: The current CompanyProfile state.
        
    Returns:
        A dictionary containing the partial state updates (operating_margin and margin_score).
    """
    margin = fetch_operating_margin(state.ticker)
    
    score = None
    if margin is not None:
        score = normalize_margin_score(margin)
        
    return {
        "operating_margin": margin,
        "margin_score": score
    }

