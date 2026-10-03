import json
from pathlib import Path


def test_karya_object_and_license_boundary_run331():
    p = Path('data/source_census/karya_translation_verification_run331_2026-09-14.json')
    data = json.loads(p.read_text(encoding='utf-8'))
    assert data['repository'] == 'karya-inc/dataset-hindi-mundari-translation'
    assert data['manifestation'] == 'translation-hi-unr.tsv'
    assert data['github_object_sha'] == '131c55a5b8197a58d663a7e40d888a92869288c6'
    assert data['github_reported_size_bytes'] == 3788450
    assert data['license_noncommercial_only'] is True
    assert data['independent_sha256_verified'] is False
    assert data['rows_independently_verified'] is False
    assert data['participant_consent_verified'] is False
    assert data['community_validation_verified'] is False
    assert data['cultural_access_verified'] is False
    assert data['ingestion_authorized_by_mlhkp_governance'] is False
    assert data['public_cultural_claims_promoted'] == 0
