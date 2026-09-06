import sys, json, re, csv, io
from pathlib import Path
import streamlit as st
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE/'software'))
try:
 from db import rows
except Exception:
 def rows(q): return []
try:
 from auth import is_owner, OWNER_EMAIL
except Exception:
 OWNER_EMAIL=''; is_owner=lambda *args:False
MAN=BASE/'data/source_bundles/encyclopaedia_mundarica/manifest.json'; ATT=BASE/'data/source_bundles/encyclopaedia_mundarica/human_verification_attestation.json'; MASTER=BASE/'data/source_register/master_sources.json'; MMSC=BASE/'data/source_census/mmsc_index.json'; DISC=BASE/'data/source_census/mmsc_discoveries.json'
st.set_page_config(page_title='MLHKP | Munda Living Heritage & Knowledge Project',page_icon='🌿',layout='wide',initial_sidebar_state='expanded')
def load(p,d):
 try:return json.loads(p.read_text(encoding='utf-8')) if p.exists() else d
 except Exception:return d
m=load(MAN,{'volume_slots':[]}); a=m.get('audit_summary',{}); vols=m.get('volume_slots',[]); att=load(ATT,{}); masters=load(MASTER,{}).get('sources',[]); mi=load(MMSC,{}); discoveries=load(DISC,{}).get('records',[])
def db(q):
 try:return rows(q)
 except Exception:return []
def cnt(t):
 x=db(f'SELECT COUNT(*) n FROM {t}'); return x[0]['n'] if x else 0
st.markdown('''<style>.block-container{max-width:1450px;padding-top:1.2rem}.hero{padding:26px;border:1px solid #d9e1d8;border-radius:20px;background:#f7faf5}.hero h1{font-family:Georgia,serif}.small{font-size:.86rem;color:#58645d}[data-testid="stSidebar"]{background:#f1f6ef}.group{font-weight:800;color:#153f2d;margin-top:.6rem}</style>''',unsafe_allow_html=True)
GROUPS={
'Discover':['Home Research Dashboard','Universal Search','Culture Explorer','Life from Birth to Burial'],
'Culture & Knowledge':['Language & Lexicon','Kinship & Kili','Festivals & Rituals','Beliefs & Sacred Life','Stories & Oral Traditions','Songs / Dance / Music','Food & Agriculture','Ecology & Ethnobotany','Material Culture & Crafts','Dress & Ornament','Houses & Architecture','Livelihood & Economy','Customary Law & Governance','Education / Health / Demography'],
'People & Place':['Places & Landscapes','Geographic / Community Variation'],
'History & Change':['Historical Timeline','Historical Archives','Contemporary Change'],
'Research Library':['Master Munda Source Census','Mundarica I–XVI Digital Library','Books / Journals / Theses','Government & Archives','Media Archive'],
'Evidence & Research':['Evidence Explorer','Contradictions & Variants','Community Validation','Research Gaps / Completeness','Reports & Downloads'],
'MLHKP':['About','Governance & Ethics','Contribute / Correct']}
if 'page' not in st.session_state:st.session_state.page='Home Research Dashboard'
with st.sidebar:
 st.markdown('## 🌿 MLHKP'); st.caption('Munda Cultural Dataset · Evidence-preserving research infrastructure')
 for g,ps in GROUPS.items():
  with st.expander(g,expanded=g=='Discover'):
   for p in ps:
    if st.button(p,key='nav_'+p,use_container_width=True):st.session_state.page=p
 st.divider(); st.caption('Research Pro · Institutional · API · Report Studio · Book Studio — future, disabled by default')
page=st.session_state.page

def metrics():
 c=st.columns(6); c[0].metric('Domains',cnt('cultural_domains')); c[1].metric('Subdomains',cnt('cultural_subdomains')); c[2].metric('Indicators',cnt('cultural_indicators')); c[3].metric('Master sources',len(masters)); c[4].metric('Evidence',cnt('evidence')); c[5].metric('Mundarica located/working',sum(1 for v in vols if v.get('external_source') or v.get('volume')==1))
