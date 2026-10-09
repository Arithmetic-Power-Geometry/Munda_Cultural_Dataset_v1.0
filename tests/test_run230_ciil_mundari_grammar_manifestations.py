import json
from pathlib import Path


def test_run230_ciil_grammar_manifestation_boundaries():
    p = Path('data/source_census/ciil_sanchika_mundari_grammar_manifestations_run230_2026-09-12.json')
    data = json.loads(p.read_text(encoding='utf-8'))
    assert data['run'] == 230
    assert data['branch'] == 'mlhkp-v2'
    assert data['identity_verification']['institutional_repository_verified'] is True
    assert data['identity_verification']['visual_cover_manifestations_verified'] == 3
    assert data['identity_verification']['full_text_verified'] is False
    keys = {x['canonical_key'] for x in data['sources']}
    assert keys == {'ciil:CIILP0091', 'ciil:BVP00202', 'ciil:BVP04856'}
    for source in data['sources']:
        assert source['direct_pdf_rendered'] is True
        assert source['cover_visually_verified'] is True
        assert source['byte_preserving_download_acquired'] is False
        assert source['independent_hash_computed'] is False
        assert source['claim_level_locator_promoted'] is False
    assert data['rights_and_governance']['public_availability_treated_as_permission'] is False
    assert data['rights_and_governance']['unrestricted_redistribution_permission_inferred'] is False
    assert data['rights_and_governance']['participant_consent_inferred'] is False
    assert data['rights_and_governance']['community_validation_inferred'] is False
    assert data['rights_and_governance']['cultural_access_permission_inferred'] is False
    assert data['deduplication']['new_identity_count_increment_permitted'] is False
    assert data['promotion']['promoted_beyond_discovery_only'] is True
    assert data['promotion']['promoted_to_claim_evidence_graph'] is False
    assert data['release_effect']['counts_changed'] is False
    assert data['release_effect']['coverage_matrix_remains_synchronized'] is True
    assert data['release_effect']['release_gate'] == 'NOT_PASS'


def test_run230_all_class_search_log_and_synchronization():
    p = Path('data/source_census/search_log_run230.jsonl')
    row = json.loads(p.read_text(encoding='utf-8').strip())
    required = {
        'books', 'dictionaries', 'grammars', 'peer-reviewed articles',
        'theses/dissertations', 'government/TRI/Census/LSI materials',
        'archives', 'newspapers/periodicals', 'web resources', 'datasets',
        'audio', 'video', 'maps', 'relevant media'
    }
    assert row['search_id'] == 'MMSC-SEARCH-000230'
    assert required.issubset(set(row['classes_searched']))
    assert row['deduplication']['count_increment_permitted'] is False
    assert row['counts']['audited_source_identities'] == 42
    assert row['counts']['raw_web_discovery_records'] == 90
    assert row['counts']['unique_web_discovery_leads'] == 87
    assert row['counts']['duplicate_web_records'] == 3
    assert row['counts']['canonicalized_unique_web_leads'] == 14
    assert row['counts']['unresolved_unique_web_leads'] == 73
    assert row['counts']['source_claims'] == 52
    assert row['counts']['evidence_records'] == 52
    assert row['counts']['evidence_links'] == 52
    assert row['counts']['streamlit_modules'] == 42
    assert row['synchronization']['mmsc_counts'] == 'unchanged and synchronized'
    assert row['counts_changed'] is False
    assert row['release_gate'] == 'NOT_PASS'
