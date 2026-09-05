import sys, json, re, urllib.parse
from pathlib import Path
import streamlit as st

BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE/'software'))
from db import rows, execute
from auth import is_owner, OWNER_EMAIL
from reporting import send_report

st.set_page_config(page_title='MLHKP | Munda Living Heritage & Knowledge Project',page_icon='🌿',layout='wide',initial_sidebar_state='expanded')
LOGO=BASE/'assets'/'mlhkp_logo.png'
MASTER=BASE/'data'/'source_register'/'master_sources.json'
MUNDARICA=BASE/'data'/'source_bundles'/'encyclopaedia_mundarica'/'manifest.json'

st.markdown('''<style>
:root{--earth:#4b2115;--deep:#2b140e;--red:#9d2d20;--leaf:#356b3c;--cream:#fffaf0;--gold:#b8893b;--ink:#24160f;--line:#ead9c1}
.stApp{background:linear-gradient(180deg,#fffefb,#fff9ef);color:var(--ink)}
.block-container{max-width:1420px;padding-top:1.15rem;padding-bottom:3rem}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#2b140e,#4b2115 62%,#321810)}
[data-testid="stSidebar"] *{color:#fff9ef}.section{font-family:Georgia,serif;color:var(--earth);font-size:1.85rem;font-weight:800;margin:.35rem 0 .15rem}
.kicker{font-size:.78rem;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--red)}
.hero{border:1px solid var(--line);border-radius:24px;padding:30px 34px;background:radial-gradient(circle at 92% 12%,rgba(184,137,59,.2),transparent 28%),linear-gradient(135deg,#fffdf7,#f7ead5);box-shadow:0 12px 32px rgba(75,33,21,.08)}
.hero h1{font-family:Georgia,serif;color:#3d190f;font-size:2.8rem;line-height:1.04;margin:.25rem 0 .6rem}.hero p{font-size:1.08rem;color:#684a3b;max-width:900px}.mission{font-weight:800;letter-spacing:.08em;color:var(--leaf)}
.card{height:100%;border:1px solid var(--line);border-radius:17px;padding:18px;background:#fff;box-shadow:0 5px 16px rgba(75,33,21,.05)}.card h3{font-family:Georgia,serif;color:var(--earth);font-size:1.13rem;margin:.1rem 0 .5rem}
.badge{display:inline-block;padding:5px 10px;border-radius:999px;background:#eef5ec;color:#2f6533;font-weight:700;font-size:.78rem;border:1px solid #cfe0cc;margin:0 5px 5px 0}.notice{border-left:5px solid var(--red);background:#fff5e9;padding:14px 18px;border-radius:8px;margin:12px 0}.rights{border:1px solid var(--line);border-radius:15px;background:#fffdf8;padding:16px 18px}.footer{margin-top:2rem;border-top:1px solid var(--line);padding-top:1.2rem;color:#6c5548;font-size:.83rem;line-height:1.55}
div[data-testid="stMetric"]{background:#fff;border:1px solid var(--line);padding:13px;border-radius:15px;box-shadow:0 4px 12px rgba(75,33,21,.04)}.stButton>button,.stDownloadButton>button{border-radius:10px;border:1px solid #8e3a27}
@media(max-width:800px){.block-container{padding-left:1rem;padding-right:1rem;padding-top:.7rem}.hero{padding:20px 18px;border-radius:18px}.hero h1{font-size:2rem}.hero p{font-size:1rem}.section{font-size:1.5rem}.card{min-height:auto}.stHorizontalBlock{gap:.65rem}}
</style>''',unsafe_allow_html=True)

@st.cache_data
def master_sources():
    if not MASTER.exists(): return []
    try: return json.loads(MASTER.read_text(encoding='utf-8')).get('sources',[])
    except Exception: return []

@st.cache_data
def mundarica_manifest():
    if not MUNDARICA.exists(): return {'volume_slots':[]}
    try: return json.loads(MUNDARICA.read_text(encoding='utf-8'))
    except Exception: return {'volume_slots':[]}

def count(table):
    try: return rows(f'SELECT COUNT(*) n FROM {table}')[0]['n']
    except Exception: return 0

def section(title,caption=None):
    st.markdown(f'<div class="section">{title}</div>',unsafe_allow_html=True)
    if caption: st.caption(caption)

def domain_name(did):
    try:
        r=rows('SELECT domain_name FROM cultural_domains WHERE domain_id=?',(did,)); return r[0]['domain_name'] if r else did
    except Exception:return did

