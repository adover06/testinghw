from src.pricing import parse_price, format_currency, bulk_total

def load_order(path):
    """
    Reads CSV-like lines: 'name,price'
    Returns list of (name, price_float).
    """
    items = []
    with open(path, "r", encoding="utf-8") as f:
        for ln in f:
            if not ln.strip():
                continue
            parts = ln.split(",")
            if len(parts) != 2:
                raise ValueError("Malformed line: " + ln.strip())
            name, price = parts[0].strip(), parts[1].strip()
            items.append((name, parse_price(price)))
    return items

def write_receipt(path, items, discount_percent=0, tax_rate=0.07):
    prices = [price for (_name, price) in items]
    total = bulk_total(prices, discount_percent, tax_rate)
    lines = [f"{name}: {format_currency(price)}" for (name, price) in items]
    lines.append("TOTAL: " + format_currency(total))
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
