from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
MMSC=ROOT/'data'/'source_census'/'mmsc_index.json'
DISCOVERIES=ROOT/'data'/'source_census'/'mmsc_discoveries.json'
SEARCH_LOG=ROOT/'data'/'source_census'/'search_log.jsonl'
MASTER=ROOT/'data'/'source_register'/'master_sources.json'
MUNDARICA=ROOT/'data'/'source_bundles'/'encyclopaedia_mundarica'/'manifest.json'
PROTOCOL=ROOT/'docs'/'mmsc_source_census_protocol.md'


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def test_mmsc_federates_without_renumbering_legacy_sources():
    mmsc=load(MMSC); master=load(MASTER)
    ids=[x['source_id'] for x in master['sources']]
    assert ids==[f'SRC-{i:06d}' for i in range(1,15)]
    assert mmsc['metrics']['canonical_master_records']==len(ids)==14
    assert mmsc['source_registers'][0]['path']=='data/source_register/master_sources.json'


def test_mmsc_volume2_discovery_matches_mundarica_manifest():
    manifest=load(MUNDARICA)
    v2=next(v for v in manifest['volume_slots'] if v['source_id']=='SRC-MUN-V02')
    assert v2['external_source']['identifier']=='dli.bengal.10689.21001'
    assert v2['external_source']['total_pages_as_catalogued']==406
    assert v2['status']=='external_source_locator_verified_not_ingested'
    assert v2['verified_complete'] is False
    assert v2['external_source']['acquisition_status']=='locator_verified_not_acquired'
    assert v2['external_source']['rights_status']=='not_assessed'
    assert 'unverified' in v2['external_source']['verification_note'].lower()


def test_mmsc_volume3_discovery_matches_mundarica_manifest_without_promoting_ocr():
    manifest=load(MUNDARICA)
    v3=next(v for v in manifest['volume_slots'] if v['source_id']=='SRC-MUN-V03')
    assert v3['external_source']['identifier']=='in.ernet.dli.2015.14921'
    assert v3['external_source']['ark']=='ark:/13960/t3907ds0b'
    assert v3['external_source']['total_pages_as_catalogued']==264
    assert v3['status']=='external_source_locator_verified_not_ingested'
    assert v3['verified_complete'] is False
    assert v3['external_source']['acquisition_status']=='locator_verified_not_acquired'
    assert 'not_independently_assessed' in v3['external_source']['rights_status']
    assert 'unverified' in v3['external_source']['verification_note'].lower()
    assert manifest['audit_summary']['externally_located_volumes']==2
    assert manifest['audit_summary']['volume_3_local_scan_registered'] is False


def test_standalone_discovery_has_required_evidence_preserving_fields():
    discoveries=load(DISCOVERIES)['records']
    assert len(discoveries)==1
    r=discoveries[0]
    assert r['source_id']=='SRC-MMSC-000001'
    assert r['identifier']=={'scheme':'OCLC','value':'936769273'}
    assert r['verification_state']=='catalogue_metadata_verified'
    assert r['acquisition_state']=='not_acquired'
    assert r['rights_reuse_status']=='not_assessed'
    assert r['access_class']=='BIBLIOGRAPHIC_ONLY'
    for key in ['title','creator','year','source_type','language','geography','cultural_domain_coverage','canonical_catalogue_url','availability','scan_state','ocr_state','full_text_state','extraction_state','evidence_link_state','provenance']:
        assert key in r


def test_mmsc_metrics_are_current_repository_counts_not_completeness_claims():
    mmsc=load(MMSC); manifest=load(MUNDARICA); master=load(MASTER); discoveries=load(DISCOVERIES)['records']
    counted=set(x['source_id'] for x in master['sources'])
    counted.update(mmsc['source_registers'][1]['currently_counted_source_ids'])
    counted.update(x['source_id'] for x in discoveries)
    assert mmsc['metrics']['sources_discovered']==len(counted)==17
    assert mmsc['metrics']['additional_federated_discoveries']==3
    assert mmsc['metrics']['standalone_mmsc_discoveries']==len(discoveries)==1
    assert mmsc['metrics']['mundarica_volume_locators_verified']==sum(1 for v in manifest['volume_slots'] if v.get('external_source'))==2
    assert mmsc['metrics']['mundarica_authoritative_scans_registered']==manifest['audit_summary']['registered_authoritative_scans']==0
    assert mmsc['metrics']['mundarica_verified_complete_volumes']==manifest['audit_summary']['verified_complete_volumes']==0
    assert mmsc['metrics']['deduplicated_locator_matches']>=1
    assert mmsc['completeness_claim']=='source_comprehensive_under_documented_protocol_only'


def test_search_log_is_reproducible_refs_registered_sources_and_records_deduplication():
    rows=[json.loads(line) for line in SEARCH_LOG.read_text(encoding='utf-8').splitlines() if line.strip()]
    ids={r['source_id'] for r in load(DISCOVERIES)['records']} | {'SRC-MUN-V02','SRC-MUN-V03'} | {r['source_id'] for r in load(MASTER)['sources']}
    assert rows
    assert [r['search_id'] for r in rows]==[f'MMSC-SEARCH-{i:06d}' for i in range(1,len(rows)+1)]
    assert len({r['search_id'] for r in rows})==len(rows)
    assert all(r['checked_utc'] and r['repository'] and r['query'] and r['outcome'] and 'notes' in r for r in rows)
    assert all(set(r['result_source_ids']) <= ids for r in rows)
    dedup=next(r for r in rows if r['search_id']=='MMSC-SEARCH-000004')
    assert dedup['result_source_ids']==['SRC-000005']
    assert dedup['outcome']=='deduplicated_locator_match_existing_canonical_source'
    assert 'No new permanent source ID assigned' in dedup['notes']

    unresolved=next(r for r in rows if r['search_id']=='MMSC-SEARCH-000005')
    assert unresolved['result_source_ids']==[]
    assert unresolved['outcome']=='no_exact_authoritative_volume_locator_registered'
    assert 'no Volume IV source ID' in unresolved['notes']

    candidate=next(r for r in rows if r['search_id']=='MMSC-SEARCH-000006')
    assert candidate['result_source_ids']==[]
    assert candidate['outcome']=='candidate_catalogue_record_found_duplicate_check_pending'
    assert 'not assigned a permanent SRC-MMSC ID' in candidate['notes']


def test_mmsc_protocol_preserves_evidence_and_access_boundaries():
    text=PROTOCOL.read_text(encoding='utf-8')
    required=[
        'Public availability does not establish redistribution or reuse permission.',
        'Never treat OCR as verified text.',
        'scan/page image, raw OCR, working transcription, verified transcription and structured content',
        'Restricted, sacred, private or consent-limited material must not be made public',
        'not a source-completeness claim'
    ]
    for phrase in required:
        assert phrase in text
