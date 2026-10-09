import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/unicode_nag_mundari_exact_locator_run191_2026-09-11.json"
SEARCH = ROOT / "data/source_census/search_log_run191.jsonl"
STATUS = ROOT / "status/mlhkp_progress.json"


def test_run191_unicode_primary_standard_exact_locator_and_rights_boundary():
    a = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert a["identity"]["standard"] == "The Unicode Standard, Version 17.0"
    assert a["identity"]["block"] == "Nag Mundari"
    assert a["identity"]["range"] == "U+1E4D0-U+1E4FF"
    assert a["verification"]["primary_unicode_pdf_opened"] is True
    assert a["verification"]["page_image_checked"] is True
    assert a["verification"]["digits_verified"]["start"].startswith("U+1E4F0")
    assert a["verification"]["digits_verified"]["end"].startswith("U+1E4F9")
    assert a["rights_and_access"]["public_redistribution_of_chart_assumed_permitted"] is False
    assert a["rights_and_access"]["chart_or_font_bytes_ingested"] is False
    assert a["scope_classification"]["cultural_claim"] is False
    assert a["scope_classification"]["participant_derived"] is False
    assert a["promotion"]["count_bearing"] is False
    assert a["promotion"]["claims_added"] == 0
    assert a["promotion"]["evidence_records_added"] == 0
    assert a["integrity"]["independent_checksum_verified"] is False


def test_run191_all_requested_source_classes_logged_without_inflation():
    row = json.loads(SEARCH.read_text(encoding="utf-8").strip())
    required = {
        "books", "dictionaries", "grammars", "peer-reviewed articles",
        "theses/dissertations", "government/TRI/Census/LSI materials",
        "archives", "newspapers/periodicals", "web resources", "datasets",
        "audio", "video", "maps", "relevant media",
    }
    assert required.issubset(set(row["source_classes"]))
    assert row["mmsc_count_change"] == 0
    assert row["source_identity_count_change"] == 0
    assert row["claim_count_change"] == 0
    assert row["evidence_count_change"] == 0
    assert row["absolute_or_future_proof_completeness_claimed"] is False
    assert row["release_gate"] == "NOT_PASS"


def test_run191_status_keeps_audited_release_gate_open_until_full_sync():
    s = json.loads(STATUS.read_text(encoding="utf-8"))
    assert s["latest_run"] >= 190
    assert s["mmsc"]["audited_source_identities"] == 42
    assert s["mmsc"]["unresolved_unique_web_leads"] == 73
    assert s["evidence_and_schema"]["source_claims"] == 52
    assert s["release_gate"]["status"] == "NOT_PASS"
