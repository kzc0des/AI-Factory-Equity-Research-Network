from typing import Any, Dict, Optional
import yfinance # type: ignore

from src.schema.company import CompanyProfile

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
    Fetches the TTM operating margin for a given ticker using yfinance.
    Returns the margin as a percentage (e.g., 25.5 for 25.5%).
    Returns None if the data is unavailable.
    """
    try:
        stock = yfinance.Ticker(ticker)
        # yfinance typically returns operatingMargins as a decimal (e.g. 0.255)
        margin_decimal = stock.info.get("operatingMargins")
        
        if margin_decimal is not None:
            return margin_decimal * 100.0
            
    except Exception as e:
        # In a real environment, we'd log this exception
        pass
        
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
