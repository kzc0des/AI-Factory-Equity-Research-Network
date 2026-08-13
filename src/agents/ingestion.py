from typing import List, Dict, Any
from src.schema.company import CompanyProfile

# A static seed list of companies to evaluate.
# Note: In a real scenario, this would likely be loaded from a database or a larger static file.
SEED_LIST: List[Dict[str, Any]] = [
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
        "ticker": "NVDA",
        "company_name": "NVIDIA Corporation",
        "ai_factory_role": "Compute",
        "is_hyperscaler": False,
    },
    {
        "ticker": "ANET",
        "company_name": "Arista Networks",
        "ai_factory_role": "Networking",
        "is_hyperscaler": False,
    },
    {
        "ticker": "VRT",
        "company_name": "Vertiv Holdings",
        "ai_factory_role": "Power and Cooling",
        "is_hyperscaler": False,
    },
    {
        "ticker": "CEG",
        "company_name": "Constellation Energy",
        "ai_factory_role": "Power Infrastructure",
        "is_hyperscaler": False,
    },
    {
        "ticker": "AAPL",
        "company_name": "Apple Inc.",
        "ai_factory_role": None, # Zero-exposure or tech giant
        "is_hyperscaler": True, # Treating as hyperscaler/builder for this context
    }
]

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
