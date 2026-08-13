from unittest.mock import patch, MagicMock
from src.schema.company import CompanyProfile, Risk
from src.schema.risk import RiskExtraction
from src.agents.risk import risk_adjustment_node

@patch("src.agents.risk.ChatPromptTemplate")
@patch("src.agents.risk.ChatOpenAI")
def test_risk_adjustment_node_success(mock_chat_openai, mock_chat_prompt_template):
    mock_chain = MagicMock()
    mock_prompt = MagicMock()
    mock_chat_prompt_template.from_messages.return_value = mock_prompt
    mock_prompt.__or__.return_value = mock_chain
    
    mock_extraction = RiskExtraction(
        risks=[Risk.EXECUTION, Risk.CYCLICALITY]
    )
    mock_chain.invoke.return_value = mock_extraction
    
    state = CompanyProfile(
        ticker="NVDA",
        company_name="NVIDIA Corporation",
        ai_factory_role="Compute",
        is_hyperscaler=False
    )
    
    result = risk_adjustment_node(state)
    assert result == {"risks": [Risk.EXECUTION, Risk.CYCLICALITY]}
    mock_chain.invoke.assert_called_once()

@patch("src.agents.risk.ChatPromptTemplate")
@patch("src.agents.risk.ChatOpenAI")
def test_risk_adjustment_node_error(mock_chat_openai, mock_chat_prompt_template):
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
    
    result = risk_adjustment_node(state)
    assert result == {"risks": []}
