from typing import List, Annotated, TypedDict, Any, Dict
import operator

from src.schema.company import CompanyProfile

class ParentState(TypedDict):
    """
    The state for the parent orchestrator graph.
    """
    # The input list of raw companies (seed list)
    seed_list: List[Dict[str, Any]]
    
    # The reduced (aggregated) list of processed CompanyProfiles
    profiles: Annotated[List[CompanyProfile], operator.add]
    
    # The final sorted Top 20 list
    top_20: List[CompanyProfile]