def public_evidence():
    try:return rows("SELECT c.claim_id,c.claim_label,c.claim_paraphrase,c.domain_id,c.local_term,c.geographic_scope,c.claim_status,c.field_verification_status,e.evidence_id,e.evidence_type,e.verification_state,e.access_level,s.source_id,s.title,s.url FROM source_claims c JOIN evidence e ON e.claim_id=c.claim_id JOIN sources s ON s.source_id=c.source_id WHERE lower(COALESCE(e.access_level,'public')) IN ('public','open') ORDER BY c.claim_id")
    except Exception:return []

def footer():
    st.markdown('''<div class="footer"><b>Munda Living Heritage & Knowledge Project (MLHKP)</b> · Munda Cultural Dataset (MCD) evidence engine<br>Original MLHKP/MCD software, schemas, documentation and original dataset compilation: © 2026 Mohammad Amir Khusru Akhtar and Arvind Hans; Apache License 2.0 where stated. Third-party works retain their own rights. Community-contributed material remains subject to consent, cultural-access and reuse conditions. Nothing in the project copyright statement claims ownership of the Munda people, Munda identity, culture, sacred traditions or collective heritage.</div>''',unsafe_allow_html=True)

if 'owner' not in st.session_state:st.session_state.owner=False
with st.sidebar:
    if LOGO.exists():st.image(str(LOGO),use_container_width=True)
    else:
        st.markdown('## 🌿 MLHKP');st.caption('Munda Living Heritage & Knowledge Project')
    st.markdown('**Document · Preserve · Research · Publish · Educate · Empower**');st.divider()
    pages=['Home','Culture Explorer','Master Sources','Mundarica 1–16','Evidence Explorer','Research Gaps','Governance & Ethics','Report / Contribute']
    page=st.radio('Explore',pages,key='main_navigation')
    st.divider()
    with st.expander('Owner research access'):
        if not st.session_state.owner:
            email=st.text_input('Owner email',key='login_email');pw=st.text_input('Owner password',type='password',key='login_pw')
            if st.button('Sign in',use_container_width=True):
                if is_owner(email,pw,st.secrets):st.session_state.owner=True;st.rerun()
                else:st.error('Invalid owner credentials')
        else:
            st.success('Owner research mode enabled')
            if st.button('Sign out',use_container_width=True):st.session_state.owner=False;st.rerun()
    if st.session_state.owner and st.button('Open Owner Research Console',use_container_width=True):st.session_state['owner_console']=True
    st.caption(f'Corrections & scholarly correspondence\n{OWNER_EMAIL}')

if st.session_state.get('owner_console') and st.session_state.owner:
    page='Owner Research Console'

if page=='Home':
    left,right=st.columns([1,3.2],gap='large')
    with left:
        if LOGO.exists():st.image(str(LOGO),use_container_width=True)
        else:st.markdown('# 🌿')
    with right:st.markdown('''<div class="hero"><div class="kicker">Munda Living Heritage & Knowledge Project</div><h1>Johar. Explore a living cultural world.</h1><p>A long-term scholarly and community-aware knowledge infrastructure connecting language, culture, history, oral traditions, material heritage, field evidence and publications — while retaining provenance, variation and cultural access at every step.</p><div class="mission">EVERY STATEMENT CAN SHOW ITS EVIDENCE · OUR HERITAGE · OUR KNOWLEDGE · OUR FUTURE</div></div>''',unsafe_allow_html=True)
    st.write('');m=st.columns(5);m[0].metric('Domains',count('cultural_domains'));m[1].metric('Subdomains',count('cultural_subdomains'));m[2].metric('Indicators',count('cultural_indicators'));m[3].metric('Master sources',len(master_sources()));m[4].metric('Evidence',count('evidence'))
    section('One system, many ways to explore')
    cards=[('🌾 Culture','Browse 24 domains, subdomains and research indicators from life course to language, ecology, sacred life and cultural change.'),('📚 Sources','Inspect the canonical source register with permanent source IDs, provenance, rights and verification metadata.'),('📖 Mundarica','Follow the 16-volume corpus plan, page accounting and transcription status without confusing OCR with verified text.'),('🔎 Evidence','Trace public claims back through evidence IDs to sources and their documented geographic scope.'),('🛡️ Safeguards','Keep open, community-only, research-restricted, embargoed, confidential and not-for-publication material distinct.'),('🧭 Gaps','See where indicators still require field evidence, community validation, source expansion or specialist review.')]
    for batch in (cards[:3],cards[3:]):
        cols=st.columns(3)
        for col,(h,t) in zip(cols,batch):
            with col:st.markdown(f'<div class="card"><h3>{h}</h3>{t}</div>',unsafe_allow_html=True)
    st.info('Scholarly rule: a source proves that an account was reported; it does not automatically establish a universal or present-day Munda practice.')

