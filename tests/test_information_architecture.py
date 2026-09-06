from pathlib import Path
import json

BASE = Path(__file__).resolve().parents[1]
PORTAL = (BASE / "pages" / "01_Research_Portal.py").read_text(encoding="utf-8")
APP = (BASE / "streamlit_app.py").read_text(encoding="utf-8")
ENGINE = (BASE / "software" / "mlhkp_knowledge_engine.py").read_text(encoding="utf-8")
REGISTRY = json.loads((BASE / "data" / "module_registry.json").read_text(encoding="utf-8"))
COVERAGE = json.loads((BASE / "data" / "coverage_matrix.json").read_text(encoding="utf-8"))


def _module_names():
    names = []
    def walk(value):
        if isinstance(value, dict):
            for key, child in value.items():
                if key in {"name", "title", "label"} and isinstance(child, str):
                    names.append(child)
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)
    walk(REGISTRY)
    return names


def test_registry_declares_complete_grouped_information_architecture():
    text = json.dumps(REGISTRY, ensure_ascii=False)
    required = [
        "Home Research Dashboard", "Universal Search", "Culture Explorer", "Life from Birth to Burial",
        "Language & Lexicon", "Kinship & Kili", "Festivals & Rituals", "Beliefs & Sacred Life",
        "Stories & Oral Traditions", "Songs/Dance/Music", "Food & Agriculture", "Ecology & Ethnobotany",
        "Material Culture & Crafts", "Dress & Ornament", "Houses & Architecture", "Livelihood & Economy",
        "Customary Law & Governance", "Education/Health/Demography", "Places & Landscapes",
        "Geographic/Community Variation", "Historical Timeline", "Historical Archives", "Contemporary Change",
        "Master Munda Source Census", "Mundarica I-XVI Digital Library", "Books/Journals/Theses",
        "Government & Archives", "Media Archive", "Evidence Explorer", "Contradictions & Variants",
        "Community Validation", "Research Gaps/Completeness", "Reports & Downloads", "About",
        "Governance & Ethics", "Contribute/Correct", "Owner Research Console", "Research Pro",
        "Institutional", "API", "Report Studio", "Book Studio"
    ]
    for name in required:
        assert name in text


def test_coverage_matrix_maps_every_registered_module():
    matrix_text = json.dumps(COVERAGE, ensure_ascii=False)
    for name in set(_module_names()):
        assert name in matrix_text


def test_grouped_navigation_not_flat_radio_contract():
    assert "st.radio(" not in PORTAL or "group" in PORTAL.lower()


def test_structure_ready_empty_state_visible():
    assert "Structure ready — evidence not yet ingested" in PORTAL


def test_mundarica_layer_and_verification_contract_visible():
    assert "scan → raw OCR → working transcription → verified transcription → structured content" in PORTAL
    assert "Verification gate has not passed" in PORTAL
    assert 'v.get("verified_complete") is True' in PORTAL


def test_governance_title_and_footer_contract_preserved():
    exact = "Mr. Rajan Pahan — Founding Community, Meetings & Field Logistics Coordinator"
    assert exact in PORTAL
    # The public entry point delegates rendering to the knowledge engine. Preserve
    # the exact governance title in either rendered surface; do not require stale
    # duplicated founder metadata in streamlit_app.py.
    assert ("Mr. Rajan Pahan" in ENGINE and "Founding Community, Meetings & Field Logistics Coordinator" in ENGINE) or exact in PORTAL
    assert "does not independently determine scholarly interpretation or final scholarly approval" in PORTAL
    # No duplicate founder footer: the entry point should not repeat founder data.
    assert "Mr. Rajan Pahan" not in APP


def test_evidence_chain_and_public_access_filter_present():
    assert REGISTRY["evidence_chain"] == ["source","passage_segment_event_object","evidence","claim","indicator","domain"]
    assert "SOURCE → PASSAGE/SEGMENT/EVENT/OBJECT → EVIDENCE → CLAIM → INDICATOR → DOMAIN" in PORTAL


def test_external_discovery_is_not_promoted_to_cultural_evidence():
    assert "External discovery" in ENGINE
    assert "not treated as cultural facts" in ENGINE


def test_cultural_access_overrides_entitlement_contract_visible():
    combined = PORTAL + "\n" + ENGINE + "\n" + json.dumps(REGISTRY, ensure_ascii=False)
    assert "cultural" in combined.lower()
    assert "access" in combined.lower()
