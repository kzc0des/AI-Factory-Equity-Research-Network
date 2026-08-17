import os
from typing import Any, Dict, cast
from pydantic import SecretStr
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

import json
from src.schema.company import CompanyProfile
from src.schema.moat import MoatCriteria
from src.agents.utils import get_llm, is_demo_mode

def calculate_moat_score(criteria: MoatCriteria) -> float:
    """
    Calculates the overall 0-5 moat score based on the boolean criteria.
    Currently, this simply sums the 4 boolean values.
    """
    score = 0.0
    if criteria.has_architectural_lock_in:
        score += 1.0
    if criteria.has_ecosystem_dominance:
        score += 1.0
    if criteria.has_high_switching_costs:
        score += 1.0
    if criteria.has_scarcity_or_bottleneck:
        score += 1.0
    
    # Scale from max 4.0 to max 5.0
    return score * 1.25

def moat_analysis_node(state: CompanyProfile) -> Dict[str, Any]:
    """
    LangGraph node to evaluate a company's moat using an LLM.
    
    Args:
        state: The current CompanyProfile state.
        
    Returns:
        A dictionary containing the partial state updates (moat_score).
    """
    if is_demo_mode():
        cache_path = os.path.join("data", "llm_cache", f"{state.ticker}.json")
        if os.path.exists(cache_path):
            try:
                with open(cache_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return {"moat_score": data.get("moat_score")}
            except Exception:
                pass
        return {"moat_score": None}

    llm = get_llm()
    
    structured_llm = llm.with_structured_output(MoatCriteria)
    
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are an expert equity research analyst specializing in the AI Factory supply chain. "
            "Your task is to evaluate a company's economic moat based on its profile. "
            "Evaluate the company against the 4 distinct boolean criteria and return the structured JSON output."
        ),
        (
            "human",
            "Evaluate the moat for the following company:\n"
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
        
        criteria = cast(MoatCriteria, raw_result)
        
        score = calculate_moat_score(criteria)
        return {"moat_score": score}
        
    except Exception as e:
        # Fallback or error handling
        # In a real environment, we'd log this exception
        return {"moat_score": None}
