import sys, json, sqlite3, urllib.parse, re
from pathlib import Path
import streamlit as st

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE / "software"))
from db import rows, execute
from auth import is_owner, OWNER_EMAIL
from reporting import send_report

st.set_page_config(page_title="MLHKP | Munda Living Heritage & Knowledge Project", page_icon="🌿", layout="wide", initial_sidebar_state="expanded")

# ---------- Visual identity ----------
st.markdown("""
<style>
:root{--earth:#4a1f12;--red:#a52b1f;--leaf:#376b3a;--cream:#fffaf0;--gold:#b8842f;--ink:#24160f;}
.stApp{background:linear-gradient(180deg,#fffdf8 0%,#fffaf0 100%);color:var(--ink)}
.block-container{max-width:1450px;padding-top:1.4rem;padding-bottom:3rem}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#2d160f 0%,#4a1f12 65%,#2b1711 100%)}
[data-testid="stSidebar"] *{color:#fffaf0}
[data-testid="stSidebar"] hr{border-color:rgba(255,255,255,.2)}
.mlhkp-hero{border:1px solid #e3d2b8;border-radius:24px;padding:28px 34px;background:radial-gradient(circle at 90% 15%,rgba(184,132,47,.18),transparent 30%),linear-gradient(135deg,#fffdf7,#f8edda);box-shadow:0 12px 35px rgba(74,31,18,.08);margin-bottom:1.25rem}
.eyebrow{font-size:.78rem;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:#a52b1f}
.hero-title{font-family:Georgia,serif;font-size:2.65rem;line-height:1.05;color:#3b180e;margin:.25rem 0 .55rem;font-weight:800}
.hero-sub{font-size:1.08rem;color:#684a3b;max-width:900px}
.mission{font-weight:800;letter-spacing:.08em;color:#376b3a;margin-top:1rem}
.info-card{border:1px solid #eadbc7;border-radius:18px;padding:18px;background:#fff;min-height:150px;box-shadow:0 5px 18px rgba(74,31,18,.05)}
.info-card h3{font-family:Georgia,serif;color:#4a1f12;margin:.1rem 0 .5rem;font-size:1.15rem}
.section-title{font-family:Georgia,serif;color:#4a1f12;font-size:1.7rem;font-weight:800;margin-top:.7rem}
.badge{display:inline-block;padding:5px 10px;border-radius:999px;background:#eef5ec;color:#2f6533;font-weight:700;font-size:.78rem;border:1px solid #cfe0cc;margin-right:5px}
.notice{border-left:5px solid #a52b1f;background:#fff7ee;padding:14px 18px;border-radius:8px;margin:12px 0}
.footer{margin-top:2rem;border-top:1px solid #e3d2b8;padding-top:1.2rem;color:#6c5548;font-size:.84rem;line-height:1.6}
div[data-testid="stMetric"]{background:#fff;border:1px solid #eadbc7;padding:14px;border-radius:16px;box-shadow:0 4px 14px rgba(74,31,18,.04)}
.stButton>button,.stDownloadButton>button{border-radius:10px;border:1px solid #8e3a27}
</style>
""", unsafe_allow_html=True)

LOGO = BASE / "assets" / "mlhkp_logo.png"

# ---------- Session / access ----------
if "owner" not in st.session_state:
    st.session_state.owner = False

with st.sidebar:
    if LOGO.exists():
        st.image(str(LOGO), use_container_width=True)
    else:
        st.markdown("## 🌿 MLHKP")
        st.caption("Munda Living Heritage & Knowledge Project")
    st.markdown("**Document · Preserve · Research · Publish · Educate · Empower**")
    st.divider()
    st.subheader("Access")
    if not st.session_state.owner:
        email = st.text_input("Owner email", key="login_email")
        pw = st.text_input("Owner password", type="password", key="login_pw")
        if st.button("Owner sign in", use_container_width=True):
            if is_owner(email, pw, st.secrets):
                st.session_state.owner = True
                st.success("Owner research access enabled")
                st.rerun()
            else:
                st.error("Invalid owner credentials")
    else:
        st.success("Owner research mode")
        if st.button("Sign out", use_container_width=True):
            st.session_state.owner = False
            st.rerun()
    st.divider()
    pages = ["Home", "Culture Explorer", "Master Sources", "Mundarica Corpus", "Source-backed Claims", "Indicators", "Evidence Explorer", "Research Gaps", "Governance & Ethics", "Report / Contribute"]
    if st.session_state.owner:
        pages.append("Owner Research Console")
    page = st.radio("Explore", pages)
    st.divider()
    st.caption(f"Corrections & scholarly correspondence\n{OWNER_EMAIL}")


