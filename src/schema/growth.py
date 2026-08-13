from pydantic import BaseModel, Field

class GrowthExtraction(BaseModel):
    """
    Extracted growth metrics from SEC filings or transcripts.
    """
    cagr_3yr: float = Field(description="The extracted or estimated 3-year CAGR percentage (e.g. 15.5 for 15.5%).")
    confidence: float = Field(description="Confidence score of the extraction (0.0 to 1.0).")
    reasoning: str = Field(description="Brief reasoning for the extracted CAGR based on backlog or guidance.")
