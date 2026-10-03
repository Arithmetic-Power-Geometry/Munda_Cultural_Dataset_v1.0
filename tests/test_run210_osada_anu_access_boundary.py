import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/osada_2008_mundari_chapter_and_anu_access_boundary_run210_2026-09-11.json"
LOG = ROOT / "data/source_census/search_log_run210.jsonl"


def test_run210_osada_2008_exact_range_without_claim_promotion():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    osada = data["records"]["osada_2008_mundari_chapter"]
    ver = data["verification"]
    assert data["run"] == 210
    assert osada["pages"] == "99-164"
    assert osada["glottolog_reference_id"] == "477414"
    assert osada["grambank_locator_reconciled"] == "Osada 2008: 107-108"
    assert ver["osada_2008_chapter_range_verified"] is True
    assert ver["grambank_107_108_range_containment_verified"] is True
    assert ver["osada_2008_pages_107_108_directly_verified"] is False
    assert ver["linguistic_claim_promoted"] is False
    assert ver["cultural_claim_promoted"] is False
    assert ver["count_bearing_registration_performed"] is False


def test_run210_anu_access_boundaries():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    art2005 = data["records"]["evans_osada_2005_word_classes"]
    art2011 = data["records"]["evans_osada_2011_reciprocals"]
    gov = data["rights_access_consent_cultural_governance"]
    assert art2005["doi"] == "10.1515/lity.2005.9.3.351"
    assert art2005["anu_handle"] == "1885/54663"
    assert art2005["anu_access_statement_observed"] == "Open Access"
    assert art2005["direct_pdf_bytes_acquired"] is False
    assert art2011["anu_handle"] == "1885/24925"
    assert art2011["repository_restriction_observed_until"] == "2037-12-31"
    assert gov["restricted_2011_files_circumvented"] is False
    assert gov["unauthorized_mirrors_used_for_evidence"] is False
    assert gov["participant_consent_inferred"] is False
    assert gov["community_validation_inferred"] is False
    assert gov["cultural_access_permission_inferred"] is False


def test_run210_all_requested_source_classes_logged_and_counts_frozen():
    row = json.loads(LOG.read_text(encoding="utf-8").strip())
    expected = {
        "books", "dictionaries", "grammars", "peer-reviewed articles",
        "theses/dissertations", "government/TRI/Census/LSI", "archives",
        "newspapers/periodicals", "web resources", "datasets", "audio",
        "video", "maps", "relevant media"
    }
    assert row["search_id"] == "MMSC-SEARCH-000210"
    assert expected.issubset(set(row["classes"]))
    assert row["counts_changed"] is False
    assert row["audited_source_identities"] == 42
    assert row["unresolved_unique_web_leads"] == 73
    assert row["source_claims"] == 52
    assert row["evidence_records"] == 52
    assert row["evidence_links"] == 52
    assert row["streamlit_modules"] == 42
    assert row["cultural_claims_added"] == 0
    assert row["linguistic_claims_added"] == 0
