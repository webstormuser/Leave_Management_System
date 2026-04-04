import sqlite3

DB_NAME = "leave_system.db"


# ================= CONNECTION =================
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # VERY IMPORTANT
    return conn


# ================= CREATE TABLE =================
def create_leave_table():
    conn = get_connection()
    c = conn.cursor()

    # ================= BASE TABLE =================
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

    # ================= CHECK EXISTING COLUMNS =================
    c.execute("PRAGMA table_info(leaves)")
    columns = [col["name"] for col in c.fetchall()]

    # ================= SAFE COLUMN ADD =================
    if "days" not in columns:
        c.execute("ALTER TABLE leaves ADD COLUMN days INTEGER")

    if "designation" not in columns:
        c.execute("ALTER TABLE leaves ADD COLUMN designation TEXT")

    if "mobile" not in columns:
        c.execute("ALTER TABLE leaves ADD COLUMN mobile TEXT")

    if "alt_staff" not in columns:
        c.execute("ALTER TABLE leaves ADD COLUMN alt_staff TEXT")

    # ✅ FILE PATH STORAGE
    if "proof" not in columns:
        c.execute("ALTER TABLE leaves ADD COLUMN proof TEXT")

    # ✅ TRACK WHETHER PRINCIPAL VIEWED PROOF
    if "proof_viewed" not in columns:
        c.execute("ALTER TABLE leaves ADD COLUMN proof_viewed INTEGER DEFAULT 0")

    # ================= FIX OLD WINDOWS PATHS =================
    # Replace "\" with "/" in stored paths
    c.execute("""
        UPDATE leaves
        SET proof = REPLACE(proof, '\\\\', '/')
        WHERE proof LIKE '%\\\\%'
    """)

    conn.commit()
    conn.close()


# ================= GET LEAVES =================
def get_leaves():
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM leaves ORDER BY rowid DESC")
    rows = c.fetchall()

    conn.close()
    return rows


# ================= GET ALL LEAVES (DICT FORMAT) =================
def get_all_leaves():
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM leaves ORDER BY rowid DESC")
    rows = c.fetchall()

    conn.close()
    return [dict(row) for row in rows]


# ================= GET LEAVE BY ID =================
def get_leave_by_id(leave_id):
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM leaves WHERE id = ?", (leave_id,))
    row = c.fetchone()

    conn.close()
    return dict(row) if row else None


# ================= UPDATE STATUS =================
def update_status(leave_id, status):
    conn = get_connection()
    c = conn.cursor()

    c.execute("UPDATE leaves SET status = ? WHERE id = ?", (status, leave_id))

    conn.commit()
    conn.close()


# ================= MARK PROOF VIEWED =================
def mark_proof_viewed(leave_id):
    conn = get_connection()
    c = conn.cursor()

    c.execute("UPDATE leaves SET proof_viewed = 1 WHERE id = ?", (leave_id,))

    conn.commit()
    conn.close()


# ================= INIT =================
def init_db():
    create_leave_table()