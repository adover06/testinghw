import pytest
from src.pricing import parse_price, format_currency, bulk_total, add_tax, apply_discount


#Note: - Review the pytest documentation - You need to use one or more pytest features (e.g.,
#@pytest.mark.parametrize, fixtures). Document in README what pytest features you used

@pytest.mark.parametrize("input_str,expected", [
    ("$1,234.50", 1234.50),
    ("12.5", 12.5),
    (" $0.99", 0.99),
])

def test_parse_price(input_str, expected):
    assert parse_price(input_str) == expected



@pytest.mark.parametrize("input_value,expected", [
    (0, "$0.00"),
    (12.5, "$12.50"),
    (1000.0, "$1,000.00"),
    (1234.567, "$1,234.57"),
])
def test_format_currency(input_value, expected):
    assert format_currency(input_value) == expected


@pytest.mark.parametrize("input_value, input_discount, expected", [
    (100, 10, 90.0),
    (200, 0, 200.0),
    
])
def test_apply_discount(input_value, input_discount, expected):
    assert apply_discount(input_value, input_discount) == expected




@pytest.mark.parametrize("input_value, input_tax_rate, expected", [
    (100, 0.07, 107.0),
    (200, 0.10, 220.0),
])
def test_add_tax(input_value, input_tax_rate, expected):
    assert add_tax(input_value, input_tax_rate) == expected
    with pytest.raises(ValueError):
        add_tax(100, -0.05)
    


@pytest.mark.parametrize("prices,discount_percent,tax_rate,expected_total", [
    ([100, 200, 300], 10, 0.07, pytest.approx(603.0)),
    ([100, 200, 300], 0, 0.05, pytest.approx(630.0)),
])
def test_bulk_total(prices, discount_percent, tax_rate, expected_total):
    assert bulk_total(prices, discount_percent=discount_percent, tax_rate=tax_rate) == expected_total
    
