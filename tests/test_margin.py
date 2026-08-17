import pytest
import os
import json
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

@patch("src.agents.margin.yf")
@patch("src.agents.margin.is_demo_mode")
def test_fetch_operating_margin_live(mock_is_demo_mode, mock_yf):
    # Arrange
    mock_is_demo_mode.return_value = False
    mock_ticker = MagicMock()
    mock_ticker.info = {"operatingMargins": 0.255}
    mock_yf.Ticker.return_value = mock_ticker

    # Act
    margin = fetch_operating_margin("NVDA")

    # Assert
    mock_is_demo_mode.assert_called_once()
    mock_yf.Ticker.assert_called_once()
    assert margin == 25.5

@patch("src.agents.margin.yf")
@patch("src.agents.margin.is_demo_mode")
def test_fetch_operating_margin_live_missing_data(mock_is_demo_mode, mock_yf):
    # Arrange
    mock_is_demo_mode.return_value = False
    mock_ticker = MagicMock()
    mock_ticker.info = {}
    mock_yf.Ticker.return_value = mock_ticker

    # Act
    margin = fetch_operating_margin("NVDA")

    # Assert
    assert margin is None

@patch("src.agents.margin.is_demo_mode")
@patch("os.path.exists")
@patch("builtins.open")
def test_fetch_operating_margin_demo(mock_open, mock_exists, mock_is_demo_mode):
    # Arrange
    mock_is_demo_mode.return_value = True
    mock_exists.return_value = True
    
    mock_file = MagicMock()
    mock_file.__enter__.return_value = mock_file
    mock_file.read.return_value = json.dumps({"NVDA": 35.5})
    mock_open.return_value = mock_file

    # Act
    margin = fetch_operating_margin("NVDA")

    # Assert
    mock_is_demo_mode.assert_called_once()
    assert margin == 35.5

@patch("src.agents.margin.is_demo_mode")
@patch("os.path.exists")
def test_fetch_operating_margin_demo_missing_cache(mock_exists, mock_is_demo_mode):
    # Arrange
    mock_is_demo_mode.return_value = True
    mock_exists.return_value = False

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

@patch("src.agents.margin.yf")
@patch("src.agents.margin.is_demo_mode")
@patch("src.agents.margin.logger")
def test_fetch_operating_margin_exception(mock_logger, mock_is_demo_mode, mock_yf):
    # Arrange
    mock_is_demo_mode.return_value = False
    mock_yf.Ticker.side_effect = Exception("API error")

    # Act
    margin = fetch_operating_margin("NVDA")

    # Assert
    assert margin is None
    mock_logger.error.assert_called_once_with("Error fetching operating margin for NVDA: API error")

