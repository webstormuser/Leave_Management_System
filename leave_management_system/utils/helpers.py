import uuid
from datetime import datetime

def generate_request_id():
    uid = str(uuid.uuid4()).replace("-", "")[:6].upper()
    date_part = datetime.now().strftime("%d%m")
    return f"REQ-{date_part}-{uid}"