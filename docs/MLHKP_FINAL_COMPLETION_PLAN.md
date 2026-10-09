# MLHKP Final Completion Plan

## Goal

Build the **Munda Living Heritage & Knowledge Project (MLHKP)** as a long-lived, evidence-linked cultural knowledge system in which the Munda Cultural Dataset (MCD) is the structured data engine. The project must be able to absorb new books, all available *Encyclopaedia Mundarica* volumes, journal articles, theses, archives, websites, interviews, observations, objects, photographs, audio, video, maps, field notes and community validation without redesigning the core architecture.

The completion standard is **not** a claim that no unknown cultural practice can ever exist. The standard is that every known item has a defined place, every factual claim is traceable to evidence, every restriction is respected, every disagreement is preserved, and every known gap is explicitly visible.

## Stage sequence

### Stage 1 — MCD v1 → MLHKP v2 migration audit

**Purpose:** prove that the existing seed corpus is preserved intact before expansion.

Checks:
- 24 domains preserved;
- 266 subdomains preserved;
- 798 adaptive candidate indicators preserved;
- source, claim, evidence and evidence-link records preserved;
- permanent IDs unchanged;
- no duplicate permanent IDs;
- no orphan subdomains or indicators;
- no broken evidence links;
- no public/restricted access regression;
- original MCD v1 remains recoverable.

**Exit criterion:** migration audit passes with zero critical errors.

### Stage 2 — Master Source Register

Create one authoritative source registry for every documentary source. Required source classes include encyclopaedias, books, dictionaries, journal articles, theses/dissertations, government reports, census/administrative material, gazetteers, archival material, missionary records, legal sources, museum catalogues, newspapers, websites, documentaries, maps and existing datasets.

Each source receives a permanent `SRC-*` identifier and records bibliographic metadata, temporal/geographic scope, source type, language, edition, URL/archive locator, copyright/reuse information, ingestion status and verification status.

**Exit criterion:** every source already used by MCD is registered and future sources can be added without schema change.

### Stage 3 — Complete Encyclopaedia Mundarica Corpus

Prepare the complete available 16-volume corpus under a single collection manifest. Each volume must preserve source provenance and, where feasible, page, headword/entry, definition, passage, example, cross-reference, plate/table reference, lexical form and cultural entity links.

Critical rule: OCR is discovery assistance only. Verified transcription is authoritative for quotation, claims, reports and books.

**Exit criterion:** all available volumes registered; every ingested passage has volume/page provenance and explicit verification status.

### Stage 4 — Systematic literature census

Search domain-by-domain and subdomain-by-subdomain for Munda/Mundari literature. Register every relevant source before extracting claims.

**Exit criterion:** all 24 domains and 266 subdomains have documented literature-search status and unresolved search gaps are explicit.

### Stage 5 — Source extraction and evidence graph population

Extract passages, claims, terms, objects, places, roles, events and other entities from registered sources. Link each item through permanent IDs.

Core path:
`Source → Entry/Passage → Evidence → Claim → Indicator → Domain`.

**Exit criterion:** no source-derived public claim exists without provenance.

### Stage 6 — Ontology discovery and expansion

Use all source corpora to detect culturally significant concepts not represented by the existing 798 indicators. New material enters `DISC-*` first and is reviewed before creating or modifying an indicator/subdomain.

**Exit criterion:** no source concept is silently forced into an inappropriate existing indicator.

### Stage 7 — Master cultural lexicon and entity registers

Build permanent registers for terminology, kili/kinship, cultural roles, objects, foods, plants, animals, instruments, dress, ornaments, houses, sacred sites, burial/memorial sites, songs, dances, stories, festivals, rituals and events.

**Exit criterion:** entities can be referenced independently by sources, fieldwork, media, indicators and publications.

### Stage 8 — Completeness and research-gap dashboard

For each indicator calculate documentary coverage, Mundarica coverage, modern-literature coverage, field coverage, media coverage, community-validation coverage, contradiction status and unresolved gaps.

**Exit criterion:** administrators can see exactly what evidence is still missing for every domain.

