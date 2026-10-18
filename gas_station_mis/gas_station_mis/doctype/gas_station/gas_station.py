import frappe
from frappe.model.document import Document

class GasStation(Document):
    def validate(self):
        if not self.station_name or not self.company:
            frappe.throw("Station name and company are required.")
