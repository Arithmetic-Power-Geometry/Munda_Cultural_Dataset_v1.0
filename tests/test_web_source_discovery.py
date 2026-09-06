from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
CENSUS_DIR = ROOT / 'data' / 'source_census'


def discovery_files():
    return sorted(CENSUS_DIR.glob('web_discovery*.json'))


def load_documents():
    return [json.loads(path.read_text(encoding='utf-8')) for path in discovery_files()]


def all_records():
    records = []
    for document in load_documents():
        records.extend(document.get('records', []))
    return records


def test_web_discovery_records_have_unique_ids_and_urls():
    records = all_records()
    ids = [r['id'] for r in records]
    urls = [r['url'] for r in records]
    assert len(records) == 32
    assert len(ids) == len(set(ids))
    assert len(urls) == len(set(urls))
    assert ids == [f'WEB-MUN-{i:04d}' for i in range(1, 33)]


def test_web_discovery_is_source_lead_layer_not_claim_layer():
    purposes = ' '.join(document.get('purpose', '') for document in load_documents()).lower()
    assert 'source leads' in purposes
    assert 'not extracted cultural claims' in purposes
    assert 'not proof' in purposes
    for record in all_records():
        for key in ['id', 'title', 'source_class', 'publisher', 'url', 'notes', 'verification_state', 'access_class', 'rights_note']:
            assert record.get(key)


def test_government_and_bibliographic_records_preserve_rights_boundaries():
    records = {r['id']: r for r in all_records()}
    for source_id in ['WEB-MUN-0008', 'WEB-MUN-0009', 'WEB-MUN-0010', 'WEB-MUN-0011', 'WEB-MUN-0012', 'WEB-MUN-0014', 'WEB-MUN-0015', 'WEB-MUN-0016', 'WEB-MUN-0017', 'WEB-MUN-0021', 'WEB-MUN-0022', 'WEB-MUN-0027', 'WEB-MUN-0029', 'WEB-MUN-0031']:
        note = records[source_id]['rights_note'].lower()
        assert any(term in note for term in ['terms', 'does not', 'rights', 'reuse', 'permission', 'copyright'])
    glottolog = records['WEB-MUN-0013']
    assert 'cc by 4.0' in glottolog['rights_note'].lower()
    assert 'does not transfer rights' in glottolog['rights_note'].lower()


def test_archival_audio_is_discovery_only_and_contextualized():
    records = {r['id']: r for r in all_records()}
    for source_id in ['WEB-MUN-0018', 'WEB-MUN-0019', 'WEB-MUN-0020', 'WEB-MUN-0030']:
        record = records[source_id]
        assert record['source_class'] == 'audio_archive'
        assert record['verification_state'] == 'national_library_catalogue_verified'
        assert '1914' in record['notes']
        assert any(term in record['rights_note'].lower() for term in ['does not', 'depend', 'conditions'])


def test_new_dataset_and_nlp_leads_preserve_access_boundaries():
    records = {r['id']: r for r in all_records()}
    paradise = records['WEB-MUN-0023']
    assert '10.4225/72/585bea79cf9dd' in paradise['notes']
    assert 'cc by-sa 4.0' in paradise['rights_note'].lower()
    assert 'item-level' in paradise['rights_note'].lower()
    muntts = records['WEB-MUN-0026']
    assert 'restricted_dataset' in muntts['source_class']
    assert 'by-nc-sa-fs 1.0' in muntts['rights_note'].lower()
    assert 'no commercial-reuse entitlement' in muntts['rights_note'].lower()
    kera = records['WEB-MUN-0028']
    assert 'kera mundari community' in kera['rights_note'].lower()
    assert 'must not be distributed or reproduced without permission' in kera['rights_note'].lower()
    bangladesh_archive = records['WEB-MUN-0032']
    assert 'consent' in bangladesh_archive['rights_note'].lower()
    assert 'commercial-reuse' in bangladesh_archive['rights_note'].lower()


def test_source_leads_do_not_claim_ingestion_or_verification_of_cultural_facts():
    records = all_records()
    forbidden_states = {'verified_complete', 'cultural_fact_verified', 'community_validated'}
    assert not (forbidden_states & {r['verification_state'] for r in records})
    assert any('page-level' in r['notes'].lower() for r in records)
    assert any('must not be universalized' in r['notes'].lower() for r in records)
    assert any('source-reported' in r['notes'].lower() for r in records)
