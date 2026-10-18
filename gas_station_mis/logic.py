"""Pure, deterministic station reporting calculations (no Frappe dependency)."""
from datetime import datetime, timedelta
from decimal import Decimal

def calculate_shift_totals(values):
    """Return (total_sales, expected_cash, cash_difference), preserving Decimal precision.

    Requires a mapping of validated, nonnegative Decimals from the DocType controller.
    No values are posted to the accounting ledger.
    """
    sales = sum(
        (values[k] for k in ("cash_sales", "mobile_money_sales", "card_sales", "other_sales")),
        Decimal("0"),
    )
    expected_cash = (
        values["opening_cash"] + values["cash_sales"]
        - values["cash_expenses"] - values["cash_removed"]
    )
    difference = values["counted_cash"] - expected_cash
    return sales, expected_cash, difference

def report_deadline(report_date, time_text, grace_minutes):
    """Return a naive deadline in the Frappe site's configured timezone.

    This is a wall-clock time, not UTC. For schedules that span midnight,
    report_date is the date on which the shift ends.
    """
    if hasattr(time_text, "isoformat"):
        time_text = time_text.isoformat()
    parts = str(time_text).split(":")
    if len(parts) < 2:
        raise ValueError("Expected HH:MM or HH:MM:SS")
    hour, minute = int(parts[0]), int(parts[1])
    second = int(float(parts[2])) if len(parts) > 2 else 0
    return datetime(report_date.year, report_date.month, report_date.day, hour, minute, second) + timedelta(minutes=int(grace_minutes))
