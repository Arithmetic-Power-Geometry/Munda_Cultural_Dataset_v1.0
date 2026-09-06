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
    assert len(records) == 52
    assert len(ids) == len(set(ids))
    assert len(urls) == len(set(urls))
    assert ids == [f'WEB-MUN-{i:04d}' for i in range(1, 53)]


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
    for source_id in ['WEB-MUN-0008', 'WEB-MUN-0009', 'WEB-MUN-0010', 'WEB-MUN-0011', 'WEB-MUN-0012', 'WEB-MUN-0014', 'WEB-MUN-0015', 'WEB-MUN-0016', 'WEB-MUN-0017', 'WEB-MUN-0021', 'WEB-MUN-0022', 'WEB-MUN-0027', 'WEB-MUN-0029', 'WEB-MUN-0031', 'WEB-MUN-0033', 'WEB-MUN-0034', 'WEB-MUN-0038', 'WEB-MUN-0040', 'WEB-MUN-0041', 'WEB-MUN-0042', 'WEB-MUN-0043', 'WEB-MUN-0044', 'WEB-MUN-0048', 'WEB-MUN-0049', 'WEB-MUN-0050', 'WEB-MUN-0051', 'WEB-MUN-0052']:
        note = records[source_id]['rights_note'].lower()
        assert any(term in note for term in ['terms', 'does not', 'rights', 'reuse', 'permission', 'copyright', 'licence'])
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
    proto_munda = records['WEB-MUN-0035']
    assert 'zenodo' in proto_munda['publisher'].lower()
    assert '127' in proto_munda['notes']
    assert 'commercial-reuse determination' in proto_munda['rights_note'].lower()
    mmloso = records['WEB-MUN-0036']
    assert 'dataset' in mmloso['source_class']
    assert 'separately audited' in mmloso['notes'].lower()
    assert 'dataset-level licence' in mmloso['rights_note'].lower()
    translation = records['WEB-MUN-0037']
    assert '17,826' in translation['notes']
    assert 'by-nc-sa-fs 1.0' in translation['rights_note'].lower()
    assert 'no commercial-reuse entitlement' in translation['rights_note'].lower()


def test_map_and_media_leads_preserve_primary_evidence_boundaries():
    records = {r['id']: r for r in all_records()}
    munda_map = records['WEB-MUN-0039']
    assert 'cc by-sa 3.0' in munda_map['rights_note'].lower()
    assert 'authoritative census/geospatial sources' in munda_map['notes'].lower()
    hockey = records['WEB-MUN-0040']
    assert 'primary rule book' in hockey['notes'].lower()
    assert 'separate permission' in hockey['rights_note'].lower()
    museum = records['WEB-MUN-0041']
    assert 'separate source records' in museum['notes'].lower()
    assert 'cultural access' in museum['rights_note'].lower()
    ezcc = records['WEB-MUN-0047']
    assert 'cc by 3.0' in ezcc['rights_note'].lower()
    assert '4:28' in ezcc['notes'] and '6:00' in ezcc['notes'] and '11:12' in ezcc['notes']
    assert 'cultural-access' in ezcc['rights_note'].lower()


def test_new_field_research_leads_are_context_bounded_and_safety_aware():
    records = {r['id']: r for r in all_records()}
    land = records['WEB-MUN-0043']
    assert 'must not be universalized' in land['notes'].lower()
    food = records['WEB-MUN-0045']
    assert 'nine villages' in food['notes'].lower()
    assert 'must not be generalized' in food['notes'].lower()
    ethnobotany = records['WEB-MUN-0046']
    assert 'no medicinal recommendation' in ethnobotany['notes'].lower()
    assert 'safety' in ethnobotany['rights_note'].lower()
    assert 'cultural-access' in ethnobotany['rights_note'].lower()


def test_run7_linguistic_debate_and_historical_sources_are_contextualized():
    records = {r['id']: r for r in all_records()}
    flexible = records['WEB-MUN-0048']
    peterson = records['WEB-MUN-0049']
    assert 'contradiction' in flexible['notes'].lower()
    assert 'rather than treated as a single definitive' in peterson['notes'].lower()
    primer = records['WEB-MUN-0050']
    assert primer['year'] == 1873
    assert 'exact page locators' in primer['notes'].lower()
    assert 'noncommercial' in primer['rights_note'].lower() or 'nicht kommerzielle' in primer['rights_note'].lower()
    grammar = records['WEB-MUN-0051']
    assert grammar['year'] == 1882
    assert 'historical grammar' in grammar['notes'].lower()
    phonetics = records['WEB-MUN-0052']
    assert '10.21437/tai.2023-17' in phonetics['notes'].lower()
    assert 'participant-derived' in phonetics['rights_note'].lower()


def test_source_leads_do_not_claim_ingestion_or_verification_of_cultural_facts():
    records = all_records()
    forbidden_states = {'verified_complete', 'cultural_fact_verified', 'community_validated'}
    assert not (forbidden_states & {r['verification_state'] for r in records})
    assert any('page-level' in r['notes'].lower() for r in records)
    assert any('must not be universalized' in r['notes'].lower() for r in records)
    assert any('source-reported' in r['notes'].lower() for r in records)
