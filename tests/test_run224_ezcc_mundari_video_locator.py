import json
from pathlib import Path


def test_run224_ezcc_mundari_video_locator():
    p = Path('data/source_census/ezcc_jharkhand_mundari_video_exact_locator_run224_2026-09-12.json')
    data = json.loads(p.read_text(encoding='utf-8'))
    assert data['run'] == 224
    assert data['branch'] == 'mlhkp-v2'
    assert data['youtube_video_id'] == 'jcaVTX0BCtQ'
    assert data['manifestation']['reported_sha1'] == 'eb3421c6428ea386f8f340520ab9aa0672de6000'
    assert data['manifestation']['independent_sha1_recomputed'] is False
    labels = {(x['timestamp'], x['label']) for x in data['exact_locators']}
    assert ('00:04:28', 'Paika (Munda community)') in labels
    assert ('00:06:00', 'Mundari') in labels
    assert ('00:11:12', 'Mundari (Marriage)') in labels
    assert data['rights']['commons_license'] == 'CC BY 3.0 Unported'
    assert data['rights']['public_availability_treated_as_participant_consent'] is False
    assert data['rights']['public_availability_treated_as_community_validation'] is False
    assert data['rights']['license_treated_as_cultural_access_clearance'] is False
    assert data['promotion']['discovery_only'] is False
    assert data['promotion']['exact_locator_evidence_record_created'] is True
    assert data['promotion']['public_cultural_claim_promoted'] is False
    assert data['release_effect']['counts_changed'] is False
    assert data['release_effect']['release_gate'] == 'NOT_PASS'


def test_run224_media_coverage_is_live_partial():
    p = Path('data/coverage_matrix.json')
    data = json.loads(p.read_text(encoding='utf-8'))
    row = next(r for r in data['rows'] if r['coverage_id'] == 'COV-008')
    assert row['data_type'] == 'oral_story_song_media'
    assert row['coverage_state'] == 'live_partial'
    assert 'consent and rights' in row['gap_rule']
