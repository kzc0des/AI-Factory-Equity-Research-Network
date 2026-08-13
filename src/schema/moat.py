from pydantic import BaseModel, Field

class MoatCriteria(BaseModel):
    """
    Represents the 4 distinct boolean criteria used to evaluate a company's moat
    in the AI Factory ecosystem.
    """
    has_architectural_lock_in: bool = Field(
        description="Does the company have architectural lock-in (e.g., CUDA, proprietary networking)?"
    )
    has_ecosystem_dominance: bool = Field(
        description="Does the company have ecosystem dominance (e.g., design wins, reference architectures)?"
    )
    has_high_switching_costs: bool = Field(
        description="Does the company benefit from high switching costs or standard-setting influence?"
    )
    has_scarcity_or_bottleneck: bool = Field(
        description="Does the company hold a scarcity or bottleneck position in the AI Factory supply chain?"
    )
