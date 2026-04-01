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


# ================= SAFE DATE HANDLER =================
def get_dates(data):
    """
    Handles both formats:
    - from_date / to_date
    - from / to
    """
    from_date = data.get("from_date") or data.get("from") or ""
    to_date = data.get("to_date") or data.get("to") or ""
    return from_date, to_date


# ================= HOD EMAIL =================
def send_hod_email(request_id, form, hod):

    from_date, to_date = get_dates(form)

    body = f"""
    <p>Dear {hod.get('name', 'HOD')},</p>

    <p>A leave application requires your approval.</p>

    <table border="1" cellpadding="6">
        <tr><td>Name</td><td>{form.get('name')}</td></tr>
        <tr><td>Department</td><td>{form.get('department')}</td></tr>
        <tr><td>Leave Type</td><td>{form.get('leave_type')}</td></tr>
        <tr><td>Duration</td><td>{from_date} to {to_date}</td></tr>
        <tr><td>Reason</td><td>{form.get('reason')}</td></tr>
    </table>

    <br>
    <a href="{APP_URL}/hod" style="padding:10px;background:#2e7d32;color:white;text-decoration:none;">
    Open Dashboard
    </a>
    """

    html = email_template("HOD Approval Required", body)

    logger.info(f"HOD email → {hod.get('email')} | ReqID: {request_id}")
    send_email(hod.get("email"), f"Leave Approval Required | {request_id}", html)


# ================= PRINCIPAL EMAIL =================
def send_principal_email(request_id, leave):

    from_date, to_date = get_dates(leave)

    body = f"""
    <p>Dear Principal,</p>

    <p>Leave application requires your approval.</p>

    <table border="1" cellpadding="6">
        <tr><td>Name</td><td>{leave.get('name')}</td></tr>
        <tr><td>Department</td><td>{leave.get('department')}</td></tr>
        <tr><td>Leave Type</td><td>{leave.get('leave_type')}</td></tr>
        <tr><td>Duration</td><td>{from_date} to {to_date}</td></tr>
        <tr><td>Reason</td><td>{leave.get('reason')}</td></tr>
    </table>

    <br>
    <a href="{APP_URL}/principal" style="padding:10px;background:#2e7d32;color:white;text-decoration:none;">
    Open Dashboard
    </a>
    """

    html = email_template("Principal Approval Required", body)

    logger.info(f"Principal email → {PRINCIPAL} | ReqID: {request_id}")
    send_email(PRINCIPAL, f"Principal Approval Required | {request_id}", html)


# ================= APPLICANT EMAIL =================
def send_applicant_email(email, name, status):

    body = f"""
    <p>Dear {name},</p>

    <p>Your leave application has been <b>{status}</b>.</p>
    """

    html = email_template("Leave Status Update", body)

    logger.info(f"Applicant email → {email} | {status}")
    send_email(email, "Leave Application Status", html)