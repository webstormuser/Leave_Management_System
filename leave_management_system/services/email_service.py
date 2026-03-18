import yagmail
import threading
from config.config import PRINCIPAL, CREATOR_NAME
from utils.logger import get_logger

# ✅ Logger
logger = get_logger("email")

# ---------------- EMAIL CONFIG ----------------

EMAIL = "yourgmail@gmail.com"
APP_PASSWORD = "your_app_password"

APP_URL = "http://localhost:8501"


# ---------------- CORE SEND FUNCTION ----------------

def _send_email(to, subject, html):
    try:
        yag = yagmail.SMTP(EMAIL, APP_PASSWORD)

        yag.send(
            to=to,
            subject=subject,
            contents=html
        )

        logger.info(f"Email sent successfully → {to} | Subject: {subject}")

    except Exception as e:
        logger.error(f"Email failed → {to} | Error: {e}")


# ---------------- ASYNC WRAPPER ----------------

def send_email(to, subject, html):
    try:
        thread = threading.Thread(
            target=_send_email,
            args=(to, subject, html)
        )
        thread.start()

        logger.info(f"Email thread started → {to}")

    except Exception as e:
        logger.error(f"Thread start failed → {to} | Error: {e}")


# ---------------- EMAIL TO HOD ----------------

def send_hod_email(request_id, form, hod):

    approve_link = f"{APP_URL}?action=HOD_APPROVE&id={request_id}"
    reject_link = f"{APP_URL}?action=HOD_REJECT&id={request_id}"

    html = f"""
    <p>Dear {hod['name']},</p>

    <p>A leave application requires approval.</p>

    <table border="1" cellpadding="6">
    <tr><td>Name</td><td>{form['name']}</td></tr>
    <tr><td>Department</td><td>{form['department']}</td></tr>
    <tr><td>Leave Type</td><td>{form['leave_type']}</td></tr>
    <tr><td>Duration</td><td>{form['from']} to {form['to']}</td></tr>
    <tr><td>Reason</td><td>{form['reason']}</td></tr>
    </table>

    <br>

    <a href="{approve_link}" style="padding:10px;background:#2e7d32;color:white;text-decoration:none;">
    APPROVE
    </a>

    &nbsp;&nbsp;

    <a href="{reject_link}" style="padding:10px;background:#c62828;color:white;text-decoration:none;">
    REJECT
    </a>

    <br><br>

    Regards<br>
    {CREATOR_NAME}
    """

    logger.info(f"Sending email to HOD → {hod['email']} | ReqID: {request_id}")
    send_email(hod["email"], f"Leave Approval Required | {request_id}", html)


# ---------------- EMAIL TO PRINCIPAL ----------------

def send_principal_email(request_id, leave):

    approve_link = f"{APP_URL}?action=PRINCIPAL_APPROVE&id={request_id}"
    reject_link = f"{APP_URL}?action=PRINCIPAL_REJECT&id={request_id}"

    html = f"""
    <p>Dear {PRINCIPAL['name']},</p>

    <p>Leave application requires your approval.</p>

    <table border="1" cellpadding="6">
    <tr><td>Name</td><td>{leave['name']}</td></tr>
    <tr><td>Department</td><td>{leave['department']}</td></tr>
    <tr><td>Leave Type</td><td>{leave['leave_type']}</td></tr>
    <tr><td>Duration</td><td>{leave['from']} to {leave['to']}</td></tr>
    <tr><td>Reason</td><td>{leave['reason']}</td></tr>
    </table>

    <br>

    <a href="{approve_link}" style="padding:10px;background:#2e7d32;color:white;text-decoration:none;">
    APPROVE
    </a>

    &nbsp;&nbsp;

    <a href="{reject_link}" style="padding:10px;background:#c62828;color:white;text-decoration:none;">
    REJECT
    </a>
    """

    logger.info(f"Sending email to Principal → {PRINCIPAL['email']} | ReqID: {request_id}")
    send_email(PRINCIPAL["email"], f"Principal Approval Required | {request_id}", html)


# ---------------- EMAIL TO APPLICANT ----------------

def send_applicant_email(email, name, status):

    html = f"""
    <p>Dear {name},</p>

    <p>Your leave application has been <b>{status}</b>.</p>

    Regards<br>
    {CREATOR_NAME}
    """

    logger.info(f"Sending email to Applicant → {email} | Status: {status}")
    send_email(email, "Leave Application Status", html)