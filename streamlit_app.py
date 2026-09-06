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
MMSC = BASE / "data" / "source_census" / "mmsc_index.json"
MMSC_DISCOVERIES = BASE / "data" / "source_census" / "mmsc_discoveries.json"
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
def mmsc_index():
    try: return json.loads(MMSC.read_text(encoding="utf-8")) if MMSC.exists() else {"metrics": {}, "source_registers": []}
    except Exception: return {"metrics": {}, "source_registers": []}
@st.cache_data
def mmsc_discoveries():
    try: return json.loads(MMSC_DISCOVERIES.read_text(encoding="utf-8")).get("records", []) if MMSC_DISCOVERIES.exists() else []
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
def public_evidence():
    try: return rows("""SELECT c.claim_id,c.claim_label,c.claim_paraphrase,c.domain_id,c.local_term,c.geographic_scope,c.claim_status,c.field_verification_status,e.evidence_id,e.evidence_type,e.verification_state,e.access_level,s.source_id,s.title,s.url FROM source_claims c JOIN evidence e ON e.claim_id=c.claim_id JOIN sources s ON s.source_id=c.source_id WHERE lower(COALESCE(e.access_level,'public')) IN ('public','open') ORDER BY c.claim_id""")
    except Exception: return []
def show_logo(width="100%"):
    if LOGO.exists(): st.image(str(LOGO),use_container_width=True)
    elif LOGO_DATA_URI: st.markdown(f'<div class="logo-shell"><img src="{LOGO_DATA_URI}" style="width:{width};max-width:360px" alt="MLHKP logo"></div>',unsafe_allow_html=True)
    else: st.markdown("## 🌿 MLHKP")
def founder_cards():
    cards=[("Dr. Mohammad Amir Khusru Akhtar","Founder · Founding Chairperson · Founding Principal Investigator","Principal intellectual creator and scholarly lead. Leads the research agenda, methodology, dataset architecture, schema, ontology, codebooks, validation standards, research instruments, books, papers and scholarly resources; holds final authority over scholarly methodology, interpretation and final scholarly approval."),("Dr. Arvind Hans","Founding Project Director","Leads project management, field operations, external review, expert network, media and outreach. Manages implementation schedules, primary-data collection under approved research instruments, consent/source/field-metadata quality control, external experts, publishers, media operations and approved community programmes."),("Mr. Rajan Pahan","Founding Community, Meetings & Field Logistics Coordinator","Coordinates community consultations and field meetings; identifies and contacts elders, Pahans, customary leaders, practitioners, families, youth, women, performers, artisans, musicians and storytellers; facilitates culturally appropriate introductions, local communication, meetings, venues, travel, recording locations, guides, participant mobilisation and follow-up records. This coordination and field-logistics role does not independently determine scholarly interpretation or final scholarly approval.")]
    for col,(name,role,body) in zip(st.columns(3),cards):
        with col: st.markdown(f'<div class="leader"><h3>{name}</h3><div class="role">{role}</div><p>{body}</p></div>',unsafe_allow_html=True)
def footer():
    st.markdown("""<div class="footer"><b>Munda Living Heritage & Knowledge Project (MLHKP)</b> · Munda Cultural Dataset (MCD) evidence engine<br>Original eligible MLHKP/MCD software, schemas, documentation and original dataset compilation are protected as applicable; Apache License 2.0 applies where expressly stated. Third-party works retain their own rights. Community-contributed and culturally restricted material remains subject to consent, access, reuse and publication conditions. No Project IP right is interpreted as ownership of the Munda community, identity, culture, sacred traditions or collective heritage.</div>""",unsafe_allow_html=True)
def badge(text):
    st.markdown(f"**{text}**")

