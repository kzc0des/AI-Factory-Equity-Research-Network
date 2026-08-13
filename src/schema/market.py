from pydantic import BaseModel, Field

class MarketMappingResult(BaseModel):
    """
    Schema for the Market Mapping Agent output.
    """
    ai_factory_role: str = Field(
        description="The primary AI Factory role: Compute, Networking, Power, Cooling, or Construction."
    )
    is_hyperscaler: bool = Field(
        description="True if the company is a builder/spender (e.g., MSFT, GOOG) rather than a picks and shovels provider."
    )
