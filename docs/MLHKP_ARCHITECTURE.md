# MLHKP v2 Architecture

## Purpose

The Munda Living Heritage & Knowledge Project (MLHKP) uses one integrated knowledge system with multiple linked evidence layers. The system must accept future material without destructive redesign and must preserve provenance, variation, access restrictions and correction history.

## Canonical architecture

```text
MLHKP/
├── project/
│   ├── project_manifest.json
│   ├── governance/
│   ├── ethics/
│   ├── consent_templates/
│   ├── access_policy/
│   └── cultural_safeguards/
│
├── ontology/
│   ├── domains.*
│   ├── subdomains.*
│   ├── indicators.*
│   ├── relationship_types.*
│   └── controlled_vocabularies/
│
├── data/
│   ├── source_bundles/
│   │   ├── encyclopaedia_mundarica/
│   │   ├── books/
│   │   ├── journals/
│   │   ├── theses/
│   │   ├── government/
│   │   ├── archives/
│   │   ├── websites/
│   │   └── dictionaries/
│   ├── fieldwork/
│   │   ├── interviews/
│   │   ├── oral_histories/
│   │   ├── observations/
│   │   ├── events/
│   │   ├── ritual_steps/
│   │   ├── field_notes/
│   │   ├── surveys/
│   │   └── community_validations/
│   ├── entities/
│   │   ├── terms/
│   │   ├── kinship/
│   │   ├── kili/
│   │   ├── objects/
│   │   ├── foods/
│   │   ├── plants/
│   │   ├── animals/
│   │   ├── instruments/
│   │   ├── places/
│   │   ├── songs/
│   │   ├── dances/
│   │   └── stories/
│   └── evidence_graph/
│       ├── claims.*
│       ├── evidence.*
│       ├── evidence_links.*
│       ├── contradictions.*
│       ├── variations.*
│       ├── validations.*
│       ├── discoveries.*
│       └── provenance.*
│
├── media/
│   ├── photographs/
│   ├── audio/
│   ├── video/
│   ├── scans/
│   ├── maps/
│   └── 3d_objects/
│
├── analysis/
│   ├── commonality/
│   ├── variation/
│   ├── temporal_change/
│   ├── geographic_distribution/
│   ├── lexical_change/
│   └── evidence_gaps/
│
├── publications/
│   ├── birth_to_burial_book/
│   ├── domain_books/
│   ├── dictionaries/
│   ├── reports/
│   ├── research_papers/
│   └── teaching_materials/
│
├── imports/
│   └── pending/
│
├── ingestion/
│   └── ingest.py
│
├── releases/
│   ├── public/
│   ├── research/
│   └── archive/
│
└── admin/
    ├── audit_log/
    ├── corrections/
    ├── contribution_register/
    └── release_approvals/
```

## Permanent identifiers

Recommended prefixes:

| Prefix | Record |
|---|---|
| DOM | Domain |
| SUB | Subdomain |
| IND | Cultural indicator |
| SRC | Source |
| ENT | Source entry/headword |
| PAS | Source passage |
| CLM | Claim |
| EVD | Evidence |
| TRM | Term |
| OBJ | Object |
| PLC | Place |
| EVT | Event |
| STP | Event or ritual step |
| INT | Interview |
| SEG | Interview/audio/video segment |
| MED | Media |
| VAL | Validation |
| VAR | Variation |
| CON | Contradiction |
| DISC | Discovery |
| BOOK | Book/publication claim |

IDs are never reused.

## Evidence chain

```text
SOURCE
  ↓
ENTRY / PASSAGE / SEGMENT / EVENT / OBJECT
  ↓
EVIDENCE
  ↓
CLAIM
  ↓
INDICATOR
  ↓
DOMAIN
```

This chain supports reverse traversal for reports and books.

## Source status

A source record may be historical, contemporary, bibliographic, archival, contextual, field-derived or community-validated. Historical source text does not automatically establish present-day practice.

Recommended claim/evidence states include:

- `source_reported`
- `historical_source_reported`
- `bibliographic_pointer`
- `contextual_not_munda_exclusive`
- `field_documented`
- `community_validated`
- `contested`
- `superseded_interpretation`
- `restricted`

## Access classes

- `open`
- `community_access_only`
- `research_restricted`
- `embargoed`
- `confidential`
- `not_for_publication`

Access class applies independently of evidentiary strength.

## Universal source bundle

Every imported textual or field source should use the same outer envelope. The bundle identifies itself; folder location is organizational only.

```json
{
  "mcd_schema": "2.0",
  "record_type": "source_bundle",
  "source_type": "book",
  "source": {},
  "entries": [],
  "passages": [],
  "claims": [],
  "terms": [],
  "objects": [],
  "places": [],
  "events": [],
  "relationships": [],
  "metadata": {}
}
```

Field bundles may additionally include interview, consent, segment or event structures. Media binaries remain files; their metadata and segment-level descriptions are represented in JSON/database records.

## Encyclopaedia Mundarica corpus

Treat the complete series as a corpus, not as a set of independent facts.

```text
encyclopaedia_mundarica/
├── manifest.json
├── volume_01.json
├── volume_02.json
├── ...
└── volume_16.json
```

Each volume can preserve:

- volume metadata
- PDF/printed page reference
- headword/entry
- original transcription
- normalized search form
- definition
- examples
- cross-references
- plate/table references
- cultural passages
- candidate claims
- MCD indicator links
- verification status

OCR must never be silently treated as verified transcription.

## PostgreSQL + JSONB

Use relational columns/tables for permanent IDs, joins, status, access, provenance and integrity. Use JSONB for source-specific or future attributes that do not yet justify a first-class column.

Known structure = relational.

Unexpected but valid future structure = JSONB.

## Public Streamlit mode

Public users can:

- browse domains and indicators
- search terms, sources, claims and evidence
- inspect evidence trails
- view public source records
- generate permitted research reports
- download public data subsets
- cite records
- report corrections

Public users cannot alter records.

## Owner mode

Owner functions:

- add/import data
- edit interpretation and metadata
- archive/restore
- merge/split
- link evidence
- approve/reject candidate claims
- validate terminology
- review contradictions
- generate reports
- create book evidence packs
- approve public releases

Hard deletion should be exceptional; archival/versioning is preferred.

## Report engine

A report request such as `Marriage` should retrieve linked material across the graph, not merely rows whose primary domain equals Marriage.

Report families:

1. Quick summary
2. Detailed research report
3. Evidence audit
4. Historical comparison
5. Commonality and variation report
6. Book research report
7. Evidence-gap map

Every factual paragraph in generated scholarly reports should retain claim/evidence/source IDs.

## Book production

```text
MCD knowledge system
   ↓
Domain/topic evidence retrieval
   ↓
Research report
   ↓
Book evidence pack
   ↓
Narrative manuscript
```

One MCD master system can support the general Birth-to-Burial book and multiple domain monographs without creating new databases.

## Integrity gates

Before a public release:

- no duplicate permanent IDs
- no broken parent/child ontology links
- no orphan claims
- no evidence links to missing targets
- no public restricted records
- no missing provenance on source-backed public claims
- no invalid JSON bundles
- no silent overwrite of earlier versions
- no unreviewed OCR presented as verified source text

## Visual identity

The Streamlit interface should use a restrained MLHKP visual system derived from the project emblem: warm cream backgrounds, earth-brown typography, sal-leaf green, limited red accents, subtle geometric borders, serif display headings, modern sans-serif body text and ample whitespace. Cultural imagery should support navigation and identity without becoming decorative clutter.

Suggested home message:

> **Johar. Explore a living cultural world.**
>
> Every statement can show its evidence.
