import pytest
from unittest.mock import patch, MagicMock
from src.agents.margin import normalize_margin_score, fetch_operating_margin, margin_analysis_node
from src.schema.company import CompanyProfile

def test_normalize_margin_score():
    assert normalize_margin_score(45.0) == 5
    assert normalize_margin_score(40.1) == 5
    assert normalize_margin_score(40.0) == 4
    assert normalize_margin_score(30.0) == 4
    assert normalize_margin_score(29.9) == 3
    assert normalize_margin_score(20.0) == 3
    assert normalize_margin_score(15.0) == 2
    assert normalize_margin_score(10.0) == 2
    assert normalize_margin_score(9.9) == 1
    assert normalize_margin_score(-5.0) == 1

@patch("src.agents.margin.yfinance")
def test_fetch_operating_margin(mock_yfinance):
    # Arrange
    mock_ticker = MagicMock()
    # yfinance typically returns decimals like 0.255 for 25.5%
    mock_ticker.info = {"operatingMargins": 0.255}
    mock_yfinance.Ticker.return_value = mock_ticker

    # Act
    margin = fetch_operating_margin("NVDA")

    # Assert
    mock_yfinance.Ticker.assert_called_once_with("NVDA")
    assert margin == 25.5

@patch("src.agents.margin.yfinance")
def test_fetch_operating_margin_missing_data(mock_yfinance):
    # Arrange
    mock_ticker = MagicMock()
    mock_ticker.info = {}
    mock_yfinance.Ticker.return_value = mock_ticker

    # Act
    margin = fetch_operating_margin("NVDA")

    # Assert
    assert margin is None

@patch("src.agents.margin.fetch_operating_margin")
def test_margin_analysis_node(mock_fetch):
    # Arrange
    mock_fetch.return_value = 35.0
    
    state = CompanyProfile(
        ticker="NVDA",
        company_name="NVIDIA Corporation",
        ai_factory_role="Compute",
        is_hyperscaler=False
    )
    
    # Act
    update = margin_analysis_node(state)
    
    # Assert
    assert update["operating_margin"] == 35.0
    assert update["margin_score"] == 4

@patch("src.agents.margin.fetch_operating_margin")
def test_margin_analysis_node_missing_margin(mock_fetch):
    # Arrange
    mock_fetch.return_value = None
    
    state = CompanyProfile(
        ticker="NVDA",
        company_name="NVIDIA Corporation",
        ai_factory_role="Compute",
        is_hyperscaler=False
    )
    
    # Act
    update = margin_analysis_node(state)
    
    # Assert
    assert update["operating_margin"] is None
    assert update["margin_score"] is None
