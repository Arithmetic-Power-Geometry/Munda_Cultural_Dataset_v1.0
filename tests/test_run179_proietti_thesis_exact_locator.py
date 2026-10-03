import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/proietti_2025_adivasi_women_thesis_exact_locator_run179_2026-09-11.json"
LOG = ROOT / "data/source_census/search_log_run179.jsonl"
STATUS = ROOT / "status/mlhkp_progress.json"


def test_run179_proietti_identity_and_boundaries():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert data["run"] == 179
    assert data["identity"]["author"] == "Marilena Proietti"
    assert data["identity"]["handle_national_repository"] == "20.500.14242/212639"
    assert data["identity"]["handle_institutional_repository"] == "11573/1740709"
    assert data["identity"]["nbn"] == "URN:NBN:IT:UNIROMA1-212639"
    assert data["manifestation"]["open_access_from"] == "2026-05-27"
    assert data["manifestation"]["exact_cc_variant_verified"] is False
    assert data["manifestation"]["bytes_acquired"] is False
    assert data["manifestation"]["independent_checksum_computed"] is False
    assert data["manifestation"]["page_level_locators_verified"] is False
    assert data["promotion"]["cultural_claims_promoted"] == 0
    assert data["promotion"]["participant_records_ingested"] == 0
    gates = data["rights_consent_cultural_access"]
    assert gates["community_validation_inferred"] is False
    assert gates["participant_consent_inferred"] is False
    assert gates["cultural_access_permission_inferred"] is False
    assert data["deduplication"]["new_permanent_mmsc_identity_created"] is False


def test_run179_search_log_covers_all_required_classes():
    rows = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    classes = {row["class"] for row in rows}
    required = {
        "books_dictionaries_grammars", "peer_reviewed_articles", "theses_dissertations",
        "government_tri_census_lsi", "archives", "newspapers_periodicals",
        "web_resources", "datasets", "audio", "video", "maps", "relevant_media"
    }
    assert required <= classes
    assert all(row["search_id"] == "MMSC-SEARCH-000179" for row in rows)


def test_run179_no_count_inflation():
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    assert status["mmsc"]["audited_source_identities"] == 42
    assert status["mmsc"]["raw_web_discovery_records"] == 90
    assert status["mmsc"]["unique_web_discovery_leads"] == 87
    assert status["mmsc"]["duplicate_web_records"] == 3
    assert status["mmsc"]["canonicalized_unique_web_leads"] == 14
    assert status["mmsc"]["unresolved_unique_web_leads"] == 73
    assert status["evidence_and_schema"]["source_claims"] == 52
    assert status["evidence_and_schema"]["evidence_records"] == 52
    assert status["evidence_and_schema"]["evidence_links"] == 52