def empty(req): st.info('Structure ready — evidence not yet ingested. Missing-data requirements: '+req)
def evidence_rows(): return db("SELECT c.claim_id,c.claim_label,c.claim_paraphrase,c.domain_id,c.local_term,c.geographic_scope,c.claim_status,c.field_verification_status,e.evidence_id,e.evidence_type,e.verification_state,e.access_level,s.source_id,s.title,s.url FROM source_claims c JOIN evidence e ON e.claim_id=c.claim_id JOIN sources s ON s.source_id=c.source_id WHERE lower(COALESCE(e.access_level,'public')) IN ('public','open') ORDER BY c.claim_id")
def source_rows():
 out=[]
 for s in masters: out.append({'type':'source','id':s.get('source_id'),'title':s.get('title'),'author':s.get('author') or s.get('creator'),'year':s.get('year') or s.get('publication_year'),'domain':'','geography':s.get('geography'),'language':s.get('language'),'period':'','verification':s.get('verification_state'),'access':s.get('access_class'),'source':s})
 for v in vols:
  e=v.get('external_source',{}); out.append({'type':'Mundarica','id':v.get('source_id'),'title':e.get('title_as_catalogued') or f'Encyclopaedia Mundarica Volume {v.get("volume")}','author':e.get('creator_as_catalogued'),'year':e.get('publication_year_as_catalogued'),'domain':'Mundarica','geography':'','language':'English / Mundari','period':'historical','verification':'VERIFIED COMPLETE' if v.get('verified_complete') else 'not complete','access':e.get('rights_status') or 'not assessed','source':v})
 return out

def universal_search():
 st.header('Universal Search'); st.caption('Search permitted MLHKP sources and public evidence. Restricted records are excluded from public results.')
 q=st.text_input('Search Munda knowledge',placeholder='term, Kili, place, festival, person, source, author…')
 c=st.columns(4); typ=c[0].selectbox('Content',['All','source','Mundarica','evidence']); ver=c[1].text_input('Verification filter'); yr=c[2].text_input('Year'); lang=c[3].text_input('Language')
 data=source_rows();
 for x in evidence_rows(): data.append({'type':'evidence','id':x.get('evidence_id'),'title':x.get('claim_label'),'author':'','year':'','domain':x.get('domain_id'),'geography':x.get('geographic_scope'),'language':'','period':'','verification':x.get('verification_state'),'access':x.get('access_level'),'source':x})
 def hit(x):
  blob=' '.join(str(x.get(k,'')) for k in ['id','title','author','year','domain','geography','language','period','verification']).lower()
  return (not q or q.lower() in blob) and (typ=='All' or x['type']==typ) and (not ver or ver.lower() in str(x.get('verification','')).lower()) and (not yr or yr in str(x.get('year',''))) and (not lang or lang.lower() in str(x.get('language','')).lower())
 res=[x for x in data if hit(x)]; st.write(f'**{len(res)} permitted result(s)**')
 for x in res[:200]:
  with st.expander(f"{x['type']} · {x.get('title') or x.get('id')}"):
   st.write('**Permanent ID:**',x.get('id')); st.write('**Domain:**',x.get('domain') or '—'); st.write('**Verification:**',x.get('verification') or '—'); st.write('**Access:**',x.get('access') or '—'); st.write('**Geography:**',x.get('geography') or '—')
   s=x['source'];
   if x['type']=='evidence': st.write(s.get('claim_paraphrase') or ''); st.write('Source:',s.get('source_id'),s.get('title')); st.write('Evidence ID:',s.get('evidence_id'))
   elif x['type']=='Mundarica' and s.get('external_source',{}).get('canonical_url'): st.link_button('Open repository record',s['external_source']['canonical_url'])

