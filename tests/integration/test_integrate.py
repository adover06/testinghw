import pytest
from src.order_io import write_receipt, load_order
from src.pricing import bulk_total

@pytest.fixture
def sample_order(tmp_path):
    csv_path = tmp_path / "data.csv"
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write("name,price\n")
        f.write(" nuts,$10.00\n")
        f.write("butter,20.00 \n")
    return csv_path

def test_csv_integration(tmp_path, sample_order):
    items = load_order(sample_order)

    assert items == [("nuts", 10.0), ("butter", 20.0)]
    
    receipt_path = tmp_path / "receipt.txt"
    write_receipt(receipt_path, items, discount_percent=10, tax_rate=0.1)
    
    with open(receipt_path, "r", encoding="utf-8") as f:
        receipt_content = f.read()
    
    expected_total = bulk_total([10.0, 20.0], discount_percent=10, tax_rate=0.1)
    expected_receipt = (
        "nuts: $10.00\n"
        "butter: $20.00\n"
        f"TOTAL: ${expected_total:,.2f}"
    )
    assert "nuts" in  items[0]
    assert "butter" in items[1]
    assert len(items) == 2
    assert receipt_content.strip() == expected_receipt