import sys, json, re, urllib.parse
from pathlib import Path
import streamlit as st

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE / "software"))
from db import rows, execute
from auth import is_owner, OWNER_EMAIL
from reporting import send_report
try:
    from assets.mlhkp_logo_data import LOGO_DATA_URI
except Exception:
    LOGO_DATA_URI = ""

st.set_page_config(
    page_title="MLHKP | Munda Living Heritage & Knowledge Project",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

LOGO = BASE / "assets" / "mlhkp_logo.png"
MASTER = BASE / "data" / "source_register" / "master_sources.json"
MUNDARICA = BASE / "data" / "source_bundles" / "encyclopaedia_mundarica" / "manifest.json"

st.markdown("""
<style>
:root{
 --forest:#153f2d;--forest2:#0e2d21;--sal:#2d6845;--leaf:#5f8c4a;
 --earth:#5b2a1a;--terracotta:#a4472d;--red:#8f2d24;--cream:#fbf6e9;
 --sand:#efe2c7;--gold:#bd8d3e;--ink:#1f231f;--muted:#66706a;--line:#dfd7c5;
}
.stApp{background:linear-gradient(180deg,#fbfcf8 0%,#f7f4e8 100%);color:var(--ink)}
.block-container{max-width:1380px;padding-top:1.4rem;padding-bottom:3rem}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#edf4ee 0%,#f7f4e8 72%,#eee4d1 100%);border-right:1px solid #d7dfd7}
[data-testid="stSidebar"] *{color:#18382b}
[data-testid="stSidebar"] hr{border-color:#ced9d1}
[data-testid="stSidebar"] .stRadio label{font-size:.94rem}
[data-testid="stSidebar"] div[role="radiogroup"]>label{padding:.15rem .35rem;border-radius:8px}
[data-testid="stSidebar"] div[role="radiogroup"]>label:hover{background:#dfeae1}
.kicker{font-size:.73rem;font-weight:900;letter-spacing:.16em;text-transform:uppercase;color:var(--sal)}
.hero{border:1px solid #d7e0d8;border-radius:22px;padding:28px 30px;background:radial-gradient(circle at 90% 12%,rgba(189,141,62,.16),transparent 30%),linear-gradient(135deg,#f4f8f3,#fffdf8);box-shadow:0 8px 24px rgba(21,63,45,.07)}
.hero h1{font-family:Georgia,serif;color:var(--forest2);font-size:2.55rem;line-height:1.08;margin:.28rem 0 .65rem}
.hero p{font-size:1.04rem;color:#4f6256;max-width:920px;line-height:1.68}
.mission{font-size:.82rem;font-weight:900;letter-spacing:.08em;color:var(--terracotta);margin-top:.85rem}
.section{font-family:Georgia,serif;color:var(--forest2);font-size:1.72rem;font-weight:800;margin:1.25rem 0 .2rem}
.subsection{font-weight:800;color:var(--earth);font-size:1.05rem;margin:.45rem 0}
.card{height:100%;border:1px solid var(--line);border-radius:15px;padding:17px 18px;background:#fff;box-shadow:0 4px 14px rgba(29,52,38,.04)}
.card h3{font-family:Georgia,serif;color:var(--forest);font-size:1.08rem;margin:.05rem 0 .48rem}
.card p{color:#58665d;line-height:1.5;margin:0;font-size:.93rem}
.leader{height:100%;border-top:4px solid var(--terracotta);border-radius:14px;padding:17px;background:#fff;border-left:1px solid var(--line);border-right:1px solid var(--line);border-bottom:1px solid var(--line)}
.leader h3{font-family:Georgia,serif;color:var(--earth);font-size:1.05rem;margin:0 0 .3rem}
.leader .role{font-weight:800;color:var(--forest);font-size:.88rem;margin-bottom:.55rem}
.leader p{font-size:.89rem;line-height:1.48;color:#586159}
.badge{display:inline-block;padding:5px 10px;border-radius:999px;background:#e9f2e8;color:#285f3c;font-weight:750;font-size:.76rem;border:1px solid #cbdccf;margin:0 5px 5px 0}
.notice{border-left:4px solid var(--terracotta);background:#fff8ec;padding:13px 16px;border-radius:8px;margin:12px 0}
.rights{border:1px solid #d9d1bd;border-radius:14px;background:#fffdf7;padding:16px 18px}
.footer{margin-top:2.3rem;border-top:1px solid var(--line);padding-top:1.15rem;color:#687068;font-size:.81rem;line-height:1.55}
.logo-shell{text-align:center;padding:8px 4px 12px}.logo-shell img{max-width:100%;height:auto;filter:drop-shadow(0 6px 14px rgba(64,38,22,.10))}
.sidebar-brand{text-align:center;font-family:Georgia,serif;font-weight:800;color:#173d2b;font-size:1.02rem;line-height:1.25}
.sidebar-tag{text-align:center;color:#6c5b4a;font-size:.74rem;letter-spacing:.05em;margin-top:.25rem}
div[data-testid="stMetric"]{background:#fff;border:1px solid var(--line);padding:12px;border-radius:14px;box-shadow:0 3px 10px rgba(21,63,45,.035)}
.stButton>button,.stDownloadButton>button{border-radius:9px;border:1px solid #65826f}
@media(max-width:800px){
 .block-container{padding-left:.85rem;padding-right:.85rem;padding-top:.7rem}
 .hero{padding:20px 18px;border-radius:17px}.hero h1{font-size:1.9rem}.hero p{font-size:.98rem}
 .section{font-size:1.42rem}.card,.leader{min-height:auto}.stHorizontalBlock{gap:.65rem}
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def master_sources():
    if not MASTER.exists():
        return []
    try:
        return json.loads(MASTER.read_text(encoding="utf-8")).get("sources", [])
    except Exception:
        return []

@st.cache_data
def mundarica_manifest():
    if not MUNDARICA.exists():
        return {"volume_slots": []}
    try:
        return json.loads(MUNDARICA.read_text(encoding="utf-8"))
    except Exception:
        return {"volume_slots": []}

def count(table):
    try:
        return rows(f"SELECT COUNT(*) n FROM {table}")[0]["n"]
    except Exception:
        return 0

def section(title, caption=None):
    st.markdown(f'<div class="section">{title}</div>', unsafe_allow_html=True)
    if caption:
        st.caption(caption)

def domain_name(did):
    try:
        r = rows("SELECT domain_name FROM cultural_domains WHERE domain_id=?", (did,))
        return r[0]["domain_name"] if r else did
    except Exception:
        return did

def public_evidence():
    try:
        return rows("""SELECT c.claim_id,c.claim_label,c.claim_paraphrase,c.domain_id,c.local_term,
        c.geographic_scope,c.claim_status,c.field_verification_status,e.evidence_id,e.evidence_type,
        e.verification_state,e.access_level,s.source_id,s.title,s.url
        FROM source_claims c JOIN evidence e ON e.claim_id=c.claim_id
        JOIN sources s ON s.source_id=c.source_id
        WHERE lower(COALESCE(e.access_level,'public')) IN ('public','open')
        ORDER BY c.claim_id""")
    except Exception:
        return []

def logo_markup(width="100%"):
    if LOGO.exists():
        return None
    if LOGO_DATA_URI:
        return f'<div class="logo-shell"><img src="{LOGO_DATA_URI}" style="width:{width};max-width:360px" alt="MLHKP logo"></div>'
    return None

def show_logo(width="100%"):
    if LOGO.exists():
        st.image(str(LOGO), use_container_width=True)
    else:
        html = logo_markup(width)
        if html:
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.markdown("## 🌿 MLHKP")

def founder_cards():
    cols = st.columns(3)
    cards = [
        (
            "Dr. Mohammad Amir Khusru Akhtar",
            "Founder · Founding Chairperson · Founding Principal Investigator",
            "Principal intellectual creator and scholarly lead. Leads the research agenda, methodology, dataset architecture, schema, ontology, codebooks, validation standards, research instruments, books, papers and scholarly resources; holds final authority over scholarly methodology, interpretation and final scholarly approval."
        ),
        (
            "Dr. Arvind Hans",
            "Founding Project Director",
            "Leads project management, field operations, external review, expert network, media and outreach. Manages implementation schedules, primary-data collection under approved research instruments, consent/source/field-metadata quality control, external experts, publishers, media operations and approved community programmes."
        ),
        (
            "Mr. Rajan Pahan",
            "Founding Community Coordination, Meetings & Logistics Lead",
            "Coordinates community consultations and field meetings; identifies and contacts elders, Pahans, customary leaders, practitioners, families, youth, women, performers, artisans, musicians and storytellers; facilitates culturally appropriate introductions, local communication, venues, travel, recording locations, guides, participant mobilisation and follow-up records."
        ),
    ]
    for col, (name, role, body) in zip(cols, cards):
        with col:
            st.markdown(
                f'<div class="leader"><h3>{name}</h3><div class="role">{role}</div><p>{body}</p></div>',
                unsafe_allow_html=True,
            )

def footer():
    st.markdown(
        """<div class="footer"><b>Munda Living Heritage & Knowledge Project (MLHKP)</b> · Munda Cultural Dataset (MCD) evidence engine<br>
        Founding record: Dr. Mohammad Amir Khusru Akhtar — Founder, Founding Chairperson & Founding Principal Investigator;
        Dr. Arvind Hans — Founding Project Director; Mr. Rajan Pahan — Founding Community Coordination, Meetings & Logistics Lead.<br>
        Original eligible MLHKP/MCD software, schemas, documentation and original dataset compilation are protected as applicable; Apache License 2.0 applies where expressly stated.
        Third-party works retain their own rights. Community-contributed and culturally restricted material remains subject to consent, access, reuse and publication conditions.
        No Project IP right is interpreted as ownership of the Munda community, identity, culture, sacred traditions or collective heritage.</div>""",
        unsafe_allow_html=True,
    )

if "owner" not in st.session_state:
    st.session_state.owner = False

with st.sidebar:
    show_logo()
    st.markdown('<div class="sidebar-brand">Munda Living Heritage & Knowledge Project</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-tag">DOCUMENT · PRESERVE · RESEARCH · PUBLISH · EDUCATE · EMPOWER</div>', unsafe_allow_html=True)
    st.divider()
    st.caption("START")
    pages = ["Home","Culture Explorer","Master Sources","Mundarica 1–16","Evidence Explorer","Research Gaps","Governance & Ethics","Report / Contribute"]
    page = st.radio("Explore", pages, key="main_navigation", label_visibility="collapsed")
    st.divider()
    st.caption("ADMINISTRATION")
    with st.expander("Owner research access"):
        if not st.session_state.owner:
            email = st.text_input("Owner email", key="login_email")
            pw = st.text_input("Owner password", type="password", key="login_pw")
            if st.button("Sign in", use_container_width=True):
                if is_owner(email, pw, st.secrets):
                    st.session_state.owner = True
                    st.rerun()
                else:
                    st.error("Invalid owner credentials")
        else:
            st.success("Owner research mode enabled")
            if st.button("Sign out", use_container_width=True):
                st.session_state.owner = False
                st.rerun()
    if st.session_state.owner and st.button("Open Owner Research Console", use_container_width=True):
        st.session_state["owner_console"] = True
    st.caption(f"Corrections & scholarly correspondence\n{OWNER_EMAIL}")

if st.session_state.get("owner_console") and st.session_state.owner:
    page = "Owner Research Console"

if page == "Home":
    left, right = st.columns([1.15, 3.4], gap="large")
    with left:
        show_logo()
    with right:
        st.markdown("""<div class="hero"><div class="kicker">Munda Living Heritage & Knowledge Project</div>
        <h1>Johar. Explore a living cultural world.</h1>
        <p>MLHKP is a long-term cultural, research, digital, publication, media and community initiative for the responsible documentation, preservation, research, teaching, publication, digitisation and dissemination of Munda language, culture, history, oral traditions, knowledge systems and living heritage.</p>
        <div class="mission">OUR HERITAGE · OUR KNOWLEDGE · OUR FUTURE</div></div>""", unsafe_allow_html=True)

    st.write("")
    m = st.columns(5)
    m[0].metric("Domains", count("cultural_domains"))
    m[1].metric("Subdomains", count("cultural_subdomains"))
    m[2].metric("Indicators", count("cultural_indicators"))
    m[3].metric("Master sources", len(master_sources()))
    m[4].metric("Evidence", count("evidence"))

    section("Explore the knowledge system")
    cards = [
        ("🌾 Culture Explorer","Browse domains, subdomains and research indicators from life course, language and ecology to sacred life, material culture and cultural change."),
        ("📚 Master Sources","Inspect the canonical source register with permanent source IDs, provenance, rights, scope and verification metadata."),
        ("📖 Mundarica 1–16","Follow the 16-volume corpus page by page while keeping scan authority, OCR, transcription and verification state distinct."),
        ("🔎 Evidence Explorer","Trace public claims through evidence IDs back to the source and documented geographic scope."),
        ("🧭 Research Gaps","See exactly which subdomains still need literature, field evidence, community validation or specialist review."),
        ("🛡️ Governance & Ethics","Understand consent, cultural access, privacy, authorship, rights, provenance and responsible release rules."),
    ]
    for batch in (cards[:3], cards[3:]):
        cols = st.columns(3)
        for col, (h, t) in zip(cols, batch):
            with col:
                st.markdown(f'<div class="card"><h3>{h}</h3><p>{t}</p></div>', unsafe_allow_html=True)

    section("Founders & leadership")
    st.caption("Permanent founding record and operational roles under the MLHKP Founders' Collaboration & Governance Agreement.")
    founder_cards()
    st.info("Scholarly rule: a source proves that an account was reported; it does not automatically establish a universal or present-day Munda practice.")

elif page == "Culture Explorer":
    section("Culture Explorer","Search the MCD ontology while preserving permanent IDs and legitimate cultural variation.")
    q = st.text_input("Search culture", placeholder="Marriage, Sarna, food, song, burial, language …")
    ds = rows("SELECT * FROM cultural_domains ORDER BY sort_order")
    shown = 0
    for d in ds:
        sds = rows("SELECT * FROM cultural_subdomains WHERE domain_id=? ORDER BY sort_order", (d["domain_id"],))
        inds = rows("SELECT indicator_id,indicator_label,research_prompt,verification_status FROM cultural_indicators WHERE domain_id=? ORDER BY indicator_id", (d["domain_id"],))
        if q and q.lower() not in json.dumps([d,sds,inds], ensure_ascii=False).lower():
            continue
        shown += 1
        with st.expander(f"{d['domain_id']} · {d['domain_name']}  |  {len(sds)} subdomains · {len(inds)} indicators"):
            st.caption(d.get("parent_group",""))
            for sd in sds:
                st.markdown(f"**{sd['subdomain_id']} — {sd['subdomain_name']}**")
    if not shown:
        st.info("No matching domain found. Try a broader cultural term.")

elif page == "Master Sources":
    section("Master Source Register","Canonical source metadata preserving all original source IDs and richer provenance, scope and rights metadata.")
    data = master_sources()
    q = st.text_input("Search title, creator, type, place or scope")
    if q:
        data = [x for x in data if q.lower() in json.dumps(x, ensure_ascii=False).lower()]
    a,b,c = st.columns(3)
    a.metric("Canonical sources", len(master_sources()))
    b.metric("Visible matches", len(data))
    c.metric("Legacy IDs preserved", 14)
    for x in data:
        with st.expander(f"{x.get('source_id')} · {x.get('title','Untitled')}"):
            c1,c2 = st.columns([2,1])
            with c1:
                st.markdown(f"**Creator:** {x.get('creator') or '—'}  \n**Type:** {x.get('source_type') or '—'}  \n**Geographic scope:** {x.get('geographic_scope') or '—'}  \n**Scope:** {x.get('scope_note') or '—'}")
            with c2:
                st.markdown(f"**Year:** {x.get('year') or '—'}  \n**Access:** {x.get('access_class') or '—'}  \n**Verification:** {x.get('verification_status') or '—'}  \n**Reuse:** {x.get('reuse_status') or '—'}")
            st.caption(x.get("source_of_truth_policy") or "")
            for loc in x.get("locators", []):
                if str(loc.get("value","")).startswith("http"):
                    st.link_button(loc.get("label") or "Open source", loc["value"])

elif page == "Mundarica 1–16":
    section("Encyclopaedia Mundarica · 16-Volume Corpus","Historical corpus with scan authority, OCR provenance and explicit verification state.")
    st.markdown('<span class="badge">16 volume slots</span><span class="badge">scan = authority</span><span class="badge">OCR ≠ verified text</span><span class="badge">uncertain readings flagged</span>', unsafe_allow_html=True)
    man = mundarica_manifest()
    slots = man.get("volume_slots", [])
    labels = [f"Volume {int(x['volume']):02d} · {x['source_id']} · {x['status']}" for x in slots]
    selected = st.selectbox("Select volume", labels if labels else ["No manifest available"])
    v = int(re.search(r"Volume (\d+)", selected).group(1)) if slots else 0
    st.markdown(f'<div class="notice"><b>Corpus rule.</b> {man.get("source_of_truth_policy","Verified transcription takes precedence over OCR.")}</div>', unsafe_allow_html=True)
    corpus = BASE / "Mundarika1.md"
    if v == 1 and corpus.exists():
        text = corpus.read_text(encoding="utf-8", errors="replace")
        pages = re.findall(r"^## (?:Scan|PDF) page\s+(\d+)", text, flags=re.M|re.I)
        a,b,c = st.columns(3)
        a.metric("Page blocks detected", len(pages))
        b.metric("First block", pages[0] if pages else "—")
        c.metric("Last block", pages[-1] if pages else "—")
        if pages:
            ints = list(map(int,pages))
            p = st.number_input("Open scan/PDF page block", min_value=min(ints), max_value=max(ints), value=6 if 6 in ints else min(ints), step=1)
            mm = re.search(rf"(?ms)^## (?:Scan|PDF) page\s+{int(p)}\s*$\n(.*?)(?=^## (?:Scan|PDF) page\s+\d+\s*$|\Z)", text, flags=re.I)
            if mm:
                st.text_area(f"Volume I · page {int(p)} · working transcription", mm.group(1).strip(), height=500, disabled=True)
        st.warning("Volume I is a working transcription. Presence of a page block does not by itself mean that page has been visually verified against the scan.")
    else:
        st.info("This volume slot is reserved but its structured corpus is not yet present in the current build.")
    st.caption("No volume is labelled VERIFIED COMPLETE until page accounting, scan comparison, unresolved-reading review and integrity checks pass.")

elif page == "Evidence Explorer":
    section("Evidence Explorer","Trace public claim → evidence → source. Restricted evidence is excluded from the public view.")
    data = public_evidence()
    q = st.text_input("Search claim, term, place, evidence ID or source")
    if q:
        data = [x for x in data if q.lower() in json.dumps(x, ensure_ascii=False).lower()]
    st.metric("Public evidence trails shown", len(data))
    for x in data:
        with st.expander(f"{x['claim_id']} · {x['claim_label']} · {x['evidence_id']}"):
            st.write(x["claim_paraphrase"])
            st.markdown(f"**Domain:** {domain_name(x['domain_id'])}  \n**Term(s):** {x.get('local_term') or '—'}  \n**Geographic scope:** {x.get('geographic_scope') or '—'}  \n**Claim state:** {x.get('claim_status') or '—'}  \n**Field verification:** {x.get('field_verification_status') or '—'}  \n**Evidence state:** {x.get('verification_state') or '—'}  \n**Source:** {x['source_id']} — {x['title']}")
            if x.get("url"):
                st.link_button("Open source", x["url"])

elif page == "Research Gaps":
    section("Research Gaps","A transparent gap map: absence of evidence is recorded rather than silently filled.")
    inds = rows("SELECT indicator_id,domain_id,subdomain_id,indicator_label,research_prompt,verification_status FROM cultural_indicators ORDER BY indicator_id")
    claims = rows("SELECT DISTINCT domain_id,subdomain_id FROM source_claims")
    covered = {(x["domain_id"],x["subdomain_id"]) for x in claims}
    gaps = [x for x in inds if (x["domain_id"],x["subdomain_id"]) not in covered]
    a,b,c = st.columns(3)
    a.metric("Indicators",len(inds))
    b.metric("Indicators in uncovered subdomains",len(gaps))
    c.metric("Field observations",count("observations"))
    dom = st.selectbox("Filter domain",["All"]+[f"{d['domain_id']} — {d['domain_name']}" for d in rows("SELECT * FROM cultural_domains ORDER BY sort_order")])
    view = gaps if dom == "All" else [x for x in gaps if x["domain_id"] == dom.split(" — ")[0]]
    st.dataframe(view,use_container_width=True,hide_index=True)
    st.info("This is a structural gap indicator, not a claim that knowledge does not exist in communities or literature.")

elif page == "Governance & Ethics":
    section("Governance, Ethics & Cultural Access","Research infrastructure must protect provenance, people, permissions and living heritage.")
    st.markdown('<div class="rights"><b>Permanent founding record</b><br>Dr. Mohammad Amir Khusru Akhtar — Founder, Founding Chairperson & Founding Principal Investigator<br>Dr. Arvind Hans — Founding Project Director<br>Mr. Rajan Pahan — Founding Community Coordination, Meetings & Logistics Lead</div>', unsafe_allow_html=True)
    section("Roles under the Founders’ Agreement")
    founder_cards()
    st.markdown("### Responsibility & authority")
    st.markdown(
        "- **Dr. Mohammad Amir Khusru Akhtar:** final authority on scholarly methodology, research design, dataset architecture, codebooks, source standards, scholarly interpretation, research publications, books principally authored by him and final scholarly approval.\n"
        "- **Dr. Arvind Hans:** operational authority within approved plans for field operations, reviewer coordination, external experts, media operations, implementation schedules and outreach.\n"
        "- **Mr. Rajan Pahan:** operational authority within approved plans for meetings, community liaison and logistics; community coordination and field logistics support do not by themselves determine scholarly interpretation or authorship."
    )
    st.markdown("### Core safeguards")
    st.markdown(
        "- **Collection is not publication permission.** Consent, cultural sensitivity, source rights and access class remain separate decisions.\n"
        "- **Variation is evidence.** Village, clan/kili, region, dialect, family, generation and knowledge-holder differences may be preserved rather than collapsed.\n"
        "- **Restricted knowledge stays restricted.** Sacred, ritual, clan-specific, medicinal, burial-related, confidential or embargoed material can be access-controlled.\n"
        "- **Historical ≠ current.** Historical reports remain distinguishable from field-documented and community-validated evidence.\n"
        "- **Privacy by design.** Public interfaces must not expose confidential participant information or restricted media."
    )
    st.markdown("### Rights statement")
    st.info("Project copyright and software licensing apply only to eligible original Project Outputs. They do not constitute ownership of the Munda people, Munda identity, culture, sacred traditions, collective heritage, or third-party works. Community material remains governed by consent and applicable cultural-access conditions.")

elif page == "Report / Contribute":
    section("Report a Correction or Contribute Evidence","Public users cannot edit records directly. Submissions enter a review path.")
    target = st.text_input("Record ID, source ID or topic (optional)")
    name = st.text_input("Your name")
    email = st.text_input("Your email (optional)")
    report = st.text_area("Correction, concern, variation, source lead or additional evidence")
    st.caption("Do not submit confidential, sacred or personally sensitive material through this public form. Contact the project team first for restricted material.")
    if st.button("Submit for review"):
        if not report.strip():
            st.warning("Please enter the information you want reviewed.")
        else:
            try:
                execute("INSERT INTO reports(target_type,target_id,reporter_name,reporter_email,report_text) VALUES (?,?,?,?,?)",("record",target,name,email,report))
            except Exception:
                pass
            body = f"Reporter: {name}\nEmail: {email}\nRecord/topic: {target}\n\n{report}"
            sent,_ = send_report(f"MLHKP review submission: {target or 'general'}", body, st.secrets)
            st.success("Submission added to the review path." if not sent else "Submission added to the review path and emailed to the project contact.")
            if not sent:
                subject = urllib.parse.quote(f"MLHKP review submission: {target or 'general'}")
                encoded = urllib.parse.quote(body)
                st.markdown(f"[Email this submission to {OWNER_EMAIL}](mailto:{OWNER_EMAIL}?subject={subject}&body={encoded})")

elif page == "Owner Research Console":
    section("Owner Research Console","Protected research administration. Permanent IDs remain immutable.")
    if not st.session_state.owner:
        st.error("Owner access required.")
    else:
        tabs = st.tabs(["Data editor","Review queue","Integrity snapshot"])
        with tabs[0]:
            editable = {"cultural_domains":"domain_id","cultural_subdomains":"subdomain_id","cultural_indicators":"indicator_id","sources":"source_id","source_claims":"claim_id","evidence":"evidence_id","places":"place_id"}
            table = st.selectbox("Dataset",list(editable))
            pk = editable[table]
            recs = rows(f"SELECT * FROM {table} ORDER BY {pk} LIMIT 2000")
            ids = [r[pk] for r in recs]
            rid = st.selectbox("Record",ids) if ids else None
            if rid:
                rec = next(r for r in recs if r[pk] == rid)
                st.caption("Permanent ID is locked. Every saved change receives an audit-log record.")
                new = {}
                for k,v in rec.items():
                    if k == pk:
                        st.text_input(k,str(v or ""),disabled=True,key=f"locked_{table}_{rid}_{k}")
                    else:
                        new[k] = st.text_area(k,str(v or ""),height=68,key=f"edit_{table}_{rid}_{k}")
                reason = st.text_input("Reason for change")
                if st.button("Save audited changes"):
                    changed = {k:v for k,v in new.items() if str(rec.get(k) or "") != v}
                    if not changed:
                        st.info("No changes detected.")
                    elif not reason.strip():
                        st.warning("A reason is required for an audited change.")
                    else:
                        execute(f"UPDATE {table} SET {', '.join(f'{k}=?' for k in changed)} WHERE {pk}=?", tuple(list(changed.values())+[rid]))
                        execute("INSERT INTO audit_log(actor,entity_type,entity_id,operation,old_data,new_data,reason) VALUES (?,?,?,?,?,?,?)",(OWNER_EMAIL,table,rid,"update",json.dumps(rec,ensure_ascii=False),json.dumps(changed,ensure_ascii=False),reason))
                        st.success("Saved with audit record.")
                        st.rerun()
        with tabs[1]:
            try:
                st.dataframe(rows("SELECT * FROM reports ORDER BY created_at DESC LIMIT 250"),use_container_width=True,hide_index=True)
            except Exception:
                st.info("No review queue is available in this deployment.")
        with tabs[2]:
            m = st.columns(5)
            m[0].metric("Domains",count("cultural_domains"))
            m[1].metric("Indicators",count("cultural_indicators"))
            m[2].metric("Sources",count("sources"))
            m[3].metric("Claims",count("source_claims"))
            m[4].metric("Evidence",count("evidence"))
            st.caption("Use GitHub validation workflows for release-grade integrity checks; this panel is a live operational snapshot.")

footer()
