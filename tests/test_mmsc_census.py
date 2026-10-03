from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
MMSC = ROOT / 'data' / 'source_census' / 'mmsc_index.json'
DISCOVERIES = ROOT / 'data' / 'source_census' / 'mmsc_discoveries.json'
SEARCH_LOG = ROOT / 'data' / 'source_census' / 'search_log.jsonl'
MASTER = ROOT / 'data' / 'source_register' / 'master_sources.json'
MUNDARICA = ROOT / 'data' / 'source_bundles' / 'encyclopaedia_mundarica' / 'manifest.json'
PROTOCOL = ROOT / 'docs' / 'mmsc_source_census_protocol.md'


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def externally_located_ids(manifest):
    return [v['source_id'] for v in manifest['volume_slots'] if v.get('external_source')]


def web_discovery_records(mmsc):
    layer = mmsc['web_discovery_layer']
    paths = [layer['path'], *layer.get('additional_paths', [])]
    records = []
    for rel in paths:
        records.extend(load(ROOT / rel)['records'])
    return records


def test_mmsc_federates_without_renumbering_legacy_sources():
    mmsc = load(MMSC)
    master = load(MASTER)
    ids = [x['source_id'] for x in master['sources']]
    assert ids == [f'SRC-{i:06d}' for i in range(1, 15)]
    assert mmsc['metrics']['canonical_master_records'] == len(ids) == 14
    assert mmsc['source_registers'][0]['path'] == 'data/source_register/master_sources.json'


def test_mundarica_locator_count_is_derived_from_manifest():
    mmsc = load(MMSC)
    manifest = load(MUNDARICA)
    ids = externally_located_ids(manifest)
    assert ids == [f'SRC-MUN-V{i:02d}' for i in range(2, 14)]
    assert len(ids) == 12
    assert mmsc['source_registers'][1]['currently_counted_source_ids'] == ids
    assert mmsc['source_registers'][1]['counted_records'] == len(ids)
    assert mmsc['metrics']['mundarica_volume_locators_verified'] == len(ids)
    assert manifest['audit_summary']['externally_located_volumes'] == len(ids)
    assert all(not v['verified_complete'] for v in manifest['volume_slots'])


def test_external_mundarica_ocr_never_promotes_machine_verification():
    manifest = load(MUNDARICA)
    for volume in manifest['volume_slots']:
        ext = volume.get('external_source')
        if not ext:
            continue
        assert volume['status'] == 'external_source_locator_verified_not_ingested'
        assert volume['verified_complete'] is False
        assert ext['acquisition_status'] == 'locator_verified_not_acquired'
        rights = ext.get('rights_status', 'not_assessed')
        assert rights in {'not_assessed','repository_metadata_observed_not_independently_assessed_for_redistribution'}
    assert manifest['audit_summary']['registered_authoritative_scans'] == 0
    assert manifest['audit_summary']['verified_complete_volumes'] == 0


def test_standalone_discoveries_have_required_evidence_preserving_fields():
    discoveries = load(DISCOVERIES)['records']
    assert len(discoveries) >= 2
    assert [r['source_id'] for r in discoveries] == [f'SRC-MMSC-{i:06d}' for i in range(1, len(discoveries) + 1)]
    first, second = discoveries[:2]
    assert first['identifier'] == {'scheme': 'OCLC', 'value': '936769273'}
    assert first['verification_state'] == 'catalogue_metadata_verified'
    assert first['acquisition_state'] == 'not_acquired'
    assert first['rights_reuse_status'] == 'not_assessed'
    assert first['access_class'] == 'BIBLIOGRAPHIC_ONLY'
    assert second['identifier'] == {'scheme': 'DOI', 'value': '10.30884/seh/2025.02.01'}
    assert second['verification_state'] == 'publisher_metadata_doi_and_abstract_verified'
    assert second['acquisition_state'] == 'metadata_and_abstract_only'
    assert second['extraction_state'] == 'abstract_level_scope_evidence_extracted'
    assert second['evidence_link_state'] == 'one_scope_bounded_claim_linked'
    for r in discoveries:
        for key in ['title','creator','year','source_type','language','geography','cultural_domain_coverage','canonical_catalogue_url','availability','scan_state','ocr_state','full_text_state','extraction_state','evidence_link_state','provenance']:
            assert key in r


