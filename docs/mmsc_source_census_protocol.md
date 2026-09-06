# Master Munda Source Census (MMSC) protocol

## Purpose

MMSC is the discovery-and-accounting layer for MLHKP. It does not claim that a finite registry is metaphysically or permanently complete. A defensible claim is limited to: all sources discovered through the documented search protocol are registered or referenced; obtainable sources are processed according to rights and access rules; unavailable, restricted or unresolved sources remain explicitly represented as gaps.

## Search layers

The census is expanded systematically across: Encyclopaedia Mundarica and related Hoffmann works; S. C. Roy and other classical ethnography; Ram Dayal Munda works; modern books; journal literature; theses and dissertations; Ministry of Tribal Affairs, Tribal Research Institutes and SCSTRTI resources; Census of India and linguistic surveys; gazetteers, settlement, land, tenancy and administrative records; grammars, dictionaries, primers, lexicons and dialect studies; oral literature; song, dance and ethnomusicology; religion and sacred-life studies; life-course studies; material culture; ecology and ethnobotany; geographic variation; contemporary change; fieldwork; audio/video/photo media; and community-validation records.

## Discovery repositories

Searches should preferentially use authoritative or preservation-oriented catalogues and repositories, including Internet Archive, government and Tribal Research Institute repositories, Census of India, Shodhganga and university repositories, national/international library catalogues, publisher/catalogue metadata, DOI-indexed scholarly literature, and bibliographies that can be followed back to primary catalogue records.

## Evidence-preserving rules

1. Preserve permanent source IDs; never renumber an existing source.
2. Keep bibliographic discovery separate from acquisition and separate again from content extraction.
3. Public availability does not establish redistribution or reuse permission.
4. Keep scan/page image, raw OCR, working transcription, verified transcription and structured content as separate artifacts.
5. Never treat OCR as verified text.
6. Never silently normalize uncertain Mundari or comparative forms.
7. Restricted, sacred, private or consent-limited material must not be made public merely because a citation exists.
8. Deduplicate catalogue records while preserving edition, translation, reprint and volume relationships.
9. Register unavailable or restricted sources bibliographically when lawful rather than excluding them from the census.
10. A source can support only what its provenance, scope, date and evidence actually establish.

## Minimum discovery record

Each newly discovered source should resolve, where the catalogue supports it: permanent SRC ID; title; creator; year; source type; language; geography; cultural-domain coverage; canonical URL or catalogue locator; external identifier; availability; scan/OCR/full-text state; acquisition state; rights/reuse status; extraction state; evidence-link state; verification state; provenance; edition relationships; and notes on uncertainty or restriction.

## Count rules

`data/source_census/mmsc_index.json` is a federated census index. Canonical records remain in their authoritative repository files and are referenced rather than copied. Metrics must be calculated from actual repository records, must avoid double-counting the same permanent source ID, and must distinguish discovery from acquisition, extraction, evidence linkage and verification. A volume locator alone is not an acquired artifact; an acquired scan alone is not verified transcription; structural page completeness alone is not VERIFIED COMPLETE.

## Search log

Every systematic discovery cycle should record the repository/catalogue searched, query family, date checked, number of candidate records reviewed, permanent IDs created or linked, duplicate/edition decisions, rights/access uncertainty, unresolved candidates and next search target. Search logs may report zero discoveries; they must never manufacture sources to improve coverage metrics.

## Current baseline

The initial MMSC federation references the 14 preserved canonical MLHKP master-source records and one independently verified Internet Archive locator for `SRC-MUN-V02`. This is a starting baseline only, not a source-completeness claim.
