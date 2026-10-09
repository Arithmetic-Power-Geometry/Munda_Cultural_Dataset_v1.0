import json,csv,io,re
from pathlib import Path
import streamlit as st
BASE=Path(__file__).resolve().parents[1]
def load(rel,default):
 p=BASE/rel
 try:return json.loads(p.read_text(encoding='utf-8')) if p.exists() else default
 except Exception:return default
MAN=load('data/source_bundles/encyclopaedia_mundarica/manifest.json',{'volume_slots':[]})
ATT=load('data/source_bundles/encyclopaedia_mundarica/human_verification_attestation.json',{})
MASTER=load('data/source_register/master_sources.json',{}).get('sources',[])
DISC=load('data/source_census/mmsc_discoveries.json',{}).get('records',[])
WEB=load('data/source_census/web_discovery_seed_2026-09-06.json',{}).get('records',[])
VOLS=MAN.get('volume_slots',[]); AUD=MAN.get('audit_summary',{})
try:
 import sys;sys.path.insert(0,str(BASE/'software'));from db import rows
except Exception:
 rows=lambda q:[]
def evidence():
 try:return rows("SELECT c.claim_id,c.claim_label,c.claim_paraphrase,c.domain_id,c.local_term,c.geographic_scope,c.claim_status,c.field_verification_status,e.evidence_id,e.evidence_type,e.verification_state,e.access_level,s.source_id,s.title,s.url FROM source_claims c JOIN evidence e ON e.claim_id=c.claim_id JOIN sources s ON s.source_id=c.source_id WHERE lower(COALESCE(e.access_level,'public')) IN ('public','open') ORDER BY c.claim_id")
 except Exception:return []
def safe_access(x):return str(x or '').lower() not in {'restricted','sacred','private','closed','embargoed'}
def records():
 out=[]
 for s in MASTER:
  if safe_access(s.get('access_class')):out.append({'kind':'MLHKP source','id':s.get('source_id'),'title':s.get('title'),'author':s.get('author') or s.get('creator'),'year':s.get('year') or s.get('publication_year'),'topic':s.get('domain') or s.get('source_class'),'status':s.get('verification_state'),'url':s.get('url'),'summary':s.get('description') or s.get('notes'),'raw':s})
 for v in VOLS:
  e=v.get('external_source',{});out.append({'kind':'Mundarica','id':v.get('source_id'),'title':e.get('title_as_catalogued') or f'Encyclopaedia Mundarica Volume {v.get("volume")}','author':e.get('creator_as_catalogued'),'year':e.get('publication_year_as_catalogued'),'topic':'Mundarica','status':'VERIFIED COMPLETE' if v.get('verified_complete') else ('located / not machine-complete' if e else 'locator pending'),'url':e.get('canonical_url'),'summary':f"Volume {v.get('volume')} evidence/source record",'raw':v})
 for w in WEB:
  out.append({'kind':'External discovery','id':w.get('id'),'title':w.get('title'),'author':w.get('author'),'year':w.get('year'),'topic':w.get('source_class'),'status':w.get('verification_state'),'url':w.get('url'),'summary':w.get('notes'),'raw':w})
 for x in evidence():
  out.append({'kind':'Evidence','id':x.get('evidence_id'),'title':x.get('claim_label') or x.get('claim_id'),'author':'','year':'','topic':x.get('domain_id'),'status':x.get('verification_state'),'url':x.get('url'),'summary':x.get('claim_paraphrase'),'raw':x})
 return out
def blob(x):return ' '.join(str(v or '') for v in [x.get('id'),x.get('title'),x.get('author'),x.get('year'),x.get('topic'),x.get('summary'),x.get('status')]).lower()
def leadership():
 st.subheader('Founding leadership')
 c=st.columns(3)
 data=[('Dr. Mohammad Amir Khusru Akhtar','Founder · Founding Chairperson · Founding Principal Investigator','Scholarly lead for research agenda, methodology, data architecture, ontology, validation standards and scholarly interpretation.'),('Dr. Arvind Hans','Founding Project Director','Project management, field operations, external review, expert network, media and outreach under approved research and governance procedures.'),('Mr. Rajan Pahan','Founding Community, Meetings & Field Logistics Coordinator','Community consultations, culturally appropriate introductions, local communication, meetings, venues, travel, guides, participant mobilisation and follow-up. This role is not independent final scholarly approval authority.')]
 for col,(n,r,d) in zip(c,data):
  with col:st.markdown(f'### {n}\n**{r}**\n\n{d}')
