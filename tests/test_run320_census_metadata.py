import json
from pathlib import Path


def test_run320_census_metadata():
    data = json.loads(Path('data/source_census/census_cross_table_audit_run320_2026-09-14.json').read_text())
    assert data['run'] == 320
    assert len(data['sources']) == 3
    assert all(item['numeric_claims_promoted'] == 0 for item in data['sources'])
