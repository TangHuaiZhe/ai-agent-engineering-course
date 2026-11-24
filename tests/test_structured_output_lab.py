import json
import unittest

from examples.structured_output_lab import FAKE_SOURCES, validate_metric


class TestStructuredOutputLab(unittest.TestCase):
    def setUp(self):
        self.valid = dict(FAKE_SOURCES["fictional-report-2025-p42"])
        self.valid["source_id"] = "fictional-report-2025-p42"

    def reason(self, **changes):
        return validate_metric({**self.valid, **changes}, FAKE_SOURCES)[1]

    def test_valid_synthetic_record(self):
        self.assertEqual(self.reason(), "ok")

    def test_json_string_round_trip(self):
        self.assertEqual(validate_metric(json.dumps(self.valid), FAKE_SOURCES), (True, "ok"))

    def test_extra_field(self):
        self.assertEqual(self.reason(secret="something"), "wrong_fields")

    def test_missing_field(self):
        invalid = dict(self.valid)
        del invalid["source_id"]
        self.assertEqual(validate_metric(invalid, FAKE_SOURCES)[1], "wrong_fields")

    def test_boolean_not_integer(self):
        self.assertEqual(self.reason(fiscal_year=True), "invalid_year")

    def test_string_not_number(self):
        self.assertEqual(self.reason(value="120.5"), "invalid_value")

    def test_nonfinite_number(self):
        self.assertEqual(self.reason(value=float("nan")), "invalid_value")

    def test_invalid_json_constant(self):
        text = json.dumps(self.valid).replace("120.5", "NaN")
        self.assertEqual(validate_metric(text, FAKE_SOURCES)[1], "invalid_json")

    def test_unhashable_metric_type(self):
        self.assertEqual(self.reason(metric=["revenue"]), "invalid_metric")

    def test_unhashable_unit_type(self):
        self.assertEqual(self.reason(unit=["million"]), "invalid_unit")

    def test_nonfinite_large_integer(self):
        self.assertEqual(self.reason(value=10 ** 1000), "invalid_value")

    def test_wrong_currency(self):
        self.assertEqual(self.reason(currency="CNY"), "source_mismatch")

    def test_unknown_currency(self):
        self.assertEqual(self.reason(currency="BTC"), "invalid_currency")

    def test_wrong_company(self):
        self.assertEqual(self.reason(company="Other Co."), "source_mismatch")

    def test_wrong_value_even_if_schema_valid(self):
        self.assertEqual(self.reason(value=999.0), "source_mismatch")

    def test_source_missing(self):
        self.assertEqual(self.reason(source_id="invented-source"), "source_not_found")

    def test_list_is_not_record(self):
        self.assertEqual(validate_metric([], FAKE_SOURCES)[1], "not_object")


if __name__ == "__main__":
    unittest.main()
