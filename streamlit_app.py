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

st.set_page_config(page_title="MLHKP | Munda Living Heritage & Knowledge Project", page_icon="🌿", layout="wide", initial_sidebar_state="expanded")
LOGO = BASE / "assets" / "mlhkp_logo.png"
MASTER = BASE / "data" / "source_register" / "master_sources.json"
MUNDARICA = BASE / "data" / "source_bundles" / "encyclopaedia_mundarica" / "manifest.json"

st.markdown("""
<style>
:root{--forest:#153f2d;--forest2:#0e2d21;--sal:#2d6845;--earth:#5b2a1a;--terracotta:#a4472d;--cream:#fbf6e9;--line:#dfd7c5}
.stApp{background:linear-gradient(180deg,#fbfcf8 0%,#f7f4e8 100%)}
.block-container{max-width:1380px;padding-top:1.4rem;padding-bottom:3rem}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#edf4ee 0%,#f7f4e8 72%,#eee4d1 100%);border-right:1px solid #d7dfd7}
[data-testid="stSidebar"] *{color:#18382b}
.hero{border:1px solid #d7e0d8;border-radius:22px;padding:28px 30px;background:linear-gradient(135deg,#f4f8f3,#fffdf8)}
.hero h1,.section{font-family:Georgia,serif;color:var(--forest2)}
.hero h1{font-size:2.55rem}.section{font-size:1.72rem;font-weight:800;margin:1.25rem 0 .2rem}
.kicker{font-size:.73rem;font-weight:900;letter-spacing:.16em;text-transform:uppercase;color:var(--sal)}
.mission{font-size:.82rem;font-weight:900;color:var(--terracotta)}
.card,.leader{height:100%;border:1px solid var(--line);border-radius:15px;padding:17px 18px;background:#fff}
.leader{border-top:4px solid var(--terracotta)}.leader h3{font-family:Georgia,serif;color:var(--earth)}.leader .role{font-weight:800;color:var(--forest);font-size:.88rem}.leader p{font-size:.89rem;line-height:1.48;color:#586159}
.footer{margin-top:2.3rem;border-top:1px solid var(--line);padding-top:1.15rem;color:#687068;font-size:.81rem;line-height:1.55}
.logo-shell{text-align:center;padding:8px}.sidebar-brand{text-align:center;font-family:Georgia,serif;font-weight:800}.sidebar-tag{text-align:center;font-size:.74rem}
</style>""", unsafe_allow_html=True)

@st.cache_data
def master_sources():
    try: return json.loads(MASTER.read_text(encoding="utf-8")).get("sources", []) if MASTER.exists() else []
    except Exception: return []

@st.cache_data
def mundarica_manifest():
    try: return json.loads(MUNDARICA.read_text(encoding="utf-8")) if MUNDARICA.exists() else {"volume_slots": []}
    except Exception: return {"volume_slots": []}

def count(table):
    try: return rows(f"SELECT COUNT(*) n FROM {table}")[0]["n"]
    except Exception: return 0

def section(title, caption=None):
    st.markdown(f'<div class="section">{title}</div>', unsafe_allow_html=True)
    if caption: st.caption(caption)

def domain_name(did):
    try:
        r=rows("SELECT domain_name FROM cultural_domains WHERE domain_id=?",(did,)); return r[0]["domain_name"] if r else did
    except Exception: return did

def public_evidence():
    try: return rows("""SELECT c.claim_id,c.claim_label,c.claim_paraphrase,c.domain_id,c.local_term,c.geographic_scope,c.claim_status,c.field_verification_status,e.evidence_id,e.evidence_type,e.verification_state,e.access_level,s.source_id,s.title,s.url FROM source_claims c JOIN evidence e ON e.claim_id=c.claim_id JOIN sources s ON s.source_id=c.source_id WHERE lower(COALESCE(e.access_level,'public')) IN ('public','open') ORDER BY c.claim_id""")
    except Exception: return []

def show_logo(width="100%"):
    if LOGO.exists(): st.image(str(LOGO),use_container_width=True)
    elif LOGO_DATA_URI: st.markdown(f'<div class="logo-shell"><img src="{LOGO_DATA_URI}" style="width:{width};max-width:360px" alt="MLHKP logo"></div>',unsafe_allow_html=True)
    else: st.markdown("## 🌿 MLHKP")

