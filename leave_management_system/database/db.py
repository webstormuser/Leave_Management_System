import sqlite3

DB_NAME = "leave_system.db"


# ================= CONNECTION =================

def get_connection():
    return sqlite3.connect(DB_NAME)


# ================= CREATE TABLE =================

def create_leave_table():

    conn = get_connection()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS leaves (
        id TEXT PRIMARY KEY,
        name TEXT,
        department TEXT,
        leave_type TEXT,
        from_date TEXT,
        to_date TEXT,
        reason TEXT,
        status TEXT,
        email TEXT,
        days INTEGER
    )
    """)

    conn.commit()
    conn.close()


# ================= INIT =================

def init_db():
    create_leave_table()   # ✅ ONLY THIS