"""Disposable Frappe Bench smoke test. Run ONLY on an isolated evaluation site."""
import frappe
from frappe.utils import today

from gas_station_mis.api import approve_report, return_report, submit_report


def run():
    """Bench: bench --site test_site execute gas_station_mis.smoke.run"""
    required = (
        "Gas Station", "Gas Station Staff Assignment",
        "Gas Station Shift Schedule", "Gas Station Shift Report", "Gas Station Alert",
        "Employee",
    )
    missing = [doctype for doctype in required if not frappe.db.exists("DocType", doctype)]
    if missing:
        raise AssertionError("Missing installed DocTypes: " + ", ".join(missing))

    # ERPNext's setup wizard normally seeds this type; a bare CI site may not.
    if not frappe.db.exists("Warehouse Type", "Transit"):
        frappe.get_doc({"doctype": "Warehouse Type", "name": "Transit"}).insert(ignore_permissions=True)

    company = frappe.db.get_value("Company", {}, "name")
    if not company:
        company = frappe.get_doc({
            "doctype": "Company",
            "company_name": "Station Integration Test Company",
            "abbr": "SIT",
            "country": "Rwanda",
            "default_currency": "RWF",
        }).insert(ignore_permissions=True).name

    station = frappe.get_doc({
        "doctype": "Gas Station",
        "station_name": "Smoke Test Station",
        "company": company,
        "cash_variance_threshold": 100,
    }).insert(ignore_permissions=True)

    schedule = frappe.get_doc({
        "doctype": "Gas Station Shift Schedule",
        "station": station.name,
        "shift_name": "Smoke Test Closing",
        "end_time": "22:00:00",
        "grace_minutes": 45,
    }).insert(ignore_permissions=True)

    report = frappe.get_doc({
        "doctype": "Gas Station Shift Report",
        "station": station.name,
        "shift_schedule": schedule.name,
        "report_date": today(),
        "status": "Draft",
        "opening_cash": 1000,
        "cash_sales": 400,
        "mobile_money_sales": 200,
        "card_sales": 100,
        "cash_expenses": 50,
        "cash_removed": 250,
        "counted_cash": 1100,
        "notes": "Integration smoke-test shift",
    }).insert(ignore_permissions=True)

    assert float(report.total_sales) == 700.0
    assert float(report.expected_closing_cash) == 1100.0
    assert float(report.cash_difference) == 0.0

    submit_report(report.name)
    assert frappe.db.get_value("Gas Station Shift Report", report.name, "status") == "Submitted"
    return_report(report.name, "Add the supervisor summary")
    assert frappe.db.get_value("Gas Station Shift Report", report.name, "status") == "Returned"
    revision = frappe.get_doc("Gas Station Shift Report", report.name)
    revision.notes = "Revised supervisor summary"
    revision.save(ignore_permissions=True)
    submit_report(report.name)
    approve_report(report.name)
    assert frappe.db.get_value("Gas Station Shift Report", report.name, "status") == "Approved"

    locked = frappe.get_doc("Gas Station Shift Report", report.name)
    locked.notes = "This modification must not succeed"
    try:
        locked.save(ignore_permissions=True)
    except frappe.ValidationError:
        pass
    else:
        raise AssertionError("Approved report was unexpectedly editable")

    approval_alert = frappe.db.get_value(
        "Gas Station Alert",
        {"alert_key": "APPROVAL:" + report.name},
        "status",
    )
    assert approval_alert == "Resolved", f"Unexpected approval alert: {approval_alert}"
    print("Gas Station MIS live smoke test PASSED")
    return {"station": station.name, "report": report.name, "status": "passed"}
