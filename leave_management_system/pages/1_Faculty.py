import streamlit as st
from utils.logger import get_logger
from utils.style import load_css
from database.leave_db import insert_leave, generate_request_id, get_leaves
import pandas as pd

# ✅ Load CSS
load_css()

# ✅ Logger
logger = get_logger("faculty")

# 🔐 ACCESS CONTROL
if st.session_state.get("role") != "Faculty":
    st.error("Unauthorized Access ❌")
    logger.warning("Unauthorized access attempt to Faculty Dashboard")
    st.stop()

st.title("Faculty Dashboard")

# 🔴 LOGOUT BUTTON
col1, col2 = st.columns([8, 1])
with col2:
    if st.button("Logout"):
        logger.info(f"{st.session_state.get('user')} logged out from Faculty")
        st.session_state.clear()
        st.switch_page("pages/login.py")

# ================= STAFF DATA =================

staffByDepartment = {
    "Computer Engineering": [
        "Dr. Krishnakant P. Adhiya","Dr. Manoj E. Patil (HOD)","Mr. Ashish T. Bhole",
        "Dr. Dnyaneshwar Kirange","Dr. Akash D. Waghmare","Dr. P. H. Zope",
        "Dr. S. P. Ramteke","Dr. Sheetal Patil","Dr. S. H. Rajput",
        "Mr. Mohan P. Patil","Mr. Ramkrishna H. Patil","Ms. Pooja Khandar",
        "Ms. Priyanka Vinod Medhe","Mr. Krunal Pawar","Ms. Ashwini A. Kakde",
        "Ms. Mayuri Chandratre","Ms. Shama Pawar","Mr. Pramod B. Gosavi"
    ],
    "Civil Engineering": [
        "Dr. Pankaj R. Punase (HOD)","Dr. Mujahid Husain","Dr. Pravin A. Shirule",
        "Dr. Farooq I. Chavan","Dr. Sonali B. Patil","Mrs. Jyoti R. Mali",
        "Ganesh Sonawane","Ms. Dipika Mali","Ms. Sushma Mahale"
    ],
    "Chemical Engineering": [
        "Dr. Sandeep A. Thakur (HOD)","Ms. Manasi Shashikant Nhalade",
        "Mrs. Sarika S. Pawar","Mr. Vijay P. Sangore"
    ],
    "Electrical Engineering": [
        "Mr. M. Mujtahid Ansari (HOD)","Mr. Vijay S. Pawar","Dr. Suhas M. Shembekar",
        "Mr. Muqueem M. Khan","Mr. Tanveer Husain","Mr. Vijay A. Shinde",
        "Ms. Shaikh Uzma Sabir","Dr. R. R. Karhe"
    ],
    "Mechanical Engineering": [
        "Mr. Navneet K. Patil","Dr. Krishna S. Shrivastava",
        "Dr. Prajitsen G. Damle (HOD)","Dr. Devendra B. Sadaphale",
        "Dr. Pradeep M. Solanki","Dr. Ajay R. Bhardwaj","Dr. Dipak C. Talele"
    ],
    "First Year Engineering": [
        "Dr. Sandip S. Patil (HOD)","Dr. Kiran S. Patil","Dr. Sunita S. Patil",
        "Mr. Y. K. Chitte","Dr. Prashant N. Ulhe","Dr. A. C. Wani",
        "Ms. Priti R. Sharma","Dr. Chandrashekhar U. Nikam","Dr. Pravin D. Patil",
        "Mr. Mahendra B. Patil","Ms. Meera V. Kulkarni","Ms. Dhanashree S. Tayade",
        "Mr. Ujwalsingh T. Patil","Ms. Tanuja Y. Chouhan","Ms. Jayshree R. Tayade",
        "Mr. Sachin Bhalerao","Dr. Devendra B. Sadaphale",
        "Ms. Siddhi Neve","Ms. Anjali Jain"
    ]
}

# ================= FORM =================

department = st.selectbox("Department", list(staffByDepartment.keys()))
faculty_list = staffByDepartment.get(department, [])

name = st.selectbox("Name", faculty_list)

designation = st.selectbox(
    "Designation",
    ["Assistant Professor", "Associate Professor", "Head of the Department"]
)

# ================= 🔥 AUTO EMAIL LOGIC =================

def generate_email(name):
    name = name.replace("Dr.", "").replace("Mr.", "").replace("Ms.", "").replace("Mrs.", "")
    name = name.replace("(HOD)", "").strip()
    parts = name.split()

    if len(parts) >= 2:
        return f"{parts[0].lower()}.{parts[-1].lower()}@sscoetjalgaon.ac.in"
    return ""

auto_email = generate_email(name)

# 👉 Auto-fill but editable
email = st.text_input("Email", value=auto_email)

# 🔴 VALIDATE (prevent Gmail)
if email and not email.endswith("@sscoetjalgaon.ac.in"):
    st.error("Only official college email allowed ❌")

mobile = st.text_input("Mobile")

from_date = st.date_input("From Date")
to_date = st.date_input("To Date")

leave_type = st.selectbox("Leave Type", ["CL","LWP","ML","EL","DL","SP"])

reason = st.text_area("Reason")

alt_staff = st.selectbox("Alternate Staff", faculty_list)

if alt_staff == name:
    st.warning("Alternate Staff cannot be same as applicant")

# ================= SUBMIT =================

if st.button("Submit Leave Application"):

    if not email or not reason:
        st.error("Please fill all required fields")

    elif not email.endswith("@sscoetjalgaon.ac.in"):
        st.error("Use official email only ❌")

    elif alt_staff == name:
        st.error("Applicant and Alternate Staff must be different")

    elif from_date > to_date:
        st.error("Invalid date range")

    else:
        days = (to_date - from_date).days + 1

        request_id = generate_request_id()

        data = (
            request_id, name, department, leave_type,
            str(from_date), str(to_date), reason,
            "Pending Approval", email, days
        )

        insert_leave(data)

        logger.info(f"Leave Submitted | {name} | ReqID: {request_id}")

        st.success("Leave Submitted Successfully ✅")
        st.info(f"Request ID: {request_id}")