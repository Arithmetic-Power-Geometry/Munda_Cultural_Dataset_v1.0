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
engine.render()
