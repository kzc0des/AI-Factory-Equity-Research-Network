from typing import Any, Dict
from src.schema.company import CompanyProfile, Risk
from src.schema.state import ParentState

def compute_risk_discount(risks: list[Risk]) -> float:
    """
    Computes a risk discount multiplier based on identified risks.
    Base multiplier is 1.0.
    'execution' reduces by 10% (0.9).
    'cyclicality' reduces by 20% (0.8).
    'customer concentration' reduces by 15% (0.85).
    """
    discount = 1.0
    for risk in risks:
        if risk == Risk.EXECUTION:
            discount *= 0.9
        if risk == Risk.CYCLICALITY:
            discount *= 0.8
        if risk == Risk.CUSTOMER_CONCENTRATION:
            discount *= 0.85
    return discount

def compute_tafgs(profile: CompanyProfile) -> float:
    """
    Computes the Total AI Factory Growth Score (TAFGS).
    TAFGS = (Moat * Margin) * Growth * RiskDiscount
    
    If any of the required components are missing, returns 0.0.
    """
    moat = profile.moat_score
    margin = profile.margin_score
    growth = profile.growth_cagr
    
    if moat is None or margin is None or growth is None:
        return 0.0
        
    base_score = (moat * margin) * growth
    discount = compute_risk_discount(profile.risks)
    return base_score * discount

def ranking_node(state: ParentState) -> Dict[str, Any]:
    """
    LangGraph node to reduce completed profiles, compute TAFGS, and sort the Top 20.
    
    Args:
        state: The current ParentState containing the list of processed profiles.
        
    Returns:
        A dictionary updating the top_20 list and any profiles with their final total_score.
    """
    profiles = state.get("profiles", [])
    
    # Compute TAFGS for each profile
    updated_profiles = []
    for profile in profiles:
        if isinstance(profile, dict):
            profile = CompanyProfile(**profile)
        total_score = compute_tafgs(profile)
        discount = compute_risk_discount(profile.risks)
        # Update the profile (create a copy to avoid mutating state directly if using BaseModel)
        profile_dict = profile.model_dump()
        profile_dict["total_score"] = total_score
        profile_dict["risk_discount"] = discount
        updated_profiles.append(CompanyProfile(**profile_dict))
        
    # Sort by total_score descending
    sorted_profiles = sorted(
        updated_profiles, 
        key=lambda x: x.total_score if x.total_score is not None else 0.0, 
        reverse=True
    )
    
    # Select top 20
    top_20 = sorted_profiles[:20]
    
    return {
        "top_20": top_20,
        "profiles": updated_profiles  # Optional: return updated profiles if we want to save them
    }
