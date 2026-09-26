import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCATOR = ROOT / "data/source_census/murugesan_driemel_murphy_mundari_cyclic_agree_exact_locator_run359_2026-09-14.json"
SEARCH = ROOT / "audits/mmsc_search_run359_2026-09-14.json"


def test_run359_locator_promotion_boundary():
    data = json.loads(LOCATOR.read_text(encoding="utf-8"))
    assert data["work"]["doi"] == "10.1007/s11049-024-09628-2"
    assert data["work"]["refereed"] is True
    assert data["exact_manifestation"]["filename"] == "murugesanEtAl_24_Omnivoro.3.pdf"
    assert data["exact_manifestation"]["licence_as_declared_by_provider"] == "CC-BY 2.5"
    assert data["controlled_claims_added"] == 0
    assert data["controlled_evidence_records_added"] == 0
    assert data["controlled_counts_changed"] is False
    boundary = " ".join(data["not_promoted"]).lower()
    for term in ("linguistic", "participant consent", "community validation", "cultural-access"):
        assert term in boundary


def test_run359_census_workbook_remains_unverified():
    data = json.loads(SEARCH.read_text(encoding="utf-8"))
    census = next(x for x in data["fresh_reobservations"] if x["class"] == "government_TRI_Census_LSI")
    disposition = census["disposition"].lower()
    assert "blocked" in disposition
    assert "hash" in disposition
    assert "numeric values remain unverified and unpromoted" in disposition
    assert data["count_change_this_run"] is False
