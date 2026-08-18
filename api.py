import os, sys
from pathlib import Path
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE/"software"))
from db import rows, execute
app=FastAPI(title="Munda Cultural Dataset API",version="1.0.0")
ADMIN_TOKEN=os.getenv("MCD_ADMIN_TOKEN","")

def admin(auth):
    if not ADMIN_TOKEN or auth != f"Bearer {ADMIN_TOKEN}": raise HTTPException(403,"Owner token required")

@app.get("/health")
def health(): return {"status":"ok","version":"1.0.0"}
@app.get("/domains")
def domains(): return rows("SELECT * FROM cultural_domains ORDER BY sort_order")
@app.get("/indicators")
def indicators(domain_id:str|None=None,q:str|None=None,limit:int=200):
    sql="SELECT * FROM cultural_indicators WHERE 1=1"; p=[]
    if domain_id: sql+=" AND domain_id=?"; p.append(domain_id)
    if q: sql+=" AND (indicator_label LIKE ? OR research_prompt LIKE ?)"; p += [f"%{q}%",f"%{q}%"]
    sql+=" ORDER BY indicator_id LIMIT ?"; p.append(min(limit,1000)); return rows(sql,tuple(p))
@app.get("/claims")
def claims(q:str|None=None,limit:int=200):
    sql="SELECT c.*,s.title source_title,s.url source_url FROM source_claims c JOIN sources s ON s.source_id=c.source_id WHERE 1=1"; p=[]
    if q: sql+=" AND (c.claim_label LIKE ? OR c.claim_paraphrase LIKE ? OR c.local_term LIKE ?)"; p += [f"%{q}%"]*3
    sql+=" ORDER BY c.claim_id LIMIT ?"; p.append(min(limit,1000)); return rows(sql,tuple(p))
@app.get("/claims/{claim_id}")
def claim(claim_id:str):
    r=rows("SELECT c.*,s.title source_title,s.url source_url FROM source_claims c JOIN sources s ON s.source_id=c.source_id WHERE claim_id=?",(claim_id,))
    if not r: raise HTTPException(404,"Not found")
    ev=rows("SELECT * FROM evidence WHERE claim_id=?",(claim_id,)); return {"claim":r[0],"evidence":ev}
class ClaimPatch(BaseModel): claim_paraphrase:str; reason:str
@app.patch("/claims/{claim_id}")
def patch_claim(claim_id:str,p:ClaimPatch,authorization:str|None=Header(default=None)):
    admin(authorization); old=rows("SELECT * FROM source_claims WHERE claim_id=?",(claim_id,))
    if not old: raise HTTPException(404,"Not found")
    execute("UPDATE source_claims SET claim_paraphrase=?, updated_at=CURRENT_TIMESTAMP WHERE claim_id=?",(p.claim_paraphrase,claim_id))
    execute("INSERT INTO audit_log(actor,entity_type,entity_id,operation,old_data,new_data,reason) VALUES (?,?,?,?,?,?,?)",('owner','source_claim',claim_id,'update',str(old[0]),p.claim_paraphrase,p.reason))
    return {"status":"updated","claim_id":claim_id}
