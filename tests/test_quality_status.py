"""Tests for the shared top-level quality contract."""

from lib import quality, schema


def _report(*, errors=None, warnings=None):
    return schema.Report(
        topic="quality contract",
        range_from="2026-07-01",
        range_to="2026-07-24",
        generated_at="2026-07-24T00:00:00+00:00",
        provider_runtime=schema.ProviderRuntime(
            reasoning_provider="local",
            planner_model="dummy",
            rerank_model="dummy",
        ),
        query_plan=schema.QueryPlan(
            intent="overview",
            freshness_mode="balanced_recent",
            cluster_mode="none",
            raw_topic="quality contract",
            subqueries=[],
            source_weights={},
        ),
        clusters=[],
        ranked_candidates=[],
        items_by_source={},
        errors_by_source=errors or {},
        warnings=warnings or [],
    )


def test_quality_status_vocabulary_is_stable():
    assert quality.STATUSES == {"PASS", "WARN", "FAIL", "BLOCKED", "DATA_PENDING"}


def test_completed_clean_report_passes():
    assert quality.assess_reports([_report()]) == ("PASS", [])


def test_report_source_errors_and_warnings_are_warn():
    status, reasons = quality.assess_reports(
        [_report(errors={"reddit": "dummy"}, warnings=["dummy warning"])]
    )
    assert status == "WARN"
    assert reasons == ["source_errors:reddit", "warnings:1"]


def test_missing_completed_report_is_blocked():
    assert quality.assess_reports([]) == ("BLOCKED", ["no_completed_report"])
