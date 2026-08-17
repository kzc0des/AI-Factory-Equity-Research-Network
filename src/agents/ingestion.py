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
        "ticker": "AAPL",
        "company_name": "Apple Inc.",
        "ai_factory_role": None,
        "is_hyperscaler": True,
    },
    # Compute
    {
        "ticker": "NVDA",
        "company_name": "NVIDIA Corporation",
        "ai_factory_role": "Compute",
        "is_hyperscaler": False,
    },
    {
        "ticker": "AMD",
        "company_name": "Advanced Micro Devices, Inc.",
        "ai_factory_role": "Compute",
        "is_hyperscaler": False,
    },
    {
        "ticker": "SMCI",
        "company_name": "Super Micro Computer, Inc.",
        "ai_factory_role": "Compute",
        "is_hyperscaler": False,
    },
    {
        "ticker": "DELL",
        "company_name": "Dell Technologies Inc.",
        "ai_factory_role": "Compute",
        "is_hyperscaler": False,
    },
    {
        "ticker": "HPE",
        "company_name": "Hewlett Packard Enterprise",
        "ai_factory_role": "Compute",
        "is_hyperscaler": False,
    },
    # Networking
    {
        "ticker": "ANET",
        "company_name": "Arista Networks, Inc.",
        "ai_factory_role": "Networking",
        "is_hyperscaler": False,
    },
    {
        "ticker": "AVGO",
        "company_name": "Broadcom Inc.",
        "ai_factory_role": "Networking",
        "is_hyperscaler": False,
    },
    {
        "ticker": "LITE",
        "company_name": "Lumentum Holdings Inc.",
        "ai_factory_role": "Networking",
        "is_hyperscaler": False,
    },
    {
        "ticker": "COHR",
        "company_name": "Coherent Corp.",
        "ai_factory_role": "Networking",
        "is_hyperscaler": False,
    },
    # Power
    {
        "ticker": "CEG",
        "company_name": "Constellation Energy Corporation",
        "ai_factory_role": "Power",
        "is_hyperscaler": False,
    },
    {
        "ticker": "VST",
        "company_name": "Vistra Corp.",
        "ai_factory_role": "Power",
        "is_hyperscaler": False,
    },
    {
        "ticker": "GE",
        "company_name": "General Electric Company",
        "ai_factory_role": "Power",
        "is_hyperscaler": False,
    },
    {
        "ticker": "ETN",
        "company_name": "Eaton Corporation plc",
        "ai_factory_role": "Power",
        "is_hyperscaler": False,
    },
    # Cooling
    {
        "ticker": "VRT",
        "company_name": "Vertiv Holdings Co.",
        "ai_factory_role": "Cooling",
        "is_hyperscaler": False,
    },
    {
        "ticker": "MOD",
        "company_name": "Modine Manufacturing Company",
        "ai_factory_role": "Cooling",
        "is_hyperscaler": False,
    },
    {
        "ticker": "AAON",
        "company_name": "AAON, Inc.",
        "ai_factory_role": "Cooling",
        "is_hyperscaler": False,
    },
    # Construction
    {
        "ticker": "ACM",
        "company_name": "AECOM",
        "ai_factory_role": "Construction",
        "is_hyperscaler": False,
    },
    {
        "ticker": "J",
        "company_name": "Jacobs Solutions Inc.",
        "ai_factory_role": "Construction",
        "is_hyperscaler": False,
    },
    {
        "ticker": "EME",
        "company_name": "EMCOR Group, Inc.",
        "ai_factory_role": "Construction",
        "is_hyperscaler": False,
    },
    {
        "ticker": "PWR",
        "company_name": "Quanta Services, Inc.",
        "ai_factory_role": "Construction",
        "is_hyperscaler": False,
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
