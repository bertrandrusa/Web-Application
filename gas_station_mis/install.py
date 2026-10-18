import frappe

def ensure_roles():
    """Create the base role used by station members; it is not itself a station grant."""
    if not frappe.db.exists("Role", "Gas Station User"):
        frappe.get_doc({
            "doctype": "Role",
            "role_name": "Gas Station User",
            "desk_access": 1,
        }).insert(ignore_permissions=True)
