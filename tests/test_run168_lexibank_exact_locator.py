import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/lexibank_peiros_mundari_exact_locator_run168_2026-09-10.json"
LOG = ROOT / "data/source_census/search_log_run168.jsonl"


def test_run168_lexibank_exact_locator_and_rights_boundary():
    d = json.loads(AUDIT.read_text(encoding="utf-8"))
    s = d["source"]
    assert d["branch"] == "mlhkp-v2"
    assert s["language_name"] == "Mundari"
    assert s["glottocode"] == "mund1320"
    assert s["iso639_3"] == "unr"
    assert s["zenodo_doi"] == "10.5281/zenodo.5127536"
    assert s["version"] == "v1.0"
    assert s["database_license"] == "CC BY 4.0"
    assert d["promotion"]["dataset_rows_ingested"] is False
    assert d["promotion"]["lexical_forms_ingested"] is False
    assert d["promotion"]["cultural_claims_added"] == 0
    assert d["promotion"]["counts_changed"] is False
    r = d["rights_and_uncertainty"]
    assert r["underlying_source_rights_inferred"] is False
    assert r["participant_consent_inferred"] is False
    assert r["community_validation_inferred"] is False
    assert r["cultural_access_permission_inferred"] is False


def test_run168_requested_source_classes_logged():
    rows = [json.loads(x) for x in LOG.read_text(encoding="utf-8").splitlines() if x.strip()]
    classes = {r.get("class") for r in rows}
    expected = {
        "books_dictionaries_grammars", "peer_reviewed_articles", "theses_dissertations",
        "government_tri_census_lsi", "archives", "newspapers_periodicals", "web_resources",
        "datasets", "audio", "video", "maps", "relevant_media"
    }
    assert expected <= classes
