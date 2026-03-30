import yagmail
import threading
from config.config import PRINCIPAL, CREATOR_NAME
from utils.logger import get_logger

logger = get_logger("email")

# ================= EMAIL CONFIG =================

EMAIL = "yourgmail@gmail.com"
APP_PASSWORD = "your_app_password"

APP_URL = "http://127.0.0.1:5000"


# ================= CORE SEND =================

def _send_email(to, subject, html):
    try:
        yag = yagmail.SMTP(EMAIL, APP_PASSWORD)

        yag.send(
            to=to,
            subject=subject,
            contents=html
        )

        logger.info(f"Email sent → {to} | {subject}")

    except Exception as e:
        logger.error(f"Email failed → {to} | Error: {e}")


# ================= ASYNC HANDLER =================

def send_email(to, subject, html):
    try:
        thread = threading.Thread(
            target=_send_email,
            args=(to, subject, html),
            daemon=True
        )
        thread.start()

    except Exception as e:
        logger.error(f"Thread error → {to} | {e}")


# ================= TEMPLATE =================

def email_template(title, body):
    return f"""
    <div style="font-family:Segoe UI;padding:20px;">
        <h2 style="color:#2e7d32;">{title}</h2>
        <div>{body}</div>
        <br><hr>
        <p>{CREATOR_NAME}</p>
    </div>
    """


# ================= HOD EMAIL =================

def send_hod_email(request_id, form, hod):

    body = f"""
    <p>Dear {hod['name']},</p>

    <p>A leave application requires your approval.</p>

    <table border="1" cellpadding="6">
        <tr><td>Name</td><td>{form['name']}</td></tr>
        <tr><td>Department</td><td>{form['department']}</td></tr>
        <tr><td>Leave Type</td><td>{form['leave_type']}</td></tr>
        <tr><td>Duration</td><td>{form['from']} to {form['to']}</td></tr>
        <tr><td>Reason</td><td>{form['reason']}</td></tr>
    </table>

    <br>
    <a href="{APP_URL}/hod" style="padding:10px;background:#2e7d32;color:white;">
    Open Dashboard
    </a>
    """

    html = email_template("HOD Approval Required", body)

    logger.info(f"HOD email → {hod['email']} | ReqID: {request_id}")
    send_email(hod["email"], f"Leave Approval Required | {request_id}", html)


# ================= PRINCIPAL EMAIL =================

def send_principal_email(request_id, leave):

    principal_email = PRINCIPAL

    body = f"""
    <p>Dear Principal,</p>

    <p>Leave application requires your approval.</p>

    <table border="1" cellpadding="6">
        <tr><td>Name</td><td>{leave['name']}</td></tr>
        <tr><td>Department</td><td>{leave['department']}</td></tr>
        <tr><td>Leave Type</td><td>{leave['leave_type']}</td></tr>
        <tr><td>Duration</td><td>{leave['from']} to {leave['to']}</td></tr>
        <tr><td>Reason</td><td>{leave['reason']}</td></tr>
    </table>

    <br>
    <a href="{APP_URL}/principal" style="padding:10px;background:#2e7d32;color:white;">
    Open Dashboard
    </a>
    """

    html = email_template("Principal Approval Required", body)

    logger.info(f"Principal email → {principal_email} | ReqID: {request_id}")
    send_email(principal_email, f"Principal Approval Required | {request_id}", html)


# ================= APPLICANT EMAIL =================

def send_applicant_email(email, name, status):

    body = f"""
    <p>Dear {name},</p>

    <p>Your leave application has been <b>{status}</b>.</p>
    """

    html = email_template("Leave Status Update", body)

    logger.info(f"Applicant email → {email} | {status}")
    send_email(email, "Leave Application Status", html)