def count(table):
    try:
        return rows(f"SELECT COUNT(*) n FROM {table}")[0]["n"]
    except Exception:
        return 0


def domain_name(did):
    r = rows("SELECT domain_name FROM cultural_domains WHERE domain_id=?", (did,))
    return r[0]["domain_name"] if r else did


def hero():
    c_logo, c_text = st.columns([1, 3.3], gap="large")
    with c_logo:
        if LOGO.exists():
            st.image(str(LOGO), use_container_width=True)
        else:
            st.markdown("# 🌿")
    with c_text:
        st.markdown("""
        <div class="mlhkp-hero">
          <div class="eyebrow">Munda Living Heritage & Knowledge Project</div>
          <div class="hero-title">A living evidence system for Munda heritage</div>
          <div class="hero-sub">An evolving scholarly and community-aware knowledge infrastructure connecting language, culture, history, oral traditions, material heritage, field evidence and publications — with provenance retained at every step.</div>
          <div class="mission">OUR HERITAGE · OUR KNOWLEDGE · OUR FUTURE</div>
        </div>
        """, unsafe_allow_html=True)


# ---------- Pages ----------
if page == "Home":
    hero()
    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Cultural domains", count("cultural_domains"))
    c2.metric("Subdomains", count("cultural_subdomains"))
    c3.metric("Indicators", count("cultural_indicators"))
    c4.metric("Registered sources", count("sources"))
    c5.metric("Evidence records", count("evidence"))

    st.markdown('<div class="section-title">Explore the knowledge system</div>', unsafe_allow_html=True)
    a,b,c = st.columns(3)
    with a:
        st.markdown('<div class="info-card"><h3>🌾 Culture Explorer</h3>Browse the birth-to-burial ontology: domains, subdomains and evolving cultural indicators. The structure grows without silently overwriting earlier knowledge.</div>', unsafe_allow_html=True)
    with b:
        st.markdown('<div class="info-card"><h3>📚 Sources & Mundarica</h3>Trace books, historical corpora, journals, theses, government records, archives, maps and multimedia. Mundarica is treated as a page-accounted archival corpus.</div>', unsafe_allow_html=True)
    with c:
        st.markdown('<div class="info-card"><h3>🔎 Evidence, not assertion</h3>Move from a cultural claim back to its evidence and source. Published descriptions remain source-reported until stronger field/community validation is available.</div>', unsafe_allow_html=True)
    d,e,f = st.columns(3)
    with d:
        st.markdown('<div class="info-card"><h3>🗣️ Living variation</h3>Village, clan, region, dialect, family, generation and knowledge-holder variants are preserved rather than forced into a single account.</div>', unsafe_allow_html=True)
    with e:
        st.markdown('<div class="info-card"><h3>🛡️ Cultural safeguards</h3>Open, community-only, research-restricted, embargoed, confidential and not-for-publication states support responsible access.</div>', unsafe_allow_html=True)
    with f:
        st.markdown('<div class="info-card"><h3>🧭 Research gaps</h3>Absence is recorded too. The project distinguishes documented knowledge from material awaiting verification, fieldwork or community review.</div>', unsafe_allow_html=True)

    st.markdown("### Current scholarly rule")
    st.info("A source is evidence that an account was reported; it is not automatically proof that the account is universal across all Munda communities. Provenance, variation, verification and cultural access remain explicit.")

elif page == "Culture Explorer":
    st.markdown('<div class="section-title">Culture Explorer</div>', unsafe_allow_html=True)
    st.caption("24-domain evidence architecture for documenting cultural life without collapsing legitimate variation.")
    q = st.text_input("Search domains and subdomains", placeholder="Try marriage, kinship, agriculture, song, burial …")
    ds = rows("SELECT * FROM cultural_domains ORDER BY sort_order")
    for d in ds:
        sds = rows("SELECT * FROM cultural_subdomains WHERE domain_id=? ORDER BY sort_order", (d["domain_id"],))
        hay = (d["domain_name"] + " " + " ".join(x["subdomain_name"] for x in sds)).lower()
        if q and q.lower() not in hay:
            continue
        with st.expander(f"{d['domain_id']}  ·  {d['domain_name']}  —  {len(sds)} subdomains"):
            for x in sds:
                st.markdown(f"**{x['subdomain_id']}** — {x['subdomain_name']}")

