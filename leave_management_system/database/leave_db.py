from database.db import get_connection   # ✅ FIXED
from datetime import datetime
from utils.logger import get_logger

# ✅ Logger
logger = get_logger("leave_db")


# ================= CREATE TABLE =================

def create_leave_table():

    try:
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
            days INTEGER   -- ✅ IMPORTANT
        )
        """)

        conn.commit()
        conn.close()

        logger.info("Leave table ensured/created successfully")

    except Exception as e:
        logger.error(f"Error creating table: {e}")


# ================= GENERATE REQUEST ID =================

def generate_request_id():
    return "REQ" + datetime.now().strftime("%Y%m%d%H%M%S")


# ================= INSERT LEAVE =================

def insert_leave(data):

    try:
        conn = get_connection()
        c = conn.cursor()

        c.execute("""
        INSERT INTO leaves
        (id, name, department, leave_type, from_date, to_date, reason, status, email, days)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, data)

        conn.commit()
        conn.close()

        logger.info(f"Leave inserted | ReqID: {data[0]} | Name: {data[1]}")

    except Exception as e:
        logger.error(f"Error inserting leave: {e}")


# ================= GET ALL LEAVES =================

def get_leaves():

    try:
        conn = get_connection()
        c = conn.cursor()

        rows = c.execute("SELECT * FROM leaves").fetchall()

        conn.close()

        logger.info("Fetched all leave records")

        return rows

    except Exception as e:
        logger.error(f"Error fetching leaves: {e}")
        return []


# ================= GET SINGLE LEAVE =================

def get_leave_by_id(request_id):

    try:
        conn = get_connection()
        c = conn.cursor()

        row = c.execute(
            "SELECT * FROM leaves WHERE id=?",
            (request_id,)
        ).fetchone()

        conn.close()

        logger.info(f"Fetched leave | ReqID: {request_id}")

        return row

    except Exception as e:
        logger.error(f"Error fetching leave {request_id}: {e}")
        return None


# ================= UPDATE STATUS =================

def update_status(request_id, status):

    try:
        conn = get_connection()
        c = conn.cursor()

        c.execute(
            "UPDATE leaves SET status=? WHERE id=?",
            (status, request_id)
        )

        conn.commit()
        conn.close()

        logger.info(f"Status updated | ReqID: {request_id} → {status}")

    except Exception as e:
        logger.error(f"Error updating status for {request_id}: {e}")