def search_page(home=False):
 if home:st.markdown('## Ask or search documented Munda knowledge')
 else:st.header('Search & Ask MLHKP')
 q=st.text_input('Search',placeholder='Try: Kili, Mundari grammar, marriage, Sarhul, songs, Birsa, agriculture…',key='main_search')
 allr=records();kinds=sorted(set(x['kind'] for x in allr));c=st.columns(4);kind=c[0].multiselect('Sources',kinds,default=kinds);topic=c[1].text_input('Topic/domain');author=c[2].text_input('Author');year=c[3].text_input('Year')
 res=[x for x in allr if x['kind'] in kind and (not q or q.lower() in blob(x)) and (not topic or topic.lower() in str(x.get('topic','')).lower()) and (not author or author.lower() in str(x.get('author','')).lower()) and (not year or year in str(x.get('year','')))]
 if not q and home:
  st.caption('Searches MLHKP evidence, Mundarica records and verified external-source discovery metadata. External discovery results are source leads, not extracted cultural claims.');return
 st.write(f'**{len(res)} result(s)**')
 tabs=st.tabs(['Knowledge & evidence','Mundarica','External sources','Download this result'])
 groups=[['Evidence','MLHKP source'],['Mundarica'],['External discovery']]
 for tab,ks in zip(tabs[:3],groups):
  with tab:
   rr=[x for x in res if x['kind'] in ks]
   if not rr:st.info('No matching records in this layer yet.')
   for x in rr[:100]:
    with st.expander(f"{x['title'] or x['id']} · {x['kind']}"):
     if x.get('summary'):st.write(x['summary'])
     st.caption(' · '.join(str(z) for z in [x.get('author'),x.get('year'),x.get('topic'),x.get('status')] if z))
     if x.get('url'):st.link_button('Open source / citation',x['url'])
     st.code(x.get('id') or 'no-id',language=None)
 with tabs[3]:
  flat=[{k:x.get(k) for k in ['kind','id','title','author','year','topic','status','url','summary']} for x in res];buf=io.StringIO()
  if flat:
   w=csv.DictWriter(buf,fieldnames=list(flat[0]));w.writeheader();w.writerows(flat)
  st.download_button('Download search results (CSV)',buf.getvalue(),file_name='mlhkp_search_results.csv',mime='text/csv',disabled=not flat)
  st.download_button('Download search results (JSON)',json.dumps(flat,ensure_ascii=False,indent=2),file_name='mlhkp_search_results.json',mime='application/json',disabled=not flat)
def explore():
 st.header('Explore Munda Knowledge');st.caption('One explorer replaces repetitive empty pages. Choose a knowledge area; available evidence and sources appear together.')
 areas=['Language & Lexicon','Kinship & Kili','Life Cycle','Festivals & Rituals','Beliefs & Sacred Life','Stories & Oral Traditions','Songs · Dance · Music','Food & Agriculture','Ecology & Ethnobotany','Material Culture · Crafts · Dress','Houses & Architecture','Livelihood & Economy','Customary Law & Governance','Education · Health · Demography','Places & Landscapes','History & Change']
 area=st.selectbox('Knowledge area',areas);terms={'Language & Lexicon':['language','lexicon','grammar','mundari'],'Kinship & Kili':['kinship','kili'],'Life Cycle':['birth','marriage','death'],'Festivals & Rituals':['festival','ritual'],'Beliefs & Sacred Life':['belief','sacred','religion'],'Stories & Oral Traditions':['story','oral','tale','proverb'],'Songs · Dance · Music':['song','durang','dance','music'],'Food & Agriculture':['food','agriculture','crop'],'Ecology & Ethnobotany':['ecology','plant','forest'],'Material Culture · Crafts · Dress':['material','craft','dress'],'Houses & Architecture':['house','architecture'],'Livelihood & Economy':['livelihood','economy','market'],'Customary Law & Governance':['law','governance','land'],'Education · Health · Demography':['education','health','demography'],'Places & Landscapes':['place','village','landscape'],'History & Change':['history','historical','change']};rr=[x for x in records() if any(t in blob(x) for t in terms[area])];st.metric('Available linked records',len(rr));st.dataframe([{k:x.get(k) for k in ['kind','id','title','year','topic','status']} for x in rr],hide_index=True,use_container_width=True) if rr else st.info('Knowledge home is defined, but provenance-linked records for this area are not yet populated.')
