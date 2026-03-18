import os

project_name = "leave_management_system"

folders = [
    "pages",
    "auth",
    "database",
    "services",
    "analytics",
    "models",
    "utils",
    "config",
    "assets"
]

files = {

"app.py":"""
import streamlit as st

st.set_page_config(
page_title="Leave Management System",
page_icon="📋",
layout="wide"
)

st.title("Leave Management System")

st.markdown(
'''
### Welcome

Use the sidebar to select your role

Faculty → Apply for leave  
HOD → Approve leave  
Principal → Final approval
'''
)
""",

"pages/1_Faculty.py":"""
import streamlit as st

st.title("Faculty Leave Application")
st.write("Faculty leave application form will appear here.")
""",

"pages/2_HOD.py":"""
import streamlit as st

st.title("HOD Dashboard")
st.write("Approve or reject faculty leave here.")
""",

"pages/3_Principal.py":"""
import streamlit as st

st.title("Principal Dashboard")
st.write("Final approval of leave requests.")
""",

"auth/login.py":"",

"database/db.py":"""
import sqlite3

DB_NAME="leave_system.db"

def get_connection():
    return sqlite3.connect(DB_NAME)
""",

"database/faculty_db.py":"",
"database/leave_db.py":"",

"services/email_service.py":"",
"services/approval_service.py":"",

"analytics/charts.py":"",

"models/leave_model.py":"",

"utils/helpers.py":"""
import uuid

def generate_request_id():
    return "REQ-"+str(uuid.uuid4())[:6].upper()
""",

"config/config.py":"",
"assets/styles.css":"",

"requirements.txt":"""
streamlit
pandas
plotly
bcrypt
yagmail
"""
}

# create root folder
os.makedirs(project_name, exist_ok=True)

# create subfolders
for folder in folders:
    os.makedirs(os.path.join(project_name, folder), exist_ok=True)

# create files
for path, content in files.items():

    full_path = os.path.join(project_name, path)

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Project structure created successfully.")