def founder_cards():
    cards=[
      ("Dr. Mohammad Amir Khusru Akhtar","Founder · Founding Chairperson · Founding Principal Investigator","Principal intellectual creator and scholarly lead. Leads the research agenda, methodology, dataset architecture, schema, ontology, codebooks, validation standards, research instruments, books, papers and scholarly resources; holds final authority over scholarly methodology, interpretation and final scholarly approval."),
      ("Dr. Arvind Hans","Founding Project Director","Leads project management, field operations, external review, expert network, media and outreach. Manages implementation schedules, primary-data collection under approved research instruments, consent/source/field-metadata quality control, external experts, publishers, media operations and approved community programmes."),
      ("Mr. Rajan Pahan","Founding Community, Meetings & Field Logistics Coordinator","Coordinates community consultations and field meetings; identifies and contacts elders, Pahans, customary leaders, practitioners, families, youth, women, performers, artisans, musicians and storytellers; facilitates culturally appropriate introductions, local communication, meetings, venues, travel, recording locations, guides, participant mobilisation and follow-up records. This coordination and field-logistics role does not independently determine scholarly interpretation or final scholarly approval.")]
    for col,(name,role,body) in zip(st.columns(3),cards):
        with col: st.markdown(f'<div class="leader"><h3>{name}</h3><div class="role">{role}</div><p>{body}</p></div>',unsafe_allow_html=True)

def footer():
    st.markdown("""<div class="footer"><b>Munda Living Heritage & Knowledge Project (MLHKP)</b> · Munda Cultural Dataset (MCD) evidence engine<br>
    Original eligible MLHKP/MCD software, schemas, documentation and original dataset compilation are protected as applicable; Apache License 2.0 applies where expressly stated. Third-party works retain their own rights. Community-contributed and culturally restricted material remains subject to consent, access, reuse and publication conditions. No Project IP right is interpreted as ownership of the Munda community, identity, culture, sacred traditions or collective heritage.</div>""",unsafe_allow_html=True)

if "owner" not in st.session_state: st.session_state.owner=False
with st.sidebar:
    show_logo(); st.markdown('<div class="sidebar-brand">Munda Living Heritage & Knowledge Project</div>',unsafe_allow_html=True); st.markdown('<div class="sidebar-tag">DOCUMENT · PRESERVE · RESEARCH · PUBLISH · EDUCATE · EMPOWER</div>',unsafe_allow_html=True); st.divider()
    pages=["Home","Culture Explorer","Master Sources","Mundarica 1–16","Evidence Explorer","Research Gaps","Governance & Ethics","Report / Contribute"]
    page=st.radio("Explore",pages,key="main_navigation",label_visibility="collapsed"); st.divider()
    with st.expander("Owner research access"):
        if not st.session_state.owner:
            email=st.text_input("Owner email",key="login_email"); pw=st.text_input("Owner password",type="password",key="login_pw")
            if st.button("Sign in",use_container_width=True):
                if is_owner(email,pw,st.secrets): st.session_state.owner=True; st.rerun()
                else: st.error("Invalid owner credentials")
        else:
            st.success("Owner research mode enabled")
            if st.button("Sign out",use_container_width=True): st.session_state.owner=False; st.rerun()
    if st.session_state.owner and st.button("Open Owner Research Console",use_container_width=True): st.session_state["owner_console"]=True
    st.caption(f"Corrections & scholarly correspondence\n{OWNER_EMAIL}")
if st.session_state.get("owner_console") and st.session_state.owner: page="Owner Research Console"

