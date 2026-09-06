import json
import sys
from pathlib import Path
import streamlit as st

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE / "software"))
try:
    from db import rows
except Exception:
    rows = None

REGISTRY = BASE / "data" / "module_registry.json"
COVERAGE = BASE / "data" / "coverage_matrix.json"
MODEL = BASE / "data" / "information_model.json"
MMSC = BASE / "data" / "source_census" / "mmsc_index.json"
MASTER = BASE / "data" / "source_register" / "master_sources.json"
MUNDARICA = BASE / "data" / "source_bundles" / "encyclopaedia_mundarica" / "manifest.json"

st.set_page_config(page_title="MLHKP Research Portal", page_icon="🌿", layout="wide")

EMPTY = "Structure ready — evidence not yet ingested"

@st.cache_data
def load_json(path, fallback):
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.exists() else fallback
    except Exception:
        return fallback

registry = load_json(REGISTRY, {"modules": []})
coverage = load_json(COVERAGE, {"rows": []})
model = load_json(MODEL, {"record_families": [], "record_contract": {}})
mmsc = load_json(MMSC, {"metrics": {}})
master = load_json(MASTER, {"sources": []}).get("sources", [])
mundarica = load_json(MUNDARICA, {"volume_slots": []})
modules = registry.get("modules", [])
record_families = model.get("record_families", [])
model_domains = sorted({d for family in record_families for d in family.get("domains", [])})

st.markdown("""
<style>
.block-container{max-width:1440px;padding-top:1.2rem}
.portal-hero{padding:1.4rem 1.5rem;border:1px solid #dfe7df;border-radius:20px;background:linear-gradient(135deg,#f4f8f3,#fffaf1)}
.portal-hero h1{font-family:Georgia,serif;color:#103c2a;margin:.1rem 0 .4rem}
.badge{display:inline-block;padding:.2rem .5rem;border-radius:999px;background:#edf4ee;border:1px solid #d5e3d8;font-size:.75rem;margin-right:.25rem}
.module-card{padding:1rem 1.1rem;border:1px solid #e3ded2;border-radius:14px;background:white;margin:.5rem 0}
.module-title{font-size:1.15rem;font-weight:800;color:#153f2d}
.empty{padding:1rem;border-left:4px solid #a4472d;background:#fff8f3;border-radius:8px}
</style>
""", unsafe_allow_html=True)

st.markdown("""<div class="portal-hero"><div style="font-size:.75rem;font-weight:900;letter-spacing:.13em;color:#2d6845">MUNDA LIVING HERITAGE & KNOWLEDGE PROJECT</div><h1>Research & Public Knowledge Portal</h1><div>Architecture first, evidence always. Every module below has a defined data home, provenance contract and gap state; empty modules are shown honestly rather than populated with invented cultural facts.</div></div>""", unsafe_allow_html=True)

metrics = mmsc.get("metrics", {})
volumes = mundarica.get("volume_slots", [])
verified = sum(1 for v in volumes if v.get("verified_complete") is True)
cols = st.columns(6)
cols[0].metric("Registered source discoveries", metrics.get("sources_discovered", len(master)))
cols[1].metric("Mundarica volume slots", len(volumes))
cols[2].metric("Mundarica VERIFIED COMPLETE", verified)
cols[3].metric("Architecture modules", len(modules))
cols[4].metric("Information-model domains", len(model_domains))
cols[5].metric("Coverage rows", len(coverage.get("rows", [])))
st.caption("Metrics are calculated from registered repository state only. Public availability never implies reuse permission; OCR never implies verified transcription.")

# Grouped navigation: intentionally not one giant flat radio list.
group_order = ["Discover","Culture & Knowledge","People & Place","History & Change","Research Library","Evidence & Research","MLHKP","Future (disabled by default)"]
groups = [g for g in group_order if any(m.get("group") == g for m in modules)]
nav1, nav2 = st.columns([1,2])
with nav1:
    group = st.selectbox("Section", groups, index=0)
with nav2:
    group_modules = [m for m in modules if m.get("group") == group]
    labels = [m.get("label") for m in group_modules]
    label = st.selectbox("Module", labels, index=0)
module = next(m for m in group_modules if m.get("label") == label)

if module.get("enabled") is False:
    st.info("Future capability — disabled by default. Cultural access restrictions will override any future subscription or institutional entitlement.")
    st.stop()

st.markdown(f"### {module['label']}")
st.markdown(" ".join(f'<span class="badge">{d}</span>' for d in module.get("domains", [])), unsafe_allow_html=True)

if label == "Home Research Dashboard":
    st.subheader("Complete data skeleton")
    c = st.columns(4)
    c[0].metric("Record families", len(record_families))
    c[1].metric("Explicit domain homes", len(model_domains))
    c[2].metric("Applicable record fields", len(model.get("record_contract", {}).get("required_for_applicable_records", [])))
    c[3].metric("Evidence-chain stages", len(model.get("evidence_chain", [])))
    st.caption("These are schema/architecture counts, not evidence-completeness claims.")
    family_rows = [{"family_id":f.get("family_id"), "data home":f.get("label"), "domains":", ".join(f.get("domains", [])), "schemas":", ".join(f.get("primary_schemas", [])), "access rule":f.get("access_rule", "standard evidence/access contract")} for f in record_families]
    st.dataframe(family_rows, use_container_width=True, hide_index=True)
    st.info("All record families are structure-ready. Evidence coverage remains independently audited through the coverage matrix and source/evidence registries.")

