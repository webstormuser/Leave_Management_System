
import uuid

def generate_request_id():
    return "REQ-"+str(uuid.uuid4())[:6].upper()
