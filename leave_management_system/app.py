import streamlit as st
from database.db import init_db
from utils.style import load_css   # ✅ ADD THIS

# ✅ Initialize DB
init_db()

# ✅ Load CSS (VERY IMPORTANT)
load_css()

# ✅ Page config
st.set_page_config(
    page_title="Leave Management System",
    page_icon="📋",
    layout="wide"
)

# ✅ PREMIUM HEADER (STEP 4)
st.markdown("""
<h1>📋 Leave Management System</h1>
<p style='text-align:center; font-size:18px;'>
Smart Leave Tracking Dashboard
</p>
""", unsafe_allow_html=True)

# ✅ GLASS CARD (STEP 2)
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

st.info("👉 Please select 'login' from the sidebar to continue")

# ✅ Session info
if st.session_state.get("logged_in"):
    st.success(f"Logged in as {st.session_state.get('role')}")
else:
    st.warning("You are not logged in")

st.markdown('</div>', unsafe_allow_html=True)