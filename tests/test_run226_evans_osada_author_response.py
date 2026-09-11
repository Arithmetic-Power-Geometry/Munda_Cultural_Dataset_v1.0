import json
from pathlib import Path


def test_run226_evans_osada_author_response_boundary():
    p = Path('data/source_census/evans_osada_2005_author_response_exact_locator_run226_2026-09-12.json')
    data = json.loads(p.read_text(encoding='utf-8'))
    assert data['run'] == 226
    assert data['branch'] == 'mlhkp-v2'
    assert data['source']['doi'] == '10.1515/lity.2005.9.3.442'
    assert data['source']['anu_handle'] == '1885/32609'
    assert data['source']['pages'] == '442-457'
    assert data['source']['anu_access_statement'] == 'Open Access'
    assert data['identity_verification']['doi_matches_across_anu_repository_and_anu_research_portal'] is True
    assert data['locator_state']['article_level_locator_verified'] is True
    assert data['locator_state']['bitstream_bytes_acquired'] is False
    assert data['locator_state']['independent_hash_computed'] is False
    assert data['locator_state']['page_image_inspected'] is False
    assert data['rights_and_governance']['open_access_treated_as_blanket_redistribution_license'] is False
    assert data['rights_and_governance']['participant_consent_inferred'] is False
    assert data['rights_and_governance']['community_validation_inferred'] is False
    assert data['rights_and_governance']['cultural_access_permission_inferred'] is False
    assert data['deduplication']['new_identity_count_increment_permitted'] is False
    assert data['promotion']['promoted_to_claim_evidence_graph'] is False
    assert data['promotion']['linguistic_proposition_promoted'] is False
    assert data['release_effect']['counts_changed'] is False
    assert data['release_effect']['release_gate'] == 'NOT_PASS'


def test_run226_all_class_search_log_and_counts_frozen():
    p = Path('data/source_census/search_log_run226.jsonl')
    row = json.loads(p.read_text(encoding='utf-8').strip())
    required = {
        'books', 'dictionaries', 'grammars', 'peer-reviewed articles',
        'theses/dissertations', 'government/TRI/Census/LSI materials',
        'archives', 'newspapers/periodicals', 'web resources', 'datasets',
        'audio', 'video', 'maps', 'relevant media'
    }
    assert row['search_id'] == 'MMSC-SEARCH-000226'
    assert required.issubset(set(row['classes_searched']))
    assert row['deduplication']['count_increment_permitted'] is False
    assert row['counts']['audited_source_identities'] == 42
    assert row['counts']['unresolved_unique_web_leads'] == 73
    assert row['counts']['source_claims'] == 52
    assert row['counts']['evidence_records'] == 52
    assert row['counts']['evidence_links'] == 52
    assert row['counts']['streamlit_modules'] == 42
    assert row['counts_changed'] is False
    assert row['release_gate'] == 'NOT_PASS'