def mundarica():
 st.header('Mundarica I–XVI Digital Library'); st.caption('All sixteen permanent slots remain visible. Scan, OCR, transcription, human review and machine completeness are separate layers.')
 c=st.columns(5); c[0].metric('Volumes',16); c[1].metric('Located external',a.get('externally_located_volumes',0)); c[2].metric('Page-accounted',a.get('page_accounting_complete_volumes',0)); c[3].metric('Human review','I–XVI' if att.get('attestation',{}).get('status')=='human_review_attested' else '—'); c[4].metric('VERIFIED COMPLETE',a.get('verified_complete_volumes',0))
 st.warning('OCR is never treated as verified transcription. Human attestation does not automatically set VERIFIED COMPLETE.')
 summary=[]
 for v in vols:
  e=v.get('external_source',{}); n=v.get('volume'); summary.append({'Vol':n,'ID':v.get('source_id'),'State':'Working corpus' if n==1 else ('Located' if e else 'Pending locator'),'Pages':e.get('total_pages_as_catalogued') or (a.get('volume_1_declared_scan_pages') if n==1 else None),'OCR':'Repository OCR · unverified' if e else ('Working transcription' if n==1 else '—'),'Rights':e.get('rights_status','not assessed'),'Complete':'YES' if v.get('verified_complete') else 'NO'})
 st.dataframe(summary,use_container_width=True,hide_index=True)
 q=st.text_input('Search this library metadata'); choices=[v for v in vols if not q or q.lower() in json.dumps(v).lower()]; opts=[f"Volume {v['volume']} · {v['source_id']}" for v in choices]
 if not opts:return
 sel=st.selectbox('Open volume',opts); v=choices[opts.index(sel)]; e=v.get('external_source',{}); n=v['volume']; tabs=st.tabs(['Read','Entries','Stories','Songs','Terms','Places','Cultural Topics','Source & Provenance','Verification'])
 with tabs[0]:
  if n==1: st.success('324/324 structural page blocks accounted; working transcription registered.'); st.info('Working transcription remains non-scan-verified until authoritative-artifact reconciliation.')
  elif e: st.info('Repository locator and catalogue metadata registered; OCR is unverified.'); st.link_button('Open source record',e['canonical_url'])
  else: empty('exact source locator; permitted artifact; page accounting; OCR/transcription; provenance.')
 for t,label in zip(tabs[1:7],['entries','stories','songs','terms','places','cultural topics']):
  with t: empty(f'provenance-linked {label} records for this volume.')
 with tabs[7]: st.dataframe([{'Field':k,'Value':str(val)} for k,val in ({'Permanent ID':v.get('source_id'),'Status':v.get('status'),**e}).items() if val not in (None,'')],use_container_width=True,hide_index=True)
 with tabs[8]:
  st.write('**Human review:**',att.get('attestation',{}).get('status','not recorded'),'· Lead:',att.get('attestation',{}).get('named_lead_reviewer','—')); st.caption(att.get('provenance',{}).get('uncertainty',''))
  gates=[('Permanent ID',bool(v.get('source_id'))),('Source/artifact located',bool(e) or n==1),('Page accounting',n==1 and bool(a.get('volume_1_page_order_complete'))),('Authoritative artifact reconciled',n==1 and bool(a.get('volume_1_scan_registered'))),('Verified transcription',bool(v.get('verified_transcription_complete'))),('Structured audit',bool(v.get('structured_content_complete'))),('Completeness audit',bool(v.get('verified_complete')))]
  st.dataframe([{'Gate':x,'State':'PASS' if y else 'PENDING'} for x,y in gates],hide_index=True,use_container_width=True)

def generic(title,req):
 st.header(title); metrics(); ev=evidence_rows(); hits=[x for x in ev if title.lower().split()[0] in (' '.join(str(v) for v in x.values())).lower()]
 if hits: st.dataframe(hits,use_container_width=True,hide_index=True)
 else: empty(req)

if page=='Home Research Dashboard':
 st.markdown('<div class="hero"><h1>Johar. Explore a living cultural world.</h1><p>MLHKP connects cultural knowledge to sources, evidence, verification, provenance and access controls without turning historical reports into universal or current facts.</p></div>',unsafe_allow_html=True); metrics(); st.subheader('Research status'); st.dataframe([{'Stream':'Mundarica I–XVI','State':f"{sum(1 for v in vols if v.get('external_source') or v.get('volume')==1)}/16 located or working; {a.get('verified_complete_volumes',0)}/16 machine complete"},{'Stream':'Master Munda Source Census','State':f"{len(masters)} canonical source records; {len(discoveries)} discovery records currently loaded"},{'Stream':'Evidence graph','State':f"{cnt('evidence')} evidence records"},{'Stream':'Information architecture','State':'Complete module homes visible progressively; evidence population ongoing'}],hide_index=True,use_container_width=True)
elif page=='Universal Search': universal_search()
elif page=='Mundarica I–XVI Digital Library': mundarica()
elif page=='Master Munda Source Census':
 st.header(page); mm=mi.get('metrics',{}); st.caption('Only repository-calculated census records are displayed; no completeness claim is inferred.'); st.dataframe(masters,use_container_width=True,hide_index=True) if masters else empty('canonical source records and systematic search-log entries.')
elif page=='Evidence Explorer':
 st.header(page); ev=evidence_rows(); st.dataframe(ev,use_container_width=True,hide_index=True) if ev else empty('public provenance-linked claims and evidence.')
