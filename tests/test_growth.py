from unittest.mock import patch, MagicMock
from src.schema.company import CompanyProfile
from src.schema.growth import GrowthExtraction
from src.agents.growth import growth_forecast_node, retrieve_financial_documents

def test_retrieve_financial_documents():
    docs = retrieve_financial_documents("NVDA")
    assert "NVDA" in docs
    assert "15-20%" in docs

@patch("src.agents.growth.ChatPromptTemplate")
@patch("src.agents.growth.ChatOpenAI")
def test_growth_forecast_node_success(mock_chat_openai, mock_chat_prompt_template):
    mock_chain = MagicMock()
    mock_prompt = MagicMock()
    mock_chat_prompt_template.from_messages.return_value = mock_prompt
    mock_prompt.__or__.return_value = mock_chain
    
    mock_extraction = GrowthExtraction(
        cagr_3yr=17.5,
        confidence=0.9,
        reasoning="Midpoint of 15-20% guidance."
    )
    mock_chain.invoke.return_value = mock_extraction
    
    state = CompanyProfile(
        ticker="NVDA",
        company_name="NVIDIA Corporation",
        ai_factory_role="Compute",
        is_hyperscaler=False
    )
    
    result = growth_forecast_node(state)
    assert result == {"growth_cagr": 17.5}
    mock_chain.invoke.assert_called_once()

@patch("src.agents.growth.ChatPromptTemplate")
@patch("src.agents.growth.ChatOpenAI")
def test_growth_forecast_node_error(mock_chat_openai, mock_chat_prompt_template):
    mock_chain = MagicMock()
    mock_prompt = MagicMock()
    mock_chat_prompt_template.from_messages.return_value = mock_prompt
    mock_prompt.__or__.return_value = mock_chain
    
    mock_chain.invoke.side_effect = Exception("API Error")
    
    state = CompanyProfile(
        ticker="NVDA",
        company_name="NVIDIA Corporation",
        ai_factory_role="Compute",
        is_hyperscaler=False
    )
    
    result = growth_forecast_node(state)
    assert result == {"growth_cagr": None}
