import sqlite3
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"database"/"munda_cultural.db"
con=sqlite3.connect(p)
assert con.execute("select count(*) from cultural_domains").fetchone()[0] >= 20
assert con.execute("select count(*) from cultural_indicators").fetchone()[0] >= 300
assert con.execute("select count(*) from source_claims").fetchone()[0] >= 30
assert con.execute("select count(*) from sources").fetchone()[0] >= 10
print("seed database OK")
