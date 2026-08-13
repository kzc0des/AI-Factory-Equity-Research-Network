from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field

class Risk(str, Enum):
    EXECUTION = "execution"
    CYCLICALITY = "cyclicality"
    CUSTOMER_CONCENTRATION = "customer concentration"


class CompanyProfile(BaseModel):
    """
    Represents the state of a single company throughout the LangGraph pipeline.
    """
    ticker: str = Field(description="The stock ticker symbol of the company.")
    company_name: str = Field(description="The full name of the company.")
    ai_factory_role: Optional[str] = Field(
        default=None, 
        description="The company's role in the AI Factory ecosystem (e.g., Compute, Networking, Power, Cooling)."
    )
    is_hyperscaler: bool = Field(
        default=False, 
        description="True if the company is a builder/spender (e.g., MSFT, GOOG) rather than a picks and shovels provider."
    )
    revenue_exposure: Optional[float] = Field(
        default=None,
        description="Revenue exposure to AI Factory builds (% of total revenue)."
    )
    moat_score: Optional[float] = Field(
        default=None, 
        description="Calculated Moat Score (0-5) based on distinct boolean criteria."
    )
    operating_margin: Optional[float] = Field(
        default=None, 
        description="Actual TTM operating margin as a percentage (e.g., 25.5 for 25.5%)."
    )
    margin_score: Optional[int] = Field(
        default=None, 
        description="Normalized Margin Score (1-5)."
    )
    growth_cagr: Optional[float] = Field(
        default=None, 
        description="Forecasted 3-Year CAGR % driven by AI Factory demand."
    )
    total_score: Optional[float] = Field(
        default=None, 
        description="Total AI Factory Growth Score (Moat * Margin * Growth)."
    )
    risks: List[Risk] = Field(
        default_factory=list, 
        description="Key risks identified for this target (e.g., cyclicality, customer concentration)."
    )
    catalysts: List[str] = Field(
        default_factory=list,
        description="Key growth catalysts."
    )
    risk_discount: Optional[float] = Field(
        default=None,
        description="Calculated risk discount factor."
    )
