import csv
import json
import software.mlhkp_knowledge_engine as engine

# Additively load every external-discovery expansion file so new verified source
# leads become searchable without manually editing this entry point each cycle.
web_records = list(engine.WEB)
seen_ids = {record.get('id') for record in web_records if record.get('id')}
for path in sorted((engine.BASE / 'data' / 'source_census').glob('web_discovery_expansion_*.json')):
    try:
        document = json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        continue
    for record in document.get('records', []):
        source_id = record.get('id')
        if source_id and source_id not in seen_ids:
            web_records.append(record)
            seen_ids.add(source_id)

engine.WEB = web_records

# The immutable SQLite seed can lag additive v2 CSV/JSON evidence between full
# database rebuilds. Extend the public catalogue from the canonical additive
# registers so newly audited MMSC sources and public evidence are searchable in
# the same commit, while retaining the engine's access filtering and never
# turning discovery metadata into cultural facts.
_base_catalogue = engine.catalogue

def _csv_rows(rel):
    path = engine.BASE / rel
    if not path.exists():
        return []
    with path.open(encoding='utf-8-sig', newline='') as handle:
        return list(csv.DictReader(handle))


def _synchronized_catalogue():
    records = _base_catalogue()
    existing_ids = {r.get('id') for r in records if r.get('id')}

    source_lookup = {s.get('source_id'): s for s in list(engine.MASTER) + list(engine.DISC)}
    for source in engine.DISC:
        sid = source.get('source_id')
        if not sid or sid in existing_ids or not engine.safe(source.get('access_class')):
            continue
        records.append({
            'kind': 'MLHKP source',
            'id': sid,
            'title': source.get('title'),
            'author': source.get('creator'),
            'year': source.get('year'),
            'topic': source.get('source_class'),
            'status': source.get('verification_state'),
            'url': source.get('canonical_catalogue_url'),
            'text': source.get('provenance', {}).get('caution') or '',
        })
        existing_ids.add(sid)

    claims = {r.get('claim_id'): r for r in _csv_rows('data/source_claims.csv') if r.get('claim_id')}
    existing_evidence = {r.get('id') for r in records if r.get('kind') == 'Evidence' and r.get('id')}
    for evidence in _csv_rows('data/evidence.csv'):
        eid = evidence.get('evidence_id')
        if not eid or eid in existing_evidence:
            continue
        if str(evidence.get('access_level') or 'public').lower() not in {'public', 'open'}:
            continue
        claim = claims.get(evidence.get('claim_id'), {})
        source = source_lookup.get(evidence.get('source_id'), {})
        records.append({
            'kind': 'Evidence',
            'id': eid,
            'title': claim.get('claim_label') or evidence.get('claim_id'),
            'author': '',
            'year': source.get('year') or source.get('publication_year') or '',
            'topic': claim.get('domain_id'),
            'status': evidence.get('verification_state'),
            'url': source.get('canonical_catalogue_url') or source.get('url'),
            'text': claim.get('claim_paraphrase') or '',
            'source_id': evidence.get('source_id'),
            'source_title': source.get('title'),
            'geography': claim.get('geographic_scope'),
        })
        existing_evidence.add(eid)
    return records

engine.catalogue = _synchronized_catalogue
engine.render()