elif page == "Master Sources":
    st.markdown('<div class="section-title">Master Source Register</div>', unsafe_allow_html=True)
    st.caption("The source register is the provenance backbone. Source identity is preserved even when interpretation changes.")
    q = st.text_input("Search source register")
    data = rows("SELECT * FROM sources ORDER BY source_id")
    if q:
        data = [x for x in data if q.lower() in json.dumps(x, ensure_ascii=False).lower()]
    st.metric("Sources currently available to the application database", len(data))
    for x in data:
        title = x.get("title") or "Untitled source"
        with st.expander(f"{x.get('source_id','')} · {title}"):
            st.json(x, expanded=False)
            if x.get("url"):
                st.link_button("Open source", x["url"])
    st.info("The MLHKP v2 source-register layer is designed to extend beyond the current seed database to encyclopaedias, books, articles, theses, government records, archives, websites, maps, datasets and audio/video sources.")

elif page == "Mundarica Corpus":
    st.markdown('<div class="section-title">Encyclopaedia Mundarica · Corpus Explorer</div>', unsafe_allow_html=True)
    st.markdown('<span class="badge">16-volume architecture</span><span class="badge">OCR retained</span><span class="badge">scan is authority</span><span class="badge">verification tracked</span>', unsafe_allow_html=True)
    st.markdown("""
    <div class="notice"><b>Preservation rule.</b> Raw OCR is retained as provenance. A transcription is called verified only after comparison with the authoritative scan. Unclear Mundari or comparative forms are flagged for review rather than guessed.</div>
    """, unsafe_allow_html=True)
    vols = [f"Volume {i:02d}" for i in range(1,17)]
    selected = st.selectbox("Select volume", vols)
    v = int(selected.split()[-1])
    if v == 1 and (BASE / "Mundarika1.md").exists():
        st.success("Volume 01 corpus file is present in this repository.")
        text = (BASE / "Mundarika1.md").read_text(encoding="utf-8", errors="replace")
        pages_found = re.findall(r"^## PDF Page\s+(\d+)", text, flags=re.M)
        c1,c2,c3 = st.columns(3)
        c1.metric("Page blocks detected", len(pages_found))
        c2.metric("First page block", pages_found[0] if pages_found else "—")
        c3.metric("Last page block", pages_found[-1] if pages_found else "—")
        page_no = st.number_input("Open PDF page block", min_value=1, max_value=max([int(x) for x in pages_found], default=1), value=6, step=1)
        pattern = rf"(?ms)^## PDF Page\s+{int(page_no)}\s*$\n(.*?)(?=^## PDF Page\s+\d+\s*$|\Z)"
        m = re.search(pattern, text)
        if m:
            st.markdown(f"#### Volume 01 · PDF Page {int(page_no)}")
            st.text_area("Preserved corpus text", m.group(1).strip(), height=480, disabled=True)
        else:
            st.warning("No matching page block was found in the current corpus file.")
    else:
        st.warning(f"{selected} is registered in the 16-volume architecture but its complete corpus is not yet present in this application build.")
    st.caption("A volume must not be labelled VERIFIED COMPLETE until page accounting, OCR alignment, scan verification, unresolved-reading review and integrity checks have passed.")

elif page == "Source-backed Claims":
    st.markdown('<div class="section-title">Source-backed Claims</div>', unsafe_allow_html=True)
    q = st.text_input("Search claims, terms or places")
    data = rows("SELECT c.*, s.title source_title, s.url source_url FROM source_claims c JOIN sources s ON s.source_id=c.source_id ORDER BY c.claim_id")
    if q:
        data = [x for x in data if q.lower() in json.dumps(x,ensure_ascii=False).lower()]
    for x in data:
        with st.expander(f"{x['claim_id']} · {x['claim_label']}"):
            st.write(x['claim_paraphrase'])
            st.write({"domain":domain_name(x['domain_id']),"local_term":x['local_term'],"scope":x['geographic_scope'],"status":x['claim_status'],"field_verification":x['field_verification_status']})
            if x.get('source_url'): st.link_button("Open source",x['source_url'])

