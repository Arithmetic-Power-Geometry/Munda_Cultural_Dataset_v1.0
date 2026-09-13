import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/scstrti_mundari_photo_handbook_exact_locator_run298_2026-09-13.json"
SEARCH = ROOT / "data/source_census/search_log_run298.jsonl"


def test_run298_exact_manifestation_and_boundary():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    work = data["canonical_work"]
    assert data["run_id"] == 298
    assert data["scope"] == "non-Mundarica"
    assert work["record_id"] == "SCST/2016/0055"
    assert work["handle"] == "123456789/73851"
    assert work["file_name"] == "SCST_2016_handbook_0055.pdf"
    assert work["declared_pagination"] == 28
    assert work["isbn_13"] == "978-93-80705-53-8"
    verification = data["verification"]
    assert verification["first_party_repository_search_result_verified"] is True
    assert verification["pdf_bytes_acquired"] is False
    assert verification["independent_sha256_computed"] is False
    assert verification["page_image_concordance_verified"] is False
    assert verification["ocr_verified"] is False
    assert verification["content_claims_promoted"] is False
    governance = data["rights_access_governance"]
    assert governance["participant_consent_inferred"] is False
    assert governance["community_validation_inferred"] is False
    assert governance["cultural_access_permission_inferred"] is False
    assert governance["cultural_claims_promoted"] is False
    assert data["deduplication"]["new_controlled_source_identity_counted"] is False
    assert data["promotion"]["controlled_claims_added"] == 0
    assert data["promotion"]["controlled_evidence_records_added"] == 0
    assert data["promotion"]["controlled_evidence_links_added"] == 0


def test_run298_search_log_has_all_required_classes_once():
    rows = [json.loads(line) for line in SEARCH.read_text(encoding="utf-8").splitlines() if line.strip()]
    required = {
        "books", "dictionaries", "grammars", "peer_reviewed_articles",
        "theses_dissertations", "government_TRI_Census_LSI", "archives",
        "newspapers_periodicals", "web_resources", "datasets", "audio",
        "video", "maps", "relevant_media"
    }
    classes = [row["class"] for row in rows]
    assert len(rows) == 14
    assert set(classes) == required
    assert len(classes) == len(set(classes))
    assert all(row["run_id"] == 298 for row in rows)
