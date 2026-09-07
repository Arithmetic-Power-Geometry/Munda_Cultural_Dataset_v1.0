import json,csv,io,re,sys
from pathlib import Path
import streamlit as st
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'software'))
def load(rel,default):
 p=BASE/rel
 try:return json.loads(p.read_text(encoding='utf-8')) if p.exists() else default
 except Exception:return default
MAN=load('data/source_bundles/encyclopaedia_mundarica/manifest.json',{'volume_slots':[]})
ATT=load('data/source_bundles/encyclopaedia_mundarica/human_verification_attestation.json',{})
MASTER=load('data/source_register/master_sources.json',{}).get('sources',[])
DISC=load('data/source_census/mmsc_discoveries.json',{}).get('records',[])
WEB=load('data/source_census/web_discovery_seed_2026-09-06.json',{}).get('records',[])
VOLS=MAN.get('volume_slots',[]);AUD=MAN.get('audit_summary',{})
try:
 from db import rows
except Exception:
 rows=lambda q:[]
def query(sql):
 try:return rows(sql)
 except Exception:return []
def evid():
 return query("SELECT c.claim_id,c.claim_label,c.claim_paraphrase,c.domain_id,c.local_term,c.geographic_scope,c.claim_status,c.field_verification_status,e.evidence_id,e.evidence_type,e.verification_state,e.access_level,s.source_id,s.title,s.url FROM source_claims c JOIN evidence e ON e.claim_id=c.claim_id JOIN sources s ON s.source_id=c.source_id WHERE lower(COALESCE(e.access_level,'public')) IN ('public','open') ORDER BY c.claim_id")
def safe(v):return str(v or '').lower() not in {'restricted','sacred','private','closed','embargoed'}
def catalogue():
 out=[]
 for s in MASTER:
  if safe(s.get('access_class')):out.append({'kind':'MLHKP source','id':s.get('source_id'),'title':s.get('title'),'author':s.get('author') or s.get('creator'),'year':s.get('year') or s.get('publication_year'),'topic':s.get('domain') or s.get('source_class'),'status':s.get('verification_state'),'url':s.get('url'),'text':s.get('description') or s.get('notes') or ''})
 for v in VOLS:
  e=v.get('external_source',{});out.append({'kind':'Mundarica','id':v.get('source_id'),'title':e.get('title_as_catalogued') or f'Encyclopaedia Mundarica Volume {v.get("volume")}','author':e.get('creator_as_catalogued'),'year':e.get('publication_year_as_catalogued'),'topic':'Mundarica','status':'VERIFIED COMPLETE' if v.get('verified_complete') else ('located / not machine-complete' if e else 'locator pending'),'url':e.get('canonical_url'),'text':f"Volume {v.get('volume')} source record"})
 for w in WEB:
  out.append({'kind':'External discovery','id':w.get('id'),'title':w.get('title'),'author':w.get('author'),'year':w.get('year'),'topic':w.get('source_class'),'status':w.get('verification_state'),'url':w.get('url'),'text':w.get('notes') or ''})
 for x in evid():
  out.append({'kind':'Evidence','id':x.get('evidence_id'),'title':x.get('claim_label') or x.get('claim_id'),'author':'','year':'','topic':x.get('domain_id'),'status':x.get('verification_state'),'url':x.get('url'),'text':x.get('claim_paraphrase') or '','source_id':x.get('source_id'),'source_title':x.get('title'),'geography':x.get('geographic_scope')})
 return out
