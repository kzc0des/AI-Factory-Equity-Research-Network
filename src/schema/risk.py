from typing import List
from pydantic import BaseModel, Field
from src.schema.company import Risk

class RiskExtraction(BaseModel):
    """
    Extracted list of risks for a company.
    """
    risks: List[Risk] = Field(
        description="List of key risks identified for this target (execution, cyclicality, customer concentration)."
    )
