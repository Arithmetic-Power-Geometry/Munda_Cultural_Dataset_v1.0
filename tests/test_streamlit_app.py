from pathlib import Path
import json
from streamlit.testing.v1 import AppTest

ROOT=Path(__file__).resolve().parents[1]
APP=ROOT/'streamlit_app.py'
PUBLIC_PAGES=['Home','Culture Explorer','Master Sources','Mundarica 1–16','Evidence Explorer','Research Gaps','Governance & Ethics','Report / Contribute']

def run_page(page):
    at=AppTest.from_file(str(APP),default_timeout=30).run()
    assert not at.exception, at.exception
    nav=next(r for r in at.radio if r.key=='main_navigation')
    nav.set_value(page).run(timeout=30)
    assert not at.exception, at.exception
    return at

def test_all_public_pages_render_without_exception():
    for page in PUBLIC_PAGES:
        run_page(page)

def test_home_exposes_project_identity_and_founders():
    at=run_page('Home')
    text=' '.join(x.value for x in at.markdown)
    assert 'Munda Living Heritage & Knowledge Project' in text
    assert 'Johar' in text
    assert 'Dr. Mohammad Amir Khusru Akhtar' in text
    assert 'Dr. Arvind Hans' in text
    assert 'Mr. Rajan Pahan' in text
    assert 'Founding Community Coordination, Meetings & Logistics Lead' in text

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

def test_mundarica_manifest_has_all_16_slots_and_volume1_page_blocks():
    manifest=json.loads((ROOT/'data'/'source_bundles'/'encyclopaedia_mundarica'/'manifest.json').read_text(encoding='utf-8'))
    assert [x['source_id'] for x in manifest['volume_slots']]==[f'SRC-MUN-V{i:02d}' for i in range(1,17)]
    text=(ROOT/'Mundarika1.md').read_text(encoding='utf-8')
    assert '## Scan page 6' in text or '## PDF Page 6' in text
    assert not run_page('Mundarica 1–16').exception

def test_mundarica_streamlit_selector_reflects_artifact_registry_state():
    manifest=json.loads((ROOT/'data'/'source_bundles'/'encyclopaedia_mundarica'/'manifest.json').read_text(encoding='utf-8'))
    assert manifest['artifact_registry']=='artifact_registry.json'
    assert manifest['audit_summary']['registered_artifacts']==1
    assert manifest['audit_summary']['registered_authoritative_scans']==0
    assert manifest['audit_summary']['verified_complete_volumes']==0
    at=run_page('Mundarica 1–16')
    selector=next(x for x in at.selectbox if x.label=='Select volume')
    assert any('SRC-MUN-V01' in str(option) and 'working_transcription_registered_page_accounting_complete' in str(option) for option in selector.options)
    assert not any('VERIFIED COMPLETE' in str(option) for option in selector.options)

def test_public_app_has_no_owner_console_in_navigation():
    at=AppTest.from_file(str(APP),default_timeout=30).run()
    nav=next(r for r in at.radio if r.key=='main_navigation')
    assert 'Owner Research Console' not in nav.options

def test_rights_roles_and_safeguards_are_visible():
    at=run_page('Governance & Ethics')
    body=' '.join([x.value for x in at.markdown]+[x.value for x in at.info])
    assert 'do not constitute ownership of the Munda people' in body
    assert 'Collection is not publication permission' in body
    assert 'final authority on scholarly methodology' in body
    assert 'operational authority within approved plans for field operations' in body
    assert 'operational authority within approved plans for meetings, community liaison and logistics' in body
