from src.pricing import apply_discount
import pytest

def test_apply_discount_regression():
    
    result = apply_discount(50.0, 20)
    # should be 40
    assert result == 40.0