### Stage 9 — Field instruments generated from gaps

Design interview schedules, observation sheets, event templates, object records, language/pronunciation forms and community-validation instruments from the uncovered gaps rather than collecting unstructured material.

**Exit criterion:** every field question maps to one or more indicators/discoveries and has consent/access metadata.

### Stage 10 — Fieldwork ingestion

Add interviews, oral histories, observations, events, ritual steps, field notes, photographs, audio, video, maps and object documentation.

**Exit criterion:** raw evidence remains preserved; transcripts/interpretations are versioned separately; consent and cultural-access status are mandatory.

### Stage 11 — Variation, contradiction and historical-change analysis

Preserve village, kili, dialect, family, gender/age, generation, geographic and historical differences rather than collapsing them into one universal description.

Relationship examples: `SUPPORTS`, `CONTRADICTS`, `VARIANT_OF`, `HISTORICAL_FORM_OF`, `CONTINUES_AS`, `REPLACED_BY`, `USED_IN`, `PERFORMED_BY`, `LOCATED_AT`, `VALIDATED_BY`.

**Exit criterion:** contradictory evidence remains discoverable and reportable.

### Stage 12 — Community validation and cultural-access review

Supported access classes:
- `OPEN`
- `COMMUNITY_ACCESS_ONLY`
- `RESEARCH_RESTRICTED`
- `EMBARGOED`
- `CONFIDENTIAL`
- `NOT_FOR_PUBLICATION`

**Exit criterion:** public exports cannot expose restricted cultural or personal material.

### Stage 13 — Research-report engine

A topic/domain query such as `Marriage` must retrieve all linked historical, lexical, documentary, field and media evidence and produce an evidence-backed report with claim/evidence/source IDs.

Report modes:
- quick overview;
- detailed research report;
- evidence audit;
- historical comparison;
- commonality and variation;
- book research report.

**Exit criterion:** factual report statements remain traceable to evidence.

### Stage 14 — Book Studio

Generate a domain evidence pack containing research report, claim ledger, evidence ledger, terminology, variations, contradictions, gaps, references, suggested figures/tables and chapter map.

Core workflow:
`MCD → Domain Report → Evidence Pack → Book`.

**Exit criterion:** books are written from the evidence graph rather than from unsupported synthesis.

### Stage 15 — Public Streamlit application

Public users receive read-only access to Explore, Search, Evidence, Sources, Mundarica, Maps/Places, Timeline, Reports, Downloads and About. Restricted data are never included in public search/download.

Visual identity: warm cream, earth brown, restrained sal-leaf green and textile red; generous whitespace; subtle geometric motifs; evidence graph/root metaphor; `Johar` as the opening greeting.

### Stage 16 — Owner Research Console

Owner capabilities: Add Data, Search, Review, Edit, Archive/Restore, Merge/Split, Validate, Evidence Graph, Generate Report, Book Studio, Release and Administration.

Default preservation rule: archive/version rather than destructive deletion.

### Stage 17 — One-click GitHub ingestion and release workflow

Routine administrator process:
1. put JSON/metadata into `imports/pending/`;
2. commit/push;
3. run **MLHKP Ingest & Publish**;
4. validate;
5. deduplicate;
6. check IDs and provenance;
7. route data;
8. run tests;
9. rebuild indexes/releases;
10. deploy only after integrity gate passes.

### Stage 18 — Final reproducibility, preservation and release audit

Required automated checks include duplicate IDs, orphan records, broken evidence links, invalid JSON/schema, missing provenance, missing consent/access metadata, restricted material leaking into public release, unresolved file references and reproducibility of generated release statistics.

**Final completion definition:** the release is structurally complete, evidence-traceable, versioned, culturally access-aware and explicit about remaining research gaps. It does not claim that future fieldwork can never discover new knowledge.

## Publication principle

MLHKP is the umbrella project. MCD is the structured evidence engine. Source corpora, field evidence, media and entity registers feed the evidence graph; the evidence graph feeds analysis, reports and publications.

`Source / Field / Media → Evidence → Claim → Indicator → Domain → Report / Dataset / Book`
