import software.mlhkp_knowledge_engine as engine

engine.WEB = engine.WEB + engine.load(
    'data/source_census/web_discovery_expansion_2026-09-06_run2.json',
    {},
).get('records', [])

engine.render()