def searchable(x):return ' '.join(str(x.get(k) or '') for k in ['id','title','author','year','topic','status','text','source_title','geography']).lower()
def live_metrics():
 allr=catalogue(); source_ids={x['id'] for x in allr if x['kind'] in {'MLHKP source','Mundarica','External discovery'} and x.get('id')}; verified={x['id'] for x in allr if x.get('id') and str(x.get('status') or '').lower() in {'verified','web_locator_verified','catalogue_verified','metadata_verified','verified complete'}}
 located={x['id'] for x in allr if x.get('id') and (x.get('url') or x['kind']=='MLHKP source')};ev=evid();eids={x.get('evidence_id') for x in ev if x.get('evidence_id')}; entities=query('SELECT COUNT(*) n FROM entities') or query('SELECT COUNT(*) n FROM cultural_entities');entity_n=(entities[0].get('n',0) if entities else 0)
 structured={x.get('source_id') for x in ev if x.get('source_id')}; permitted={x['id'] for x in allr if x.get('id') and x['kind']!='External discovery'}
 return {'Sources discovered':len(source_ids),'Source records verified':len(verified),'Full text / locator available':len(located),'Permitted/registered for processing':len(permitted),'Structured/evidence-linked sources':len(structured),'Evidence records':len(eids),'Entities':entity_n,'Unresolved Mundarica locators':sum(1 for v in VOLS if v.get('volume')!=1 and not v.get('external_source'))}
def metric_strip():
 m=live_metrics();st.caption('Live repository metrics — calculated from currently loaded records; never substituted with illustrative counts.')
 cols=st.columns(4)
 for i,(k,v) in enumerate(m.items()):cols[i%4].metric(k,v)
def result_download(rr,prefix='mlhkp_topic'):
 flat=[{k:x.get(k) for k in ['kind','id','title','author','year','topic','status','url','text','source_id','source_title','geography']} for x in rr]
 b=io.StringIO()
 if flat:
  w=csv.DictWriter(b,fieldnames=list(flat[0]));w.writeheader();w.writerows(flat)
 c=st.columns(2);c[0].download_button('Download CSV',b.getvalue(),file_name=prefix+'.csv',mime='text/csv',disabled=not flat);c[1].download_button('Download JSON',json.dumps(flat,ensure_ascii=False,indent=2),file_name=prefix+'.json',mime='application/json',disabled=not flat)
def answer_block(q,rr):
 ev=[x for x in rr if x['kind']=='Evidence' and x.get('text')]
 st.subheader('Evidence-grounded answer')
 if not ev:
  st.info('MLHKP does not currently contain sufficient public, provenance-linked evidence to synthesize this answer confidently. Relevant source-discovery results are shown below for research, but they are not treated as cultural facts.')
  return
 st.write('The following answer is assembled only from currently permitted MLHKP evidence. It is not a free-form model answer.')
 for i,x in enumerate(ev[:8],1):
  st.markdown(f"**[{i}] {x.get('title') or x.get('id')}** — {x.get('text')}")
  meta=' · '.join(str(z) for z in [x.get('source_title'),x.get('geography'),x.get('status')] if z);st.caption(meta)
  if x.get('url'):st.link_button(f'Open source [{i}]',x['url'],key=f'cite_{i}_{x.get("id")}')
