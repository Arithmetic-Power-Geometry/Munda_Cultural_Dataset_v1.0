import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = json.loads((ROOT / "data" / "information_model.json").read_text(encoding="utf-8"))
PORTAL = (ROOT / "pages" / "01_Research_Portal.py").read_text(encoding="utf-8")

REQUIRED_FIELDS = {
    "permanent_id", "canonical_name", "alternate_names", "description", "date_or_period",
    "geography", "actors", "language", "related_entity_ids", "source_ids", "exact_locator",
    "evidence_state", "verification_state", "access_class", "rights_or_licence",
    "commercial_reuse_status", "contributor_ids", "reviewer_ids", "uncertainty", "confidence",
    "variant_or_contradiction_ids", "created_at", "updated_at"
}

REQUIRED_DOMAINS = {
    "people","roles","families","kinship","kili","community_institutions",
    "language","dialects","scripts","phonology","morphology","grammar","syntax","lexicon","etymology","variants","examples",
    "pregnancy","birth","naming","childhood","youth","courtship","marriage","household","parenthood","ageing","death","funeral","burial","remembrance",
    "festivals","calendar","seasons","rituals","ceremonial_steps","participants","exclusions","ritual_objects","formulae","prayers",
    "beliefs","cosmology","deities","spirits","sacred_institutions","sacred_restrictions",
    "oral_histories","stories","myths","legends","folk_tales","proverbs","riddles",
    "songs","durang","dance","music","instruments","rhythm","performance_context",
    "food","drink","recipes","agriculture","crops",
    "forests","plants","ethnobotany","medicinal_knowledge","animals","ecology","weather","seasonality",
    "houses","architecture","material_culture","tools","crafts","dress","ornaments",
    "livelihoods","economy","markets","labour","migration",
    "land","customary_law","governance","political_institutions",
    "education","health","demography","language_vitality",
    "historical_events","historical_persons","movements",
    "contemporary_change","technology","media","urbanisation",
    "village_variation","geographic_variation","community_variation","kili_variation","family_variation","gender_variation","generation_variation","dialect_variation","period_variation",
    "contradictions","contested_interpretations","historical_vs_current_practice",
    "interviews","oral_history_fieldwork","observations","surveys","field_events","field_notes","consent","community_validation",
    "photographs","audio","video","scans","maps","drawings","3d_objects",
    "books","articles","theses","dictionaries","grammars","government","tri","census","lsi","archives","newspapers","web_resources",
    "rights","licence","access","commercial_reuse_status","provenance","version","audit","corrections","research_gaps","completeness",
    "reports","books_publication_mapping","publications"
}


def test_full_record_contract_is_machine_readable():
    fields = set(MODEL["record_contract"]["required_for_applicable_records"])
    assert REQUIRED_FIELDS <= fields
    assert MODEL["evidence_chain"] == ["source","passage_segment_event_object","evidence","claim","indicator","domain"]


def test_every_required_domain_has_an_explicit_data_home():
    families = MODEL["record_families"]
    ids = [f["family_id"] for f in families]
    assert len(ids) == len(set(ids))
    assert all(f.get("primary_schemas") for f in families)
    represented = {d for f in families for d in f.get("domains", [])}
    assert REQUIRED_DOMAINS <= represented


def test_evidence_access_and_ocr_safeguards_are_structural_rules():
    rules = MODEL["record_contract"]["rules"]
    for key in [
        "permanent_ids_immutable",
        "historical_source_reported_not_universalized",
        "ocr_never_implies_verified_transcription",
        "public_availability_never_implies_reuse_permission",
        "cultural_access_overrides_entitlement",
        "restricted_private_sacred_confidential_never_public",
        "uncertain_forms_never_silently_corrected",
        "verification_requires_explicit_evidence",
    ]:
        assert rules.get(key) is True


def test_mundarica_layer_separation_is_exact():
    assert MODEL["layer_contracts"]["mundarica"] == [
        "scan", "raw_ocr", "working_transcription", "verified_transcription", "structured_content"
    ]


def test_information_model_is_visible_without_claiming_evidence_completion():
    assert "Complete data skeleton" in PORTAL
    assert "Information-model domains" in PORTAL
    assert "These are schema/architecture counts, not evidence-completeness claims." in PORTAL
    assert "All record families are structure-ready" in PORTAL
