import sqlite3

DB_NAME = "leave_system.db"


# ================= CONNECTION =================
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row   # ✅ IMPORTANT (returns dict-like rows)
    return conn


# ================= CREATE TABLE =================
def create_leave_table():
    conn = get_connection()
    c = conn.cursor()

    # Base table
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
        email TEXT
    )
    """)

    # ================= SAFE COLUMN ADD =================
    c.execute("PRAGMA table_info(leaves)")
    columns = [col["name"] for col in c.fetchall()]  # ✅ FIXED (Row object)

    # Add missing columns safely
    if "days" not in columns:
        c.execute("ALTER TABLE leaves ADD COLUMN days INTEGER")

    if "designation" not in columns:
        c.execute("ALTER TABLE leaves ADD COLUMN designation TEXT")

    if "mobile" not in columns:
        c.execute("ALTER TABLE leaves ADD COLUMN mobile TEXT")

    if "alt_staff" not in columns:
        c.execute("ALTER TABLE leaves ADD COLUMN alt_staff TEXT")

    conn.commit()
    conn.close()


# ================= GET ALL LEAVES =================
def get_all_leaves():
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM leaves")
    rows = c.fetchall()

    conn.close()

    return [dict(row) for row in rows]   # ✅ always dictionary


# ================= GET LEAVE BY ID =================
def get_leave_by_id(leave_id):
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM leaves WHERE id = ?", (leave_id,))
    row = c.fetchone()

    conn.close()

    return dict(row) if row else None   # ✅ FIXES YOUR ERROR


# ================= UPDATE STATUS =================
def update_status(leave_id, status):
    conn = get_connection()
    c = conn.cursor()

    c.execute("UPDATE leaves SET status = ? WHERE id = ?", (status, leave_id))

    conn.commit()
    conn.close()


# ================= INIT =================
def init_db():
    create_leave_table()