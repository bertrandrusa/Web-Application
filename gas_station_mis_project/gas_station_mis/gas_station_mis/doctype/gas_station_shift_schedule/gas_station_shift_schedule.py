import frappe
from frappe.model.document import Document
from frappe.utils import cint

class GasStationShiftSchedule(Document):
    def validate(self):
        if not self.shift_name or not self.station:
            frappe.throw("Station and shift name are required.")
        if not 0 <= cint(self.grace_minutes) <= 1440:
            frappe.throw("Grace period must be between 0 and 1440 minutes.")
        if frappe.db.exists(
            "Gas Station Shift Schedule",
            {"station": self.station, "shift_name": self.shift_name, "name": ["!=", self.name or ""]},
        ):
            frappe.throw("This shift name is already configured at this station.")

    def before_save(self):
        old = self.get_doc_before_save()
        if old and old.station != self.station:
            frappe.throw("You cannot move a shift schedule to another station.")
