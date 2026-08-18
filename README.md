# Munda Cultural Dataset v1.0

**Cultural Indicators, Customs, Usages and Commonalities — From Birth to Burial**

Copyright © 2026 Mohammad Amir Khusru Akhtar and Arvind Hans. Licensed under the Apache License, Version 2.0.

## Purpose

Munda Cultural Dataset (MCD) is an extensible, evidence-linked cultural knowledge system for documenting Munda cultural life from pregnancy and birth through childhood, youth, kinship, marriage, household life, sacred life, festivals, material culture, language and performance, elderhood, death, mourning, memorialisation, ancestors, and cultural change.

The release uses a **hybrid architecture**:

- relational core for permanent identifiers, integrity and reproducible joins;
- JSON/JSONB extension fields for unexpected or evolving ethnographic attributes;
- evidence graph links so every claim can connect to books, journal articles, government records, interviews, observations, objects, photographs, video, audio and community validation;
- immutable source/evidence records plus versioned interpretation and audit history;
- SQLite seed database for zero-configuration Streamlit deployment;
- PostgreSQL schema for production research deployment.

## Evidence policy

A published statement is not automatically treated as a universal fact about all Munda communities. Records are explicitly distinguished as `source_reported`, `bibliographic_pointer`, `contextual_not_munda_exclusive`, or later `field_documented` / `community_validated`. Field research may confirm, modify, localize, contest or supersede a published claim without erasing its provenance.

## Core hierarchy

`Domain → Subdomain → Indicator → Observation/Event/Object/Expression → Evidence → Source → Validation → Book mapping`

Permanent IDs are never reused. New knowledge is added through new records, JSON extensions or new relationship types rather than destructive schema changes.

## Current release content

- 24 top-level cultural domains
- 266 subdomains
- 798 adaptive candidate indicators
- 14 curated seed sources
- 38 source-backed claims/pointers with provenance
- 38 evidence records and explicit evidence links
- OCM crosswalk entries using only HRAF codes verified in the cited HRAF material
- blank fieldwork tables for observations, events, ritual steps, objects, interviews, media, validation, contradictions, discoveries and book mapping

The seed layer is intentionally conservative: it is a **verified starting corpus, not a claim of exhaustive coverage of every publication ever produced**. The architecture is designed so further literature mining and field documentation can be added without redesign.

## Deploy on Streamlit Community Cloud

1. Push this repository to GitHub.
2. In Streamlit Community Cloud, select `streamlit_app.py` as the entry point.
3. Add the owner password hash in **Secrets**:

```toml
OWNER_PASSWORD_HASH = "pbkdf2_sha256$..."
```

Generate it locally:

```bash
python software/generate_password_hash.py
```

Only `akakhtar.2024@gmail.com` plus the configured password can enter edit mode. The owner data editor covers domains, subdomains, indicators, sources, source-backed claims, evidence and places, and all edits are audit logged. Public users can browse and report corrections. If SMTP secrets are configured, the report is sent directly to `akakhtar.2024@gmail.com`; otherwise the app provides a pre-filled email link.

The included SQLite database works immediately on Streamlit. For durable multi-user editing, configure an external PostgreSQL database with `DATABASE_URL` and run `database/schema.sql` plus a seed/import workflow.

## API

`api.py` provides a FastAPI read API and owner-token protected write endpoint. Streamlit Community Cloud is intended for the Streamlit application; the FastAPI service can be deployed separately when a public machine API is required. Set `MCD_ADMIN_TOKEN` in the API deployment environment.

Example endpoints:

- `GET /health`
- `GET /domains`
- `GET /indicators?domain_id=DOM-06`
- `GET /claims?q=Patthalgari`
- `GET /claims/CLM-000001`
- `PATCH /claims/{claim_id}` — owner token required

## Data model principle

Every cultural indicator can answer, where applicable:

**What + Name + Who + When + Where + How + Sequence + Object + Material + Words + Performance + Food/Drink + Kinship + Gender/Age + Meaning + Function + Restriction + Variation + History + Change + Commonality + Evidence + Validation + Access + Book mapping.**

## Source citation

Every researched row contains a `source_id`; `data/sources.csv` contains the bibliographic record and URL. Source wording is paraphrased except for short labels/terms. Researchers should consult the underlying source before quoting it.

## Repository structure

```text
Munda_Cultural_Dataset_v1.0/
├── streamlit_app.py
├── api.py
├── LICENSE
├── NOTICE
├── CITATION.cff
├── requirements.txt
├── data/
├── docs/
├── ontology/
├── database/
├── software/
├── media/
├── tests/
└── releases/
```

## Citation

Akhtar, M. A. K., & Hans, A. (2026). *Munda Cultural Dataset (MCD): Cultural Indicators, Customs, Usages and Commonalities from Birth to Burial* (Version 1.0).

## License

Apache License 2.0 applies to original code, schemas, documentation and original dataset compilation. Third-party source material retains its original copyright/license. This repository stores source metadata and paraphrased claims rather than redistributing copyrighted full texts, images, audio or video.
