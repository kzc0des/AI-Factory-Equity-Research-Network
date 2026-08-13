from unittest.mock import patch, MagicMock
from src.schema.company import CompanyProfile
from src.schema.market import MarketMappingResult
from src.agents.market import market_mapping_node

@patch("src.agents.market.ChatOpenAI")
def test_market_mapping_node(mock_chat_openai):
    mock_llm = MagicMock()
    mock_chat_openai.return_value = mock_llm
    
    mock_structured_llm = MagicMock()
    mock_llm.with_structured_output.return_value = mock_structured_llm
    
    # We mock the entire chain invocation because we are using LangChain pipelines
    mock_chain = MagicMock()
    mock_chain.invoke.return_value = MarketMappingResult(
        ai_factory_role="Compute",
        is_hyperscaler=False
    )
    
    # We patch the prompt | structured_llm pipeline creation in the node
    with patch("src.agents.market.ChatPromptTemplate.from_messages") as mock_prompt:
        # Mock the __or__ operator (`|`)
        mock_prompt_instance = MagicMock()
        mock_prompt.return_value = mock_prompt_instance
        mock_prompt_instance.__or__.return_value = mock_chain
        
        state = CompanyProfile(
            ticker="NVDA",
            company_name="Nvidia Corp"
        )
        
        result = market_mapping_node(state)
        
        assert result["ai_factory_role"] == "Compute"
        assert result["is_hyperscaler"] is False
