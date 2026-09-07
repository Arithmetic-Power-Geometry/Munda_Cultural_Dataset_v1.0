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
    assert len(records) == 72
    assert len(ids) == len(set(ids))
    assert len(urls) == len(set(urls))
    assert ids == [f'WEB-MUN-{i:04d}' for i in range(1, 73)]


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
    for source_id in ['WEB-MUN-0008','WEB-MUN-0009','WEB-MUN-0010','WEB-MUN-0011','WEB-MUN-0012','WEB-MUN-0014','WEB-MUN-0015','WEB-MUN-0016','WEB-MUN-0017','WEB-MUN-0021','WEB-MUN-0022','WEB-MUN-0027','WEB-MUN-0029','WEB-MUN-0031','WEB-MUN-0033','WEB-MUN-0034','WEB-MUN-0038','WEB-MUN-0040','WEB-MUN-0041','WEB-MUN-0042','WEB-MUN-0043','WEB-MUN-0044','WEB-MUN-0048','WEB-MUN-0049','WEB-MUN-0050','WEB-MUN-0051','WEB-MUN-0052','WEB-MUN-0053','WEB-MUN-0054','WEB-MUN-0055','WEB-MUN-0056','WEB-MUN-0057','WEB-MUN-0058','WEB-MUN-0059','WEB-MUN-0060','WEB-MUN-0062','WEB-MUN-0063','WEB-MUN-0064','WEB-MUN-0065','WEB-MUN-0066','WEB-MUN-0067','WEB-MUN-0068','WEB-MUN-0069','WEB-MUN-0070','WEB-MUN-0071','WEB-MUN-0072']:
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
    muntts = records['WEB-MUN-0026']
    assert 'restricted_dataset' in muntts['source_class']
    assert 'by-nc-sa-fs 1.0' in muntts['rights_note'].lower()
    assert 'no commercial-reuse entitlement' in muntts['rights_note'].lower()
    translation = records['WEB-MUN-0037']
    assert '17,826' in translation['notes']
    assert 'by-nc-sa-fs 1.0' in translation['rights_note'].lower()


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
    ezcc = records['WEB-MUN-0047']
    assert 'cc by 3.0' in ezcc['rights_note'].lower()


def test_new_field_research_leads_are_context_bounded_and_safety_aware():
    records = {r['id']: r for r in all_records()}
    land = records['WEB-MUN-0043']
    assert 'must not be universalized' in land['notes'].lower()
    food = records['WEB-MUN-0045']
    assert 'must not be generalized' in food['notes'].lower()
    ethnobotany = records['WEB-MUN-0046']
    assert 'no medicinal recommendation' in ethnobotany['notes'].lower()
    assert 'safety' in ethnobotany['rights_note'].lower()


def test_run7_linguistic_debate_and_historical_sources_are_contextualized():
    records = {r['id']: r for r in all_records()}
    assert 'contradiction' in records['WEB-MUN-0048']['notes'].lower()
    assert 'rather than treated as a single definitive' in records['WEB-MUN-0049']['notes'].lower()
    assert records['WEB-MUN-0050']['year'] == 1873
    assert records['WEB-MUN-0051']['year'] == 1882
    assert '10.21437/tai.2023-17' in records['WEB-MUN-0052']['notes'].lower()


def test_run8_demographic_comparative_and_web_media_scope_boundaries():
    records = {r['id']: r for r in all_records()}
    assert 'cultural identity' in records['WEB-MUN-0053']['notes'].lower()
    assert 'exact atlas page/map locators' in records['WEB-MUN-0054']['notes'].lower()
    assert 'not as direct evidence about mundari' in records['WEB-MUN-0055']['notes'].lower()
    assert 'item-level provenance' in records['WEB-MUN-0056']['notes'].lower()


def test_run9_dissertations_tri_grammar_and_lexical_dataset_boundaries():
    records = {r['id']: r for r in all_records()}
    assert 'must not be generalized' in records['WEB-MUN-0057']['notes'].lower()
    assert 'full item is restricted' in records['WEB-MUN-0058']['notes'].lower()
    assert 'drmtwri/1993/0007' in records['WEB-MUN-0059']['notes'].lower()
    assert 'pages 99-164' in records['WEB-MUN-0060']['notes'].lower()
    assert 'cc by 4.0' in records['WEB-MUN-0061']['rights_note'].lower()


def test_run10_song_standard_audio_and_tri_boundaries():
    records = {r['id']: r for r in all_records()}
    assert records['WEB-MUN-0062']['year'] == 1942
    assert 'u+1e4d0' in records['WEB-MUN-0063']['notes'].lower()
    assert 'm036832' in records['WEB-MUN-0064']['notes'].lower()
    assert 'none are promoted as current or universal facts' in records['WEB-MUN-0065']['notes'].lower()


def test_run11_dictionary_article_ethnography_and_web_resource_boundaries():
    records = {r['id']: r for r in all_records()}
    dictionary = records['WEB-MUN-0066']
    assert dictionary['year'] == 1931
    assert 'exact page/entry locator' in dictionary['notes'].lower()
    mimetic = records['WEB-MUN-0067']
    assert '10.1017/cnj.2017.13' in mimetic['notes'].lower()
    assert 'language- and corpus-scoped' in mimetic['notes'].lower()
    roy = records['WEB-MUN-0068']
    assert roy['year'] == 1912
    assert 'lccn 43045615' in roy['notes'].lower()
    assert 'present-day or universal' in roy['notes'].lower()
    web = records['WEB-MUN-0069']
    assert 'individual lesson provenance' in web['notes'].lower()
    assert 'model training' in web['rights_note'].lower()
    assert 'cultural-access' in web['rights_note'].lower()


def test_run12_multimodal_archive_and_folk_literature_boundaries():
    records = {r['id']: r for r in all_records()}
    choksi = records['WEB-MUN-0070']
    assert '10.1017/s0047404519000824' in choksi['notes'].lower()
    assert 'participant/consent provenance' in choksi['notes'].lower()
    ideophones = records['WEB-MUN-0071']
    assert '10.4225/72/585bea79cf9dd' in ideophones['notes'].lower()
    assert 'cc by-sa 4.0' in ideophones['rights_note'].lower()
    assert 'item-level verification' in ideophones['rights_note'].lower()
    folk = records['WEB-MUN-0072']
    assert '10.5958/0975-6884.2023.00017.8' in folk['notes'].lower()
    assert 'not promoted as universal/current munda facts' in folk['notes'].lower()


def test_source_leads_do_not_claim_ingestion_or_verification_of_cultural_facts():
    records = all_records()
    forbidden_states = {'verified_complete', 'cultural_fact_verified', 'community_validated'}
    assert not (forbidden_states & {r['verification_state'] for r in records})
    assert any('page-level' in r['notes'].lower() for r in records)
    assert any('must not be universalized' in r['notes'].lower() for r in records)
    assert any('source-reported' in r['notes'].lower() for r in records)
