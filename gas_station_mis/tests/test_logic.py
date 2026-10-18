"""Offline tests for core business calculations and due-date behavior."""
from datetime import date, datetime
from decimal import Decimal
from unittest import TestCase
from gas_station_mis.logic import calculate_shift_totals, report_deadline

class TestShiftLogic(TestCase):
    def test_totals_keep_exact_money(self):
        row = {
            "opening_cash": Decimal("1000.00"),
            "cash_sales": Decimal("123.45"),
            "mobile_money_sales": Decimal("200.10"),
            "card_sales": Decimal("300.25"),
            "other_sales": Decimal("0"),
            "cash_expenses": Decimal("23.45"),
            "cash_removed": Decimal("100.00"),
            "counted_cash": Decimal("1001.00"),
        }
        total, expected, diff = calculate_shift_totals(row)
        self.assertEqual(total, Decimal("623.80"))
        self.assertEqual(expected, Decimal("1000.00"))
        self.assertEqual(diff, Decimal("1.00"))

    def test_deadline_crosses_midnight(self):
        actual = report_deadline(date(2026, 10, 18), "23:45:00", 30)
        self.assertEqual(actual, datetime(2026, 10, 19, 0, 15))

    def test_deadline_without_seconds(self):
        self.assertEqual(
            report_deadline(date(2026, 10, 18), "22:00", 45),
            datetime(2026, 10, 18, 22, 45),
        )
