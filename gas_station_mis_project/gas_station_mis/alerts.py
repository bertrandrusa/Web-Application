"""Idempotent in-app alerts; the scheduler does not send external messages."""
import frappe
from frappe.utils import now_datetime

def create_alert(station, alert_key, alert_type, message, related_report=None):
    existing = frappe.db.exists("Gas Station Alert", {"alert_key": alert_key})
    if existing:
        return existing
    doc = frappe.get_doc({
        "doctype": "Gas Station Alert",
        "station": station,
        "alert_key": alert_key,
        "alert_type": alert_type,
        "message": message,
        "related_report": related_report,
        "status": "Open",
    })
    doc.insert(ignore_permissions=True)
    return doc.name

def close_alert(alert_key, user=None):
    name = frappe.db.exists("Gas Station Alert", {"alert_key": alert_key, "status": "Open"})
    if name:
        doc = frappe.get_doc("Gas Station Alert", name)
        doc.status = "Resolved"
        doc.resolved_by = user or frappe.session.user
        doc.resolved_on = now_datetime()
        doc.save(ignore_permissions=True)
