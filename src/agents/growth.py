import os
from typing import Any, Dict, cast
from pydantic import SecretStr
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

import re
from src.schema.company import CompanyProfile
from src.schema.growth import GrowthExtraction
from src.agents.utils import get_llm, is_demo_mode, load_cached_llm_profile

def retrieve_financial_documents(ticker: str) -> str:
    """
    Simulated document retrieval for SEC filings and earnings call transcripts.
    In a production system, this would use EDGAR or a financial data provider API.
    """
    # Mocked up context based on the ticker
    return (
        f"Recent 10-K and Earnings Call Transcript for {ticker}:\n"
        f"Management guidance indicates a strong demand environment driven by AI Factory builds.\n"
        f"Backlog has grown significantly. We expect our revenue to grow at an annualized rate "
        f"of approximately 15-20% over the next 3 years as AI infrastructure investments accelerate."
    )

def growth_forecast_node(state: CompanyProfile) -> Dict[str, Any]:
    """
    LangGraph node to parse documents and extract a numerical 3-year CAGR forecast.
    
    Args:
        state: The current CompanyProfile state.
        
    Returns:
        A dictionary containing the partial state updates (growth_cagr).
    """
    if is_demo_mode():
        # First try to load from the LLM cache JSON
        data = load_cached_llm_profile(state.ticker)
        if data:
            cagr = data.get("growth_cagr")
            if cagr is not None:
                return {"growth_cagr": float(cagr)}

        # Fallback: load and parse the local transcript file
        transcript_path = os.path.join("data", "transcripts", f"{state.ticker}.txt")
        if os.path.exists(transcript_path):
            try:
                with open(transcript_path, "r", encoding="utf-8") as f:
                    content = f.read()
                # Search for "CAGR of [value]%"
                match = re.search(r"CAGR of (\d+(?:\.\d+)?)%", content, re.IGNORECASE)
                if match:
                    return {"growth_cagr": float(match.group(1))}
            except Exception:
                pass
        return {"growth_cagr": None}

    documents = retrieve_financial_documents(state.ticker)
    
    llm = get_llm()
    
    structured_llm = llm.with_structured_output(GrowthExtraction)
    
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are an expert financial analyst. Your task is to extract a definitive 3-year "
            "Compound Annual Growth Rate (CAGR) percentage from the provided financial documents. "
            "Focus specifically on stated backlog growth and management guidance. "
            "Provide the cagr_3yr as a float representing a percentage (e.g. 15.5 for 15.5%). "
            "If a range is given, you may use the midpoint."
        ),
        (
            "human",
            "Company: {company_name} ({ticker})\n\n"
            "Financial Documents:\n{documents}"
        )
    ])
    
    chain = prompt | structured_llm
    
    try:
        raw_result = chain.invoke({
            "ticker": state.ticker,
            "company_name": state.company_name,
            "documents": documents
        })
        
        extraction = cast(GrowthExtraction, raw_result)
        
        return {"growth_cagr": extraction.cagr_3yr}
        
    except Exception as e:
        # Fallback or error handling
        return {"growth_cagr": None}
