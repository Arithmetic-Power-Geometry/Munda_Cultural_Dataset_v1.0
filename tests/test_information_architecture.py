import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = json.loads((ROOT / "data" / "module_registry.json").read_text(encoding="utf-8"))
COVERAGE = json.loads((ROOT / "data" / "coverage_matrix.json").read_text(encoding="utf-8"))
PORTAL = (ROOT / "pages" / "01_Research_Portal.py").read_text(encoding="utf-8")
APP = (ROOT / "streamlit_app.py").read_text(encoding="utf-8")

REQUIRED_GROUPS = {
    "Discover","Culture & Knowledge","People & Place","History & Change",
    "Research Library","Evidence & Research","MLHKP","Future (disabled by default)"
}
REQUIRED_MODULES = {
    "Home Research Dashboard","Universal Search","Culture Explorer","Life from Birth to Burial",
    "Language & Lexicon","Kinship & Kili","Festivals & Rituals","Beliefs & Sacred Life",
    "Stories & Oral Traditions","Songs / Dance / Music","Food & Agriculture","Ecology & Ethnobotany",
    "Material Culture & Crafts","Dress & Ornament","Houses & Architecture","Livelihood & Economy",
    "Customary Law & Governance","Education / Health / Demography","Places & Landscapes",
    "Geographic / Community Variation","Historical Timeline","Historical Archives","Contemporary Change",
    "Master Munda Source Census","Mundarica I–XVI Digital Library","Books / Journals / Theses",
    "Government & Archives","Media Archive","Evidence Explorer","Contradictions & Variants",
    "Community Validation","Research Gaps / Completeness","Reports & Downloads","About",
    "Governance & Ethics","Contribute / Correct","Owner Research Console","Research Pro","Institutional",
    "API","Report Studio","Book Studio"
}


def test_complete_grouped_information_architecture_is_registered():
    modules = REGISTRY["modules"]
    assert {m["group"] for m in modules} == REQUIRED_GROUPS
    assert REQUIRED_MODULES <= {m["label"] for m in modules}
    ids = [m["module_id"] for m in modules]
    assert len(ids) == len(set(ids))
    assert all(m.get("schemas") and m.get("domains") for m in modules)


def test_future_commercial_modules_disabled_and_cultural_access_override_present():
    future = [m for m in REGISTRY["modules"] if m["group"] == "Future (disabled by default)"]
    assert future and all(m.get("enabled") is False for m in future)
    assert "cultural_access_overrides_entitlement" in json.dumps(REGISTRY)
    assert "Cultural access and consent restrictions override commercial" in PORTAL


def test_coverage_matrix_maps_every_row_to_registered_public_module():
    labels = {m["label"] for m in REGISTRY["modules"]}
    assert COVERAGE["rows"]
    ids = [r["coverage_id"] for r in COVERAGE["rows"]]
    assert len(ids) == len(set(ids))
    for row in COVERAGE["rows"]:
        mapped = [x.strip() for x in row["streamlit_module"].split(";")]
        assert all(x in labels for x in mapped)
        assert row["schema"] and row["source_layer"] and row["evidence_layer"] and row["gap_rule"]


def test_portal_uses_grouped_navigation_and_truthful_empty_state():
    assert 'group = st.selectbox("Section"' in PORTAL
    assert 'label = st.selectbox("Module"' in PORTAL
    assert "Structure ready — evidence not yet ingested" in PORTAL
    assert "not one giant flat radio list" in PORTAL
    assert "st.json(" not in PORTAL


def test_mundarica_layer_and_verification_contract_visible():
    assert "scan → raw OCR → working transcription → verified transcription → structured content" in PORTAL
    assert "Verification gate has not passed" in PORTAL
    assert 'v.get("verified_complete") is True' in PORTAL


def test_governance_title_and_footer_contract_preserved():
    exact = "Mr. Rajan Pahan — Founding Community, Meetings & Field Logistics Coordinator"
    assert exact in PORTAL
    assert "does not independently determine scholarly interpretation or final scholarly approval" in PORTAL
    assert exact.replace(" — ", "\",\"") not in APP  # no requirement to duplicate the title in footer
    footer_tail = APP.split("def footer():",1)[1].split("if \"owner\"",1)[0]
    assert "Founding record:" not in footer_tail


def test_evidence_chain_and_public_access_filter_present():
    assert REGISTRY["evidence_chain"] == ["source","passage_segment_event_object","evidence","claim","indicator","domain"]
    assert "SOURCE → PASSAGE/SEGMENT/EVENT/OBJECT → EVIDENCE → CLAIM → INDICATOR → DOMAIN" in PORTAL
    assert "lower(COALESCE(e.access_level,'public')) IN ('public','open')" in PORTAL
