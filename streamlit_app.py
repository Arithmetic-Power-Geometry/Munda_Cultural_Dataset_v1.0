import sys, json, sqlite3, urllib.parse
from pathlib import Path
import streamlit as st
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE/"software"))
from db import rows, execute
from auth import is_owner, OWNER_EMAIL
from reporting import send_report

st.set_page_config(page_title="Munda Cultural Dataset", page_icon="📚", layout="wide")
st.title("Munda Cultural Dataset v1.0")
st.caption("Cultural Indicators, Customs, Usages and Commonalities — From Birth to Burial")

if "owner" not in st.session_state: st.session_state.owner=False
with st.sidebar:
    st.subheader("Access")
    if not st.session_state.owner:
        email=st.text_input("Owner email",key="login_email")
        pw=st.text_input("Owner password",type="password",key="login_pw")
        if st.button("Owner sign in"):
            if is_owner(email,pw,st.secrets): st.session_state.owner=True; st.success("Owner access enabled"); st.rerun()
            else: st.error("Invalid owner credentials")
    else:
        st.success("Owner edit mode")
        if st.button("Sign out"): st.session_state.owner=False; st.rerun()
    st.divider()
    st.markdown(f"Corrections or concerns: **{OWNER_EMAIL}**")

pages=["Overview","Hierarchy","Source-backed claims","Indicators","Evidence graph","Report an issue"]
if st.session_state.owner: pages.append("Owner data editor")
page=st.sidebar.radio("Browse",pages)

def domain_name(did):
    r=rows("SELECT domain_name FROM cultural_domains WHERE domain_id=?",(did,)); return r[0]['domain_name'] if r else did

if page=="Overview":
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Domains",rows("SELECT COUNT(*) n FROM cultural_domains")[0]['n'])
    c2.metric("Indicators",rows("SELECT COUNT(*) n FROM cultural_indicators")[0]['n'])
    c3.metric("Sources",rows("SELECT COUNT(*) n FROM sources")[0]['n'])
    c4.metric("Source-backed claims",rows("SELECT COUNT(*) n FROM source_claims")[0]['n'])
    st.markdown("**Evidence rule:** published-source records are stored as source-reported claims until field verification and community validation are added. Contextual Jharkhand-wide claims are not automatically treated as Munda-universal.")
    st.markdown("**Permanent IDs:** indicators, claims, evidence, places and sources are never reused. New knowledge is added; earlier records are versioned rather than silently overwritten.")

elif page=="Hierarchy":
    ds=rows("SELECT * FROM cultural_domains ORDER BY sort_order")
    for d in ds:
        with st.expander(f"{d['domain_id']} — {d['domain_name']}"):
            sds=rows("SELECT * FROM cultural_subdomains WHERE domain_id=? ORDER BY sort_order",(d['domain_id'],))
            st.write([f"{x['subdomain_id']} — {x['subdomain_name']}" for x in sds])

elif page=="Source-backed claims":
    q=st.text_input("Search claims, terms or places")
    data=rows("SELECT c.*, s.title source_title, s.url source_url FROM source_claims c JOIN sources s ON s.source_id=c.source_id ORDER BY c.claim_id")
    if q:
        ql=q.lower(); data=[x for x in data if ql in json.dumps(x,ensure_ascii=False).lower()]
    for x in data:
        with st.expander(f"{x['claim_id']} · {x['claim_label']}"):
            st.write(x['claim_paraphrase'])
            st.write({"domain":domain_name(x['domain_id']),"local_term":x['local_term'],"scope":x['geographic_scope'],"status":x['claim_status'],"field_verification":x['field_verification_status']})
            st.link_button("Open source",x['source_url'])
            if st.session_state.owner:
                new=st.text_area("Edit paraphrase",x['claim_paraphrase'],key=f"e_{x['claim_id']}")
                reason=st.text_input("Reason for edit",key=f"r_{x['claim_id']}")
                if st.button("Save",key=f"s_{x['claim_id']}"):
                    old=json.dumps(x,ensure_ascii=False)
                    execute("UPDATE source_claims SET claim_paraphrase=?, updated_at=CURRENT_TIMESTAMP WHERE claim_id=?",(new,x['claim_id']))
                    execute("INSERT INTO audit_log(actor,entity_type,entity_id,operation,old_data,new_data,reason) VALUES (?,?,?,?,?,?,?)",(OWNER_EMAIL,'source_claim',x['claim_id'],'update',old,json.dumps({'claim_paraphrase':new},ensure_ascii=False),reason))
                    st.success("Saved with audit record"); st.rerun()
            else:
                subject=urllib.parse.quote(f"Munda Cultural Dataset report: {x['claim_id']}")
                body=urllib.parse.quote(f"Record: {x['claim_id']}\nSource: {x['source_url']}\n\nPlease describe the issue:\n")
                st.markdown(f"[Report this record by email](mailto:{OWNER_EMAIL}?subject={subject}&body={body})")

