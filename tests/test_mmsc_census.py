from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
MMSC=ROOT/'data'/'source_census'/'mmsc_index.json'
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
    mmsc=load(MMSC); manifest=load(MUNDARICA)
    v2=next(v for v in manifest['volume_slots'] if v['source_id']=='SRC-MUN-V02')
    latest=mmsc['latest_discovery']
    assert latest['source_id']=='SRC-MUN-V02'
    assert latest['canonical_url']==v2['external_source']['canonical_url']
    assert latest['identifier']==v2['external_source']['identifier']
    assert latest['provenance']['catalogued_pages']==v2['external_source']['total_pages_as_catalogued']==406
    assert v2['status']=='external_source_locator_verified_not_ingested'
    assert v2['verified_complete'] is False
    assert v2['external_source']['acquisition_status']=='locator_verified_not_acquired'
    assert v2['external_source']['rights_status']=='not_assessed'
    assert 'unverified' in v2['external_source']['verification_note'].lower()


def test_mmsc_metrics_are_current_repository_counts_not_completeness_claims():
    mmsc=load(MMSC); manifest=load(MUNDARICA)
    counted=set()
    master=load(MASTER)
    counted.update(x['source_id'] for x in master['sources'])
    counted.update(mmsc['source_registers'][1]['currently_counted_source_ids'])
    assert mmsc['metrics']['sources_discovered']==len(counted)==15
    assert mmsc['metrics']['additional_federated_discoveries']==1
    assert mmsc['metrics']['mundarica_volume_locators_verified']==sum(
        1 for v in manifest['volume_slots'] if v.get('external_source')
    )
    assert mmsc['metrics']['mundarica_authoritative_scans_registered']==manifest['audit_summary']['registered_authoritative_scans']==0
    assert mmsc['metrics']['mundarica_verified_complete_volumes']==manifest['audit_summary']['verified_complete_volumes']==0
    assert mmsc['completeness_claim']=='source_comprehensive_under_documented_protocol_only'


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
