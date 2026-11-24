"""Lab 00: deterministic validation of model-like structured outputs.

This is NOT an LLM and the fixtures are fictional. No API key or third-party
dependencies are required.
"""

from __future__ import annotations

import json
import math
from collections.abc import Mapping
from typing import Any

FIELDS = frozenset(
    {"company", "fiscal_year", "metric", "value", "unit", "currency", "source_id"}
)
METRICS = frozenset({"revenue", "gross_profit", "net_income"})
CURRENCIES = frozenset({"CNY", "USD", "EUR"})
UNITS = frozenset({"million", "billion"})

# Fictional evidence catalog. The values have no relationship to any issuer.
FAKE_SOURCES: dict[str, dict[str, Any]] = {
    "fictional-report-2025-p42": {
        "company": "Example Inc.",
        "fiscal_year": 2025,
        "metric": "revenue",
        "value": 120.5,
        "unit": "million",
        "currency": "USD",
    }
}


def _bad_json_constant(value: str) -> None:
    raise ValueError(f"Non-JSON numeric constant: {value}")


def validate_metric(
    payload: str | Mapping[str, Any],
    trusted_sources: Mapping[str, Mapping[str, Any]],
) -> tuple[bool, str]:
    """Return (accepted, stable_reason_code), without pretending to validate the web.

    'trusted_sources' must come from a separate, independently verified source
    retrieval process. This teaching fixture is explicitly synthetic.
    """
    if isinstance(payload, str):
        try:
            data = json.loads(payload, parse_constant=_bad_json_constant)
        except (ValueError, TypeError):
            return False, "invalid_json"
    else:
        data = payload
    if not isinstance(data, Mapping):
        return False, "not_object"
    if set(data) != FIELDS:
        return False, "wrong_fields"
    if not isinstance(data["company"], str) or not data["company"].strip():
        return False, "invalid_company"
    if type(data["fiscal_year"]) is not int or not 1900 <= data["fiscal_year"] <= 2100:
        return False, "invalid_year"
    if not isinstance(data["metric"], str) or data["metric"] not in METRICS:
        return False, "invalid_metric"
    if type(data["value"]) not in (int, float):
        return False, "invalid_value"
    try:
        if not math.isfinite(data["value"]):
            return False, "invalid_value"
    except OverflowError:
        return False, "invalid_value"
    if not isinstance(data["unit"], str) or data["unit"] not in UNITS:
        return False, "invalid_unit"
    if not isinstance(data["currency"], str) or data["currency"] not in CURRENCIES:
        return False, "invalid_currency"
    if not isinstance(data["source_id"], str):
        return False, "invalid_source"
    source = trusted_sources.get(data["source_id"])
    if source is None:
        return False, "source_not_found"
    for key in FIELDS - {"source_id", "value"}:
        if data[key] != source.get(key):
            return False, "source_mismatch"
    expected_value = source.get("value")
    if type(expected_value) not in (int, float):
        return False, "source_mismatch"
    if not math.isclose(data["value"], expected_value, rel_tol=1e-10, abs_tol=1e-10):
        return False, "source_mismatch"
    return True, "ok"


if __name__ == "__main__":
    sample = dict(FAKE_SOURCES["fictional-report-2025-p42"])
    sample["source_id"] = "fictional-report-2025-p42"
    print(validate_metric(json.dumps(sample, ensure_ascii=False), FAKE_SOURCES))
