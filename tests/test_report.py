import os
from src.schema.company import CompanyProfile
from src.schema.state import ParentState
from src.agents.report import generate_markdown_report, report_node

def test_generate_markdown_report():
    profiles = [
        CompanyProfile(
            ticker="NVDA",
            company_name="NVIDIA",
            ai_factory_role="Compute",
            moat_score=4.0,
            margin_score=5,
            growth_cagr=20.0,
            total_score=400.0,
            risks=["cyclicality"],
            risk_discount=0.8,
            catalysts=["New GPU generation"]
        )
    ]
    
    state: ParentState = {
        "seed_list": [],
        "profiles": profiles,
        "top_20": profiles
    }
    
    report = generate_markdown_report(state)
    assert "Top 20 AI Factory Growth Equity Targets" in report
    assert "1. NVIDIA (NVDA)" in report
    assert "400.00" in report
    assert "**Risk Discount Applied:** 0.80x" in report
    assert "New GPU generation" in report
    assert "cyclicality" in report

def test_report_node(tmp_path):
    profiles = [
        CompanyProfile(
            ticker="NVDA",
            company_name="NVIDIA",
            ai_factory_role="Compute",
            moat_score=4.0,
            margin_score=5,
            growth_cagr=20.0,
            total_score=400.0
        )
    ]
    
    state: ParentState = {
        "seed_list": [],
        "profiles": profiles,
        "top_20": profiles
    }
    
    # We should run it but need to intercept file writing so we don't mess up the workspace
    # Since it writes to 'output/report.md', we can let it write there for the test, 
    # but using a patch is better. Let's patch open.
    from unittest.mock import patch
    with patch("builtins.open") as mock_open:
        with patch("os.makedirs") as mock_makedirs:
            result = report_node(state)
            assert result["report_generated"] is True
            mock_makedirs.assert_called_with("output", exist_ok=True)
            mock_open.assert_called_with("output/report.md", "w", encoding="utf-8")