elif page=='Culture Explorer':
    section('Culture Explorer','Search the full MCD ontology while preserving permanent IDs and legitimate variation.')
    q=st.text_input('Search culture',placeholder='Marriage, Sarna, food, song, burial, language …')
    ds=rows('SELECT * FROM cultural_domains ORDER BY sort_order')
    shown=0
    for d in ds:
        sds=rows('SELECT * FROM cultural_subdomains WHERE domain_id=? ORDER BY sort_order',(d['domain_id'],))
        inds=rows('SELECT indicator_id,indicator_label,research_prompt,verification_status FROM cultural_indicators WHERE domain_id=? ORDER BY indicator_id',(d['domain_id'],))
        hay=json.dumps([d,sds,inds],ensure_ascii=False).lower()
        if q and q.lower() not in hay:continue
        shown+=1
        with st.expander(f"{d['domain_id']} · {d['domain_name']}  |  {len(sds)} subdomains · {len(inds)} indicators"):
            st.caption(d.get('parent_group',''))
            for sd in sds:st.markdown(f"**{sd['subdomain_id']} — {sd['subdomain_name']}**")
    if not shown:st.info('No matching domain found. Try a broader cultural term.')

elif page=='Master Sources':
    section('Master Source Register','Canonical source metadata — richer than the legacy compatibility CSV and preserving all original SRC IDs.')
    data=master_sources();q=st.text_input('Search title, creator, type, place or scope')
    if q:data=[x for x in data if q.lower() in json.dumps(x,ensure_ascii=False).lower()]
    a,b,c=st.columns(3);a.metric('Canonical sources',len(master_sources()));b.metric('Visible matches',len(data));c.metric('Legacy IDs preserved',14)
    for x in data:
        with st.expander(f"{x.get('source_id')} · {x.get('title','Untitled')}"):
            c1,c2=st.columns([2,1]);
            with c1:
                st.markdown(f"**Creator:** {x.get('creator') or '—'}  \n**Type:** {x.get('source_type') or '—'}  \n**Geographic scope:** {x.get('geographic_scope') or '—'}  \n**Scope:** {x.get('scope_note') or '—'}")
            with c2:
                st.markdown(f"**Year:** {x.get('year') or '—'}  \n**Access:** {x.get('access_class') or '—'}  \n**Verification:** {x.get('verification_status') or '—'}  \n**Reuse:** {x.get('reuse_status') or '—'}")
            st.caption(x.get('source_of_truth_policy') or '')
            for loc in x.get('locators',[]):
                if str(loc.get('value','')).startswith('http'):st.link_button(loc.get('label') or 'Open source',loc['value'])

elif page=='Mundarica 1–16':
    section('Encyclopaedia Mundarica · 16-Volume Corpus','Historical source corpus with scan authority, OCR provenance and explicit verification state.')
    st.markdown('<span class="badge">16 volume slots</span><span class="badge">scan = authority</span><span class="badge">OCR ≠ verified text</span><span class="badge">uncertain readings flagged</span>',unsafe_allow_html=True)
    man=mundarica_manifest();slots=man.get('volume_slots',[])
    labels=[f"Volume {int(x['volume']):02d} · {x['source_id']} · {x['status']}" for x in slots]
    selected=st.selectbox('Select volume',labels if labels else ['No manifest available']);v=int(re.search(r'Volume (\d+)',selected).group(1)) if slots else 0
    st.markdown(f'<div class="notice"><b>Corpus rule.</b> {man.get("source_of_truth_policy","Verified transcription takes precedence over OCR.")}</div>',unsafe_allow_html=True)
    corpus=BASE/'Mundarika1.md'
    if v==1 and corpus.exists():
        text=corpus.read_text(encoding='utf-8',errors='replace');pages=re.findall(r'^## (?:Scan|PDF) page\s+(\d+)',text,flags=re.M|re.I)
        a,b,c=st.columns(3);a.metric('Page blocks detected',len(pages));b.metric('First block',pages[0] if pages else '—');c.metric('Last block',pages[-1] if pages else '—')
        if pages:
            p=st.number_input('Open scan/PDF page block',min_value=min(map(int,pages)),max_value=max(map(int,pages)),value=6 if 6 in map(int,pages) else min(map(int,pages)),step=1)
            mm=re.search(rf'(?ms)^## (?:Scan|PDF) page\s+{int(p)}\s*$\n(.*?)(?=^## (?:Scan|PDF) page\s+\d+\s*$|\Z)',text,flags=re.I)
            if mm:st.text_area(f'Volume I · page {int(p)} · working transcription',mm.group(1).strip(),height=500,disabled=True)
        st.warning('Volume I is a working transcription. Presence of a page block does not by itself mean that page has been visually verified against the scan.')
    else:st.info('This volume slot is reserved but its structured corpus is not yet present in the current build.')
    st.caption('No volume is labelled VERIFIED COMPLETE until page accounting, scan comparison, unresolved-reading review and integrity checks pass.')

