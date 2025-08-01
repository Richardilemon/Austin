from datetime import datetime

def validate_row(row):
    errors = []

    if not row.get("permit_id"):
        errors.append("Missing permit_id")

    try:
        val = float(row.get("valuation", 0))
        if val < 0:
            errors.append("Negative valuation")
    except:
        errors.append("Invalid valuation")

    try:
        datetime.strptime(row.get("date_issued", ""), "%Y-%m-%d")
    except:
        errors.append("Invalid date_issued format")

    return errors
