import re
import json


def clean_price(price_str):
    """Remove spaces and convert to float"""
    return float(price_str.replace(" ", "").replace(",", "."))


def parse_receipt(file_path):
    with open(file_path, encoding="utf-8") as f:
        text = f.read()

    result = {}

    #1Extract all prices
    price_pattern = r'\d{1,3}(?: \d{3})*,\d{2}'
    prices = re.findall(price_pattern, text)
    result["all_prices"] = prices

    #2Extract product names
    product_pattern = r'\d+\.\s*\n(.+?)\n\d+,\d{3} x'
    products = re.findall(product_pattern, text, re.DOTALL)
    result["products"] = [p.strip() for p in products]

    #3Extract total amount
    total_pattern = r'ИТОГО:\s*\n([\d ]+,\d{2})'
    total_match = re.search(total_pattern, text)
    if total_match:
        result["total_amount"] = clean_price(total_match.group(1))

    #4Extract date and time
    date_pattern = r'Время:\s*(\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2})'
    date_match = re.search(date_pattern, text)
    if date_match:
        result["datetime"] = date_match.group(1)

    #5Extract payment method
    payment_pattern = r'(Банковская карта|Наличные)'
    payment_match = re.search(payment_pattern, text)
    if payment_match:
        result["payment_method"] = payment_match.group(1)

    return result


if __name__ == "__main__":
    parsed_data = parse_receipt("raw.txt")
    print(json.dumps(parsed_data, indent=4, ensure_ascii=False))