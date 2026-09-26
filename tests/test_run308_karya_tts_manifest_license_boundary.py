import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data" / "source_census" / "karya_mundari_tts_manifest_license_audit_run308_2026-09-13.json"
SEARCH_LOG = ROOT / "data" / "source_census" / "search_log_run308.jsonl"


def _audit():
    return json.loads(AUDIT.read_text(encoding="utf-8"))


def test_run308_exact_manifest_and_declared_checksum_locator():
    d = _audit()
    assert d["canonical_source"]["repository"] == "karya-inc/dataset-mundari-tts"
    assert d["publisher_declared_corpus_metadata"]["utterances"] == 26870
    assert d["publisher_declared_corpus_metadata"]["speakers"] == 2
    assert d["publisher_declared_corpus_metadata"]["speaker_breakdown"] == {"female": 19868, "male": 7002}
    assert d["first_party_exact_locators"]["sample_archive"] == "data-sample.tgz"
    assert d["first_party_exact_locators"]["full_archive_declared_filename"] == "dataset-mundari-tts-full.tgz"
    assert d["first_party_exact_locators"]["publisher_declared_sha1"] == "46c8bfceb5cf25decc8523479378793537f2bad7"


def test_run308_rights_and_participant_boundary_is_not_collapsed():
    d = _audit()
    b = d["license_boundary"]
    v = d["verification_boundary"]
    assert b["verified_from_repository_license_text"] is True
    assert b["participant_consent_inferred"] is False
    assert b["community_validation_inferred"] is False
    assert b["cultural_access_permission_inferred"] is False
    assert b["commercial_permission_inferred"] is False
    assert v["full_archive_bytes_independently_acquired"] is False
    assert v["full_archive_sha1_independently_recomputed"] is False
    assert v["sample_audio_or_transcript_content_promoted"] is False
    assert v["linguistic_claims_promoted"] == 0
    assert v["cultural_claims_promoted"] == 0
    assert v["controlled_evidence_records_promoted"] == 0
    assert v["controlled_provenance_links_promoted"] == 0


def test_run308_is_count_neutral_until_numbered_register_reconciliation():
    d = _audit()
    c = d["deduplication_and_counting"]
    assert c["numbered_web_mun_reconciliation_complete"] is False
    assert c["new_audited_source_identity_counted"] is False
    assert "count-neutral" in c["count_effect"]


def test_run308_search_log_covers_all_controlled_classes():
    rows = [json.loads(line) for line in SEARCH_LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(rows) == 14
    assert {r["class"] for r in rows} == {
        "books", "dictionaries", "grammars", "peer_reviewed_articles",
        "theses_dissertations", "government_TRI_Census_LSI", "archives",
        "newspapers", "web_resources", "datasets", "audio", "video",
        "maps", "relevant_media"
    }
