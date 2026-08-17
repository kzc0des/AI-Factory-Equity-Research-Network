import os
from unittest.mock import patch
from src.agents.utils import is_demo_mode

def test_is_demo_mode_default():
    with patch.dict(os.environ, {}, clear=True):
        assert is_demo_mode() is False

def test_is_demo_mode_true():
    with patch.dict(os.environ, {"DEMO_MODE": "True"}):
        assert is_demo_mode() is True

def test_is_demo_mode_true_lowercase():
    with patch.dict(os.environ, {"DEMO_MODE": "true"}):
        assert is_demo_mode() is True

def test_is_demo_mode_true_whitespace():
    with patch.dict(os.environ, {"DEMO_MODE": " true "}):
        assert is_demo_mode() is True

def test_is_demo_mode_false():
    with patch.dict(os.environ, {"DEMO_MODE": "False"}):
        assert is_demo_mode() is False

def test_is_demo_mode_other():
    with patch.dict(os.environ, {"DEMO_MODE": "some_value"}):
        assert is_demo_mode() is False
