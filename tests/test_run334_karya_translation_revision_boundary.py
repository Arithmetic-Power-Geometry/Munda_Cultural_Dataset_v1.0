import json
from pathlib import Path


def test_run334_karya_fixed_revision_boundary():
    p = Path("audits/karya_hindi_mundari_fixed_revision_audit_run334_2026-09-14.json")
    data = json.loads(p.read_text(encoding="utf-8"))
    src = data["source"]
    ver = data["verification"]
    gov = data["rights_and_governance"]
    decision = data["promotion_decision"]

    assert src["repository_commit_sha"] == "243bb780906750fcf6e2b27693dd24898f0c79d1"
    assert src["manifestation_path"] == "translation-hi-unr.tsv"
    assert src["git_blob_sha"] == "131c55a5b8197a58d663a7e40d888a92869288c6"
    assert src["git_tree_reported_bytes"] == 3788450
    assert src["readme_declared_sentence_pairs"] == 17826

    assert ver["upstream_revision_pinned"] is True
    assert ver["independent_file_sha256_verified"] is False
    assert ver["independent_row_recount_verified"] is False
    assert gov["item_level_ingestion_authorized"] is False
    assert decision["exact_locator_promoted"] is True
    assert decision["dataset_rows_promoted"] is False
    assert decision["linguistic_claims_promoted"] is False
    assert decision["cultural_claims_promoted"] is False
    assert decision["controlled_counts_changed"] is False
