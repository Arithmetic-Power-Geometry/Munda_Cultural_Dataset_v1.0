import json
from pathlib import Path
import streamlit as st
BASE=Path(__file__).resolve().parent
MAN=BASE/'data/source_bundles/encyclopaedia_mundarica/manifest.json'; ATT=BASE/'data/source_bundles/encyclopaedia_mundarica/human_verification_attestation.json'
st.set_page_config(page_title='MLHKP · Munda Cultural Dataset',page_icon='🌿',layout='wide')
def load(p,d):
 try:return json.loads(p.read_text(encoding='utf-8')) if p.exists() else d
 except Exception:return d
m=load(MAN,{'volume_slots':[]}); a=m.get('audit_summary',{}); vols=m.get('volume_slots',[]); h=load(ATT,{})
st.title('Munda Living Heritage & Knowledge Project')
st.caption('Munda Cultural Dataset · evidence-preserving public research workspace')
st.header('Encyclopaedia Mundarica · Volumes I–XVI')
st.write('Readers can inspect the work already completed while source discovery, OCR, transcription, human review and machine verification remain explicitly separate evidence layers.')
c=st.columns(6); c[0].metric('Volumes',16); c[1].metric('Located',a.get('externally_located_volumes',0)); c[2].metric('Page-accounted',a.get('page_accounting_complete_volumes',0)); c[3].metric('Working texts',a.get('registered_working_transcriptions',0)); c[4].metric('Human review','I–XVI' if h.get('attestation',{}).get('status')=='human_review_attested' else '—'); c[5].metric('VERIFIED COMPLETE',a.get('verified_complete_volumes',0))
if h.get('attestation',{}).get('status')=='human_review_attested': st.success('Human review attested for Volumes I–XVI — named lead reviewer: Dr. Arvind Hans; review team identities/dates were not supplied in the retrospective attestation.')
st.warning('Human-review attestation does not automatically verify repository OCR or set VERIFIED COMPLETE. Machine completeness remains evidence-gated.')
summary=[]
for v in vols:
 e=v.get('external_source',{}); n=v.get('volume'); summary.append({'Volume':n,'Permanent ID':v.get('source_id'),'Completed work':'324/324 page blocks + working transcription' if n==1 else ('Repository locator + catalogue metadata' if e else 'Structure ready'),'Pages':e.get('total_pages_as_catalogued') or (a.get('volume_1_declared_scan_pages') if n==1 else None),'Text layer':'Working transcription' if n==1 else ('Repository OCR available · unverified' if e else 'Not ingested'),'Human review':'Attested' if h.get('attestation',{}).get('status')=='human_review_attested' else '—','Machine complete':'YES' if v.get('verified_complete') else 'NO'})
st.dataframe(summary,use_container_width=True,hide_index=True)
opts=[f"Volume {v['volume']} · {v['source_id']}" for v in vols]; sel=st.selectbox('Read / inspect volume',opts); v=vols[opts.index(sel)]; e=v.get('external_source',{}); n=v['volume']
st.subheader(sel); tabs=st.tabs(['Reader / Work completed','Source & provenance','Verification','Structured knowledge'])
with tabs[0]:
 if n==1:
  st.success('324/324 structural page blocks are accounted for and a working-transcription artifact is registered.')
  st.info('The working text is retained as a distinct, non-scan-verified layer until authoritative-artifact reconciliation is complete.')
 elif e:
  st.success('The Internet Archive repository locator and available catalogue metadata are registered.')
  st.info('Repository OCR is reference material, not verified MLHKP transcription.')
  if e.get('canonical_url'): st.link_button('Open source record',e['canonical_url'])
 else: st.info('Structure ready — evidence not yet ingested.')
with tabs[1]:
 st.write('**Permanent source ID:**',v.get('source_id')); st.write('**Corpus state:**',v.get('status'))
 if e:
  fields={'Repository':e.get('repository'),'Catalogue title':e.get('title_as_catalogued'),'Creator':e.get('creator_as_catalogued'),'Year':e.get('publication_year_as_catalogued'),'Pages':e.get('total_pages_as_catalogued'),'Identifier':e.get('identifier'),'ARK':e.get('ark'),'Publisher':e.get('publisher_as_catalogued'),'Source institution':e.get('source_institution'),'Scanning centre':e.get('scanning_centre'),'OCR':e.get('ocr_engine_as_catalogued'),'Rights assessment':e.get('rights_status'),'Acquisition':e.get('acquisition_status')}
  st.dataframe([{'Field':k,'Value':str(x)} for k,x in fields.items() if x not in (None,'')],use_container_width=True,hide_index=True)
  if e.get('available_derivatives_observed'): st.write('**Observed derivatives:**',', '.join(e['available_derivatives_observed']))
  if e.get('verification_note'): st.caption(e['verification_note'])
with tabs[2]:
 at=h.get('attestation',{}); st.write('**Human-review status:**',at.get('status','not recorded')); st.write('**Named lead reviewer:**',at.get('named_lead_reviewer','—')); st.write('**Attested review scope:**',h.get('scope',{}).get('review_scope_as_attested','—')); st.caption(h.get('provenance',{}).get('uncertainty',''))
 gates=[('Permanent source ID',bool(v.get('source_id'))),('Source/artifact located',bool(e) or n==1),('Page accounting',n==1 and bool(a.get('volume_1_page_order_complete'))),('Authoritative artifact reconciled',n==1 and bool(a.get('volume_1_scan_registered'))),('Verified transcription',bool(v.get('verified_transcription_complete'))),('Structured-content audit',bool(v.get('structured_content_complete'))),('Completeness audit',bool(v.get('verified_complete')))]
 st.dataframe([{'Gate':x,'State':'PASS' if y else 'PENDING'} for x,y in gates],use_container_width=True,hide_index=True)
with tabs[3]: st.info('Entries, stories, songs, terms, places and cultural-topic records will appear here only after provenance linking and access review. Empty structure is never counted as completed evidence.')
st.divider(); st.markdown('**Founding leadership:** Dr. Mohammad Amir Khusru Akhtar — Founder · Founding Chairperson · Founding Principal Investigator · Dr. Arvind Hans — Founding Project Director · **Mr. Rajan Pahan — Founding Community, Meetings & Field Logistics Coordinator**')
st.caption('Cultural access and consent override public or commercial entitlement. Historical/source-reported statements are not automatically universal or current facts. Third-party works retain their own rights.')