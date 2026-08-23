import os
import json
from typing import List, Dict, Any
from src.schema.company import CompanyProfile

def _load_seed_list() -> List[Dict[str, Any]]:
    # Locate data/seed_list.json relative to the root directory
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    json_path = os.path.join(base_dir, "data", "seed_list.json")
    
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
            
    # Minimal fallback list if file doesn't exist
    return [
        {
            "ticker": "MSFT",
            "company_name": "Microsoft Corporation",
            "is_hyperscaler": True,
        },
        {
            "ticker": "GOOGL",
            "company_name": "Alphabet Inc.",
            "is_hyperscaler": True,
        },
        {
            "ticker": "AAPL",
            "company_name": "Apple Inc.",
            "ai_factory_role": None,
            "is_hyperscaler": True,
        },
        {
            "ticker": "NVDA",
            "company_name": "NVIDIA Corporation",
            "ai_factory_role": "Compute",
            "is_hyperscaler": False,
        },
        {
            "ticker": "ANET",
            "company_name": "Arista Networks, Inc.",
            "ai_factory_role": "Networking",
            "is_hyperscaler": False,
        },
        {
            "ticker": "CEG",
            "company_name": "Constellation Energy Corporation",
            "ai_factory_role": "Power",
            "is_hyperscaler": False,
        },
        {
            "ticker": "VRT",
            "company_name": "Vertiv Holdings Co.",
            "ai_factory_role": "Cooling",
            "is_hyperscaler": False,
        },
        {
            "ticker": "ACM",
            "company_name": "AECOM",
            "ai_factory_role": "Construction",
            "is_hyperscaler": False,
        }
    ]

SEED_LIST: List[Dict[str, Any]] = _load_seed_list()

def filter_companies(seed_list: List[Dict[str, Any]]) -> List[CompanyProfile]:
    """
    Filters the seed list to remove hyperscalers and zero-exposure companies,
    and initializes CompanyProfile objects.
    
    Args:
        seed_list: A list of dictionaries containing raw company data.
        
    Returns:
        A list of initialized CompanyProfile objects representing valid targets.
    """
    valid_targets = []
    for company_data in seed_list:
        if not company_data.get("is_hyperscaler", False):
            # Also require an AI factory role to ensure they aren't zero-exposure
            if company_data.get("ai_factory_role"):
                valid_targets.append(CompanyProfile(**company_data))
                
    return valid_targets