def mundarica_workspace():
    manifest=mundarica_manifest(); vols=manifest.get("volume_slots",[]); audit=manifest.get("audit_summary",{})
    section("Encyclopaedia Mundarica · Digital Research & Verification Workspace")
    st.caption("Sixteen-volume evidence-preserving workspace. Registry, scan, raw OCR, working transcription, verified transcription and structured content remain separate layers.")
    a,b,c,d,e=st.columns(5)
    a.metric("Volumes",manifest.get("expected_volumes",16)); b.metric("Located",audit.get("externally_located_volumes",0)); c.metric("Page-accounted",audit.get("page_accounting_complete_volumes",0)); d.metric("Authoritative scans",audit.get("registered_authoritative_scans",0)); e.metric("VERIFIED COMPLETE",audit.get("verified_complete_volumes",0))
    st.warning("VERIFIED COMPLETE is granted only by the machine-readable completeness audit after all required evidence and human-review gates pass. OCR is never treated as verified transcription.")
    summary=[]
    for v in vols:
        ext=v.get("external_source",{}); status=v.get("status","pending")
        summary.append({"Vol.":v.get("volume"),"Source ID":v.get("source_id"),"Discovery":"Located" if ext else ("Working corpus" if v.get("volume")==1 else "Pending"),"Pages": ext.get("total_pages_as_catalogued") or (audit.get("volume_1_declared_scan_pages") if v.get("volume")==1 else None),"Scan":"Registered" if (v.get("volume")==1 and audit.get("volume_1_scan_registered")) else ("External only" if ext else "Not registered"),"Text layer":"Working transcription" if v.get("volume")==1 else ("Repository OCR available · unverified" if ext else "Not ingested"),"Verified complete":"YES" if v.get("verified_complete") else "NO"})
    st.dataframe(summary,use_container_width=True,hide_index=True)
    labels=[f'Volume {v.get("volume")} · {v.get("source_id")}' for v in vols]
    selected=st.selectbox("Open volume",labels) if labels else None
    if not selected: return
    v=vols[labels.index(selected)]; ext=v.get("external_source",{}); vn=v.get("volume")
    st.subheader(f"Volume {vn} · {v.get('source_id')}")
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Status", "Working corpus" if vn==1 else ("Locator verified" if ext else "Pending")); c2.metric("Pages", ext.get("total_pages_as_catalogued") or (audit.get("volume_1_declared_scan_pages") if vn==1 else "—")); c3.metric("Authoritative scan", "Registered" if (vn==1 and audit.get("volume_1_scan_registered")) else ("External locator" if ext else "Missing")); c4.metric("Verification", "VERIFIED COMPLETE" if v.get("verified_complete") else "Not complete")
    tabs=st.tabs(["Read / Status","Entries","Stories","Songs","Terms","Places","Cultural Topics","Source & Provenance","Verification"])
    with tabs[0]:
        if vn==1:
            st.success("324/324 structural page blocks are accounted for in the registered working-transcription artifact.")
            st.info("The working transcription is preserved as a separate layer. An authoritative scan is not yet registered, so this interface does not promote any page to verified transcription.")
        elif ext:
            st.info("An authoritative repository locator has been verified, but the scan/text has not been ingested into MLHKP. Repository OCR remains machine-generated and unverified.")
            if ext.get("canonical_url"): st.link_button("Open authoritative repository record",ext["canonical_url"])
        else: st.info("Structure ready — evidence not yet ingested. Required next data: verified source locator, permitted scan/acquisition metadata, page accounting, raw OCR, working transcription and provenance.")
    for tab,label in zip(tabs[1:7],["entries","stories","songs","terms","places","cultural topics"]):
        with tab: st.info(f"Structure ready — {label} evidence not yet ingested or exposed for this volume. Records will appear only when provenance-linked and access-permitted.")
    with tabs[7]:
        st.markdown(f"**Permanent source ID:** `{v.get('source_id')}`")
        st.markdown(f"**Corpus status:** {v.get('status','pending')}")
        if ext:
            st.markdown(f"**Repository:** {ext.get('repository','—')}  \n**Catalogue title:** {ext.get('title_as_catalogued','—')}  \n**Creator metadata:** {ext.get('creator_as_catalogued','—')}  \n**Year:** {ext.get('publication_year_as_catalogued','—')}  \n**Identifier:** `{ext.get('identifier','—')}`  \n**Rights state:** {ext.get('rights_status','not assessed')}  \n**Acquisition:** {ext.get('acquisition_status','—')}")
            st.caption(ext.get("verification_note",""))
        else: st.info("No external-source metadata is currently registered for this volume.")
    with tabs[8]:
        st.markdown("**Designated textual verifier:** Dr. Mohammad Amir Khusru Akhtar")
        st.caption("Reviewer designation does not itself verify text. Each sign-off must identify the authoritative page/scan locator and retain a machine-readable review record.")
        gates={"Permanent source ID":"PASS" if v.get("source_id") else "FAIL","Page accounting":"PASS" if vn==1 and audit.get("volume_1_page_order_complete") else "PENDING","Authoritative scan registered":"PASS" if vn==1 and audit.get("volume_1_scan_registered") else "PENDING","Verified transcription":"PASS" if v.get("verified_transcription_complete") else "PENDING","Structured-content audit":"PASS" if v.get("structured_content_complete") else "PENDING","Completeness audit":"PASS" if v.get("verified_complete") else "PENDING"}
        st.dataframe([{"Gate":k,"State":val} for k,val in gates.items()],use_container_width=True,hide_index=True)
        if st.session_state.owner:
            st.info("Owner research mode is enabled. Verification actions remain evidence-gated; no OCR or working transcription is auto-approved.")
        else: st.info("Sign in through Owner research access to use future write-enabled verification controls.")

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
    section("Master Source Census"); census=mmsc_index(); metrics=census.get("metrics",{}); discoveries=mmsc_discoveries(); srcs=master_sources(); st.caption("Federated, evidence-preserving discovery census. Counts reflect records actually registered under the documented protocol, not a claim that every possible Munda source has already been discovered.")
    cm=st.columns(5); cm[0].metric("Discovered",metrics.get("sources_discovered",len(srcs))); cm[1].metric("Canonical",metrics.get("canonical_master_records",len(srcs))); cm[2].metric("Additional",metrics.get("additional_federated_discoveries",0)); cm[3].metric("Still to acquire",metrics.get("still_to_acquire_additional_discoveries",0)); cm[4].metric("Verified Mundarica",metrics.get("mundarica_verified_complete_volumes",0)); st.info("Catalogue or online availability does not establish acquisition, OCR verification, reuse permission, cultural validation or VERIFIED COMPLETE status.")
    if discoveries: st.dataframe(discoveries,use_container_width=True,hide_index=True)
    st.dataframe(srcs,use_container_width=True,hide_index=True)
