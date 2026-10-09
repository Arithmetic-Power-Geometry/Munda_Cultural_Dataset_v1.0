import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
audit_path = root / 'data/source_census/ciil_mundari_grammar_manifestation_batch_run302_2026-09-13.json'
log_path = root / 'data/source_census/search_log_run302.jsonl'


def test_run302_audit_boundary():
    data = json.loads(audit_path.read_text(encoding='utf-8'))
    assert data['run'] == 302
    assert data['branch'] == 'mlhkp-v2'
    assert len(data['records']) == 3
    assert {r['repository_identifier'] for r in data['records']} == {'BVP03961', 'BVP00202', 'BVP04856'}
    assert all(r['content_ingested'] is False for r in data['records'])
    s = data['promotion_summary']
    assert s['new_exact_manifestation_locators'] == 3
    assert s['new_controlled_cultural_claims'] == 0
    assert s['new_controlled_linguistic_claims'] == 0
    assert s['new_controlled_evidence_records'] == 0
    assert s['new_provenance_links'] == 0


def test_run302_search_class_count():
    rows = [json.loads(x) for x in log_path.read_text(encoding='utf-8').splitlines() if x.strip()]
    assert len(rows) == 14
    assert len({r['class'] for r in rows}) == 14
