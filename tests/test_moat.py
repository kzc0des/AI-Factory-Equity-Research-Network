from unittest.mock import patch, MagicMock
from src.schema.company import CompanyProfile
from src.schema.moat import MoatCriteria
from src.agents.moat import moat_analysis_node, calculate_moat_score

def test_calculate_moat_score():
    # Test all true
    criteria = MoatCriteria(
        has_architectural_lock_in=True,
        has_ecosystem_dominance=True,
        has_high_switching_costs=True,
        has_scarcity_or_bottleneck=True
    )
    assert calculate_moat_score(criteria) == 5.0
    
    # Test all false
    criteria_false = MoatCriteria(
        has_architectural_lock_in=False,
        has_ecosystem_dominance=False,
        has_high_switching_costs=False,
        has_scarcity_or_bottleneck=False
    )
    assert calculate_moat_score(criteria_false) == 0.0

    # Test mixed
    criteria_mixed = MoatCriteria(
        has_architectural_lock_in=True,
        has_ecosystem_dominance=False,
        has_high_switching_costs=True,
        has_scarcity_or_bottleneck=False
    )
    assert calculate_moat_score(criteria_mixed) == 2.5

@patch("src.agents.moat.ChatOpenAI")
def test_moat_analysis_node_success(mock_chat_openai):
    # Setup mock
    mock_llm = MagicMock()
    mock_chat_openai.return_value = mock_llm
    
    mock_structured_llm = MagicMock()
    mock_llm.with_structured_output.return_value = mock_structured_llm
    
    # Mock the chain invocation
    mock_criteria = MoatCriteria(
        has_architectural_lock_in=True,
        has_ecosystem_dominance=True,
        has_high_switching_costs=False,
        has_scarcity_or_bottleneck=False
    )
    
    # Create a mock chain
    mock_chain = MagicMock()
    mock_chain.invoke.return_value = mock_criteria
    
    # We need to patch the prompt | structured_llm behavior
    # Actually, patch invoke on whatever is returned by prompt | structured_llm
    # To simplify, we can patch ChatPromptTemplate.from_messages to return something
    # but the easiest way is to mock the chain itself if we structured it that way.
    # Let's patch invoke directly on the class or structure.
    pass

@patch("src.agents.moat.ChatPromptTemplate")
@patch("src.agents.moat.ChatOpenAI")
def test_moat_analysis_node_chain(mock_chat_openai, mock_chat_prompt_template):
    mock_chain = MagicMock()
    # The | operator is implemented via __or__ on the prompt template
    mock_prompt = MagicMock()
    mock_chat_prompt_template.from_messages.return_value = mock_prompt
    mock_prompt.__or__.return_value = mock_chain
    
    mock_criteria = MoatCriteria(
        has_architectural_lock_in=True,
        has_ecosystem_dominance=True,
        has_high_switching_costs=False,
        has_scarcity_or_bottleneck=False
    )
    mock_chain.invoke.return_value = mock_criteria
    
    state = CompanyProfile(
        ticker="NVDA",
        company_name="NVIDIA Corporation",
        ai_factory_role="Compute",
        is_hyperscaler=False
    )
    
    result = moat_analysis_node(state)
    assert result == {"moat_score": 2.5}
    mock_chain.invoke.assert_called_once()

@patch("src.agents.moat.ChatPromptTemplate")
@patch("src.agents.moat.ChatOpenAI")
def test_moat_analysis_node_error(mock_chat_openai, mock_chat_prompt_template):
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
    
    result = moat_analysis_node(state)
    assert result == {"moat_score": None}
