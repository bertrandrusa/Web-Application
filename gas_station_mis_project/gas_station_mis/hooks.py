app_name = "gas_station_mis"
app_title = "Gas Station MIS"
app_publisher = "Gas Station MIS Contributors"
app_description = "Shift close reporting, approvals, dashboards, and operational alerts"
app_email = "maintainers@example.invalid"
app_license = "MIT"

required_apps = ["erpnext", "hrms"]

before_install = "gas_station_mis.install.ensure_roles"
after_install = "gas_station_mis.install.ensure_roles"

scheduler_events = {
    "hourly": ["gas_station_mis.tasks.check_missing_shift_reports"],
}

permission_query_conditions = {
    "Gas Station": "gas_station_mis.permissions.station_query",
    "Gas Station Shift Schedule": "gas_station_mis.permissions.schedule_query",
    "Gas Station Shift Report": "gas_station_mis.permissions.report_query",
    "Gas Station Alert": "gas_station_mis.permissions.alert_query",
}

has_permission = {
    "Gas Station": "gas_station_mis.permissions.station_permission",
    "Gas Station Staff Assignment": "gas_station_mis.permissions.assignment_permission",
    "Gas Station Shift Schedule": "gas_station_mis.permissions.schedule_permission",
    "Gas Station Shift Report": "gas_station_mis.permissions.report_permission",
    "Gas Station Alert": "gas_station_mis.permissions.alert_permission",
}