elif page=="Mundarica 1–16": mundarica_workspace()
elif page=="Evidence Explorer": section("Evidence Explorer"); st.dataframe(public_evidence(),use_container_width=True,hide_index=True)
elif page=="Research Gaps":
    section("Research Gaps"); gaps=[]
    for d in rows("SELECT * FROM cultural_domains ORDER BY sort_order"):
        for sd in rows("SELECT * FROM cultural_subdomains WHERE domain_id=?",(d["domain_id"],)):
            n=rows("SELECT COUNT(*) n FROM source_claims WHERE domain_id=? AND subdomain_id=?",(d["domain_id"],sd["subdomain_id"]))[0]["n"]; gaps.append({"domain":d["domain_name"],"subdomain":sd["subdomain_name"],"claims":n,"gap":"Needs evidence" if n==0 else "Evidence present"})
    st.dataframe(gaps,use_container_width=True,hide_index=True)
elif page=="Governance & Ethics": section("Governance & Ethics"); founder_cards(); st.markdown("**Core safeguards:** collection is not publication permission; provenance and version history are retained; legitimate variation is preserved; restricted knowledge is not automatically public; Project IP does not constitute ownership of Munda people, identity, culture, sacred traditions or collective heritage.")
elif page=="Report / Contribute":
    section("Report / Contribute"); kind=st.selectbox("Type",["Correction","Contribution","Source suggestion","Access / cultural sensitivity concern"]); msg=st.text_area("Details")
    if st.button("Submit report"): send_report(kind,msg); st.success("Report recorded.")
elif page=="Owner Research Console": section("Owner Research Console"); st.success("Authenticated owner research mode")
footer()
