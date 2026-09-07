from pathlib import Path
import json
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / 'streamlit_app.py'
ENGINE = ROOT / 'software' / 'mlhkp_knowledge_engine.py'
PORTAL = ROOT / 'pages' / '01_Research_Portal.py'
VERIFY_APP = ROOT / 'pages' / '02_Mundarica_Verification.py'
PUBLIC_PAGES = [
    'Home', 'Search & Ask', 'Explore', 'Mundarica I–XVI',
    'Sources & Research Library', 'Build Report & Download',
    'Completeness Dashboard', 'About · Governance · Ethics'
]


def run_page(page):
    at = AppTest.from_file(str(APP), default_timeout=30).run()
    assert not at.exception, at.exception
    nav = next(r for r in at.radio if r.label == 'Navigate')
    nav.set_value(page).run(timeout=30)
    assert not at.exception, at.exception
    return at


def app_source():
    return APP.read_text(encoding='utf-8')


def engine_source():
    return ENGINE.read_text(encoding='utf-8')


def portal_source():
    return PORTAL.read_text(encoding='utf-8')


def test_all_public_knowledge_engine_pages_render_without_exception():
    for page in PUBLIC_PAGES:
        run_page(page)


def test_current_entrypoint_loads_all_discovery_expansions_dynamically():
    source = app_source()
    assert "glob('web_discovery_expansion_*.json')" in source
    assert "engine.WEB = web_records" in source
    seed = json.loads((ROOT/'data'/'source_census'/'web_discovery_seed_2026-09-06.json').read_text(encoding='utf-8'))['records']
    expansions = []
    for path in sorted((ROOT/'data'/'source_census').glob('web_discovery_expansion_*.json')):
        expansions.extend(json.loads(path.read_text(encoding='utf-8')).get('records', []))
    ids = [r.get('id') for r in seed + expansions if r.get('id')]
    assert len(ids) == len(set(ids))
    assert 'WEB-MUN-0069' in ids


def test_grouped_research_portal_remains_visible_and_not_flat_radio():
    source = portal_source()
    assert 'group_order = [' in source
    assert 'st.selectbox("Section"' in source
    assert 'st.selectbox("Module"' in source
    assert 'Structure ready — evidence not yet ingested' in source
    assert 'st.radio(' not in source


def test_governance_identity_role_and_access_safeguards_present():
    source = engine_source() + '\n' + portal_source()
    assert 'Dr. Mohammad Amir Khusru Akhtar' in source
    assert 'Dr. Arvind Hans' in source
    assert 'Mr. Rajan Pahan' in source
    assert 'Founding Community, Meetings & Field Logistics Coordinator' in source
    assert 'does not independently determine scholarly interpretation or final scholarly approval' in source
    assert 'Cultural access and consent restrictions override' in source
    assert 'Source availability is not proof of reuse rights' in source
    assert 'OCR is not verified transcription' in source
    assert 'Historical reports are not automatically current or universal facts' in source


def test_entrypoint_does_not_duplicate_founder_metadata():
    source = app_source()
    assert 'Mr. Rajan Pahan' not in source
    assert 'Founding record:' not in source


def test_master_source_register_is_canonical_and_preserves_ids():
    data = json.loads((ROOT/'data'/'source_register'/'master_sources.json').read_text(encoding='utf-8'))
    ids = [x['source_id'] for x in data['sources']]
    assert ids == [f'SRC-{i:06d}' for i in range(1,15)]


def test_master_source_census_live_metrics_are_internally_consistent():
    census = json.loads((ROOT/'data'/'source_census'/'mmsc_index.json').read_text(encoding='utf-8'))
    discoveries = json.loads((ROOT/'data'/'source_census'/'mmsc_discoveries.json').read_text(encoding='utf-8'))['records']
    mundarica = json.loads((ROOT/'data'/'source_bundles'/'encyclopaedia_mundarica'/'manifest.json').read_text(encoding='utf-8'))
    located = sum(1 for v in mundarica['volume_slots'] if v.get('status') == 'external_source_locator_verified_not_ingested')
    assert census['metrics']['canonical_master_records'] == 14
    assert census['metrics']['standalone_mmsc_discoveries'] == len(discoveries)
    assert census['metrics']['mundarica_volume_locators_verified'] == located
    assert census['metrics']['sources_discovered'] == census['metrics']['canonical_master_records'] + census['metrics']['additional_federated_discoveries']
    assert census['metrics']['deduplicated_locator_matches'] >= 1
    assert census['metrics']['mundarica_verified_complete_volumes'] == 0


def test_mundarica_manifest_has_all_16_slots_and_volume1_page_blocks():
    manifest = json.loads((ROOT/'data'/'source_bundles'/'encyclopaedia_mundarica'/'manifest.json').read_text(encoding='utf-8'))
    assert [x['source_id'] for x in manifest['volume_slots']] == [f'SRC-MUN-V{i:02d}' for i in range(1,17)]
    text = (ROOT/'Mundarica1.md').read_text(encoding='utf-8')
    assert '## Scan page 6' in text or '## PDF Page 6' in text
    assert manifest['audit_summary']['registered_authoritative_scans'] == 0
    assert manifest['audit_summary']['verified_complete_volumes'] == 0


def test_mundarica_designated_reviewer_registry_and_workspace():
    registry = json.loads((ROOT/'data'/'governance'/'reviewer_registry.json').read_text(encoding='utf-8'))
    reviewer = registry['reviewers'][0]
    assert reviewer['reviewer_id'] == 'REV-MLHKP-000001'
    assert reviewer['name'] == 'Dr. Mohammad Amir Khusru Akhtar'
    assert 'Encyclopaedia Mundarica' in reviewer['declared_expertise']
    assert registry['policy']['ocr_alone_can_never_be_verified_transcription'] is True
    assert registry['policy']['verified_transcription_requires_authoritative_scan_comparison'] is True
    assert registry['policy']['community_validation_is_distinct_from_textual_verification'] is True
    source = VERIFY_APP.read_text(encoding='utf-8')
    assert 'Mundarica Verification Workspace' in source
    assert 'Human verification is recorded as evidence' in source
    at = AppTest.from_file(str(VERIFY_APP), default_timeout=30).run()
    assert not at.exception, at.exception


def test_public_engine_has_no_owner_console_navigation():
    at = AppTest.from_file(str(APP), default_timeout=30).run()
    nav = next(r for r in at.radio if r.label == 'Navigate')
    assert 'Owner Research Console' not in nav.options
