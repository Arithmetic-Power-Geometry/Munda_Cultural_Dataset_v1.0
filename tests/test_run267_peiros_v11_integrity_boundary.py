import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/lexibank_peiros_mundari_version_integrity_locator_run267_2026-09-12.json"
LOG = ROOT / "data/source_census/search_log_run267.jsonl"


def test_run267_peiros_release_is_pinned_and_mundari_locator_exact():
    d = json.loads(AUDIT.read_text(encoding="utf-8"))
    src = d["source"]
    assert src["release_tag"] == "v1.1"
    assert src["release_doi"] == "10.5281/zenodo.13168443"
    assert src["tag_commit_sha"] == "b4d2e4dcee173494c90328f7cafd78c9851c0956"
    assert src["license"] == "CC-BY-4.0"
    loc = d["exact_mundari_language_locator"]
    assert loc["primary_key"] == "Mundari"
    assert loc["row_values"]["Glottocode"] == "mund1320"
    assert loc["row_values"]["ISO639P3code"] == "unr"
    assert loc["row_values"]["SubGroup"] == "MUNDA"


def test_run267_pins_cldf_blob_integrity_without_lexical_promotion():
    d = json.loads(AUDIT.read_text(encoding="utf-8"))
    i = d["release_integrity_locators"]
    assert i["forms_table"]["git_blob_sha"] == "28f882e317c2caeb8c112e3b60ae2d8c1c8b9ab5"
    assert i["forms_table"]["bytes"] == 1092739
    assert i["forms_table"]["declared_rows"] == 10706
    assert i["languages_table"]["declared_rows"] == 109
    assert d["rights_and_cultural_boundary"]["lexical_forms_promoted"] == 0
    assert d["rights_and_cultural_boundary"]["cultural_claims_promoted"] == 0
    assert d["rights_and_cultural_boundary"]["participant_consent_inferred"] is False
    assert d["rights_and_cultural_boundary"]["community_validation_inferred"] is False
    assert d["rights_and_cultural_boundary"]["cultural_access_permission_inferred"] is False


def test_run267_search_log_covers_all_controlled_classes():
    rows = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    expected = {
        "books", "dictionaries", "grammars", "peer_reviewed_articles",
        "theses_dissertations", "government_TRI_Census_LSI", "archives",
        "newspapers_periodicals", "web_resources", "datasets", "audio",
        "video", "maps", "relevant_media",
    }
    assert {r["class"] for r in rows} == expected
    assert all(r["search_id"] == "MMSC-SEARCH-000267" for r in rows)
