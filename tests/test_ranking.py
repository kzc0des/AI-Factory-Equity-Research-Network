import pytest
from src.agents.ranking import compute_risk_discount, compute_tafgs
from src.schema.company import Risk, CompanyProfile

def test_compute_risk_discount_empty():
    assert compute_risk_discount([]) == 1.0

def test_compute_risk_discount_execution():
    assert compute_risk_discount([Risk.EXECUTION]) == 0.9

def test_compute_risk_discount_cyclicality():
    assert compute_risk_discount([Risk.CYCLICALITY]) == 0.8

def test_compute_risk_discount_concentration():
    assert compute_risk_discount([Risk.CUSTOMER_CONCENTRATION]) == pytest.approx(0.85)

def test_compute_risk_discount_multiple():
    assert compute_risk_discount([Risk.EXECUTION, Risk.CYCLICALITY]) == pytest.approx(0.72)
