import frappe
from frappe.model.document import Document

class GasStationStaffAssignment(Document):
    def validate(self):
        if not frappe.db.get_value("User", self.user, "enabled"):
            frappe.throw("The selected user must be enabled.")
        if frappe.db.get_value("User", self.user, "user_type") != "System User":
            frappe.throw("The selected user must be a System User.")
        duplicate = frappe.db.exists(
            "Gas Station Staff Assignment",
            {"station": self.station, "user": self.user, "name": ["!=", self.name or ""]},
        )
        if duplicate:
            frappe.throw("A user can have only one membership per station.")
        if self.employee:
            linked_user = frappe.db.get_value("Employee", self.employee, "user_id")
            if linked_user and linked_user != self.user:
                frappe.throw("The employee record is linked to another user.")

    def on_update(self):
        if self.enabled:
            user = frappe.get_doc("User", self.user)
            if "Gas Station User" not in frappe.get_roles(self.user):
                user.add_roles("Gas Station User")
