import json
from pathlib import Path


def test_run228_ministry_tri_exact_catalogue_boundary():
    p = Path('data/source_census/ministry_tribal_affairs_munda_1993_exact_catalogue_locator_run228_2026-09-12.json')
    data = json.loads(p.read_text(encoding='utf-8'))
    assert data['run'] == 228
    assert data['branch'] == 'mlhkp-v2'
    assert data['source']['record_id'] == 'DRMTWRI/1993/0007'
    assert data['source']['pagination'] == '1-44'
    assert data['source']['reported_file'] == 'DRMTWRI_1993_0007_MUNDAJATIRaman.pdf'
    assert data['identity_verification']['official_government_repository_record'] is True
    assert data['locator_state']['catalogue_level_exact_locator_verified'] is True
    assert data['locator_state']['bitstream_bytes_acquired'] is False
    assert data['locator_state']['independent_hash_computed'] is False
    assert data['rights_and_governance']['public_availability_treated_as_permission'] is False
    assert data['rights_and_governance']['community_validation_inferred'] is False
    assert data['promotion']['promoted_beyond_discovery_only'] is True
    assert data['promotion']['promoted_to_claim_evidence_graph'] is False
    assert data['deduplication']['new_identity_count_increment_permitted'] is False
    assert data['release_effect']['counts_changed'] is False
    assert data['release_effect']['release_gate'] == 'NOT_PASS'


def test_run228_all_class_search_log_and_counts_frozen():
    p = Path('data/source_census/search_log_run228.jsonl')
    row = json.loads(p.read_text(encoding='utf-8').strip())
    required = {
        'books', 'dictionaries', 'grammars', 'peer-reviewed articles',
        'theses/dissertations', 'government/TRI/Census/LSI materials',
        'archives', 'newspapers/periodicals', 'web resources', 'datasets',
        'audio', 'video', 'maps', 'relevant media'
    }
    assert row['search_id'] == 'MMSC-SEARCH-000228'
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