elif page=='Evidence Explorer':
    section('Evidence Explorer','Trace public claim → evidence → source. Restricted evidence is excluded from the public view.')
    data=public_evidence();q=st.text_input('Search claim, term, place, evidence ID or source')
    if q:data=[x for x in data if q.lower() in json.dumps(x,ensure_ascii=False).lower()]
    st.metric('Public evidence trails shown',len(data))
    for x in data:
        with st.expander(f"{x['claim_id']} · {x['claim_label']} · {x['evidence_id']}"):
            st.write(x['claim_paraphrase']);st.markdown(f"**Domain:** {domain_name(x['domain_id'])}  \n**Term(s):** {x.get('local_term') or '—'}  \n**Geographic scope:** {x.get('geographic_scope') or '—'}  \n**Claim state:** {x.get('claim_status') or '—'}  \n**Field verification:** {x.get('field_verification_status') or '—'}  \n**Evidence state:** {x.get('verification_state') or '—'}  \n**Source:** {x['source_id']} — {x['title']}")
            if x.get('url'):st.link_button('Open source',x['url'])

elif page=='Research Gaps':
    section('Research Gaps','A transparent gap map: absence of evidence is recorded rather than silently filled.')
    inds=rows('SELECT indicator_id,domain_id,subdomain_id,indicator_label,research_prompt,verification_status FROM cultural_indicators ORDER BY indicator_id')
    claims=rows('SELECT DISTINCT domain_id,subdomain_id FROM source_claims');covered={(x['domain_id'],x['subdomain_id']) for x in claims}
    gaps=[x for x in inds if (x['domain_id'],x['subdomain_id']) not in covered]
    a,b,c=st.columns(3);a.metric('Indicators',len(inds));b.metric('Indicators in uncovered subdomains',len(gaps));c.metric('Field observations',count('observations'))
    dom=st.selectbox('Filter domain',['All']+[f"{d['domain_id']} — {d['domain_name']}" for d in rows('SELECT * FROM cultural_domains ORDER BY sort_order')])
    view=gaps if dom=='All' else [x for x in gaps if x['domain_id']==dom.split(' — ')[0]]
    st.dataframe(view,use_container_width=True,hide_index=True)
    st.info('This is a structural gap indicator, not a claim that knowledge does not exist in communities or literature. Later stages will add systematic literature census, fieldwork and community validation.')

elif page=='Governance & Ethics':
    section('Governance, Ethics & Cultural Access','Research infrastructure must protect provenance, people, permissions and living heritage.')
    st.markdown('''<div class="rights"><b>Founding project record</b><br>Dr. Mohammad Amir Khusru Akhtar — Founder, Founding Chairperson & Founding Principal Investigator<br>Dr. Arvind Hans — Founding Project Director<br>Mr. Rajan Pahan — Founding Community Coordination, Meetings & Logistics Lead</div>''',unsafe_allow_html=True)
    st.markdown('### Core safeguards')
    st.markdown('- **Collection is not publication permission.** Consent, cultural sensitivity, source rights and access class remain separate decisions.\n- **Variation is evidence.** Village, kili, region, dialect, family, generation and knowledge-holder differences are preserved.\n- **Restricted knowledge stays restricted.** Sacred, ritual, clan-specific, medicinal, burial-related, confidential or embargoed material can be access-controlled.\n- **Historical ≠ current.** Historical reports remain distinguishable from field-documented and community-validated evidence.\n- **Permanent IDs are not recycled.** Corrections are versioned and auditable; destructive deletion is exceptional.\n- **Privacy by design.** Public interfaces must not expose confidential participant information or restricted media.')
    st.markdown('### Rights statement')
    st.info('Project copyright and software licensing apply only to eligible original project outputs. They do not constitute ownership of the Munda people, Munda identity, culture, sacred traditions, collective heritage, or third-party works. Community material remains governed by consent and applicable cultural-access conditions.')

