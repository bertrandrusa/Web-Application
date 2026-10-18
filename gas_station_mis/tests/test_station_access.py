"""Offline authorization policy tests using a minimal Frappe shim.

These tests verify function-level logic, not real Frappe DB permission enforcement.
"""
import importlib.util
import sys
import types
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

PERMISSIONS = Path(__file__).resolve().parents[1] / "permissions.py"

class TestStationPermissions(TestCase):
    def setUp(self):
        frappe = types.ModuleType("frappe")
        frappe.session = types.SimpleNamespace(user="manager-a")
        frappe.get_roles = lambda user: ["System Manager"] if user == "admin" else ["Gas Station User"]
        frappe.db = types.SimpleNamespace(escape=lambda text: "'" + text.replace("'", "''") + "'")
        memberships = [
            ("manager-a", "Station A", "Manager"),
            ("supervisor-a", "Station A", "Supervisor"),
            ("manager-b", "Station B", "Manager"),
            ("disabled", "Station A", "Manager"),
        ]
        def get_all(doctype, filters=None, pluck=None, fields=None):
            filters = filters or {}
            if doctype == "Gas Station":
                return ["Station A", "Station B"]
            self.assertEqual(doctype, "Gas Station Staff Assignment")
            items = []
            for user, station, role in memberships:
                if user == "disabled":
                    continue
                if "user" in filters and user != filters["user"]:
                    continue
                if "station" in filters and station != filters["station"]:
                    continue
                if "station_role" in filters and role not in filters["station_role"][1]:
                    continue
                if fields:
                    items.append(types.SimpleNamespace(station_role=role))
                else:
                    items.append(station)
            return items
        frappe.get_all = get_all
        with patch.dict(sys.modules, {"frappe": frappe}):
            spec = importlib.util.spec_from_file_location("station_permissions_under_test", PERMISSIONS)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        self.perms = module

    def test_management_scoped_to_one_station(self):
        self.assertTrue(self.perms.can_manage("Station A", "manager-a"))
        self.assertFalse(self.perms.can_manage("Station B", "manager-a"))
        self.assertFalse(self.perms.can_manage("Station A", "supervisor-a"))
        self.assertFalse(self.perms.can_manage("Station A", "disabled"))

    def test_reporter_can_submit_but_not_approve(self):
        self.assertTrue(self.perms.can_report("Station A", "supervisor-a"))
        self.assertFalse(self.perms.can_manage("Station A", "supervisor-a"))

    def test_system_manager_can_manage_all(self):
        self.assertTrue(self.perms.can_manage("Station B", "admin"))
        self.assertEqual(self.perms.report_query("admin"), None)

    def test_query_restricts_to_assigned_station(self):
        query = self.perms.report_query("manager-a", doctype="Gas Station Shift Report")
        self.assertIn("'Station A'", query)
        self.assertNotIn("'Station B'", query)
        self.assertEqual(self.perms.report_query("disabled"), "1=0")
