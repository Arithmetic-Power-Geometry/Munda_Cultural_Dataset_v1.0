import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data" / "source_census" / "census_2011_st15_jharkhand_metadata_audit_run319_2026-09-14.json"
SEARCH_LOG = ROOT / "data" / "source_census" / "search_log_run319.jsonl"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_st15_metadata_verified_without_numeric_promotion():
    audit = load_json(AUDIT)
    assert audit["run"] == 319
    assert audit["reference_id"] == "PC11_ST15-20"
    assert audit["declared_download"] == "ST-20-00-15-DDW-2011.XLSX"
    assert audit["authority"] == "Office of the Registrar General & Census Commissioner, India"

    metadata = audit["catalogue_metadata"]
    assert metadata["munda_patar_tribe_row_declared"] is True
    assert metadata["munda_mother_tongue_code_declared"] == "91"
    assert metadata["mundari_mother_tongue_code_declared"] == "92"
    assert metadata["mundari_named_row_declared"] is True

    verification = audit["verification"]
    assert verification["catalogue_identity_verified"] is True
    assert verification["declared_workbook_filename_verified"] is True
    assert verification["table_schema_verified_from_catalogue_metadata"] is True
    assert verification["workbook_bytes_acquired"] is False
    assert verification["independent_hash_verified"] is False
    assert verification["sheet_inventory_verified"] is False
    assert verification["exact_numeric_cells_verified"] is False

    promotion = audit["promotion"]
    assert promotion["numeric_claims_promoted"] == 0
    assert promotion["cultural_claims_promoted"] == 0
    assert promotion["community_validation_claims_promoted"] == 0
    assert promotion["controlled_source_count_increment"] == 0
    assert promotion["controlled_claim_count_increment"] == 0
    assert promotion["controlled_evidence_record_increment"] == 0
    assert promotion["controlled_provenance_link_increment"] == 0

    governance = audit["rights_governance"]
    assert governance["public_catalogue_visibility_not_treated_as_reuse_permission"] is True
    assert governance["community_validation_not_inferred"] is True
    assert governance["cultural_access_authorization_not_inferred"] is True
    assert governance["cultural_access_overrides_entitlement"] is True


def test_run319_refreshes_all_controlled_source_classes():
    rows = [json.loads(line) for line in SEARCH_LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(rows) == 14
    assert {row["source_class"] for row in rows} == {
        "books", "dictionaries", "grammars", "peer-reviewed articles",
        "theses/dissertations", "government/TRI/Census/LSI", "archives",
        "newspapers", "web resources", "datasets", "audio", "video",
        "maps", "relevant media"
    }
