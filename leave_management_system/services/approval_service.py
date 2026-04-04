from database.leave_db import update_status
from services.email_service import (
    send_principal_email,
    send_applicant_email
)
from utils.logger import get_logger

logger = get_logger("approval")


def handle_approval(action, leave):

    try:
        # ================= SAFE ACCESS =================
        request_id = leave.get("id")
        leave_type = leave.get("leave_type")

        logger.info(f"Processing {action} | ReqID: {request_id}")
        logger.info(f"Leave Data: {leave}")

        # ================= HOD APPROVE =================
        if action == "HOD_APPROVE":

            # ✅ ML / DL → SEND TO PRINCIPAL
            if leave_type in ["ML", "DL"]:

                update_status(request_id, "Pending Principal Approval")

                send_principal_email(request_id, leave)

                return "Approved by HOD → Sent to Principal"

            # ✅ OTHER LEAVES → FINAL AT HOD
            else:

                update_status(request_id, "Approved by HOD")

                send_applicant_email(
                    leave.get("email"),
                    leave.get("name"),
                    "Approved by HOD"
                )

                return "Leave Approved by HOD"

        # ================= HOD REJECT =================
        elif action == "HOD_REJECT":

            update_status(request_id, "Rejected by HOD")

            send_applicant_email(
                leave.get("email"),
                leave.get("name"),
                "Rejected by HOD"
            )

            return "Leave Rejected by HOD"

        # ================= PRINCIPAL APPROVE =================
        elif action == "PRINCIPAL_APPROVE":

            update_status(request_id, "Approved by Principal")

            send_applicant_email(
                leave.get("email"),
                leave.get("name"),
                "Approved by Principal"
            )

            return "Leave Approved by Principal"

        # ================= PRINCIPAL REJECT =================
        elif action == "PRINCIPAL_REJECT":

            update_status(request_id, "Rejected by Principal")

            send_applicant_email(
                leave.get("email"),
                leave.get("name"),
                "Rejected by Principal"
            )

            return "Leave Rejected by Principal"

        # ================= INVALID =================
        else:
            logger.error(f"Invalid action: {action}")
            return "Invalid action"

    except Exception as e:
        logger.error(f"Approval Error: {str(e)}")
        return "Error processing approval"