import os
from typing import Any, Dict, cast
from pydantic import SecretStr
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from src.schema.company import CompanyProfile, Risk
from src.schema.risk import RiskExtraction
from src.agents.utils import get_llm, is_demo_mode, load_cached_llm_profile

def risk_adjustment_node(state: CompanyProfile) -> Dict[str, Any]:
    """
    LangGraph node to evaluate a company's risks using an LLM.
    
    Args:
        state: The current CompanyProfile state.
        
    Returns:
        A dictionary containing the partial state updates (risks).
    """
    if is_demo_mode():
        data = load_cached_llm_profile(state.ticker)
        if data:
            risks_str = data.get("risks", [])
            return {"risks": [Risk(r) for r in risks_str]}
        return {"risks": []}

    llm = get_llm()
    
    structured_llm = llm.with_structured_output(RiskExtraction)
    
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are an expert equity research analyst specializing in the AI Factory supply chain. "
            "Your task is to identify the key risks for a company based on its profile. "
            "Evaluate if the company has 'execution', 'cyclicality', or 'customer concentration' risks. "
            "Return the list of identified risks."
        ),
        (
            "human",
            "Evaluate the risks for the following company:\n"
            "Ticker: {ticker}\n"
            "Company Name: {company_name}\n"
            "AI Factory Role: {ai_factory_role}\n"
            "Is Hyperscaler: {is_hyperscaler}\n"
        )
    ])
    
    chain = prompt | structured_llm
    
    try:
        raw_result = chain.invoke({
            "ticker": state.ticker,
            "company_name": state.company_name,
            "ai_factory_role": state.ai_factory_role or "Unknown",
            "is_hyperscaler": state.is_hyperscaler,
        })
        
        extraction = cast(RiskExtraction, raw_result)
        
        return {"risks": extraction.risks}
        
    except Exception as e:
        return {"risks": []}