def mundarica():
 st.header('Mundarica I–XVI');st.caption('Dedicated parallel ingestion workspace. Human review, OCR, transcription and machine completeness remain separate states.');c=st.columns(4);c[0].metric('Permanent slots',16);c[1].metric('Located / working',sum(1 for v in VOLS if v.get('external_source') or v.get('volume')==1));c[2].metric('Page-accounted',AUD.get('page_accounting_complete_volumes',0));c[3].metric('VERIFIED COMPLETE',AUD.get('verified_complete_volumes',0));q=st.text_input('Search Mundarica metadata');vv=[v for v in VOLS if not q or q.lower() in json.dumps(v).lower()];st.dataframe([{'Vol':v.get('volume'),'ID':v.get('source_id'),'State':'working corpus' if v.get('volume')==1 else ('located' if v.get('external_source') else 'locator pending'),'Pages':v.get('external_source',{}).get('total_pages_as_catalogued'),'Machine complete':bool(v.get('verified_complete')),'Source':v.get('external_source',{}).get('canonical_url')} for v in vv],hide_index=True,use_container_width=True);st.info('OCR is never treated as verified transcription. Human-review attestation does not automatically set machine VERIFIED COMPLETE.')
def sources():
 st.header('Sources & Research Library');tabs=st.tabs(['All source records','External discovery','Mundarica','Evidence'])
 sets=[records(),[x for x in records() if x['kind']=='External discovery'],[x for x in records() if x['kind']=='Mundarica'],[x for x in records() if x['kind']=='Evidence']]
 for t,rr in zip(tabs,sets):
  with t:st.dataframe([{k:x.get(k) for k in ['kind','id','title','author','year','topic','status','url']} for x in rr],hide_index=True,use_container_width=True)
def reports():
 st.header('Build Report & Download Data');st.write('Use Search & Ask MLHKP to select a topic and download the exact result set as CSV or JSON. This report workspace will progressively add evidence-grounded PDF/DOCX synthesis without duplicating data.');st.info('Report generation must use only permitted evidence and must retain source citations, verification state, historical/current scope and uncertainty.')
def governance():
 st.header('About · Governance · Ethics');st.success('Cultural access and consent override public, institutional or commercial entitlement.');leadership();st.subheader('Evidence rules');st.write('Source availability is not proof of reuse rights. OCR is not verified transcription. Historical reports are not automatically current or universal facts. External web discovery is kept separate from ingested evidence. Corrections, uncertainty, provenance and verification states remain auditable.')
def render():
 st.set_page_config(page_title='MLHKP Knowledge Engine',page_icon='🌿',layout='wide');st.markdown('<style>.block-container{max-width:1450px;padding-top:1.3rem}[data-testid="stSidebar"]{background:#f2f7f1}.hero{padding:28px;border:1px solid #dce6dc;border-radius:22px;background:#f8fbf7}</style>',unsafe_allow_html=True)
 pages=['Home','Search & Ask','Explore','Mundarica I–XVI','Sources & Research Library','Build Report & Download','About · Governance · Ethics']
 with st.sidebar:
  st.markdown('## 🌿 MLHKP');st.caption('Search · Explore · Verify · Cite · Report · Download');page=st.radio('Navigate',pages,label_visibility='collapsed');st.divider();st.caption('One evidence base. Multiple views. No duplicated cultural facts.')
 if page=='Home':
  st.markdown('<div class="hero"><h1>MLHKP Knowledge Engine</h1><h3>Ask anything about documented Munda knowledge.</h3><p>Search MLHKP evidence, Mundarica I–XVI and verified external-source discovery from one place, with source links and downloadable results.</p></div>',unsafe_allow_html=True);search_page(True);c=st.columns(3);c[0].metric('Mundarica slots',16);c[1].metric('External discovery leads',len(WEB));c[2].metric('Canonical sources',len(MASTER))
 elif page=='Search & Ask':search_page()
 elif page=='Explore':explore()
 elif page=='Mundarica I–XVI':mundarica()
 elif page=='Sources & Research Library':sources()
 elif page=='Build Report & Download':reports()
 else:governance()
 st.divider();st.caption('MLHKP · Munda Cultural Dataset · Evidence, provenance, consent and cultural access preserved.')