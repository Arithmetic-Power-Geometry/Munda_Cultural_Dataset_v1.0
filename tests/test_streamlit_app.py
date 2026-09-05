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

def test_home_exposes_project_identity():
    at=run_page('Home')
    text=' '.join(x.value for x in at.markdown)
    assert 'Munda Living Heritage & Knowledge Project' in text
    assert 'Johar' in text

def test_master_source_register_is_canonical_and_preserves_ids():
    data=json.loads((ROOT/'data'/'source_register'/'master_sources.json').read_text(encoding='utf-8'))
    ids=[x['source_id'] for x in data['sources']]
    assert ids==[f'SRC-{i:06d}' for i in range(1,15)]
    at=run_page('Master Sources')
    assert not at.exception

def test_mundarica_manifest_has_all_16_slots_and_volume1_page_blocks():
    manifest=json.loads((ROOT/'data'/'source_bundles'/'encyclopaedia_mundarica'/'manifest.json').read_text(encoding='utf-8'))
    assert [x['source_id'] for x in manifest['volume_slots']]==[f'SRC-MUN-V{i:02d}' for i in range(1,17)]
    text=(ROOT/'Mundarika1.md').read_text(encoding='utf-8')
    assert '## Scan page 6' in text or '## PDF Page 6' in text
    at=run_page('Mundarica 1–16')
    assert not at.exception

def test_public_app_has_no_owner_console_in_navigation():
    at=AppTest.from_file(str(APP),default_timeout=30).run()
    nav=next(r for r in at.radio if r.key=='main_navigation')
    assert 'Owner Research Console' not in nav.options

def test_rights_and_safeguards_are_visible():
    at=run_page('Governance & Ethics')
    body=' '.join([x.value for x in at.markdown]+[x.value for x in at.info])
    assert 'does not constitute ownership of the Munda people' in body
    assert 'Collection is not publication permission' in body
