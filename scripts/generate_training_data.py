import os
import json
from typing import List, Dict, Any

# Ensure we can import from src
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.agents.ingestion import SEED_LIST, filter_companies
from src.agents.utils import get_llm
from src.schema.moat import MoatCriteria
from src.schema.growth import GrowthExtraction
from src.schema.risk import RiskExtraction
from src.schema.market import MarketMappingResult

def get_live_api_configured() -> bool:
    """
    Returns True if a real Gemini or OpenAI API key is configured.
    """
    gemini_key = os.environ.get("GEMINI_API_KEY", "")
    openai_key = os.environ.get("OPENAI_API_KEY", "")
    
    # Check for placeholder strings or empty keys
    if gemini_key and "your_gemini_api_key" not in gemini_key and gemini_key.strip():
        return True
    if openai_key and "your_openai_api" not in openai_key and openai_key.strip():
        return True
    return False

def generate_moat_criteria_from_score(score: float) -> Dict[str, bool]:
    """
    Translates a 0-5 moat score back to MoatCriteria booleans.
    """
    # Each True boolean contributes 1.25 to the score (max 5.0)
    count = round(score / 1.25)
    return {
        "has_architectural_lock_in": count >= 1,
        "has_ecosystem_dominance": count >= 2,
        "has_high_switching_costs": count >= 3,
        "has_scarcity_or_bottleneck": count >= 4
    }