elif page=='Report / Contribute':
    section('Report a Correction or Contribute Evidence','Public users cannot edit records directly. Submissions enter a review path.')
    target=st.text_input('Record ID, source ID or topic (optional)');name=st.text_input('Your name');email=st.text_input('Your email (optional)');report=st.text_area('Correction, concern, variation, source lead or additional evidence')
    st.caption('Do not submit confidential, sacred or personally sensitive material through this public form. Contact the project team first for restricted material.')
    if st.button('Submit for review'):
        if not report.strip():st.warning('Please enter the information you want reviewed.')
        else:
            try:execute('INSERT INTO reports(target_type,target_id,reporter_name,reporter_email,report_text) VALUES (?,?,?,?,?)',('record',target,name,email,report))
            except Exception:pass
            body=f'Reporter: {name}\nEmail: {email}\nRecord/topic: {target}\n\n{report}';sent,_=send_report(f'MLHKP review submission: {target or "general"}',body,st.secrets)
            st.success('Submission added to the review path.' if not sent else 'Submission added to the review path and emailed to the project contact.')
            if not sent:
                subject=urllib.parse.quote(f'MLHKP review submission: {target or "general"}');encoded=urllib.parse.quote(body);st.markdown(f'[Email this submission to {OWNER_EMAIL}](mailto:{OWNER_EMAIL}?subject={subject}&body={encoded})')

elif page=='Owner Research Console':
    section('Owner Research Console','Protected research administration. Permanent IDs remain immutable.')
    if not st.session_state.owner:st.error('Owner access required.')
    else:
        tabs=st.tabs(['Data editor','Review queue','Integrity snapshot'])
        with tabs[0]:
            editable={'cultural_domains':'domain_id','cultural_subdomains':'subdomain_id','cultural_indicators':'indicator_id','sources':'source_id','source_claims':'claim_id','evidence':'evidence_id','places':'place_id'}
            table=st.selectbox('Dataset',list(editable));pk=editable[table];recs=rows(f'SELECT * FROM {table} ORDER BY {pk} LIMIT 2000');ids=[r[pk] for r in recs];rid=st.selectbox('Record',ids) if ids else None
            if rid:
                rec=next(r for r in recs if r[pk]==rid);st.caption('Permanent ID is locked. Every saved change receives an audit-log record.');new={}
                for k,v in rec.items():
                    if k==pk:st.text_input(k,str(v or ''),disabled=True,key=f'locked_{table}_{rid}_{k}')
                    else:new[k]=st.text_area(k,str(v or ''),height=68,key=f'edit_{table}_{rid}_{k}')
                reason=st.text_input('Reason for change')
                if st.button('Save audited changes'):
                    changed={k:v for k,v in new.items() if str(rec.get(k) or '')!=v}
                    if not changed:st.info('No changes detected.')
                    elif not reason.strip():st.warning('A reason is required for an audited change.')
                    else:
                        execute(f"UPDATE {table} SET {', '.join(f'{k}=?' for k in changed)} WHERE {pk}=?",tuple(list(changed.values())+[rid]));execute('INSERT INTO audit_log(actor,entity_type,entity_id,operation,old_data,new_data,reason) VALUES (?,?,?,?,?,?,?)',(OWNER_EMAIL,table,rid,'update',json.dumps(rec,ensure_ascii=False),json.dumps(changed,ensure_ascii=False),reason));st.success('Saved with audit record.');st.rerun()
        with tabs[1]:
            try:st.dataframe(rows('SELECT * FROM reports ORDER BY created_at DESC LIMIT 250'),use_container_width=True,hide_index=True)
            except Exception:st.info('No review queue is available in this deployment.')
        with tabs[2]:
            m=st.columns(5);m[0].metric('Domains',count('cultural_domains'));m[1].metric('Indicators',count('cultural_indicators'));m[2].metric('Sources',count('sources'));m[3].metric('Claims',count('source_claims'));m[4].metric('Evidence',count('evidence'));st.caption('Use GitHub validation workflows for release-grade integrity checks; this panel is a live operational snapshot.')

footer()
