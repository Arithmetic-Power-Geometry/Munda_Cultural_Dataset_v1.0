# Munda Living Heritage & Knowledge Project (MLHKP)

**Document • Preserve • Research • Publish • Educate • Empower**

MLHKP is a long-term cultural, research, digital, publication, media and community initiative for responsible documentation of Munda language, culture, history, oral traditions, knowledge systems and living heritage.

The **Munda Cultural Dataset (MCD)** is the structured evidence engine inside MLHKP. It preserves permanent identifiers, provenance, source passages, cultural indicators, terms, objects, places, events, interviews, media metadata, claims, evidence, variation, contradictions, validation and publication mappings.

## Design principle

MLHKP is designed so that new knowledge can be added without redesigning the system.

```text
Source / Fieldwork / Media
        ↓
Passage / Segment / Event / Object
        ↓
Evidence
        ↓
Claim
        ↓
Indicator
        ↓
Domain
        ↓
Report / Dataset / Book / API
```

A historical description is not automatically treated as a present-day or universal Munda practice. Historical, source-reported, field-documented, community-validated, contested and restricted records remain distinguishable.

## Current MCD baseline

- 24 top-level cultural domains
- 266 subdomains
- 798 adaptive candidate indicators
- evidence-linked seed literature
- permanent IDs and evidence links
- SQLite zero-configuration deployment
- PostgreSQL production schema
- public Streamlit explorer
- owner editing and audit trail
- FastAPI interface

The existing MCD v1.0 data remain the baseline. The `mlhkp-v2` branch expands the repository into the wider MLHKP architecture without discarding those records.

## Core MLHKP layers

```text
MLHKP
├── 00 project governance and safeguards
├── 01 cultural ontology
├── 02 textual source corpora
├── 03 fieldwork
├── 04 media and material evidence
├── 05 cultural entities
├── 06 evidence graph
├── 07 analysis
├── 08 publications and book projects
├── 09 public/research releases
├── 10 software, API and ingestion
└── 11 audit, correction and administration
```

See [`docs/MLHKP_ARCHITECTURE.md`](docs/MLHKP_ARCHITECTURE.md).

## Encyclopaedia Mundarica corpus

The architecture supports the complete multi-volume *Encyclopaedia Mundarica* as a first-class historical corpus. Each volume should preserve page, entry/headword, definition, passage, example, cross-reference and MCD links while keeping historical-source status separate from contemporary evidence.

Recommended collection path:

```text
data/source_bundles/encyclopaedia_mundarica/
├── manifest.json
├── volume_01.json
├── volume_02.json
├── ...
└── volume_16.json
```

The ingestion engine does not hard-code Mundarica. The same JSON envelope can accept future books, journals, theses, archives, websites, interviews, observations, objects and media metadata.

## One-click JSON ingestion

1. Put a valid JSON bundle in `imports/pending/`.
2. Open **GitHub → Actions → MLHKP Ingest & Validate**.
3. Click **Run workflow**.

The workflow validates the bundle, detects its type, prevents duplicate permanent IDs, copies accepted bundles into the appropriate repository layer, rebuilds the import index, runs tests and commits the processed result back to the branch.

No source is silently converted into an established cultural fact. Semantic linking and publication status remain reviewable.

## Public and owner modes

**Public users:** browse, search, inspect evidence, generate permitted reports, download public releases, cite records and submit corrections.

**Owner mode:** add, edit, archive, restore, merge, split, validate, link evidence, review contradictions, generate research reports, build book evidence packs and approve releases.

Research records should normally be archived rather than destructively deleted.

## Reports and books

MCD is designed to generate evidence-backed reports by topic or domain. A search such as `Marriage` can retrieve linked historical sources, terminology, indicators, field evidence, objects, media, variations, contradictions, validation and evidence gaps.

The publication path is:

```text
MCD master knowledge system
        ↓
Domain / topic evidence report
        ↓
Book evidence pack
        ↓
Scholarly narrative / book / paper
```

This allows one master knowledge system to support the Birth-to-Burial companion book and future domain-specific books without creating separate databases.

## Cultural and data safeguards

MLHKP separates public, working, restricted and archival layers. Collection does not automatically imply permission to publish. Sacred, ritual, clan-specific, medicinal, burial-related, confidential, embargoed or otherwise sensitive material can be assigned controlled access.

The project preserves provenance, consent, correction history and versioning. Raw evidence is not silently altered, and legitimate variation among village, kili, region, dialect, family, generation or knowledge holder is not collapsed merely to create a single account.

## Deployment

The current Streamlit application remains deployable from `streamlit_app.py`. For durable multi-user operation, use the PostgreSQL schema under `database/` and configure an external database connection. SQLite remains useful for local and demonstration deployment.

## Citation

Akhtar, M. A. K., Hans, A., et al. (2026). *Munda Living Heritage & Knowledge Project (MLHKP): Munda Cultural Dataset and Evidence Knowledge System*.

## License and source rights

Apache License 2.0 applies to original software, schemas, documentation and original dataset compilation where stated. Third-party books, source texts, photographs, audio, video and community-contributed material retain their own copyright, consent and reuse conditions. Public availability of a source is not treated as unrestricted permission for redistribution or AI training.
