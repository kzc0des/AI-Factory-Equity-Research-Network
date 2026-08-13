from src.schema.company import CompanyProfile
from src.schema.state import ParentState
from src.agents.ranking import compute_tafgs, ranking_node

def test_compute_tafgs():
    profile = CompanyProfile(
        ticker="TEST",
        company_name="Test Inc",
        moat_score=4.0,
        margin_score=3,
        growth_cagr=15.0
    )
    # (4 * 3) * 15 = 12 * 15 = 180
    assert compute_tafgs(profile) == 180.0
    
    # Test missing fields
    profile_missing = CompanyProfile(ticker="T2", company_name="Test 2", moat_score=4.0)
    assert compute_tafgs(profile_missing) == 0.0

def test_ranking_node():
    profiles = [
        CompanyProfile(ticker="A", company_name="A", moat_score=4, margin_score=3, growth_cagr=15.0), # 180
        CompanyProfile(ticker="B", company_name="B", moat_score=2, margin_score=2, growth_cagr=10.0), # 40
        CompanyProfile(ticker="C", company_name="C", moat_score=5, margin_score=5, growth_cagr=20.0), # 500
    ]
    
    state: ParentState = {
        "seed_list": [],
        "profiles": profiles,
        "top_20": []
    }
    
    result = ranking_node(state)
    
    top_20 = result["top_20"]
    assert len(top_20) == 3
    
    # Should be sorted C, A, B
    assert top_20[0].ticker == "C"
    assert top_20[0].total_score == 500.0
    
    assert top_20[1].ticker == "A"
    assert top_20[1].total_score == 180.0
    
    assert top_20[2].ticker == "B"
    assert top_20[2].total_score == 40.0