def test_mmsc_metrics_are_repository_counts_not_completeness_claims():
    mmsc = load(MMSC)
    manifest = load(MUNDARICA)
    master = load(MASTER)
    discoveries = load(DISCOVERIES)['records']
    counted = {x['source_id'] for x in master['sources']}
    counted.update(externally_located_ids(manifest))
    counted.update(x['source_id'] for x in discoveries)
    assert mmsc['metrics']['sources_discovered'] == len(counted)
    assert mmsc['metrics']['additional_federated_discoveries'] == len(counted) - len(master['sources'])
    assert mmsc['metrics']['standalone_mmsc_discoveries'] == len(discoveries)
    assert mmsc['metrics']['mundarica_authoritative_scans_registered'] == manifest['audit_summary']['registered_authoritative_scans'] == 0
    assert mmsc['metrics']['mundarica_verified_complete_volumes'] == manifest['audit_summary']['verified_complete_volumes'] == 0
    assert mmsc['completeness_claim'] == 'source_comprehensive_under_documented_protocol_only'


def test_web_discovery_is_visible_and_only_canonicalized_leads_are_counted():
    mmsc = load(MMSC)
    web = web_discovery_records(mmsc)
    ids = [r['id'] for r in web]
    assert len(web) == mmsc['web_discovery_layer']['records']
    assert len(web) == mmsc['metrics']['web_discovery_leads_observed']
    assert ids == [f'WEB-MUN-{i:04d}' for i in range(1, len(web) + 1)]
    assert len(ids) == len(set(ids))

    canonicalized = [r for r in web if r.get('canonicalization', {}).get('status') == 'canonicalized_new_identity']
    canonical_source_ids = [r['canonicalization']['canonical_source_id'] for r in canonicalized]
    standalone_ids = {r['source_id'] for r in load(DISCOVERIES)['records']}
    expected_count = mmsc['metrics']['web_discovery_leads_counted_in_audited_identity_total']
    web_register = next(x for x in mmsc['source_registers'] if x['register_type'] == 'web_source_discovery_leads')

    assert len(canonicalized) == expected_count
    assert web_register['counted_records'] == expected_count
    assert web_register['observed_leads'] == len(web)
    assert len(canonical_source_ids) == len(set(canonical_source_ids))
    assert set(canonical_source_ids) <= standalone_ids

    latest = mmsc.get('latest_canonicalization')
    if canonicalized:
        assert latest
        assert latest['web_source_id'] in {r['id'] for r in canonicalized}
        assert latest['canonical_source_id'] in set(canonical_source_ids)
    else:
        assert expected_count == 0


def test_search_log_has_stable_ids_and_no_unregistered_permanent_references():
    mmsc = load(MMSC)
    rows = [json.loads(line) for line in SEARCH_LOG.read_text(encoding='utf-8').splitlines() if line.strip()]
    registered = {r['source_id'] for r in load(DISCOVERIES)['records']}
    registered |= {r['source_id'] for r in load(MASTER)['sources']}
    registered |= set(externally_located_ids(load(MUNDARICA)))
    registered |= {r['id'] for r in web_discovery_records(mmsc)}
    assert rows
    assert [r['search_id'] for r in rows] == [f'MMSC-SEARCH-{i:06d}' for i in range(1, len(rows) + 1)]
    assert len({r['search_id'] for r in rows}) == len(rows)
    assert all(r['checked_utc'] and r['repository'] and r['query'] and r['outcome'] and 'notes' in r for r in rows)
    assert all(set(r['result_source_ids']) <= registered for r in rows)


def test_mmsc_protocol_preserves_evidence_and_access_boundaries():
    text = PROTOCOL.read_text(encoding='utf-8')
    required = ['Public availability does not establish redistribution or reuse permission.','Never treat OCR as verified text.','scan/page image, raw OCR, working transcription, verified transcription and structured content','Restricted, sacred, private or consent-limited material must not be made public','not a source-completeness claim']
    for phrase in required:
        assert phrase in text
