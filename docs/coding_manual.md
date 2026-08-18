# Coding Manual

## Missingness
Use `unknown`, `not_asked`, `not_applicable`, and `refused` separately. Never convert them to `absent_reported`.

## Provenance
Every claim or observation must point to one or more evidence IDs. Evidence may be a source, interview segment, observation, media record, object record or validation record.

## New discoveries
If a practice does not fit the current ontology, create an `unclassified_discoveries` record. Do not force it into an existing indicator. After review it may become a new indicator while the discovery record remains preserved.

## Editing
Public users cannot edit. Owner edits are written to `audit_log`; permanent IDs are not changed.
