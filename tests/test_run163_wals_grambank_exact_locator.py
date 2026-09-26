import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/wals_grambank_mundari_typology_exact_locator_run163_2026-09-10.json"
LOG = ROOT / "data/source_census/search_log_run163.jsonl"


def test_run163_exact_locator_and_rights_boundary():
    d = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert d["branch"] == "mlhkp-v2"
    assert d["wals"]["wals_code"] == "mun"
    assert d["wals"]["iso_639_3"] == "unr"
    assert d["wals"]["exact_datapoint"]["locator"] == "https://wals.info/valuesets/83A-mun"
    assert d["wals"]["exact_datapoint"]["feature"] == "Order of Object and Verb"
    assert d["wals"]["exact_datapoint"]["value"] == "OV"
    assert set(d["wals"]["exact_datapoint"]["references_reported_by_wals"]) == {"Sinha 1975", "Osada 1992"}
    assert "Creative Commons Attribution 4.0" in d["wals"]["license"]
    assert "Creative Commons Attribution 4.0" in d["grambank"]["license"]
    assert d["rights_access_consent_cultural_uncertainty"]["underlying_grammar_fulltext_rights_inferred"] is False
    assert d["rights_access_consent_cultural_uncertainty"]["community_validation_inferred"] is False
    assert d["identity_reconciliation"]["counts_changed"] is False


def test_run163_search_log_covers_all_requested_classes():
    rows = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    header = rows[0]
    required = {
        "books", "dictionaries", "grammars", "peer_reviewed_articles", "theses_dissertations",
        "government_TRI_Census_LSI", "archives", "newspapers", "web_resources", "datasets",
        "audio", "video", "maps", "relevant_media"
    }
    assert required.issubset(set(header["classes_requested"]))
    assert header["search_id"] == "MMSC-SEARCH-000163"
