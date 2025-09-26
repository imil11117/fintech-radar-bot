import sqlite3, datetime

DB_PATH = "posted.sqlite"

def ensure_db(path: str = DB_PATH):
    con = sqlite3.connect(path)
    con.execute("CREATE TABLE IF NOT EXISTS posted (id TEXT PRIMARY KEY, ts TEXT)")
    con.commit(); con.close()

def was_posted(pid: str, path: str = DB_PATH) -> bool:
    con = sqlite3.connect(path)
    cur = con.execute("SELECT 1 FROM posted WHERE id=?", (pid,))
    ok = cur.fetchone() is not None
    con.close()
    return ok

def mark_posted(pid: str, path: str = DB_PATH):
    con = sqlite3.connect(path)
    con.execute("INSERT OR IGNORE INTO posted(id, ts) VALUES(?, ?)",
                (pid, datetime.datetime.utcnow().isoformat()))
    con.commit(); con.close()