def main():
    print("Initializing Training Dataset Generation...")
    
    # Temp remove tunnel URL so get_llm calls the actual APIs for dataset generation
    colab_tunnel = os.environ.pop("COLAB_TUNNEL_URL", None)
    
    use_live_api = get_live_api_configured()
    if use_live_api:
        print("Using LIVE API to generate gold-standard training data...")
        llm = get_llm()
    else:
        print("Valid API key not detected or placeholder found. Falling back to OFFLINE mode using cached profiles...")
        llm = None
        
    valid_companies = filter_companies(SEED_LIST)
    print(f"Loaded {len(valid_companies)} target companies from Seed List.")
    
    dataset: List[Dict[str, Any]] = []
    
    for idx, company in enumerate(valid_companies):
        ticker = company.ticker
        name = company.company_name
        role = company.ai_factory_role or "Unknown"
        is_hyperscaler = company.is_hyperscaler
        
        print(f"\n[{idx+1}/{len(valid_companies)}] Processing {name} ({ticker})...")
        
        # Load transcript if exists
        transcript_content = ""
        transcript_path = os.path.join("data", "transcripts", f"{ticker}.txt")
        if os.path.exists(transcript_path):
            with open(transcript_path, "r", encoding="utf-8") as f:
                transcript_content = f.read()
        else:
            # Fallback mock transcript
            transcript_content = (
                f"Recent 10-K and Earnings Call Transcript for {ticker}:\n"
                f"Management guides/expects revenue to grow at a 3-year CAGR of 15.0%."
            )
            
        # Load cache for offline mapping
        cache_path = os.path.join("data", "llm_cache", f"{ticker}.json")
        cached_data = {}
        if os.path.exists(cache_path):
            with open(cache_path, "r", encoding="utf-8") as f:
                cached_data = json.load(f)
                
        # 1. Market Mapping Task
        market_sys = (
            "You are an expert equity research analyst specializing in the AI Factory supply chain. "
            "Your task is to categorize a company's AI Factory spend across different infrastructure layers. "
            "Categorize the company by where they monetize AI Factory spend, choosing from: "
            "Compute, Networking, Power, Cooling, Construction. "
            "Also determine if the company is a hyperscaler (builder/spender, e.g., Microsoft, Google, Meta, Amazon) "
            "rather than a picks and shovels provider."
        )
        market_user = f"Categorize the following company:\nTicker: {ticker}\nCompany Name: {name}"
        
        market_ans = None
        if use_live_api and llm:
            try:
                chain = llm.with_structured_output(MarketMappingResult)
                res = chain.invoke(market_user)
                market_ans = res.model_dump_json()
            except Exception as e:
                print(f"Market Mapping live API call failed: {e}")
                # We will fall back to cache for this ticker
        
        if not market_ans:
            market_ans = json.dumps({
                "ai_factory_role": cached_data.get("ai_factory_role", role),
                "is_hyperscaler": cached_data.get("is_hyperscaler", is_hyperscaler)
            })
            
        dataset.append({
            "messages": [
                {"role": "system", "content": market_sys},
                {"role": "user", "content": market_user},
                {"role": "assistant", "content": market_ans}
            ]
        })
        
        # 2. Moat Analysis Task
        moat_sys = (
            "You are an expert equity research analyst specializing in the AI Factory supply chain. "
            "Your task is to evaluate a company's economic moat based on its profile. "
            "Evaluate the company against the 4 distinct boolean criteria and return the structured JSON output."
        )
        moat_user = (
            f"Evaluate the moat for the following company:\n"
            f"Ticker: {ticker}\n"
            f"Company Name: {name}\n"
            f"AI Factory Role: {role}\n"
            f"Is Hyperscaler: {is_hyperscaler}"
        )
        
        moat_ans = None
        if use_live_api and llm:
            try:
                chain = llm.with_structured_output(MoatCriteria)
                res = chain.invoke(moat_user)
                moat_ans = res.model_dump_json()
            except Exception as e:
                print(f"Moat Analysis live API call failed: {e}")
                
        if not moat_ans:
            moat_score = cached_data.get("moat_score", 3.0)
            moat_ans = json.dumps(generate_moat_criteria_from_score(moat_score))
            
        dataset.append({
            "messages": [
                {"role": "system", "content": moat_sys},
                {"role": "user", "content": moat_user},
                {"role": "assistant", "content": moat_ans}
            ]
        })
        
        # 3. Growth Forecast Task
        growth_sys = (
            "You are an expert financial analyst. Your task is to extract a definitive 3-year "
            "Compound Annual Growth Rate (CAGR) percentage from the provided financial documents. "
            "Focus specifically on stated backlog growth and management guidance. "
            "Provide the cagr_3yr as a float representing a percentage (e.g. 15.5 for 15.5%). "
            "If a range is given, you may use the midpoint."
        )
        growth_user = f"Company: {name} ({ticker})\n\nFinancial Documents:\n{transcript_content}"
        
        growth_ans = None
        if use_live_api and llm:
            try:
                chain = llm.with_structured_output(GrowthExtraction)
                res = chain.invoke(growth_user)
                growth_ans = res.model_dump_json()
            except Exception as e:
                print(f"Growth Forecast live API call failed: {e}")
                
        if not growth_ans:
            growth_ans = json.dumps({
                "cagr_3yr": float(cached_data.get("growth_cagr", 15.0))
            })
            
        dataset.append({
            "messages": [
                {"role": "system", "content": growth_sys},
                {"role": "user", "content": growth_user},
                {"role": "assistant", "content": growth_ans}
            ]
        })
        
        # 4. Risk Adjustment Task
        risk_sys = (
            "You are an expert equity research analyst specializing in the AI Factory supply chain. "
            "Your task is to identify the key risks for a company based on its profile. "
            "Evaluate if the company has 'execution', 'cyclicality', or 'customer concentration' risks. "
            "Return the list of identified risks."
        )
        risk_user = (
            f"Evaluate the risks for the following company:\n"
            f"Ticker: {ticker}\n"
            f"Company Name: {name}\n"
            f"AI Factory Role: {role}\n"
            f"Is Hyperscaler: {is_hyperscaler}"
        )
        
        risk_ans = None
        if use_live_api and llm:
            try:
                chain = llm.with_structured_output(RiskExtraction)
                res = chain.invoke(risk_user)
                risk_ans = res.model_dump_json()
            except Exception as e:
                print(f"Risk Adjustment live API call failed: {e}")
                
        if not risk_ans:
            risk_list = cached_data.get("risks", [])
            risk_ans = json.dumps({
                "risks": risk_list
            })
            
        dataset.append({
            "messages": [
                {"role": "system", "content": risk_sys},
                {"role": "user", "content": risk_user},
                {"role": "assistant", "content": risk_ans}
            ]
        })

    # Save to data/colab_training_dataset.jsonl
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "colab_training_dataset.jsonl")
    
    with open(output_path, "w", encoding="utf-8") as f:
        for item in dataset:
            f.write(json.dumps(item) + "\n")
            
    print(f"\nSuccess! Generated {len(dataset)} examples and saved to {output_path}.")
    
    # Restore the tunnel URL if it was set
    if colab_tunnel:
        os.environ["COLAB_TUNNEL_URL"] = colab_tunnel

if __name__ == "__main__":
    main()
