"""Shared top-level quality status contract."""

from __future__ import annotations

from typing import Any, Iterable

PASS = "PASS"
WARN = "WARN"
FAIL = "FAIL"
BLOCKED = "BLOCKED"
DATA_PENDING = "DATA_PENDING"
STATUSES = frozenset({PASS, WARN, FAIL, BLOCKED, DATA_PENDING})


def assess_reports(reports: Iterable[Any]) -> tuple[str, list[str]]:
    """Assess completed reports without conflating source health with quality.

    A returned report is PASS unless it carries explicit source errors or
    warnings. FAIL, BLOCKED, and DATA_PENDING remain part of the shared
    contract for callers that do not produce a completed report.
    """
    report_list = list(reports)
    if not report_list:
        return BLOCKED, ["no_completed_report"]

    reasons: list[str] = []
    error_sources: set[str] = set()
    warning_count = 0
    for report in report_list:
        error_sources.update(str(name) for name in (getattr(report, "errors_by_source", {}) or {}))
        warning_count += len(getattr(report, "warnings", []) or [])

    if error_sources:
        reasons.append("source_errors:" + ",".join(sorted(error_sources)))
    if warning_count:
        reasons.append(f"warnings:{warning_count}")
    return (WARN, reasons) if reasons else (PASS, [])
