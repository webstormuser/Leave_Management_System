from database.db import get_connection
from utils.logger import get_logger

# ✅ Logger
logger = get_logger("faculty_db")


# ================= CREATE TABLE =================

def create_faculty_table():

    try:
        conn = get_connection()
        c = conn.cursor()

        c.execute("""
        CREATE TABLE IF NOT EXISTS faculty (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT,
            department TEXT,
            role TEXT
        )
        """)

        conn.commit()
        conn.close()

        logger.info("Faculty table ensured/created successfully")

    except Exception as e:
        logger.error(f"Error creating faculty table: {e}")


# ================= INSERT FACULTY =================

def insert_faculty(name, email, password, department, role):

    try:
        conn = get_connection()
        c = conn.cursor()

        c.execute("""
        INSERT INTO faculty (name, email, password, department, role)
        VALUES (?, ?, ?, ?, ?)
        """, (name, email, password, department, role))

        conn.commit()
        conn.close()

        logger.info(f"Faculty inserted | {email}")

    except Exception as e:
        logger.error(f"Error inserting faculty: {e}")


# ================= GET ALL FACULTY =================

def get_all_faculty():

    try:
        conn = get_connection()
        c = conn.cursor()

        rows = c.execute("SELECT * FROM faculty").fetchall()

        conn.close()

        return rows

    except Exception as e:
        logger.error(f"Error fetching faculty: {e}")
        return []


# ================= GET FACULTY BY EMAIL =================

def get_faculty_by_email(email):

    try:
        conn = get_connection()
        c = conn.cursor()

        row = c.execute(
            "SELECT * FROM faculty WHERE email=?",
            (email,)
        ).fetchone()

        conn.close()

        return row

    except Exception as e:
        logger.error(f"Error fetching faculty by email: {e}")
        return None


# ================= LOGIN VALIDATION =================

def validate_user(email, password):

    try:
        conn = get_connection()
        c = conn.cursor()

        user = c.execute("""
        SELECT * FROM faculty 
        WHERE email=? AND password=?
        """, (email, password)).fetchone()

        conn.close()

        if user:
            logger.info(f"Login success | {email}")
        else:
            logger.warning(f"Login failed | {email}")

        return user

    except Exception as e:
        logger.error(f"Login error: {e}")
        return None