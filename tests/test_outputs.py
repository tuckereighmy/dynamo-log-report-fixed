"""Verify the summary report described in instruction.md.

There is exactly one test per success criterion in instruction.md. Expected values
are hard-coded from /app/access.log rather than recomputed, so that a parsing bug
cannot appear in both the solution and the verifier and cancel itself out.

Ground truth for /app/access.log (6 non-blank lines):
  192.168.0.1 -> /index.html, /index.html
  192.168.0.2 -> /about.html, /index.html
  10.0.0.5    -> /api/login, /about.html
  paths: /index.html x3, /about.html x2, /api/login x1
"""

import json
from pathlib import Path

REPORT_PATH = Path("/app/report.json")

EXPECTED_TOTAL_REQUESTS = 6
EXPECTED_UNIQUE_IPS = 3
EXPECTED_TOP_PATH = "/index.html"


def _load_report():
    assert REPORT_PATH.exists(), f"no report found at {REPORT_PATH}"
    try:
        return json.loads(REPORT_PATH.read_text())
    except json.JSONDecodeError as exc:
        raise AssertionError(f"{REPORT_PATH} is not valid JSON: {exc}") from exc


def test_report_is_json_object_with_exactly_the_required_keys():
    """instruction.md: write /app/report.json as a single JSON object with exactly
    the keys total_requests, unique_ips and top_path, and no other keys."""
    report = _load_report()
    assert isinstance(report, dict), (
        f"report must be a JSON object, got {type(report).__name__}"
    )
    assert set(report) == {"total_requests", "unique_ips", "top_path"}, (
        f"expected exactly the keys total_requests, unique_ips, top_path; "
        f"got {sorted(report)}"
    )


def test_total_requests_counts_every_non_blank_line():
    """instruction.md: total_requests (integer) is the total number of requests,
    counting each non-blank line once and ignoring blank lines."""
    report = _load_report()
    value = report["total_requests"]
    assert isinstance(value, int) and not isinstance(value, bool), (
        f"total_requests must be an integer, got {type(value).__name__}"
    )
    assert value == EXPECTED_TOTAL_REQUESTS, (
        f"expected {EXPECTED_TOTAL_REQUESTS} requests, got {value}"
    )


def test_unique_ips_counts_distinct_clients():
    """instruction.md: unique_ips (integer) is the number of distinct client IP
    addresses, taken from the first field of each line."""
    report = _load_report()
    value = report["unique_ips"]
    assert isinstance(value, int) and not isinstance(value, bool), (
        f"unique_ips must be an integer, got {type(value).__name__}"
    )
    assert value == EXPECTED_UNIQUE_IPS, (
        f"expected {EXPECTED_UNIQUE_IPS} unique IPs, got {value}"
    )


def test_top_path_is_the_most_requested_path():
    """instruction.md: top_path (string) is the path requested most often, taken
    from the request line."""
    report = _load_report()
    value = report["top_path"]
    assert isinstance(value, str), (
        f"top_path must be a string, got {type(value).__name__}"
    )
    assert value == EXPECTED_TOP_PATH, (
        f"expected top_path {EXPECTED_TOP_PATH!r}, got {value!r}"
    )
