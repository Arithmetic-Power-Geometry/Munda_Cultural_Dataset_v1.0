from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
MMSC = ROOT / 'data' / 'source_census' / 'mmsc_index.json'
DISCOVERIES = ROOT / 'data' / 'source_census' / 'mmsc_discoveries.json'
SEARCH_LOG = ROOT / 'data' / 'source_census' / 'search_log.jsonl'
MASTER = ROOT / 'data' / 'source_register' / 'master_sources.json'
MUNDARICA = ROOT / 'data' / 'source_bundles' / 'encyclopaedia_mundarica' / 'manifest.json'
WEB_DISCOVERY = ROOT / 'data' / 'source_census' / 'web_discovery_seed_2026-09-06.json'
PROTOCOL = ROOT / 'docs' / 'mmsc_source_census_protocol.md'


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def externally_located_ids(manifest):
    return [v['source_id'] for v in manifest['volume_slots'] if v.get('external_source')]


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
        assert rights in {
            'not_assessed',
            'repository_metadata_observed_not_independently_assessed_for_redistribution',
        }
    assert manifest['audit_summary']['registered_authoritative_scans'] == 0
    assert manifest['audit_summary']['verified_complete_volumes'] == 0


def test_standalone_discovery_has_required_evidence_preserving_fields():
    discoveries = load(DISCOVERIES)['records']
    assert len(discoveries) == 1
    r = discoveries[0]
    assert r['source_id'] == 'SRC-MMSC-000001'
    assert r['identifier'] == {'scheme': 'OCLC', 'value': '936769273'}
    assert r['verification_state'] == 'catalogue_metadata_verified'
    assert r['acquisition_state'] == 'not_acquired'
    assert r['rights_reuse_status'] == 'not_assessed'
    assert r['access_class'] == 'BIBLIOGRAPHIC_ONLY'
    for key in ['title', 'creator', 'year', 'source_type', 'language', 'geography', 'cultural_domain_coverage', 'canonical_catalogue_url', 'availability', 'scan_state', 'ocr_state', 'full_text_state', 'extraction_state', 'evidence_link_state', 'provenance']:
        assert key in r


def test_mmsc_metrics_are_repository_counts_not_completeness_claims():
    mmsc = load(MMSC)
    manifest = load(MUNDARICA)
    master = load(MASTER)
    discoveries = load(DISCOVERIES)['records']
    counted = {x['source_id'] for x in master['sources']}
    counted.update(externally_located_ids(manifest))
    counted.update(x['source_id'] for x in discoveries)
    assert mmsc['metrics']['sources_discovered'] == len(counted) == 27
    assert mmsc['metrics']['additional_federated_discoveries'] == 13
    assert mmsc['metrics']['standalone_mmsc_discoveries'] == len(discoveries) == 1
    assert mmsc['metrics']['mundarica_authoritative_scans_registered'] == manifest['audit_summary']['registered_authoritative_scans'] == 0
    assert mmsc['metrics']['mundarica_verified_complete_volumes'] == manifest['audit_summary']['verified_complete_volumes'] == 0
    assert mmsc['completeness_claim'] == 'source_comprehensive_under_documented_protocol_only'


def test_web_discovery_is_visible_but_not_double_counted_before_identity_dedup():
    mmsc = load(MMSC)
    web = load(WEB_DISCOVERY)['records']
    assert len(web) == 14
    assert mmsc['web_discovery_layer']['records'] == len(web)
    assert mmsc['metrics']['web_discovery_leads_observed'] == len(web)
    assert mmsc['metrics']['web_discovery_leads_counted_in_audited_identity_total'] == 0
    web_register = next(x for x in mmsc['source_registers'] if x['register_type'] == 'web_source_discovery_leads')
    assert web_register['counted_records'] == 0
    assert web_register['observed_leads'] == len(web)


def test_search_log_has_stable_ids_and_no_unregistered_permanent_references():
    rows = [json.loads(line) for line in SEARCH_LOG.read_text(encoding='utf-8').splitlines() if line.strip()]
    registered = {r['source_id'] for r in load(DISCOVERIES)['records']}
    registered |= {r['source_id'] for r in load(MASTER)['sources']}
    registered |= set(externally_located_ids(load(MUNDARICA)))
    assert rows
    assert [r['search_id'] for r in rows] == [f'MMSC-SEARCH-{i:06d}' for i in range(1, len(rows) + 1)]
    assert len({r['search_id'] for r in rows}) == len(rows)
    assert all(r['checked_utc'] and r['repository'] and r['query'] and r['outcome'] and 'notes' in r for r in rows)
    assert all(set(r['result_source_ids']) <= registered for r in rows)


def test_mmsc_protocol_preserves_evidence_and_access_boundaries():
    text = PROTOCOL.read_text(encoding='utf-8')
    required = [
        'Public availability does not establish redistribution or reuse permission.',
        'Never treat OCR as verified text.',
        'scan/page image, raw OCR, working transcription, verified transcription and structured content',
        'Restricted, sacred, private or consent-limited material must not be made public',
        'not a source-completeness claim',
    ]
    for phrase in required:
        assert phrase in text
