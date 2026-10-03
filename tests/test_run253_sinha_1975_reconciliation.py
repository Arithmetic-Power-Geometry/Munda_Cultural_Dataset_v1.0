import json
from pathlib import Path


def test_run253_sinha_1975_work_family_and_boundaries():
    p = Path("data/source_census/sinha_1975_mundari_grammar_multisource_reconciliation_run253_2026-09-12.json")
    d = json.loads(p.read_text(encoding="utf-8"))

    assert d["run_id"] == 253
    assert d["work"]["canonical_title"] == "Mundari Grammar"
    assert d["work"]["author"] == "N. K. Sinha"
    assert d["work"]["year"] == 1975
    assert d["work"]["prior_audit_run"] == 206
    assert d["deduplication"]["identity_count_change"] is False
    assert d["deduplication"]["sinha_1974_phonetic_reader_is_distinct_work"] is True

    providers = {x["provider"]: x for x in d["verified_locators"]}
    assert providers["Bharatavani"]["reported_pdf_size"] == "117.39 MB"
    assert providers["Bharatavani"]["access_statement"] == "Login to Read"
    assert providers["Bharatavani"]["bytes_acquired"] is False
    assert providers["CiNii Books"]["ncid"] == "BA46909970"
    assert providers["CiNii Books"]["lccn"] == "76901792"
    assert providers["CiNii Books"]["bibliography_locator"] == "p. [164]"
    assert providers["WALS Online"]["reference_id"] == "Sinha-1975"

    b = d["rights_access_cultural_boundary"]
    assert b["public_catalogue_visibility_is_permission"] is False
    assert b["login_access_is_redistribution_permission"] is False
    assert b["cryptographic_hash_verified"] is False
    assert b["community_validation_verified"] is False
    assert b["cultural_access_permission_verified"] is False

    promotion = d["promotion"]
    assert promotion["source_identities_added"] == 0
    assert promotion["grammar_rules_promoted"] == 0
    assert promotion["lexical_rows_promoted"] == 0
    assert promotion["cultural_claims_promoted"] == 0
    assert promotion["count_bearing_change"] is False


def test_run253_all_requested_search_classes_logged():
    rows = [
        json.loads(line)
        for line in Path("data/source_census/search_log_run253.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
        if line.strip()
    ]
    classes = {r["class"] for r in rows}
    expected = {
        "books",
        "dictionaries",
        "grammars",
        "peer_reviewed_articles",
        "theses_dissertations",
        "government_TRI_Census_LSI",
        "archives",
        "newspapers_periodicals",
        "web_resources",
        "datasets",
        "audio",
        "video",
        "maps",
        "relevant_media",
    }
    assert expected <= classes
    assert all(r["search_id"] == "MMSC-SEARCH-000253" for r in rows)
