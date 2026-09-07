# MLHKP Master Source Register

The **Master Source Register (MSR)** is the canonical source identity layer for the Munda Living Heritage & Knowledge Project (MLHKP). It preserves every source as a permanent, provenance-bearing record before passages, claims, evidence, cultural entities or book material are derived from it.

## Core principle

A source is registered once, receives a permanent `SRC-*` identifier, and is never silently replaced. New editions, volumes, mirrors, archived copies, transcriptions or access locations are added through structured metadata and locators. Cultural claims remain separate from source identity.

## Canonical files

- `data/source_register/master_sources.json` — canonical source registry
- `schemas/source_record.schema.json` — universal source record schema
- `schemas/master_source_register.schema.json` — register-level schema
- `software/validate_master_source_register.py` — migration/integrity validator
- `.github/workflows/mlhkp-source-register-audit.yml` — one-click/automatic validation

The legacy `data/sources.csv` is deliberately preserved unchanged as the historical MCD v1 source register. The Stage 2 validator uses it to prove that all original IDs and core bibliographic identity fields survive the migration. Richer v2 descriptive metadata may be normalized or split across fields, but the original row remains available through the preserved legacy register and an explicit `legacy.source_id` provenance pointer.

## Supported source families

The schema is deliberately source-agnostic. It can register, without redesign:

- encyclopaedias and multi-volume corpora;
- books, chapters, dictionaries and lexicons;
- journal articles, conference papers and scholarly abstracts;
- theses and dissertations;
- government, census, gazetteer and administrative records;
- court judgments and other legal records;
- archival and missionary records;
- museum and catalogue records;
- newspapers, magazines and newsletters;
- websites and digital exhibits;
- maps and geographic sources;
- datasets and machine-readable resources;
- audio, video, documentary and broadcast sources;
- community documents and future source categories.

`source_type` is intentionally an open string rather than a closed enumeration. New kinds of sources therefore do not require a schema redesign. Source-specific attributes belong in `identifiers`, `locators` or `extended_data` until a future version promotes a field to the common core.

## Required provenance dimensions

Every registered source stores, at minimum:

1. permanent source ID;
2. source class and type;
3. title and creator;
4. year/date representation;
5. geographic scope;
6. language;
7. access class;
8. reuse/copyright status;
9. ingestion state;
10. verification state;
11. at least one stable locator for registered legacy sources.

Additional fields support collection membership, edition, volume, issue, pages, publisher, identifiers, multiple locators, temporal scope, transcription state, source-of-truth rules, cultural sensitivity and open-ended extension metadata.

## Access classes

The register uses the project-wide cultural access vocabulary:

- `OPEN`
- `COMMUNITY_ACCESS_ONLY`
- `RESEARCH_RESTRICTED`
- `EMBARGOED`
- `CONFIDENTIAL`
- `NOT_FOR_PUBLICATION`

Registration does not imply permission to publish or redistribute source content.

## Transcription and verification

Text-bearing historical corpora distinguish source registration from transcription quality. The allowed transcription states include:

- `not_started`
- `ocr_only`
- `partially_verified`
- `verified`
- `requires_specialist_review`

For **Encyclopaedia Mundarica**, the governing rule is strict: **verified transcription takes precedence over OCR; OCR is reference/provenance only and must never silently become authoritative text.**

## Encyclopaedia Mundarica series

The collection manifest at `data/source_bundles/encyclopaedia_mundarica/manifest.json` reserves exactly sixteen permanent volume identities:

`SRC-MUN-V01` through `SRC-MUN-V16`.

These IDs are deliberately separate from the migrated legacy IDs `SRC-000001` through `SRC-000014`. The Stage 2 validator checks that no collision occurs.

## Migration guarantee

Stage 2 is considered complete only if automation proves all of the following:

- all 14 legacy source IDs are present;
- no legacy source ID was changed;
- no extra replacement record silently substituted a legacy source;
- source class, title, creator, year, source type and geographic scope remain identical for the migrated source identities;
- every legacy primary URL remains a primary locator;
- every legacy reuse status remains preserved;
- the original `data/sources.csv` remains the retained historical source row layer, linked through `legacy.source_id`;
- all source IDs are unique;
- all records validate against the universal schema;
- the register-level schema validates;
- all sixteen Mundarica volume IDs are reserved and non-colliding;
- automated tests pass in GitHub Actions.

## Future source ingestion

A new source should first be represented as a valid universal source record or source bundle. It may then be placed in the project ingestion path and processed by the MLHKP ingestion workflow. Registration creates provenance; it does **not** automatically create a cultural claim. Claims, evidence, indicators and interpretations must be generated or reviewed in their own layers.

## Relationship to the evidence graph

The expected path is:

`SOURCE → ENTRY/PASSAGE/SEGMENT → EVIDENCE → CLAIM → INDICATOR → DOMAIN`

This separation is fundamental. A historical source can report a practice without that report becoming a claim of present-day universality.