elif page=="Indicators":
    did=st.selectbox("Domain",[""]+[d['domain_id']+" — "+d['domain_name'] for d in rows("SELECT * FROM cultural_domains ORDER BY sort_order")])
    search=st.text_input("Search indicator")
    sql="SELECT * FROM cultural_indicators"; params=[]; cond=[]
    if did: cond.append("domain_id=?"); params.append(did.split(' — ')[0])
    if search: cond.append("(indicator_label LIKE ? OR research_prompt LIKE ?)"); params += [f"%{search}%",f"%{search}%"]
    if cond: sql+=' WHERE '+' AND '.join(cond)
    sql+=' ORDER BY indicator_id LIMIT 500'
    data=rows(sql,tuple(params))
    st.dataframe(data,use_container_width=True,hide_index=True)
    if st.session_state.owner:
        st.subheader("Add indicator")
        with st.form("add_indicator"):
            iid=st.text_input("Permanent indicator ID")
            dom=st.selectbox("Domain ID",[d['domain_id'] for d in rows("SELECT * FROM cultural_domains ORDER BY sort_order")])
            sds=rows("SELECT * FROM cultural_subdomains WHERE domain_id=? ORDER BY sort_order",(dom,))
            sd=st.selectbox("Subdomain ID",[s['subdomain_id'] for s in sds]) if sds else ''
            lab=st.text_input("Indicator label"); prompt=st.text_area("Research prompt")
            if st.form_submit_button("Add"):
                execute("INSERT INTO cultural_indicators(indicator_id,domain_id,subdomain_id,indicator_kind,indicator_label,research_prompt,knowledge_status,verification_status,version,status) VALUES (?,?,?,?,?,?,?,?,?,?)",(iid,dom,sd,'custom',lab,prompt,'candidate','field_verification_required',1,'active'))
                execute("INSERT INTO audit_log(actor,entity_type,entity_id,operation,new_data,reason) VALUES (?,?,?,?,?,?)",(OWNER_EMAIL,'indicator',iid,'insert',json.dumps({'label':lab}), 'owner-added'))
                st.success("Indicator added"); st.rerun()

elif page=="Evidence graph":
    st.markdown("Each source-backed claim is connected to a stable evidence ID. Field evidence can be added later without changing the claim/indicator identity.")
    data=rows("SELECT c.claim_id,c.claim_label,e.evidence_id,e.evidence_type,e.verification_state,s.source_id,s.title,s.url FROM source_claims c JOIN evidence e ON e.claim_id=c.claim_id JOIN sources s ON s.source_id=c.source_id ORDER BY c.claim_id")
    st.dataframe(data,use_container_width=True,hide_index=True)

elif page=="Report an issue":
    st.write("Reports are directed to the project contact. The public interface does not permit direct edits.")
    target=st.text_input("Record ID (optional)")
    name=st.text_input("Your name")
    email=st.text_input("Your email")
    report=st.text_area("Correction, concern or additional evidence")
    if st.button("Prepare report"):
        if report.strip():
            execute("INSERT INTO reports(target_type,target_id,reporter_name,reporter_email,report_text) VALUES (?,?,?,?,?)",('record',target,name,email,report))
            subject=urllib.parse.quote(f"Munda Cultural Dataset report: {target or 'general'}")
            body=urllib.parse.quote(f"Reporter: {name}\nEmail: {email}\nRecord: {target}\n\n{report}")
            sent,msg=send_report(f"Munda Cultural Dataset report: {target or 'general'}", f"Reporter: {name}\nEmail: {email}\nRecord: {target}\n\n{report}", st.secrets)
            if sent:
                st.success(f"Report sent to {OWNER_EMAIL} and added to the review queue.")
            else:
                st.success("Report added to the review queue.")
                st.info("Direct email is not configured on this deployment; use the email link below.")
                st.markdown(f"[Send the report to {OWNER_EMAIL}](mailto:{OWNER_EMAIL}?subject={subject}&body={body})")
        else: st.warning("Please enter a report.")

elif page=="Owner data editor":
    if not st.session_state.owner:
        st.error("Owner access required")
    else:
        st.subheader("Owner data editor")
        editable={
            "cultural_domains":"domain_id","cultural_subdomains":"subdomain_id","cultural_indicators":"indicator_id",
            "sources":"source_id","source_claims":"claim_id","evidence":"evidence_id","places":"place_id"
        }
        table=st.selectbox("Section/table",list(editable))
        pk=editable[table]
        recs=rows(f"SELECT * FROM {table} ORDER BY {pk} LIMIT 2000")
        ids=[r[pk] for r in recs]
        rid=st.selectbox("Record",ids) if ids else None
        if rid:
            rec=next(r for r in recs if r[pk]==rid)
            st.caption("Permanent IDs cannot be edited. Other values are version/audit tracked.")
            newvals={}
            for k,v in rec.items():
                if k==pk: st.text_input(k,str(v or ""),disabled=True,key=f"oe_{table}_{rid}_{k}")
                elif k in ("updated_at",): st.text_input(k,str(v or ""),disabled=True,key=f"oe_{table}_{rid}_{k}")
                else: newvals[k]=st.text_area(k,str(v or ""),height=70,key=f"oe_{table}_{rid}_{k}")
            reason=st.text_input("Reason for change",key=f"oe_reason_{table}_{rid}")
            if st.button("Save audited changes",key=f"oe_save_{table}_{rid}"):
                changed={k:v for k,v in newvals.items() if str(rec.get(k) or "")!=v}
                if not changed: st.info("No changes detected")
                else:
                    sets=", ".join([f"{k}=?" for k in changed])
                    vals=list(changed.values())+[rid]
                    execute(f"UPDATE {table} SET {sets} WHERE {pk}=?",tuple(vals))
                    execute("INSERT INTO audit_log(actor,entity_type,entity_id,operation,old_data,new_data,reason) VALUES (?,?,?,?,?,?,?)",(OWNER_EMAIL,table,rid,'update',json.dumps(rec,ensure_ascii=False),json.dumps(changed,ensure_ascii=False),reason))
                    st.success("Saved with audit record"); st.rerun()

st.divider()
st.caption("Apache License 2.0 · © 2026 Mohammad Amir Khusru Akhtar and Arvind Hans")
