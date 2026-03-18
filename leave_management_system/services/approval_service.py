from database.leave_db import update_status
from services.email_service import (
    send_principal_email,
    send_applicant_email
)


def handle_approval(action, leave):

    request_id = leave["id"]
    leave_type = leave["leave_type"]

    # ---------------- HOD APPROVAL ----------------

    if action == "HOD_APPROVE":

        if leave_type == "CL":

            update_status(request_id, "Approved by HOD")

            send_applicant_email(
                leave["email"],
                leave["name"],
                "Approved by HOD"
            )

            return "Leave Approved by HOD"

        if leave_type in ["ML", "DL"]:

            update_status(request_id, "Pending Principal Approval")

            send_principal_email(request_id, leave)

            return "Approved by HOD → Sent to Principal"


    # ---------------- HOD REJECT ----------------

    if action == "HOD_REJECT":

        update_status(request_id, "Rejected by HOD")

        send_applicant_email(
            leave["email"],
            leave["name"],
            "Rejected by HOD"
        )

        return "Leave Rejected by HOD"


    # ---------------- PRINCIPAL APPROVAL ----------------

    if action == "PRINCIPAL_APPROVE":

        update_status(request_id, "Approved by Principal")

        send_applicant_email(
            leave["email"],
            leave["name"],
            "Approved by Principal"
        )

        return "Leave Approved by Principal"


    # ---------------- PRINCIPAL REJECT ----------------

    if action == "PRINCIPAL_REJECT":

        update_status(request_id, "Rejected by Principal")

        send_applicant_email(
            leave["email"],
            leave["name"],
            "Rejected by Principal"
        )

        return "Leave Rejected by Principal"