elif page == "Indicators":
    st.markdown('<div class="section-title">Cultural Indicators</div>', unsafe_allow_html=True)
    did = st.selectbox("Domain", [""]+[d['domain_id']+" — "+d['domain_name'] for d in rows("SELECT * FROM cultural_domains ORDER BY sort_order")])
    search = st.text_input("Search indicator")
    sql="SELECT * FROM cultural_indicators"; params=[]; cond=[]
    if did: cond.append("domain_id=?"); params.append(did.split(' — ')[0])
    if search: cond.append("(indicator_label LIKE ? OR research_prompt LIKE ?)"); params += [f"%{search}%",f"%{search}%"]
    if cond: sql += " WHERE " + " AND ".join(cond)
    sql += " ORDER BY indicator_id LIMIT 1000"
    st.dataframe(rows(sql,tuple(params)),use_container_width=True,hide_index=True)

elif page == "Evidence Explorer":
    st.markdown('<div class="section-title">Evidence Explorer</div>', unsafe_allow_html=True)
    st.caption("Trace claim → evidence → source. Field evidence can be added later without changing permanent identities.")
    data=rows("SELECT c.claim_id,c.claim_label,e.evidence_id,e.evidence_type,e.verification_state,s.source_id,s.title,s.url FROM source_claims c JOIN evidence e ON e.claim_id=c.claim_id JOIN sources s ON s.source_id=c.source_id ORDER BY c.claim_id")
    st.dataframe(data,use_container_width=True,hide_index=True)

