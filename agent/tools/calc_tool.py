# agent/tools/calc_tool.py
import re
from decimal import Decimal, getcontext
getcontext().prec = 12

NUM_RE = re.compile(r"[-+]?\d[\d,]*\.?\d*")
import re

def parse_number(value):
    if isinstance(value, (int, float)):
        return value
    value = str(value).replace(",", "").replace("$", "").strip()
    try:
        return float(re.findall(r"[-+]?\d*\.\d+|\d+", value)[0])
    except Exception:
        return 0.0

def compute_ratios(context):
    """
    Extracts numeric values (like Total Debt, Total Equity, etc.) from text context
    and computes basic financial ratios.
    """
    # If input is dict, extract text
    if isinstance(context, dict):
        text = context.get("text", "")
    else:
        text = str(context)

    # Try to find numeric values from text
    total_debt = re.findall(r"total debt[:\s$]*([\d,\.]+)", text.lower())
    total_equity = re.findall(r"total equity[:\s$]*([\d,\.]+)", text.lower())

    td = parse_number(total_debt[0]) if total_debt else 0
    te = parse_number(total_equity[0]) if total_equity else 0

    if td > 0 and te > 0:
        ratio = td / te
        return f"Estimated Debt-to-Equity ratio: {ratio:.2f}"
    else:
        return "Unable to compute ratio: missing numeric data."


# example small CLI test
if __name__ == "__main__":
    p = {"total_debt": "1200000", "total_equity": "3000000", "ebit": "500000", "interest_expense": "25000"}
    print(compute_ratios(p))
