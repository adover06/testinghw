import pytest
from src.pricing import parse_price, format_currency, bulk_total, add_tax, apply_discount
from src.order_io import load_order, write_receipt

#Pricing tests

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
    
#Order IO tests

def test_load_order_simple(tmp_path):
    csv_path = tmp_path / "order.csv"
    csv_path.write_text("item,price\nitem,$10.00\nitem,$5.50\n", encoding="utf-8")

    items = load_order(csv_path)

    assert items == [
        ("item", parse_price("$10.00")),
        ("item", parse_price("$5.50")),
    ]

def test_write_receipt_creates_file(tmp_path):
    receipt_path = tmp_path / "receipt.txt"
    items = [("item", 10.0), ("item", 5.5)]

    write_receipt(receipt_path, items, discount_percent=10, tax_rate=0.1)

    text = receipt_path.read_text(encoding="utf-8")
    assert "item" in text
    assert "item" in text
    assert "TOTAL" in text