elif page == "Research Gaps":
    st.markdown('<div class="section-title">Research Gaps & Completeness</div>', unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Domains", count("cultural_domains"))
    c2.metric("Indicators", count("cultural_indicators"))
    c3.metric("Source-backed claims", count("source_claims"))
    c4.metric("Evidence records", count("evidence"))
    st.info("This page is intentionally conservative: MLHKP will report documented, partially documented, unverified and missing areas rather than claiming cultural completeness. The full gap engine will expand as the corpus and fieldwork layers are populated.")

elif page == "Governance & Ethics":
    st.markdown('<div class="section-title">Governance, Stewardship & Cultural Ethics</div>', unsafe_allow_html=True)
    st.markdown("""
**MLHKP is an umbrella cultural, research, digital, publication, media and community initiative.** The Munda Cultural Dataset is one of its structured scholarly components.

**Founding record**
- **Dr. Mohammad Amir Khusru Akhtar** — Founder, Founding Chairperson & Founding Principal Investigator; principal scholarly/technical lead and dataset architect.
- **Dr. Arvind Hans** — Founding Project Director; project management, field operations, external review, expert network, media and outreach.
- **Mr. Rajan Pahan** — Founding Community Coordination, Meetings & Logistics Lead.

**Cultural safeguards**
- Collection does not automatically create a right to publish.
- Restricted cultural material may be Open, Community-Access Only, Research-Restricted, Embargoed, Confidential or Not for Publication.
- Legitimate village, clan, region, dialect, family, generation and knowledge-holder variation should be preserved.
- Public availability does not itself imply unrestricted permission for AI training or commercial exploitation.
- Raw, working, restricted and public-release layers should remain distinct.

**Scholarly release principle**
Creation → first-level scholarly review → external/community/domain review where required → revision → final scholarly approval → technical/privacy/consent/cultural-rights checks → release → correction/versioning/archive.
    """)
    st.warning("This interface is a project implementation aid, not a substitute for the signed Founders' Agreement or applicable law.")

elif page == "Report / Contribute":
    st.markdown('<div class="section-title">Report, Correct or Contribute Evidence</div>', unsafe_allow_html=True)
    st.write("Public visitors cannot directly alter scholarly records. Reports enter the review queue so provenance and correction history can be preserved.")
    target=st.text_input("Record ID (optional)")
    name=st.text_input("Your name")
    email=st.text_input("Your email")
    report=st.text_area("Correction, concern, variant account or additional evidence")
    if st.button("Prepare report"):
        if report.strip():
            execute("INSERT INTO reports(target_type,target_id,reporter_name,reporter_email,report_text) VALUES (?,?,?,?,?)",('record',target,name,email,report))
            subject=urllib.parse.quote(f"MLHKP report: {target or 'general'}")
            body=urllib.parse.quote(f"Reporter: {name}\nEmail: {email}\nRecord: {target}\n\n{report}")
            sent,msg=send_report(f"MLHKP report: {target or 'general'}", f"Reporter: {name}\nEmail: {email}\nRecord: {target}\n\n{report}", st.secrets)
            if sent: st.success(f"Report sent to {OWNER_EMAIL} and added to the review queue.")
            else:
                st.success("Report added to the review queue.")
                st.markdown(f"[Send a copy by email](mailto:{OWNER_EMAIL}?subject={subject}&body={body})")
        else: st.warning("Please enter a report.")

elif page == "Owner Research Console":
    if not st.session_state.owner:
        st.error("Owner access required")
    else:
        st.markdown('<div class="section-title">Owner Research Console</div>', unsafe_allow_html=True)
        st.warning("Permanent IDs are immutable. Changes are audit-tracked. Cultural access restrictions and consent must be respected before public release.")
        editable={"cultural_domains":"domain_id","cultural_subdomains":"subdomain_id","cultural_indicators":"indicator_id","sources":"source_id","source_claims":"claim_id","evidence":"evidence_id","places":"place_id"}
        table=st.selectbox("Dataset/table",list(editable))
        pk=editable[table]
        recs=rows(f"SELECT * FROM {table} ORDER BY {pk} LIMIT 2000")
        ids=[r[pk] for r in recs]
        rid=st.selectbox("Record",ids) if ids else None
        if rid:
            rec=next(r for r in recs if r[pk]==rid); newvals={}
            for k,v in rec.items():
                if k==pk or k=="updated_at": st.text_input(k,str(v or ""),disabled=True,key=f"oe_{table}_{rid}_{k}")
                else: newvals[k]=st.text_area(k,str(v or ""),height=70,key=f"oe_{table}_{rid}_{k}")
            reason=st.text_input("Reason for change",key=f"reason_{table}_{rid}")
            if st.button("Save audited changes"):
                changed={k:v for k,v in newvals.items() if str(rec.get(k) or "")!=v}
                if not changed: st.info("No changes detected")
                elif not reason.strip(): st.warning("A reason is required for an audited scholarly change.")
                else:
                    sets=", ".join([f"{k}=?" for k in changed]); vals=list(changed.values())+[rid]
                    execute(f"UPDATE {table} SET {sets} WHERE {pk}=?",tuple(vals))
                    execute("INSERT INTO audit_log(actor,entity_type,entity_id,operation,old_data,new_data,reason) VALUES (?,?,?,?,?,?,?)",(OWNER_EMAIL,table,rid,'update',json.dumps(rec,ensure_ascii=False),json.dumps(changed,ensure_ascii=False),reason))
                    st.success("Saved with audit record"); st.rerun()

# ---------- Rights / provenance footer ----------
st.markdown("""
<div class="footer">
<b>Munda Living Heritage & Knowledge Project (MLHKP)</b> · Ranchi, Jharkhand, India<br>
<b>Founding record:</b> Dr. Mohammad Amir Khusru Akhtar — Founder, Founding Chairperson & Founding Principal Investigator · Dr. Arvind Hans — Founding Project Director · Mr. Rajan Pahan — Founding Community Coordination, Meetings & Logistics Lead.<br><br>
<b>Rights notice:</b> Copyright and other rights in individual Project Outputs remain with their lawful creator(s), owner(s) or licensee(s), as applicable. Project participation does not itself assign copyright or other intellectual-property rights. MLHKP does <b>not</b> claim private ownership of the underlying Munda community, identity, culture, sacred traditions, traditional knowledge or collective cultural heritage. Third-party sources, scans, photographs, recordings and publications retain their respective rights and licence conditions. Software/code is available under Apache-2.0 only where the repository or relevant component expressly states that licence. Cultural access, consent and publication restrictions take precedence over convenience of access.<br><br>
<span style="color:#8a6b59">Document · Preserve · Research · Publish · Educate · Empower</span>
</div>
""", unsafe_allow_html=True)
