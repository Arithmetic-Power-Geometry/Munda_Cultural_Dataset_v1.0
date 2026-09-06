from pathlib import Path
import json
from streamlit.testing.v1 import AppTest

ROOT=Path(__file__).resolve().parents[1]
APP=ROOT/'streamlit_app.py'
VERIFY_APP=ROOT/'pages'/'02_Mundarica_Verification.py'
PUBLIC_PAGES=['Home','Culture Explorer','Master Sources','Mundarica 1–16','Evidence Explorer','Research Gaps','Governance & Ethics','Report / Contribute']

def run_page(page):
    at=AppTest.from_file(str(APP),default_timeout=30).run()
    assert not at.exception, at.exception
    nav=next(r for r in at.radio if r.key=='main_navigation')
    nav.set_value(page).run(timeout=30)
    assert not at.exception, at.exception
    return at

def app_source():
    return APP.read_text(encoding='utf-8')

def test_all_public_pages_render_without_exception():
    for page in PUBLIC_PAGES:
        run_page(page)

def test_home_exposes_project_identity_and_founders():
    at=run_page('Home')
    text=' '.join(x.value for x in at.markdown)
    source=app_source()
    assert 'Munda Living Heritage & Knowledge Project' in text
    assert 'Johar' in text
    assert 'Dr. Mohammad Amir Khusru Akhtar' in source
    assert 'Dr. Arvind Hans' in source
    assert 'Mr. Rajan Pahan' in source
    assert 'Founding Community, Meetings & Field Logistics Coordinator' in source
    assert 'elders, Pahans, customary leaders, practitioners, families, youth, women, performers, artisans, musicians and storytellers' in source
    assert 'culturally appropriate introductions' in source
    assert 'venues, travel, recording locations, guides, participant mobilisation and follow-up records' in source
    assert 'does not independently determine scholarly interpretation or final scholarly approval' in source

def test_footer_does_not_duplicate_founder_record():
    source=app_source()
    assert 'Founding record:' not in source
    assert 'Munda Cultural Dataset (MCD) evidence engine' in source
    assert 'Community-contributed and culturally restricted material remains subject to consent, access, reuse and publication conditions.' in source
    assert 'No Project IP right is interpreted as ownership of the Munda community, identity, culture, sacred traditions or collective heritage.' in source

def test_logo_fallback_is_embedded_for_deployment():
    logo_module=ROOT/'assets'/'mlhkp_logo_data.py'
    assert logo_module.exists()
    text=logo_module.read_text(encoding='utf-8')
    assert 'data:image/webp;base64,' in text
    assert len(text)>10000

def test_master_source_register_is_canonical_and_preserves_ids():
    data=json.loads((ROOT/'data'/'source_register'/'master_sources.json').read_text(encoding='utf-8'))
    ids=[x['source_id'] for x in data['sources']]
    assert ids==[f'SRC-{i:06d}' for i in range(1,15)]
    assert not run_page('Master Sources').exception

def test_master_source_census_page_reads_live_federated_metrics():
    census=json.loads((ROOT/'data'/'source_census'/'mmsc_index.json').read_text(encoding='utf-8'))
    discoveries=json.loads((ROOT/'data'/'source_census'/'mmsc_discoveries.json').read_text(encoding='utf-8'))['records']
    mundarica=json.loads((ROOT/'data'/'source_bundles'/'encyclopaedia_mundarica'/'manifest.json').read_text(encoding='utf-8'))
    located=sum(1 for v in mundarica['volume_slots'] if v.get('status')=='external_source_locator_verified_not_ingested')
    assert census['metrics']['canonical_master_records']==14
    assert census['metrics']['standalone_mmsc_discoveries']==len(discoveries)
    assert census['metrics']['mundarica_volume_locators_verified']==located
    assert census['metrics']['sources_discovered']==census['metrics']['canonical_master_records']+census['metrics']['additional_federated_discoveries']
    assert census['metrics']['deduplicated_locator_matches']>=1
    assert census['metrics']['mundarica_verified_complete_volumes']==0
    source=app_source()
    assert 'section("Master Source Census")' in source
    assert 'mmsc_index()' in source
    assert 'mmsc_discoveries()' in source
    assert 'Catalogue or online availability does not establish acquisition, OCR verification, reuse permission, cultural validation or VERIFIED COMPLETE status.' in source
    assert not run_page('Master Sources').exception