elif page=='Reports & Downloads':
 st.header(page); st.write('Generate reader-safe research exports from currently permitted records.'); ev=evidence_rows(); src=source_rows(); choice=st.selectbox('Report',['Public evidence register','Mundarica status','Source register']); data=ev if choice=='Public evidence register' else ([{'volume':v.get('volume'),'source_id':v.get('source_id'),'status':v.get('status'),'verified_complete':v.get('verified_complete')} for v in vols] if choice=='Mundarica status' else [{k:x.get(k) for k in ['type','id','title','author','year','verification','access']} for x in src]); buf=io.StringIO();
 if data:
  w=csv.DictWriter(buf,fieldnames=list(data[0].keys())); w.writeheader(); w.writerows(data)
 st.download_button('Download CSV report',buf.getvalue(),file_name=re.sub(r'\W+','_',choice.lower())+'.csv',mime='text/csv',disabled=not bool(data)); st.caption('Exports contain only the selected permitted public/repository-status layer; cultural access restrictions override entitlement.')
elif page=='Governance & Ethics':
 st.header(page); st.success('Cultural access and consent override public, institutional or commercial entitlement.'); st.write('Historical/source-reported statements are not automatically universal or current facts. Third-party works retain their own rights.'); st.write('**Mr. Rajan Pahan — Founding Community, Meetings & Field Logistics Coordinator**')
elif page=='About': st.header('About MLHKP'); st.write('Munda Living Heritage & Knowledge Project · Munda Cultural Dataset evidence infrastructure.'); st.write('Founding leadership: Dr. Mohammad Amir Khusru Akhtar — Founder · Founding Chairperson · Founding Principal Investigator; Dr. Arvind Hans — Founding Project Director; Mr. Rajan Pahan — Founding Community, Meetings & Field Logistics Coordinator.')
elif page=='Contribute / Correct': st.header(page); st.info('Correction and contribution workflow requires provenance, contributor identity/role, consent/access classification and review before public incorporation.')
else:
 reqs={'Life from Birth to Burial':'life-stage records from pregnancy/birth through remembrance, with sources, place, period and verification.','Language & Lexicon':'dialect, script, phonology, morphology, grammar, syntax, lexicon, etymology, variants and examples.','Kinship & Kili':'people, families, kinship, Kili and community-institution records.','Festivals & Rituals':'calendar, season, ritual steps, participants/exclusions, objects, formulae/prayers and provenance.','Beliefs & Sacred Life':'belief/cosmology/deity/spirit/sacred-institution records with cultural restrictions.','Stories & Oral Traditions':'oral histories, stories, myths, legends, folk tales, proverbs and riddles.','Songs / Dance / Music':'Durang, songs, dance, instruments, rhythm and performance-context evidence.','Food & Agriculture':'food, drink, recipes, agriculture and crop records.','Ecology & Ethnobotany':'forest, plant, medicinal knowledge, animal, ecology, weather and seasonality records with safety/access controls.','Material Culture & Crafts':'objects, tools, crafts and material-culture evidence.','Dress & Ornament':'dress and ornament records with geographic/period variation.','Houses & Architecture':'house forms, architecture, materials and construction evidence.','Livelihood & Economy':'livelihood, markets, labour, migration and economic records.','Customary Law & Governance':'land, customary law, governance and political-institution evidence.','Education / Health / Demography':'education, health, demography and language-vitality evidence.','Places & Landscapes':'place, village, landscape and geographic records.','Geographic / Community Variation':'village, Kili, family, gender, generation, dialect and period variation.','Historical Timeline':'dated historical events, persons and movements.','Historical Archives':'archive records with exact locators and provenance.','Contemporary Change':'technology, media, urbanisation and contemporary-change evidence.','Books / Journals / Theses':'bibliographic records and acquisition/full-text/evidence-link states.','Government & Archives':'government, TRI, Census, LSI and archival source records.','Media Archive':'photograph, audio, video, scan, map, drawing and 3D-object records with rights/access.','Contradictions & Variants':'variant and contradiction links, contested interpretations and historical/current distinctions.','Community Validation':'consent, review, community-validation decisions and unresolved validation gaps.','Research Gaps / Completeness':'machine-readable coverage, missing sources, fieldwork gaps, restrictions and audit status.','Culture Explorer':'domain/subdomain records linked to evidence and sources.'}; generic(page,reqs.get(page,'provenance-linked records for this module.'))
st.divider(); st.caption('MLHKP · MCD evidence engine. Cultural access/consent overrides entitlement. No project IP claim is interpreted as ownership of Munda community identity, culture, sacred traditions or collective heritage.')