def search(q_default='',key='search'):
 allr=catalogue();q=st.text_input('Ask or search documented Munda knowledge',value=q_default,placeholder='Example: What are the traditional Munda marriage practices?',key=key)
 c=st.columns(4);kind=c[0].multiselect('Layer',sorted(set(x['kind'] for x in allr)),default=sorted(set(x['kind'] for x in allr)));topic=c[1].text_input('Topic/domain',key=key+'_topic');author=c[2].text_input('Author',key=key+'_author');year=c[3].text_input('Year',key=key+'_year')
 tokens=[t for t in re.findall(r"[\w'-]+",q.lower()) if len(t)>2 and t not in {'what','are','the','how','why','about','traditional','documented'}]
 rr=[x for x in allr if x['kind'] in kind and (not q or all(t in searchable(x) for t in tokens) or q.lower() in searchable(x)) and (not topic or topic.lower() in str(x.get('topic','')).lower()) and (not author or author.lower() in str(x.get('author','')).lower()) and (not year or year in str(x.get('year','')))]
 if not q:return rr
 answer_block(q,rr);st.write(f'**{len(rr)} matching record(s)**')
 tabs=st.tabs(['Knowledge & evidence','Mundarica','External sources','Data behind this answer'])
 groups=[{'Evidence','MLHKP source'},{'Mundarica'},{'External discovery'}]
 for tab,ks in zip(tabs[:3],groups):
  with tab:
   z=[x for x in rr if x['kind'] in ks]
   if not z:st.info('No matching records in this layer yet.')
   for x in z[:150]:
    with st.expander(f"{x.get('title') or x.get('id')} · {x['kind']}"):
     if x.get('text'):st.write(x['text']);st.caption(' · '.join(str(v) for v in [x.get('author'),x.get('year'),x.get('topic'),x.get('status')] if v))
     if x.get('url'):st.link_button('Open source / citation',x['url'],key='open_'+str(x.get('id')))
 with tabs[3]:result_download(rr,'mlhkp_'+re.sub(r'\W+','_',q.lower()).strip('_')[:50])
 return rr
def explore():
 st.header('Explore Munda Knowledge');areas={'Language & Lexicon':['language','grammar','lexicon','mundari'],'Kinship & Kili':['kinship','kili'],'Life Cycle':['birth','marriage','death','funeral'],'Festivals & Rituals':['festival','ritual'],'Beliefs & Sacred Life':['belief','sacred','religion'],'Stories & Oral Traditions':['story','oral','tale','proverb'],'Songs · Dance · Music':['song','durang','dance','music'],'Food & Agriculture':['food','agriculture','crop'],'Ecology & Ethnobotany':['ecology','plant','forest'],'Material Culture · Crafts · Dress':['material','craft','dress'],'Houses & Architecture':['house','architecture'],'Livelihood & Economy':['livelihood','economy','market'],'Customary Law & Governance':['law','governance','land'],'Education · Health · Demography':['education','health','demography'],'Places & Landscapes':['place','village','landscape'],'History & Change':['history','historical','change']};area=st.selectbox('Knowledge area',list(areas));rr=[x for x in catalogue() if any(t in searchable(x) for t in areas[area])];st.metric('Linked records',len(rr));st.dataframe([{k:x.get(k) for k in ['kind','id','title','year','topic','status','url']} for x in rr],hide_index=True,use_container_width=True);result_download(rr,'mlhkp_'+re.sub(r'\W+','_',area.lower()))
def mundarica():
 st.header('Mundarica I–XVI');st.caption('Parallel deep-ingestion stream. Human review, OCR, transcription, page accounting and machine completeness remain distinct.');c=st.columns(4);c[0].metric('Permanent slots',16);c[1].metric('Located / working',sum(1 for v in VOLS if v.get('external_source') or v.get('volume')==1));c[2].metric('Page-accounted',AUD.get('page_accounting_complete_volumes',0));c[3].metric('VERIFIED COMPLETE',AUD.get('verified_complete_volumes',0));st.dataframe([{'Vol':v.get('volume'),'ID':v.get('source_id'),'State':'working corpus' if v.get('volume')==1 else ('located' if v.get('external_source') else 'locator pending'),'Pages':v.get('external_source',{}).get('total_pages_as_catalogued'),'Source':v.get('external_source',{}).get('canonical_url')} for v in VOLS],hide_index=True,use_container_width=True);st.warning('OCR is never treated as verified transcription. Human-review attestation does not automatically set VERIFIED COMPLETE.')
def library():
 st.header('Sources & Research Library');rr=catalogue();tabs=st.tabs(['All','MLHKP','Mundarica','External discovery','Evidence'])
 filters=[rr,[x for x in rr if x['kind']=='MLHKP source'],[x for x in rr if x['kind']=='Mundarica'],[x for x in rr if x['kind']=='External discovery'],[x for x in rr if x['kind']=='Evidence']]
 for t,z in zip(tabs,filters):
  with t:st.dataframe([{k:x.get(k) for k in ['kind','id','title','author','year','topic','status','url']} for x in z],hide_index=True,use_container_width=True)
