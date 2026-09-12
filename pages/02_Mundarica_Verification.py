import json
from pathlib import Path
import streamlit as st

BASE = Path(__file__).resolve().parents[1]
REVIEWERS = BASE / "data" / "governance" / "reviewer_registry.json"
MANIFEST = BASE / "data" / "source_bundles" / "encyclopaedia_mundarica" / "manifest.json"
AUDIT = BASE / "data" / "source_bundles" / "encyclopaedia_mundarica" / "completeness_audit.json"
ARTIFACTS = BASE / "data" / "source_bundles" / "encyclopaedia_mundarica" / "artifact_registry.json"

st.set_page_config(page_title="Mundarica Verification | MLHKP", page_icon="✅", layout="wide")

@st.cache_data
def load_json(path, fallback):
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.exists() else fallback
    except Exception:
        return fallback

reviewers = load_json(REVIEWERS, {"reviewers": [], "policy": {}})
manifest = load_json(MANIFEST, {"volume_slots": [], "audit_summary": {}})
audit = load_json(AUDIT, {"volumes": []})
artifacts = load_json(ARTIFACTS, {"artifacts": []})

st.title("Mundarica Verification Workspace")
st.caption("Human verification is recorded as evidence. A reviewer designation never changes OCR, rights, access, or completeness status by itself.")

people = reviewers.get("reviewers", [])
if people:
    r = people[0]
    st.subheader("Designated textual reviewer")
    st.markdown(f"**{r.get('name')}**  \n{r.get('designation')}")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Declared verification expertise**")
        for x in r.get("declared_expertise", []):
            st.write(f"• {x}")
        st.markdown("**Permitted verification scope**")
        for x in r.get("verification_scope", []):
            st.write(f"• {x}")
    with c2:
        st.markdown("**Non-negotiable scope limits**")
        for x in r.get("scope_limits", []):
            st.write(f"• {x}")
        st.info(r.get("credential_note", ""))
else:
    st.warning("No designated textual reviewer is registered.")

policy = reviewers.get("policy", {})
st.subheader("Verification rules")
st.write("**Required layer order:** scan/page image → raw OCR → working transcription → verified transcription → structured content")
st.write("Verified transcription requires comparison with an authoritative scan/page image." if policy.get("verified_transcription_requires_authoritative_scan_comparison") else "Verification policy not configured.")
st.write("OCR alone can never be marked as verified transcription." if policy.get("ocr_alone_can_never_be_verified_transcription") else "OCR policy not configured.")
st.write("Community validation remains distinct from textual verification." if policy.get("community_validation_is_distinct_from_textual_verification") else "Community-validation policy not configured.")
st.write("Cultural access and consent override any public, owner, institutional or commercial entitlement." if policy.get("cultural_access_overrides_entitlement") else "Access precedence policy not configured.")

volumes = manifest.get("volume_slots", [])
audit_by_source = {x.get("source_id"): x for x in audit.get("volumes", [])}
artifact_by_source = {}
for a in artifacts.get("artifacts", []):
    artifact_by_source.setdefault(a.get("source_id"), []).append(a)

st.subheader("Volumes I–XVI · live verification state")
rows = []
for v in volumes:
    sid = v.get("source_id")
    av = audit_by_source.get(sid, {})
    aa = artifact_by_source.get(sid, [])
    rows.append({
        "volume": v.get("volume_number"),
        "source_id": sid,
        "status": v.get("status"),
        "registered_artifacts": len(aa),
        "authoritative_scan_registered": bool(v.get("authoritative_scan_registered")),
        "page_accounting_complete": bool(av.get("page_accounting_complete")),
        "verified_transcription_complete": bool(av.get("verified_transcription_complete")),
        "structured_ingestion_complete": bool(av.get("structured_ingestion_complete")),
        "verified_complete": bool(v.get("verified_complete")),
    })
st.dataframe(rows, use_container_width=True, hide_index=True)

verified = sum(1 for x in rows if x["verified_complete"])
page_accounted = sum(1 for x in rows if x["page_accounting_complete"])
scans = sum(1 for x in rows if x["authoritative_scan_registered"])
c = st.columns(4)
c[0].metric("Volume slots", len(rows))
c[1].metric("Page-accounted", page_accounted)
c[2].metric("Authoritative scans registered", scans)
c[3].metric("VERIFIED COMPLETE", verified)

st.subheader("How your verification will be recorded")
st.markdown("Each review decision must create or update a machine-readable verification record containing reviewer ID, source/volume, exact page or locator, scan/artifact locator, reviewed record/text ID, decision, uncertainty notes and review timestamp. Uncertain or illegible text remains flagged rather than guessed.")
st.warning("Reviewer sign-off can promote only the passages/pages actually checked against an authoritative scan. A whole volume becomes VERIFIED COMPLETE only after every required textual, structural, provenance, rights/access and completeness gate passes its machine-readable audit.")

st.divider()
st.caption("MLHKP · MCD evidence architecture. Textual verification does not itself establish community validation, cultural permission, redistribution rights or commercial reuse permission.")
