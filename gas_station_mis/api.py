"""Whitelisted endpoints. Every station selector is authorized server-side."""
import frappe
from frappe.utils import getdate, now_datetime, today, flt

from gas_station_mis.alerts import create_alert, close_alert
from gas_station_mis.permissions import can_manage, can_report, is_system_manager, permitted_stations
from gas_station_mis.tasks import missing_key

def _require_login():
    if frappe.session.user == "Guest":
        frappe.throw("Please log in.", frappe.PermissionError)

def _authorized_station(station, manager_only=False):
    _require_login()
    allowed = permitted_stations(roles={"Manager"} if manager_only else {"Manager", "Supervisor"})
    if station not in allowed:
        frappe.throw("You do not have access to this station.", frappe.PermissionError)
    return station

@frappe.whitelist()
def available_stations():
    _require_login()
    station_ids = permitted_stations(roles={"Manager", "Supervisor"})
    return [{"value": name, "label": name} for name in sorted(station_ids)]

@frappe.whitelist()
def get_dashboard(station):
    station = _authorized_station(station)
    current_date = getdate(today())
    reports = frappe.get_all(
        "Gas Station Shift Report",
        filters={"station": station, "report_date": current_date},
        fields=["name", "status", "total_sales", "cash_difference"],
    )
    alerts = frappe.get_all(
        "Gas Station Alert",
        filters={"station": station, "status": "Open"},
        fields=["name", "alert_type", "message", "creation"],
        order_by="creation desc",
        limit_page_length=8,
    ) if can_manage(station) else []
    membership_count = frappe.db.count(
        "Gas Station Staff Assignment", {"station": station, "enabled": 1}
    )
    approved = [r for r in reports if r.status == "Approved"]
    return {
        "station": station,
        "date": str(current_date),
        "staff_count": membership_count,
        "shift_reports": len(reports),
        "pending_reports": sum(r.status == "Submitted" for r in reports),
        "approved_reports": len(approved),
        "reported_sales_approved": sum(flt(r.total_sales) for r in approved),
        "open_alert_count": frappe.db.count("Gas Station Alert", {"station": station, "status": "Open"}) if can_manage(station) else 0,
        "recent_alerts": alerts,
    }

def _report(name):
    _require_login()
    doc = frappe.get_doc("Gas Station Shift Report", name)
    _authorized_station(doc.station)
    return doc

@frappe.whitelist()
def station_actions(station):
    _authorized_station(station)
    return {"can_manage": bool(can_manage(station))}

@frappe.whitelist()
def report_actions(name):
    doc = _report(name)
    return {
        "can_submit": bool(can_report(doc.station) and doc.status in ("Draft", "Returned")),
        "can_approve": bool(can_manage(doc.station) and doc.status == "Submitted"),
    }

@frappe.whitelist(methods=["POST"])
def submit_report(name):
    doc = _report(name)
    if not can_report(doc.station):
        frappe.throw("Not permitted to submit reports.", frappe.PermissionError)
    if doc.status not in ("Draft", "Returned"):
        frappe.throw("Only draft or returned reports can be submitted.")
    doc.flags.station_workflow_action = True
    doc.status = "Submitted"
    doc.submitted_by = frappe.session.user
    doc.submitted_on = now_datetime()
    doc.return_reason = ""
    doc.save(ignore_permissions=True)
    close_alert(missing_key(doc.station, doc.shift_schedule, doc.report_date))
    create_alert(
        doc.station,
        "APPROVAL:" + doc.name,
        "Approval Required",
        f"Shift report {doc.name} is awaiting manager approval.",
        related_report=doc.name,
    )
    return doc.name

@frappe.whitelist(methods=["POST"])
def approve_report(name):
    doc = _report(name)
    _authorized_station(doc.station, manager_only=True)
    if doc.status != "Submitted":
        frappe.throw("Only submitted reports can be approved.")
    doc.flags.station_workflow_action = True
    doc.status = "Approved"
    doc.approved_by = frappe.session.user
    doc.approved_on = now_datetime()
    doc.save(ignore_permissions=True)
    close_alert("APPROVAL:" + doc.name)
    threshold = flt(frappe.db.get_value("Gas Station", doc.station, "cash_variance_threshold"))
    if threshold > 0 and abs(flt(doc.cash_difference)) >= threshold:
        create_alert(
            doc.station,
            "VARIANCE:" + doc.name,
            "Cash Variance",
            f"Shift report {doc.name} has a cash variance requiring review.",
            related_report=doc.name,
        )
    return doc.name

@frappe.whitelist(methods=["POST"])
def return_report(name, reason):
    doc = _report(name)
    _authorized_station(doc.station, manager_only=True)
    if doc.status != "Submitted":
        frappe.throw("Only submitted reports can be returned.")
    reason = (reason or "").strip()
    if len(reason) < 5:
        frappe.throw("Provide a reason for returning the report (at least five characters).")
    doc.flags.station_workflow_action = True
    doc.status = "Returned"
    doc.return_reason = reason[:1000]
    doc.save(ignore_permissions=True)
    close_alert("APPROVAL:" + doc.name)
    return doc.name

@frappe.whitelist(methods=["POST"])
def resolve_alert(name):
    _require_login()
    alert = frappe.get_doc("Gas Station Alert", name)
    _authorized_station(alert.station, manager_only=True)
    if alert.status == "Open":
        close_alert(alert.alert_key)
    return name