def test_mundarica_manifest_has_all_16_slots_and_volume1_page_blocks():
    manifest=json.loads((ROOT/'data'/'source_bundles'/'encyclopaedia_mundarica'/'manifest.json').read_text(encoding='utf-8'))
    assert [x['source_id'] for x in manifest['volume_slots']]==[f'SRC-MUN-V{i:02d}' for i in range(1,17)]
    text=(ROOT/'Mundarika1.md').read_text(encoding='utf-8')
    assert '## Scan page 6' in text or '## PDF Page 6' in text
    assert not run_page('Mundarica 1–16').exception

def test_mundarica_streamlit_selector_reflects_artifact_and_locator_state():
    manifest=json.loads((ROOT/'data'/'source_bundles'/'encyclopaedia_mundarica'/'manifest.json').read_text(encoding='utf-8'))
    assert manifest['artifact_registry']=='artifact_registry.json'
    assert manifest['audit_summary']['registered_artifacts']==1
    assert manifest['audit_summary']['registered_authoritative_scans']==0
    assert manifest['audit_summary']['verified_complete_volumes']==0
    located=sum(1 for v in manifest['volume_slots'] if v.get('status')=='external_source_locator_verified_not_ingested')
    assert manifest['audit_summary']['externally_located_volumes']==located
    at=run_page('Mundarica 1–16')
    selector=next(x for x in at.selectbox if x.label=='Volume')
    assert any('SRC-MUN-V01' in str(option) and 'working_transcription_registered_page_accounting_complete' in str(option) for option in selector.options)
    assert any('SRC-MUN-V03' in str(option) and 'external_source_locator_verified_not_ingested' in str(option) for option in selector.options)
    assert any('SRC-MUN-V05' in str(option) and 'external_source_locator_verified_not_ingested' in str(option) for option in selector.options)
    assert not any('VERIFIED COMPLETE' in str(option) for option in selector.options)

def test_mundarica_designated_reviewer_registry_and_workspace():
    registry=json.loads((ROOT/'data'/'governance'/'reviewer_registry.json').read_text(encoding='utf-8'))
    reviewer=registry['reviewers'][0]
    assert reviewer['reviewer_id']=='REV-MLHKP-000001'
    assert reviewer['name']=='Dr. Mohammad Amir Khusru Akhtar'
    assert 'Encyclopaedia Mundarica' in reviewer['declared_expertise']
    assert 'English-language textual verification' in reviewer['declared_expertise']
    assert registry['policy']['ocr_alone_can_never_be_verified_transcription'] is True
    assert registry['policy']['verified_transcription_requires_authoritative_scan_comparison'] is True
    assert registry['policy']['community_validation_is_distinct_from_textual_verification'] is True
    source=VERIFY_APP.read_text(encoding='utf-8')
    assert 'Mundarica Verification Workspace' in source
    assert 'Human verification is recorded as evidence' in source
    assert 'A whole volume becomes VERIFIED COMPLETE only after every required textual, structural, provenance, rights/access and completeness gate passes' in source
    at=AppTest.from_file(str(VERIFY_APP),default_timeout=30).run()
    assert not at.exception, at.exception

def test_public_app_has_no_owner_console_in_navigation():
    at=AppTest.from_file(str(APP),default_timeout=30).run()
    nav=next(r for r in at.radio if r.key=='main_navigation')
    assert 'Owner Research Console' not in nav.options

def test_rights_roles_and_safeguards_are_visible():
    assert not run_page('Governance & Ethics').exception
    source=app_source()
    assert 'final authority over scholarly methodology, interpretation and final scholarly approval' in source
    assert 'primary-data collection under approved research instruments' in source
    assert 'This coordination and field-logistics role does not independently determine scholarly interpretation or final scholarly approval.' in source
    assert 'collection is not publication permission' in source
    assert 'restricted knowledge is not automatically public' in source
    assert 'Project IP does not constitute ownership of Munda people, identity, culture, sacred traditions or collective heritage' in source
