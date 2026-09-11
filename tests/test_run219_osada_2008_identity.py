import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/osada_2008_mundari_chapter_identity_run219_2026-09-11.json"
LOG = ROOT / "data/source_census/search_log_run219.jsonl"


def test_run219_osada_2008_identity_boundary():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    src = data["source_identity"]
    rec = data["cross_resource_reconciliation"]
    ver = data["verification_boundary"]
    gov = data["rights_governance"]
    assert data["run"] == 219
    assert src["title"] == "Mundari"
    assert src["year"] == 2008
    assert src["pages"] == "99-164"
    assert src["glottolog_reference_id"] == "477414"
    assert rec["grambank_datapoint"] == "GB317-mund1320"
    assert rec["grambank_displayed_citation"] == "Osada 2008: 107-108"
    assert rec["pages_107_108_directly_inspected"] is False
    assert rec["underlying_proposition_promoted"] is False
    assert "1992" in rec["wals_separate_reference_observed"]
    assert ver["bibliographic_identity_verified"] is True
    assert ver["chapter_range_verified"] is True
    assert ver["pages_107_108_directly_verified"] is False
    assert ver["linguistic_claim_promoted_to_public_evidence_graph"] is False
    assert ver["source_identity_count_changed"] is False
    assert gov["book_or_chapter_full_text_open_license_inferred"] is False
    assert gov["community_validation_inferred"] is False
    assert gov["cultural_access_permission_inferred"] is False


def test_run219_counts_and_census_are_conservative():
    row = json.loads(LOG.read_text(encoding="utf-8").strip())
    expected = {
        "books", "dictionaries", "grammars", "peer-reviewed articles",
        "theses/dissertations", "government/TRI/Census/LSI", "archives",
        "newspapers/periodicals", "web resources", "datasets", "audio",
        "video", "maps", "relevant media"
    }
    assert row["search_id"] == "MMSC-SEARCH-000219"
    assert expected.issubset(set(row["classes"]))
    assert row["counts_changed"] is False
    assert row["audited_source_identities"] == 42
    assert row["raw_web_discovery_records"] == 90
    assert row["unique_web_discovery_leads"] == 87
    assert row["duplicate_web_records"] == 3
    assert row["canonicalized_unique_web_leads"] == 14
    assert row["unresolved_unique_web_leads"] == 73
    assert row["source_claims"] == 52
    assert row["evidence_records"] == 52
    assert row["evidence_links"] == 52
    assert row["streamlit_modules"] == 42
    assert row["cultural_claims_added"] == 0
    assert row["linguistic_claims_added"] == 0
    assert row["release_gate"] == "NOT_PASS"
