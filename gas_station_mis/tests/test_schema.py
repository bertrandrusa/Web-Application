"""Dependency-free checks for the project's persisted Frappe metadata."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1] / "gas_station_mis" / "doctype"

class TestSchema(unittest.TestCase):
    def test_doctypes_have_controllers_and_metadata(self):
        expected = [
            "gas_station", "gas_station_staff_assignment",
            "gas_station_shift_schedule", "gas_station_shift_report", "gas_station_alert"
        ]
        for slug in expected:
            with self.subTest(doctype=slug):
                path = ROOT / slug
                metadata = json.loads((path / (slug + ".json")).read_text())
                self.assertEqual(metadata["doctype"], "DocType")
                self.assertTrue((path / (slug + ".py")).is_file())
                self.assertEqual(len(metadata["field_order"]), len(set(metadata["field_order"])))
                self.assertEqual(
                    set(metadata["field_order"]),
                    {field["fieldname"] for field in metadata["fields"]}
                )

    def test_report_workflow_fields_exist(self):
        data = json.loads(
            (ROOT / "gas_station_shift_report" / "gas_station_shift_report.json").read_text()
        )
        fields = {x["fieldname"]: x for x in data["fields"]}
        self.assertIn("Submitted", fields["status"]["options"])
        self.assertIn("Approved", fields["status"]["options"])
        self.assertIn("cash_difference", fields)
        self.assertIn("approved_by", fields)

    def test_alert_deduplication_is_unique(self):
        data = json.loads(
            (ROOT / "gas_station_alert" / "gas_station_alert.json").read_text()
        )
        fields = {x["fieldname"]: x for x in data["fields"]}
        self.assertTrue(fields["alert_key"].get("unique"))
if __name__ == "__main__":
    unittest.main()
