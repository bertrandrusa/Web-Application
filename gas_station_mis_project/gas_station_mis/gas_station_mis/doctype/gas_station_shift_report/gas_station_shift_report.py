"""Shift-close reporting with server-enforced immutable approvals."""
from decimal import Decimal, InvalidOperation
from hashlib import sha256

import frappe
from frappe.model.document import Document
from frappe.utils import getdate
from gas_station_mis.logic import calculate_shift_totals

MONEY_FIELDS = (
    "opening_cash", "cash_sales", "mobile_money_sales", "card_sales",
    "other_sales", "cash_expenses", "cash_removed", "counted_cash",
)

def amount(value):
    try:
        number = Decimal(str(value or "0"))
    except (ValueError, InvalidOperation):
        frappe.throw("Invalid monetary amount.")
    if not number.is_finite() or number < 0:
        frappe.throw("Amounts must be nonnegative and finite.")
    return number

class GasStationShiftReport(Document):
    def autoname(self):
        key = f"{self.station}|{self.shift_schedule}|{getdate(self.report_date).isoformat()}"
        self.name = "GSR-" + sha256(key.encode()).hexdigest()[:20].upper()

    def validate(self):
        schedule = frappe.db.get_value(
            "Gas Station Shift Schedule", self.shift_schedule, ["station", "enabled"], as_dict=True
        )
        if not schedule or schedule.station != self.station or not schedule.enabled:
            frappe.throw("Choose an active shift schedule belonging to this station.")

        values = {field: amount(self.get(field)) for field in MONEY_FIELDS}
        self.total_sales, self.expected_closing_cash, self.cash_difference = calculate_shift_totals(values)

        old = self.get_doc_before_save()
        if not old:
            if self.status != "Draft":
                frappe.throw("New reports must start as Draft.")
            return

        if (old.station, old.shift_schedule, str(old.report_date)) != (
            self.station, self.shift_schedule, str(self.report_date)
        ):
            frappe.throw("Station, shift and date cannot be changed after creation.")

        if not getattr(self.flags, "station_workflow_action", False):
            if self.status != old.status:
                frappe.throw("Use the Submit, Approve or Return action to change report status.")
            if old.status in ("Submitted", "Approved"):
                frappe.throw("Submitted and approved reports are locked.")

        if old.status == "Approved":
            frappe.throw("Approved reports are immutable. Use a separate correction process.")

    def before_save(self):
        # Do not permit staff to manipulate audit-only fields via a regular document save.
        if getattr(self.flags, "station_workflow_action", False):
            return
        old = self.get_doc_before_save()
        fields = ("submitted_by", "submitted_on", "approved_by", "approved_on", "return_reason")
        if old:
            if any(str(self.get(k) or "") != str(old.get(k) or "") for k in fields):
                frappe.throw("Approval audit fields cannot be manually edited.")
        elif any(self.get(k) for k in fields):
            frappe.throw("Approval audit fields cannot be supplied on creation.")

    def on_trash(self):
        if self.status in ("Submitted", "Approved"):
            frappe.throw("Submitted and approved reports cannot be deleted.")
