import os
from typing import Any, Dict, cast
from pydantic import SecretStr
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from src.schema.company import CompanyProfile
from src.schema.growth import GrowthExtraction

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
    documents = retrieve_financial_documents(state.ticker)
    
    # In a real environment, we'd ensure OPENAI_API_KEY is set.
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        api_key=SecretStr(os.environ.get("OPENAI_API_KEY", "dummy_key"))
    )
    
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
