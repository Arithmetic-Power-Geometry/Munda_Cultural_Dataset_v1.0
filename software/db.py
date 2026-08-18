from pathlib import Path
import os, sqlite3, json
DB_PATH = Path(__file__).resolve().parents[1] / "database" / "munda_cultural.db"

def connect():
    url=os.getenv("DATABASE_URL","")
    if url:
        try:
            from sqlalchemy import create_engine
            return create_engine(url, pool_pre_ping=True)
        except Exception:
            pass
    con=sqlite3.connect(DB_PATH, check_same_thread=False)
    con.row_factory=sqlite3.Row
    return con

def rows(sql, params=()):
    con=connect()
    if isinstance(con, sqlite3.Connection):
        cur=con.execute(sql,params); out=[dict(r) for r in cur.fetchall()]; con.close(); return out
    from sqlalchemy import text
    with con.connect() as c: return [dict(r._mapping) for r in c.execute(text(sql),params)]

def execute(sql, params=()):
    con=connect()
    if isinstance(con, sqlite3.Connection):
        cur=con.execute(sql,params); con.commit(); rid=cur.lastrowid; con.close(); return rid
    from sqlalchemy import text
    with con.begin() as c: c.execute(text(sql),params)
    return None
