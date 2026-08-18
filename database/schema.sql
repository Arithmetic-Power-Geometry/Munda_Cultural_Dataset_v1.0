-- PostgreSQL 15+ schema for Munda Cultural Dataset v1.0
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE TABLE IF NOT EXISTS cultural_domains (
 domain_id text PRIMARY KEY, parent_group text NOT NULL, domain_name text NOT NULL, sort_order integer NOT NULL);
CREATE TABLE IF NOT EXISTS cultural_subdomains (
 subdomain_id text PRIMARY KEY, domain_id text NOT NULL REFERENCES cultural_domains(domain_id), subdomain_name text NOT NULL, sort_order integer NOT NULL);
CREATE TABLE IF NOT EXISTS cultural_indicators (
 indicator_id text PRIMARY KEY, domain_id text NOT NULL REFERENCES cultural_domains(domain_id), subdomain_id text REFERENCES cultural_subdomains(subdomain_id),
 indicator_kind text, indicator_label text NOT NULL, research_prompt text, knowledge_status text NOT NULL DEFAULT 'candidate', verification_status text,
 ocm_code text, version integer NOT NULL DEFAULT 1, status text NOT NULL DEFAULT 'active', extended_data jsonb NOT NULL DEFAULT '{}'::jsonb,
 created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now());
CREATE TABLE IF NOT EXISTS sources (
 source_id text PRIMARY KEY, source_class text, title text NOT NULL, creator text, year text, url text, source_type text, geographic_scope text, scope_note text, reuse_note text,
 extended_data jsonb NOT NULL DEFAULT '{}'::jsonb);
CREATE TABLE IF NOT EXISTS source_claims (
 claim_id text PRIMARY KEY, source_id text NOT NULL REFERENCES sources(source_id), domain_id text REFERENCES cultural_domains(domain_id), subdomain_id text REFERENCES cultural_subdomains(subdomain_id),
 claim_label text NOT NULL, claim_paraphrase text NOT NULL, local_term text, geographic_scope text, claim_status text, field_verification_status text, notes text,
 extended_data jsonb NOT NULL DEFAULT '{}'::jsonb);
CREATE TABLE IF NOT EXISTS places (
 place_id text PRIMARY KEY, place_name text NOT NULL, place_type text, district_or_block text, state text, country text, latitude numeric, longitude numeric, note text, source_id text REFERENCES sources(source_id), extended_data jsonb NOT NULL DEFAULT '{}'::jsonb);
CREATE TABLE IF NOT EXISTS observations (
 observation_id text PRIMARY KEY, indicator_id text NOT NULL REFERENCES cultural_indicators(indicator_id), place_id text REFERENCES places(place_id), participant_id text, event_id text,
 value_state text, narrative text, extended_data jsonb NOT NULL DEFAULT '{}'::jsonb, evidence_status text, created_at timestamptz DEFAULT now(), updated_at timestamptz DEFAULT now());
CREATE TABLE IF NOT EXISTS entities (
 entity_id text PRIMARY KEY, entity_type text NOT NULL, native_id text NOT NULL, label text, domain_id text, subdomain_id text, extended_data jsonb NOT NULL DEFAULT '{}'::jsonb,
 UNIQUE(entity_type,native_id));
CREATE TABLE IF NOT EXISTS evidence (
 evidence_id text PRIMARY KEY, evidence_type text NOT NULL, source_id text REFERENCES sources(source_id), claim_id text REFERENCES source_claims(claim_id), representation text,
 verification_state text, access_level text NOT NULL DEFAULT 'public', locator text, notes text, extended_data jsonb NOT NULL DEFAULT '{}'::jsonb);
CREATE TABLE IF NOT EXISTS evidence_links (
 link_id text PRIMARY KEY, from_type text NOT NULL, from_id text NOT NULL, to_type text NOT NULL, to_id text NOT NULL, relationship_type text NOT NULL, extended_data jsonb NOT NULL DEFAULT '{}'::jsonb);
CREATE TABLE IF NOT EXISTS audit_log (
 audit_id uuid PRIMARY KEY DEFAULT gen_random_uuid(), actor text, entity_type text, entity_id text, operation text, old_data jsonb, new_data jsonb, reason text, changed_at timestamptz NOT NULL DEFAULT now());
CREATE INDEX IF NOT EXISTS idx_claim_domain ON source_claims(domain_id);
CREATE INDEX IF NOT EXISTS idx_claim_source ON source_claims(source_id);
CREATE INDEX IF NOT EXISTS idx_ind_domain ON cultural_indicators(domain_id,subdomain_id);
CREATE INDEX IF NOT EXISTS idx_evidence_claim ON evidence(claim_id);
CREATE INDEX IF NOT EXISTS idx_entity_json ON entities USING gin(extended_data);