# Universal Search: permitted metadata + public/open evidence only.
elif label == "Universal Search":
    q = st.text_input("Keyword", placeholder="Search permitted source metadata and public/open evidence")
    f1,f2,f3 = st.columns(3)
    with f1: author = st.text_input("Author / creator")
    with f2: year = st.text_input("Year")
    with f3: language = st.text_input("Language")
    hits = []
    for s in master:
        blob = " ".join(str(s.get(k,"")) for k in ["source_id","title","creator","author","year","language","geography","source_type"])
        if q and q.lower() not in blob.lower(): continue
        if author and author.lower() not in blob.lower(): continue
        if year and year not in blob: continue
        if language and language.lower() not in blob.lower(): continue
        hits.append({"source_id":s.get("source_id"),"title":s.get("title"),"creator":s.get("creator") or s.get("author"),"year":s.get("year"),"source_type":s.get("source_type"),"availability":s.get("availability"),"rights":s.get("rights_reuse_status") or s.get("rights_status")})
    st.metric("Permitted metadata matches", len(hits))
    if hits: st.dataframe(hits, use_container_width=True, hide_index=True)
    else: st.markdown(f'<div class="empty">{EMPTY}</div>', unsafe_allow_html=True)

elif label == "Master Munda Source Census":
    c = st.columns(6)
    c[0].metric("Discovered", metrics.get("sources_discovered",0))
    c[1].metric("Acquired", metrics.get("sources_acquired",0))
    c[2].metric("Full text / OCR", metrics.get("full_text_or_ocr_available",0))
    c[3].metric("Structured", metrics.get("structured_sources",0))
    c[4].metric("Evidence-linked", metrics.get("evidence_linked_sources",0))
    c[5].metric("Still to acquire", metrics.get("still_to_acquire_additional_discoveries",0))
    st.info("Source-comprehensive means comprehensive under the documented release protocol, with residual gaps explicit; it never means future-proof or metaphysically complete.")
    st.dataframe(master, use_container_width=True, hide_index=True)

elif label == "Mundarica I–XVI Digital Library":
    st.warning("Layer rule: scan → raw OCR → working transcription → verified transcription → structured content. Each layer remains separate.")
    if volumes:
        summary=[]
        for v in volumes:
            summary.append({"volume":v.get("volume_number"),"source_id":v.get("source_id"),"status":v.get("status"),"verified_complete":bool(v.get("verified_complete")),"scan_registered":v.get("authoritative_scan_registered"),"rights":v.get("rights_reuse_status") or v.get("rights_status")})
        st.dataframe(summary,use_container_width=True,hide_index=True)
        chosen = st.selectbox("Open volume status", [str(x.get("volume_number")) for x in volumes])
        v = next(x for x in volumes if str(x.get("volume_number")) == chosen)
        tabs = st.tabs(["Read","Entries","Stories","Songs","Terms","Places","Cultural Topics","Source & Provenance","Verification"])
        with tabs[0]: st.markdown(f'<div class="empty">{EMPTY if not v.get("working_transcription_path") else "Working transcription is registered; verification status remains separate."}</div>',unsafe_allow_html=True)
        with tabs[7]: st.dataframe([{k:v.get(k) for k in ["source_id","status","canonical_url","external_identifier","rights_reuse_status","authoritative_scan_registered"]}],hide_index=True,use_container_width=True)
        with tabs[8]:
            st.metric("VERIFIED COMPLETE", "YES" if v.get("verified_complete") is True else "NO")
            if v.get("verified_complete") is not True: st.info("Verification gate has not passed. This volume must not be represented as VERIFIED COMPLETE.")
        for t in tabs[1:7]:
            with t: st.markdown(f'<div class="empty">{EMPTY}</div>', unsafe_allow_html=True)
    else: st.markdown(f'<div class="empty">{EMPTY}</div>', unsafe_allow_html=True)

elif label == "Evidence Explorer":
    if rows:
        try:
            ev = rows("SELECT e.evidence_id,e.evidence_type,e.verification_state,e.access_level,c.claim_id,c.claim_label,c.domain_id,s.source_id,s.title FROM evidence e JOIN source_claims c ON c.claim_id=e.claim_id JOIN sources s ON s.source_id=c.source_id WHERE lower(COALESCE(e.access_level,'public')) IN ('public','open') ORDER BY e.evidence_id")
        except Exception: ev=[]
    else: ev=[]
    st.caption("Trace: SOURCE → PASSAGE/SEGMENT/EVENT/OBJECT → EVIDENCE → CLAIM → INDICATOR → DOMAIN")
    if ev: st.dataframe(ev,use_container_width=True,hide_index=True)
    else: st.markdown(f'<div class="empty">{EMPTY}</div>', unsafe_allow_html=True)

elif label == "Research Gaps / Completeness":
    st.dataframe(coverage.get("rows",[]),use_container_width=True,hide_index=True)
    st.caption("Coverage states describe repository ingestion state, not cultural importance or truth.")

elif label == "Governance & Ethics":
    st.markdown("**Mr. Rajan Pahan — Founding Community, Meetings & Field Logistics Coordinator**")
    st.write("Coordinates community consultations, culturally appropriate introductions, meetings and field logistics. This role does not independently determine scholarly interpretation or final scholarly approval.")
    st.success("Cultural access and consent restrictions override commercial, owner, institutional or future subscription entitlement.")

else:
    matching = [r for r in coverage.get("rows",[]) if label in r.get("streamlit_module","")]
    if matching:
        st.dataframe(matching,use_container_width=True,hide_index=True)
    st.markdown(f'<div class="empty"><b>{EMPTY}</b><br>Required next step: ingest permitted, provenance-linked records for this module and update the evidence graph and coverage audit in the same cycle.</div>', unsafe_allow_html=True)

st.divider()
st.caption("MLHKP · MCD evidence architecture. Third-party rights remain with their holders. Consent, cultural restrictions and heritage safeguards govern access and reuse.")