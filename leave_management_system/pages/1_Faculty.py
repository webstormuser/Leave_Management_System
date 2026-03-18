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
        "Dr. Krishnakant P. Adhiya",
        "Dr. Manoj E. Patil (HOD)",
        "Mr. Ashish T. Bhole",
        "Dr. Dnyaneshwar Kirange",
        "Dr. Akash D. Waghmare",
        "Dr. P. H. Zope",
        "Dr. S. P. Ramteke",
        "Dr. Sheetal Patil",
        "Dr. S. H. Rajput",
        "Mr. Mohan P. Patil",
        "Mr. Ramkrishna H. Patil",
        "Ms. Pooja Khandar",
        "Ms. Priyanka Vinod Medhe",
        "Mr. Krunal Pawar",
        "Ms. Ashwini A. Kakde",
        "Ms. Mayuri Chandratre",
        "Ms. Shama Pawar",
        "Mr. Pramod B. Gosavi"
    ],
    "Civil Engineering": [
        "Dr. Pankaj R. Punase (HOD)",
        "Dr. Mujahid Husain",
        "Dr. Pravin A. Shirule",
        "Dr. Farooq I. Chavan",
        "Dr. Sonali B. Patil",
        "Mrs. Jyoti R. Mali",
        "Ganesh Sonawane",
        "Ms. Dipika Mali",
        "Ms. Sushma Mahale"
    ]
    # 👉 Add other departments similarly
}

# ================= FORM =================

department = st.selectbox("Department", list(staffByDepartment.keys()))

# ✅ Safe access
faculty_list = staffByDepartment.get(department, [])

name = st.selectbox("Name", faculty_list)

designation = st.selectbox(
    "Designation",
    ["Assistant Professor", "Associate Professor", "Head of the Department"]
)

email = st.text_input("Email")
mobile = st.text_input("Mobile")

from_date = st.date_input("From Date")
to_date = st.date_input("To Date")

leave_type = st.selectbox("Leave Type", ["CL", "LWP", "ML", "EL", "DL", "SP"])

reason = st.text_area("Reason")

alt_staff = st.selectbox("Alternate Staff", faculty_list)

# 🔴 VALIDATION
if alt_staff == name:
    st.warning("Alternate Staff cannot be same as applicant")

# ================= 📊 LEAVE BALANCE =================

if st.button("📊 View My Leave Balance"):

    data = get_leaves()

    if not data:
        st.warning("No leave records found")
    else:
        # Handle old + new DB
        if len(data[0]) == 9:
            df = pd.DataFrame(data, columns=[
                "id","name","department","leave_type",
                "from","to","reason","status","email"
            ])
            df["days"] = 1
        else:
            df = pd.DataFrame(data, columns=[
                "id","name","department","leave_type",
                "from","to","reason","status","email","days"
            ])

        user_df = df[df["name"] == name]

        if user_df.empty:
            st.info("No leave data available")
        else:
            approved_df = user_df[user_df["status"].isin([
                "Approved by HOD",
                "Approved by Principal"
            ])]

            cl_used = approved_df[approved_df["leave_type"] == "CL"]["days"].sum()
            ml_used = approved_df[approved_df["leave_type"] == "ML"]["days"].sum()

            total_cl = 11
            total_ml = 11

            remaining_cl = total_cl - cl_used
            remaining_ml = total_ml - ml_used

            st.subheader("📊 Leave Balance")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("CL Used", cl_used)
                st.metric("CL Remaining", remaining_cl)

            with col2:
                st.metric("ML Used", ml_used)
                st.metric("ML Remaining", remaining_ml)

# ================= SUBMIT =================

if st.button("Submit Leave Application"):

    if not email or not reason:
        st.error("Please fill all required fields")
        logger.warning(f"{name} submitted incomplete form")

    elif alt_staff == name:
        st.error("Applicant and Alternate Staff must be different")
        logger.warning(f"{name} selected same alternate staff")

    elif from_date > to_date:
        st.error("Invalid date range")
        logger.warning(f"{name} selected invalid dates")

    else:
        # ✅ Days calculation
        days = (to_date - from_date).days + 1

        request_id = generate_request_id()

        data = (
            request_id,
            name,
            department,
            leave_type,
            str(from_date),
            str(to_date),
            reason,
            "Pending Approval",
            email,
            days
        )

        insert_leave(data)

        logger.info(f"Leave Submitted | {name} | ReqID: {request_id}")

        st.success("Leave Submitted Successfully ✅")
        st.info(f"Request ID: {request_id}")