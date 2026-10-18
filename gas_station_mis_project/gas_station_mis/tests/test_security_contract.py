"""Static safety and integration-contract tests; Frappe itself is not simulated."""
import ast
from pathlib import Path
from unittest import TestCase

SRC = Path(__file__).resolve().parents[1]

def methods(path):
    unit = ast.parse((SRC / path).read_text(encoding="utf-8"))
    return {node.name: node for node in unit.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}

class TestSecurityContracts(TestCase):
    def test_permission_handlers_accept_frappe_ptype(self):
        registry = methods("permissions.py")
        for name in ("station_permission", "assignment_permission", "schedule_permission",
                     "report_permission", "alert_permission"):
            with self.subTest(name=name):
                args = [arg.arg for arg in registry[name].args.args]
                self.assertIn("ptype", args)
                self.assertIn("user", args)
                self.assertIsNotNone(registry[name].args.kwarg)

    def test_permission_query_hooks_allow_doctype_kwargs(self):
        registry = methods("permissions.py")
        for name in ("station_query", "schedule_query", "report_query", "alert_query"):
            with self.subTest(name=name):
                self.assertIsNotNone(registry[name].args.kwarg)

    def test_workflow_mutation_endpoints_are_post_only(self):
        registry = methods("api.py")
        for name in ("submit_report", "approve_report", "return_report", "resolve_alert"):
            with self.subTest(name=name):
                node = registry[name]
                self.assertTrue(any(
                    isinstance(d, ast.Call)
                    and getattr(d.func, "attr", "") == "whitelist"
                    and any(k.arg == "methods" and isinstance(k.value, ast.List)
                            and any(isinstance(v, ast.Constant) and v.value == "POST"
                                    for v in k.value.elts)
                            for k in d.keywords)
                    for d in node.decorator_list
                ))

    def test_report_mutation_has_validation(self):
        content = (SRC / "gas_station_mis/doctype/gas_station_shift_report/gas_station_shift_report.py").read_text()
        self.assertIn("get_doc_before_save()", content)
        self.assertIn("Approved reports are immutable", content)
        self.assertIn("def on_trash", content)