def reports():
 st.header('Build Report & Download');st.caption('Build a reproducible topic dossier from the same records used by search — no duplicated cultural facts.');q=st.text_input('Report topic',placeholder='marriage, Kili, Sarhul, grammar…');rr=[x for x in catalogue() if not q or q.lower() in searchable(x) or any(t in searchable(x) for t in re.findall(r"[\w'-]+",q.lower()) if len(t)>3)];include=st.multiselect('Include layers',['Evidence','MLHKP source','Mundarica','External discovery'],default=['Evidence','MLHKP source','Mundarica']);rr=[x for x in rr if x['kind'] in include];st.subheader(q or 'Topic dossier');st.write(f'{len(rr)} permitted matching records. External discovery, when selected, is explicitly source discovery rather than verified cultural evidence.');st.dataframe([{k:x.get(k) for k in ['kind','id','title','year','status','url']} for x in rr],hide_index=True,use_container_width=True);result_download(rr,'mlhkp_report_'+re.sub(r'\W+','_',q.lower()).strip('_')[:50])
def governance():
 st.header('About · Governance · Ethics');st.success('Cultural access and consent override public, institutional or commercial entitlement.');data=[('Dr. Mohammad Amir Khusru Akhtar','Founder · Founding Chairperson · Founding Principal Investigator'),('Dr. Arvind Hans','Founding Project Director'),('Mr. Rajan Pahan','Founding Community, Meetings & Field Logistics Coordinator')];c=st.columns(3)
 for col,(n,r) in zip(c,data):
  with col:st.subheader(n);st.write('**'+r+'**')
 st.write('Source availability is not proof of reuse rights. OCR is not verified transcription. Historical reports are not automatically current or universal facts. External web discovery remains separate from ingested evidence.')
def render():
 st.set_page_config(page_title='MLHKP Knowledge Engine',page_icon='🌿',layout='wide');st.markdown('<style>.block-container{max-width:1450px;padding-top:1.2rem}[data-testid="stSidebar"]{background:#f2f7f1}.hero{padding:28px;border:1px solid #dce6dc;border-radius:22px;background:#f8fbf7}</style>',unsafe_allow_html=True)
 pages=['Home','Search & Ask','Explore','Mundarica I–XVI','Sources & Research Library','Build Report & Download','Completeness Dashboard','About · Governance · Ethics']
 with st.sidebar:st.markdown('## 🌿 MLHKP');st.caption('Search · Explore · Verify · Cite · Report · Download');page=st.radio('Navigate',pages,label_visibility='collapsed');st.divider();st.caption('One record, many outputs. No duplicated cultural facts.')
 if page=='Home':
  st.markdown('<div class="hero"><h1>MLHKP Knowledge Engine</h1><h3>Ask anything about documented Munda knowledge.</h3><p>Evidence-grounded answers, Mundarica I–XVI, source discovery, citations, topic reports and downloadable research data.</p></div>',unsafe_allow_html=True);metric_strip();search(key='home_search')
 elif page=='Search & Ask':st.header('Search & Ask MLHKP');search(key='ask_search')
 elif page=='Explore':explore()
 elif page=='Mundarica I–XVI':mundarica()
 elif page=='Sources & Research Library':library()
 elif page=='Build Report & Download':reports()
 elif page=='Completeness Dashboard':st.header('Measurable Completeness');metric_strip();st.info('These are live repository counts, not targets and not the illustrative 2,416 / 1,702 / 863 / 621 / 418 / 31,826 / 12,904 example numbers.')
 else:governance()
 st.divider();st.caption('MLHKP · Munda Cultural Dataset · Evidence, provenance, consent and cultural access preserved.')