if page=="Home":
    left,right=st.columns([1.15,3.4],gap="large")
    with left: show_logo()
    with right: st.markdown("""<div class="hero"><div class="kicker">Munda Living Heritage & Knowledge Project</div><h1>Johar. Explore a living cultural world.</h1><p>MLHKP is a long-term cultural, research, digital, publication, media and community initiative for the responsible documentation, preservation, research, teaching, publication, digitisation and dissemination of Munda language, culture, history, oral traditions, knowledge systems and living heritage.</p><div class="mission">OUR HERITAGE · OUR KNOWLEDGE · OUR FUTURE</div></div>""",unsafe_allow_html=True)
    m=st.columns(5); m[0].metric("Domains",count("cultural_domains")); m[1].metric("Subdomains",count("cultural_subdomains")); m[2].metric("Indicators",count("cultural_indicators")); m[3].metric("Master sources",len(master_sources())); m[4].metric("Evidence",count("evidence"))
    section("Founders & leadership"); st.caption("Permanent founding record and operational roles under the MLHKP Founders' Collaboration & Governance Agreement."); founder_cards(); st.info("Scholarly rule: a source proves that an account was reported; it does not automatically establish a universal or present-day Munda practice.")
elif page=="Culture Explorer":
    section("Culture Explorer"); q=st.text_input("Search culture",placeholder="Marriage, Sarna, food, song, burial, language …"); ds=rows("SELECT * FROM cultural_domains ORDER BY sort_order")
    for d in ds:
        sds=rows("SELECT * FROM cultural_subdomains WHERE domain_id=? ORDER BY subdomain_id",(d["domain_id"],)); inds=rows("SELECT * FROM cultural_indicators WHERE domain_id=? ORDER BY indicator_id",(d["domain_id"],)); hay=(d["domain_name"]+" "+" ".join(x["subdomain_name"] for x in sds)+" "+" ".join(x["indicator_label"] for x in inds)).lower()
        if q and q.lower() not in hay: continue
        with st.expander(f'{d["domain_id"]} · {d["domain_name"]} — {len(sds)} subdomains / {len(inds)} indicators'):
            for sd in sds: st.markdown(f'**{sd["subdomain_id"]} · {sd["subdomain_name"]}**')
elif page=="Master Sources":
    section("Master Source Register"); srcs=master_sources(); st.metric("Registered sources",len(srcs)); st.dataframe(srcs,use_container_width=True,hide_index=True)
elif page=="Mundarica 1–16":
    section("Encyclopaedia Mundarica · Volumes I–XVI"); manifest=mundarica_manifest(); vols=manifest.get("volume_slots",[]); labels=[f'{v.get("volume_number")}. {v.get("source_id")} · {v.get("status")}' for v in vols]; selected=st.selectbox("Volume",labels) if labels else None
    if selected:
        v=vols[labels.index(selected)]; st.json(v); st.warning("Historical-source evidence is source-reported evidence. OCR or a working transcription is not a verified transcription until checked against the authoritative scan.")
elif page=="Evidence Explorer":
    section("Evidence Explorer"); ev=public_evidence(); st.dataframe(ev,use_container_width=True,hide_index=True)
elif page=="Research Gaps":
    section("Research Gaps"); gaps=[]
    for d in rows("SELECT * FROM cultural_domains ORDER BY sort_order"):
        for sd in rows("SELECT * FROM cultural_subdomains WHERE domain_id=?",(d["domain_id"],)):
            n=rows("SELECT COUNT(*) n FROM source_claims WHERE domain_id=? AND subdomain_id=?",(d["domain_id"],sd["subdomain_id"]))[0]["n"]; gaps.append({"domain":d["domain_name"],"subdomain":sd["subdomain_name"],"claims":n,"gap":"Needs evidence" if n==0 else "Evidence present"})
    st.dataframe(gaps,use_container_width=True,hide_index=True)
elif page=="Governance & Ethics":
    section("Governance & Ethics"); founder_cards(); st.markdown("**Core safeguards:** collection is not publication permission; provenance and version history are retained; legitimate variation is preserved; restricted knowledge is not automatically public; Project IP does not constitute ownership of Munda people, identity, culture, sacred traditions or collective heritage.")
elif page=="Report / Contribute":
    section("Report / Contribute"); kind=st.selectbox("Type",["Correction","Contribution","Source suggestion","Access / cultural sensitivity concern"]); msg=st.text_area("Details");
    if st.button("Submit report"):
        send_report(kind,msg); st.success("Report recorded.")
elif page=="Owner Research Console":
    section("Owner Research Console"); st.success("Authenticated owner research mode")
footer()
