import json
from pathlib import Path


def test_run342_karya_translated500_boundary():
    path = Path('audits/karya_endangered_recipes_translated_500_run342_2026-09-14.json')
    data = json.loads(path.read_text(encoding='utf-8'))

    assert data['run'] == 342
    assert data['branch'] == 'mlhkp-v2'
    assert data['identity_verified'] is True
    assert data['provider_reported']['mundari_recipes'] == 50
    assert data['provider_reported']['mundari_sentence_pairs'] == 783
    assert data['provider_reported']['access'] == 'gated'

    # Provider metadata is not independently verified source content.
    assert data['evidence_state'] == 'provider_metadata_locator_verified_content_not_promoted'
    assert data['independent_bytes_verified'] is False
    assert data['independent_hash_verified'] is False
    assert data['provider_counts_recomputed'] is False

    # Public/provider licensing must not be converted into unsupported governance claims.
    assert data['participant_consent_independently_verified'] is False
    assert data['community_validation_independently_verified'] is False
    assert data['cultural_access_review_complete'] is False
    assert data['cultural_or_linguistic_claims_promoted'] is False

    # Keep this derivative distinct from the already-audited Karya source identities.
    note = data['deduplication_note'].lower()
    assert 'distinct derivative manifestation' in note
    assert 'elr-1000' in note
