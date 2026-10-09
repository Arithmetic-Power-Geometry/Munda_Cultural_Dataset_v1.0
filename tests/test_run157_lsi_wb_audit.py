import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_run157_lsi_wb_exact_locator_and_rights_boundary():
    rec = load_json("data/source_census/lsi_west_bengal_part1_mundari_exact_locator_run157_2026-09-10.json")
    assert rec["audit_id"] == "MLHKP-LSI-WB-MUNDARI-RUN157"
    assert rec["source"]["official_catalogue_id"] == "34826"
    assert rec["source"]["official_download_id"] == "38514"
    assert rec["source"]["official_filename"] == "LSI_WB_PART_I.pdf"
    assert rec["exact_locator"]["indexed_heading"] == "MUNDARI"
    assert rec["exact_locator"]["printed_page"] == 44
    assert rec["verification"]["official_indexed_text_found"] is True
    assert rec["verification"]["official_pdf_bytes_acquired"] is False
    assert rec["verification"]["independent_checksum_computed"] is False
    assert rec["verification"]["pdf_page_image_inspected"] is False
    assert rec["rights_and_cultural_governance"]["full_text_redistribution_authorized"] is False
    assert rec["rights_and_cultural_governance"]["participant_level_material_ingested"] is False
    assert rec["rights_and_cultural_governance"]["community_validation_inferred"] is False
    assert rec["ingestion_decision"]["promote_to_claim_graph_this_run"] is False


def test_run157_search_log_covers_requested_classes_without_count_claims():
    lines = (ROOT / "data/source_census/search_log_run157.jsonl").read_text(encoding="utf-8").splitlines()
    rows = [json.loads(line) for line in lines if line.strip()]
    assert rows
    assert {row["search_id"] for row in rows} == {"MMSC-SEARCH-000157"}
    classes = {row["class"] for row in rows}
    required = {
        "books_grammars", "government_lsi", "government_tri", "peer_reviewed_articles",
        "datasets_audio", "audio_media", "video_media", "maps",
        "newspapers_periodicals", "theses_dissertations_archives"
    }
    assert required <= classes
