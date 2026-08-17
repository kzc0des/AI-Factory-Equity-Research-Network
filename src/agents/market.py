import os
from typing import Any, Dict, cast
from pydantic import SecretStr
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from src.schema.company import CompanyProfile
from src.schema.market import MarketMappingResult
from src.agents.utils import get_llm, is_demo_mode, load_cached_llm_profile

def market_mapping_node(state: CompanyProfile) -> Dict[str, Any]:
    """
    LangGraph node to map a company to its AI Factory infrastructure layer.
    
    Args:
        state: The current CompanyProfile state.
        
    Returns:
        A dictionary containing the partial state updates (ai_factory_role, is_hyperscaler).
    """
    if is_demo_mode():
        data = load_cached_llm_profile(state.ticker)
        if data:
            return {
                "ai_factory_role": data.get("ai_factory_role"),
                "is_hyperscaler": data.get("is_hyperscaler", False),
            }
        return {
            "ai_factory_role": None,
            "is_hyperscaler": False,
        }

    llm = get_llm()
    
    structured_llm = llm.with_structured_output(MarketMappingResult)
    
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are an expert equity research analyst specializing in the AI Factory supply chain. "
            "Your task is to categorize a company's AI Factory spend across different infrastructure layers. "
            "Categorize the company by where they monetize AI Factory spend, choosing from: "
            "Compute, Networking, Power, Cooling, Construction. "
            "Also determine if the company is a hyperscaler (builder/spender, e.g., Microsoft, Google, Meta, Amazon) "
            "rather than a picks and shovels provider."
        ),
        (
            "human",
            "Categorize the following company:\n"
            "Ticker: {ticker}\n"
            "Company Name: {company_name}\n"
        )
    ])
    
    chain = prompt | structured_llm
    
    try:
        raw_result = chain.invoke({
            "ticker": state.ticker,
            "company_name": state.company_name,
        })
        
        result = cast(MarketMappingResult, raw_result)
        
        return {
            "ai_factory_role": result.ai_factory_role,
            "is_hyperscaler": result.is_hyperscaler,
        }
        
    except Exception as e:
        # Fallback or error handling
        return {
            "ai_factory_role": None,
            "is_hyperscaler": False,
        }
