import streamlit as st
from utils.logger import get_logger
from config.config import HOD_CREDENTIALS   # ✅ NEW

# ✅ Initialize logger
logger = get_logger("login")

st.title("Leave Management System")

# ✅ Initialize session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

# 🔹 LOGIN FORM
if not st.session_state.logged_in:

    role = st.selectbox("Select Role", ["Faculty", "HOD", "Principal"])

    username = st.text_input("Email / Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        # ================= FACULTY (UNCHANGED) =================
        if role == "Faculty" and username == "faculty" and password == "123":
            st.session_state.logged_in = True
            st.session_state.role = "Faculty"
            st.session_state.user = username

            logger.info(f"LOGIN SUCCESS | {username} | Faculty")
            st.success("Login Successful")

        # ================= HOD (UPDATED ✅) =================
        elif role == "HOD":

            if username in HOD_CREDENTIALS and password == HOD_CREDENTIALS[username]:

                st.session_state.logged_in = True
                st.session_state.role = "HOD"
                st.session_state.user = username

                logger.info(f"HOD LOGIN SUCCESS | {username}")
                st.success("Login Successful")

            else:
                st.error("Invalid HOD credentials ❌")
                logger.warning(f"HOD LOGIN FAILED | {username}")

        # ================= PRINCIPAL (UNCHANGED) =================
        elif role == "Principal" and username == "principal" and password == "123":
            st.session_state.logged_in = True
            st.session_state.role = "Principal"
            st.session_state.user = username

            logger.info(f"LOGIN SUCCESS | {username} | Principal")
            st.success("Login Successful")

        else:
            st.error("Invalid Credentials ❌")
            logger.warning(f"LOGIN FAILED | {username} | Role: {role}")


# 🔹 REDIRECT AFTER LOGIN
if st.session_state.logged_in:

    st.success(f"Logged in as {st.session_state.role}")

    logger.info(f"REDIRECT | {st.session_state.user} → {st.session_state.role}")

    if st.session_state.role == "Faculty":
        st.switch_page("pages/1_Faculty.py")

    elif st.session_state.role == "HOD":
        st.switch_page("pages/2_HOD.py")

    elif st.session_state.role == "Principal":
        st.switch_page("pages/3_Principal.py")