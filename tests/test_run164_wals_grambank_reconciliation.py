from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / 'data' / 'source_census' / 'wals_grambank_deterministic_reconciliation_run164_2026-09-10.json'
MMSC = ROOT / 'data' / 'source_census' / 'mmsc_index.json'
DISCOVERIES = ROOT / 'data' / 'source_census' / 'mmsc_discoveries.json'


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def test_run164_reconciliation_closes_duplicate_precondition_without_count_inflation():
    audit = load(AUDIT)
    mmsc = load(MMSC)
    decision = audit['decision']
    assert audit['run'] == 164
    assert decision['wals_existing_permanent_identity_found'] is False
    assert decision['grambank_existing_permanent_identity_found'] is False
    assert decision['wals_existing_web_observation_found'] is False
    assert decision['grambank_existing_web_observation_found'] is False
    assert decision['new_permanent_identity_assigned_in_this_commit'] is False
    assert decision['counts_changed'] is False
    assert mmsc['metrics']['sources_discovered'] == 41
    assert mmsc['metrics']['web_discovery_leads_observed'] == 90
    assert mmsc['metrics']['web_discovery_unique_leads'] == 87
    assert mmsc['metrics']['web_discovery_unique_leads_remaining_outside_audited_identity_total'] == 74


def test_run164_candidates_are_not_already_in_standalone_discoveries():
    text = DISCOVERIES.read_text(encoding='utf-8').lower()
    assert 'wals.info' not in text
    assert 'grambank.clld.org' not in text
    assert '83a-mun' not in text
    assert 'database:grambank' not in text


def test_run164_preserves_rights_and_cultural_access_boundaries():
    audit = load(AUDIT)
    boundary = audit['evidence_boundary']
    rights = audit['rights_boundary']
    assert boundary['underlying_grammar_passages_verified'] is False
    assert boundary['cultural_claim_promoted'] is False
    assert boundary['participant_content_ingested'] is False
    assert boundary['community_validation_inferred'] is False
    assert boundary['cultural_access_inferred'] is False
    assert rights['underlying_grammar_rights_inferred'] is False
    assert rights['public_access_overrides_cultural_access'] is False
