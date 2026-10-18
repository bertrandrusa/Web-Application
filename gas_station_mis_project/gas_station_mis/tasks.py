"""Hourly check for configured shift-close deadlines (site timezone)."""
from datetime import timedelta
from gas_station_mis.logic import report_deadline

import frappe
from frappe.utils import getdate, get_datetime, now_datetime

from gas_station_mis.alerts import create_alert

def missing_key(station, schedule, date):
    return f"MISSING:{station}:{schedule}:{getdate(date).isoformat()}"

def check_missing_shift_reports():
    now = now_datetime()
    schedules = frappe.get_all(
        "Gas Station Shift Schedule",
        filters={"enabled": 1},
        fields=["name", "station", "shift_name", "end_time", "grace_minutes", "creation"],
    )
    for schedule in schedules:
        if not frappe.db.get_value("Gas Station", schedule.station, "active"):
            continue
        for days_ago in (1, 0):
            day = getdate(now) - timedelta(days=days_ago)
            due = report_deadline(day, str(schedule.end_time), schedule.grace_minutes or 0)
            if now < due or get_datetime(schedule.creation) > due:
                continue
            submitted = frappe.db.exists(
                "Gas Station Shift Report",
                {
                    "station": schedule.station,
                    "shift_schedule": schedule.name,
                    "report_date": day,
                    "status": ["in", ["Submitted", "Approved", "Returned"]],
                },
            )
            if not submitted:
                create_alert(
                    schedule.station,
                    missing_key(schedule.station, schedule.name, day),
                    "Missing Report",
                    f"{schedule.shift_name} report for {day.isoformat()} is overdue.",
                )
