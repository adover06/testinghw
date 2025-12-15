from src.pricing import parse_price, format_currency, bulk_total
import csv


def load_order(path):
    items = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)

        header = next(reader, None)

        for row in reader:
            if len(row) != 2:
                continue
            name, price_text = row
            name = name.strip()
            price_text = price_text.strip()
            items.append((name, parse_price(price_text)))
    return items

def write_receipt(path, items, discount_percent=0, tax_rate=0.07):
    prices = [price for (_name, price) in items]
    total = bulk_total(prices, discount_percent, tax_rate)
    lines = [f"{name}: {format_currency(price)}" for (name, price) in items]
    lines.append("TOTAL: " + format_currency(total))
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
