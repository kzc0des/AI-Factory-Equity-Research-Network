import os
import pytest
from unittest.mock import patch
from src.agents.graph import build_parent_graph
from src.agents.ingestion import SEED_LIST

@pytest.fixture(autouse=True)
def setup_demo_mode():
    """
    Ensure DEMO_MODE is True for the integration tests.
    """
    with patch.dict(os.environ, {"DEMO_MODE": "True"}):
        yield

def test_offline_integration_runs_successfully():
    """
    Verifies that the entire map-reduce LangGraph executes end-to-end and
    generates the final report correctly when DEMO_MODE=True, completely
    bypassing live APIs and LLM calls.
    """
    # Build the parent graph
    graph = build_parent_graph().compile()
    
    # Initialize the parent state with the full SEED_LIST
    initial_state = {
        "seed_list": SEED_LIST,
        "profiles": [],
        "top_20": []
    }
    
    # Invoke the graph
    result = graph.invoke(initial_state)
    
    # Verify that all 20 picks-and-shovels targets were evaluated
    top_20 = result.get("top_20", [])
    assert len(top_20) == 20
    
    # Verify that the profiles have valid scores
    for profile in top_20:
        assert profile.moat_score is not None
        assert profile.operating_margin is not None
        assert profile.margin_score is not None
        assert profile.growth_cagr is not None
        assert profile.total_score is not None
        assert profile.risk_discount is not None
        
    # Verify that the top_20 list is properly sorted in descending order by TAFGS
    scores = [p.total_score for p in top_20]
    assert all(scores[i] >= scores[i+1] for i in range(len(scores)-1))
    
    # Verify that the report output file exists
    report_path = os.path.join("output", "report.md")
    assert os.path.exists(report_path)
    
    # Verify the content of the report
    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    assert "# Top 20 AI Factory Growth Equity Targets" in content
    assert "NVIDIA Corporation (NVDA)" in content
    assert "Broadcom Inc. (AVGO)" in content
    assert "Vertiv Holdings Co. (VRT)" in content
