import pytest
from src.agents.ingestion import filter_companies, SEED_LIST
from src.schema.company import CompanyProfile

def test_filter_companies_removes_hyperscalers():
    # Arrange
    test_seed_list = [
        {"ticker": "MSFT", "company_name": "Microsoft", "is_hyperscaler": True, "ai_factory_role": "Builder"},
        {"ticker": "NVDA", "company_name": "NVIDIA", "is_hyperscaler": False, "ai_factory_role": "Compute"}
    ]
    
    # Act
    result = filter_companies(test_seed_list)
    
    # Assert
    assert len(result) == 1
    assert result[0].ticker == "NVDA"
    assert isinstance(result[0], CompanyProfile)

def test_filter_companies_removes_zero_exposure():
    # Arrange
    test_seed_list = [
        {"ticker": "RANDOM", "company_name": "Random Corp", "is_hyperscaler": False, "ai_factory_role": None},
        {"ticker": "ANET", "company_name": "Arista", "is_hyperscaler": False, "ai_factory_role": "Networking"}
    ]
    
    # Act
    result = filter_companies(test_seed_list)
    
    # Assert
    assert len(result) == 1
    assert result[0].ticker == "ANET"

def test_filter_companies_with_default_seed_list():
    # Act
    result = filter_companies(SEED_LIST)
    
    # Assert
    tickers = [company.ticker for company in result]
    assert "MSFT" not in tickers
    assert "GOOGL" not in tickers
    assert "AAPL" not in tickers
    assert "NVDA" in tickers
    assert "ANET" in tickers
    assert "VRT" in tickers
    assert "CEG" in tickers
    assert "AMD" in tickers
    assert "VST" in tickers
    assert "J" in tickers
    assert len(result) == 20
    
    for company in result:
        assert isinstance(company, CompanyProfile)
        assert company.is_hyperscaler is False
        assert company.ai_factory_role is not None
