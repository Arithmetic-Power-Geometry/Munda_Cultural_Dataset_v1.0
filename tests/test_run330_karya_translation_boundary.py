import json
from pathlib import Path


def test_karya_translation_locator_boundary():
    p = Path('data/source_census/karya_translation_locator_run330_2026-09-14.json')
    data = json.loads(p.read_text(encoding='utf-8'))
    assert data['repository'] == 'karya-inc/dataset-hindi-mundari-translation'
    assert data['manifestation'] == 'translation-hi-unr.tsv'
    assert data['declared_sentence_pairs'] == 17826
    assert data['status'] == 'locator_verified_content_not_promoted'
    assert data['bytes_hash_verified'] is False
    assert data['rows_independently_verified'] is False
    assert data['consent_verified'] is False
    assert data['community_validation_verified'] is False
    assert data['cultural_access_verified'] is False
