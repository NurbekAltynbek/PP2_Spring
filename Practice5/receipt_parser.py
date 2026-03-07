import re
import json

# read file
with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Extract all prices
price_pattern = r"\d{1,3}(?:,\d{3})*\.\d{2}"
prices = re.findall(price_pattern, text)

# convert to float
prices_float = [float(p.replace(",", "")) for p in prices]

# 2. Find product names
product_pattern = r"\d+\.\n([^\n]+)"
products = re.findall(product_pattern, text)

# 3. Calculate total amount
calculated_total = sum(prices_float)

# 4. Extract date and time
datetime_pattern = r"\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2}"
datetime_match = re.search(datetime_pattern, text)
datetime_value = datetime_match.group() if datetime_match else None

# 5. Find payment method
payment_pattern = r"(Bank card|Cash)"
payment_match = re.search(payment_pattern, text)
payment_method = payment_match.group() if payment_match else None

# 6. Structured output
data = {
    "products": products,
    "prices": prices_float,
    "calculated_total": calculated_total,
    "payment_method": payment_method,
    "datetime": datetime_value
}

print(json.dumps(data, indent=4))