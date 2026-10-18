"""Station-scoped authorization for every station document and API."""
import frappe

MANAGEMENT = {"Manager"}
REPORTERS = {"Manager", "Supervisor"}

def is_system_manager(user=None):
    user = user or frappe.session.user
    return user == "Administrator" or "System Manager" in frappe.get_roles(user)

def membership_roles(station, user=None):
    user = user or frappe.session.user
    if not station or user == "Guest":
        return set()
    return {
        row.station_role
        for row in frappe.get_all(
            "Gas Station Staff Assignment",
            filters={"station": station, "user": user, "enabled": 1},
            fields=["station_role"],
        )
    }

def can_manage(station, user=None):
    return is_system_manager(user) or bool(membership_roles(station, user) & MANAGEMENT)

def can_report(station, user=None):
    return is_system_manager(user) or bool(membership_roles(station, user) & REPORTERS)

def permitted_stations(user=None, roles=None):
    user = user or frappe.session.user
    if user == "Guest":
        return []
    if is_system_manager(user):
        return frappe.get_all("Gas Station", pluck="name")
    filters = {"user": user, "enabled": 1}
    if roles:
        filters["station_role"] = ["in", list(roles)]
    return list(set(frappe.get_all("Gas Station Staff Assignment", filters=filters, pluck="station")))

def _condition(doctype, fieldname, user, roles=None):
    user = user or frappe.session.user
    if is_system_manager(user):
        return None
    stations = permitted_stations(user, roles)
    if not stations:
        return "1=0"
    names = ", ".join(frappe.db.escape(s) for s in stations)
    return f"`tab{doctype}`.`{fieldname}` IN ({names})"

def station_query(user=None, **kwargs):
    return _condition("Gas Station", "name", user)

def schedule_query(user=None, **kwargs):
    return _condition("Gas Station Shift Schedule", "station", user)

def report_query(user=None, **kwargs):
    return _condition("Gas Station Shift Report", "station", user, REPORTERS)

def alert_query(user=None, **kwargs):
    return _condition("Gas Station Alert", "station", user, MANAGEMENT)

def station_permission(doc, user=None, ptype=None, **kwargs):
    if is_system_manager(user):
        return True
    if ptype in ("read", "select", "print", "report", "export"):
        return bool(membership_roles(doc.name, user))
    return False

def assignment_permission(doc, user=None, ptype=None, **kwargs):
    return is_system_manager(user)

def schedule_permission(doc, user=None, ptype=None, **kwargs):
    if is_system_manager(user):
        return True
    if ptype in ("read", "select", "print", "report", "export"):
        return bool(membership_roles(doc.station, user))
    return can_manage(doc.station, user) if ptype in ("create", "write") else False

def report_permission(doc, user=None, ptype=None, **kwargs):
    if is_system_manager(user):
        return True
    if ptype in ("read", "select", "print", "report", "export"):
        return can_report(doc.station, user)
    if ptype == "create":
        return can_report(doc.station, user)
    if ptype == "write":
        return can_report(doc.station, user) and doc.status in ("Draft", "Returned")
    return False

def alert_permission(doc, user=None, ptype=None, **kwargs):
    if is_system_manager(user):
        return True
    return ptype in ("read", "select", "print", "report", "export") and can_manage(doc.station, user)
