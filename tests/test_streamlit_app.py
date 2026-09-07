from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def test_streamlit_entrypoint_exists_and_uses_research_portal():
    entry = (ROOT/'streamlit_app.py').read_text(encoding='utf-8')
    portal = ROOT/'pages'/'01_Research_Portal.py'
    assert portal.exists()
    assert 'web_discovery_expansion_' in entry


def test_research_portal_is_grouped_not_flat_navigation():
    text = (ROOT/'pages'/'01_Research_Portal.py').read_text(encoding='utf-8')
    for heading in ['Discover', 'Culture & Knowledge', 'People & Place', 'History & Change', 'Research Library', 'Evidence & Research', 'MLHKP']:
        assert heading in text


def test_external_discovery_expansions_are_present_and_searchable_by_entrypoint():
    files = sorted((ROOT/'data'/'source_census').glob('web_discovery_expansion_*.json'))
    assert files
    entry = (ROOT/'streamlit_app.py').read_text(encoding='utf-8')
    assert 'glob' in entry and 'web_discovery_expansion_' in entry


def test_governance_exact_rajan_pahan_role_is_preserved_without_duplicate_entrypoint_footer():
    expected = 'Founding Community, Meetings & Field Logistics Coordinator'
    corpus = ''
    for path in [ROOT/'streamlit_app.py', ROOT/'pages'/'01_Research_Portal.py']:
        corpus += path.read_text(encoding='utf-8')
    assert expected in corpus
    assert (ROOT/'streamlit_app.py').read_text(encoding='utf-8').count(expected) <= 1


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
    registry = json.loads((ROOT/'data'/'source_bundles'/'encyclopaedia_mundarica'/'artifact_registry.json').read_text(encoding='utf-8'))
    working = [a for a in registry['artifacts'] if a.get('source_id') == 'SRC-MUN-V01' and a.get('artifact_role') == 'transcription_working']
    assert len(working) == 1
    artifact = working[0]
    assert artifact['declared_page_count'] == 324
    assert artifact['verification_status'] == 'structurally_audited'
    assert artifact['scan_authority'] is False
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


def test_no_verified_complete_mundarica_volume_is_claimed():
    manifest = json.loads((ROOT/'data'/'source_bundles'/'encyclopaedia_mundarica'/'manifest.json').read_text(encoding='utf-8'))
    assert manifest['audit_summary']['verified_complete_volumes'] == 0


def test_cultural_access_override_contract_present():
    corpus = (ROOT/'streamlit_app.py').read_text(encoding='utf-8') + (ROOT/'pages'/'01_Research_Portal.py').read_text(encoding='utf-8')
    assert 'cultural' in corpus.lower() and 'access' in corpus.lower()


def test_publication_release_metrics_are_repository_derived():
    status = json.loads((ROOT/'status'/'mlhkp_progress.json').read_text(encoding='utf-8'))
    assert status['workstreams']['E_publication_readiness']['repository_derived_metrics'] is True
