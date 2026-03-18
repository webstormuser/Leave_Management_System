import streamlit as st
import pandas as pd
from utils.logger import get_logger
from utils.style import load_css
from database.leave_db import get_leaves
from services.approval_service import handle_approval
from analytics.charts import show_analytics

# ✅ Load CSS
load_css()

# ✅ Logger
logger = get_logger("principal")

# ================= KPI FUNCTION =================
def kpi_card(title, value, css_class):
    st.markdown(
        f"""
        <div class="kpi-card {css_class}">
            <div>{title}</div>
            <div style="font-size:28px;">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# 🔐 ACCESS CONTROL
if st.session_state.get("role") != "Principal":
    st.error("Unauthorized ❌")
    logger.warning("Unauthorized access attempt to Principal Dashboard")
    st.stop()

# ================= HEADER =================
st.markdown("""
<h1>🏛️ Principal Dashboard</h1>
<p style='text-align:center;'>Final Leave Approval System</p>
""", unsafe_allow_html=True)

# 🔴 LOGOUT
col_top1, col_top2 = st.columns([8, 1])
with col_top2:
    if st.button("Logout"):
        logger.info(f"{st.session_state.get('user')} logged out from Principal")
        st.session_state.clear()
        st.switch_page("pages/login.py")

# 📊 Analytics Button
if st.button("📊 View Analytics"):
    show_analytics()

st.divider()

# ================= LOAD DATA =================

data = get_leaves()

if not data:
    st.warning("No leave data available")
    st.stop()

# ✅ Handle both DB formats
if len(data[0]) == 9:
    df = pd.DataFrame(data, columns=[
        "id","name","department","leave_type",
        "from","to","reason","status","email"
    ])
else:
    df = pd.DataFrame(data, columns=[
        "id","name","department","leave_type",
        "from","to","reason","status","email","days"
    ])

logger.info(f"Principal {st.session_state.get('user')} accessed dashboard")

# ================= KPI =================

pending = df[df["status"] == "Pending Principal Approval"]
approved = df[df["status"] == "Approved by Principal"]
rejected = df[df["status"] == "Rejected by Principal"]

total = len(df)

col1, col2, col3, col4 = st.columns(4)

with col1:
    kpi_card("Total Requests", total, "kpi-total")

with col2:
    kpi_card("Final Approved", len(approved), "kpi-approved")

with col3:
    kpi_card("Final Rejected", len(rejected), "kpi-rejected")

with col4:
    kpi_card("Pending", len(pending), "kpi-pending")

st.divider()

# ================= PENDING APPROVAL =================

st.subheader("🕒 Pending Principal Approval")

if pending.empty:
    st.success("No pending requests ✅")
else:
    for _, row in pending.iterrows():

        leave = row.to_dict()

        # 🔥 GLASS CARD
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        st.write(f"### Request ID: {leave['id']}")
        st.write("👤 Name:", leave["name"])
        st.write("🏢 Department:", leave["department"])
        st.write("📄 Leave Type:", leave["leave_type"])
        st.write("📅 Duration:", leave["from"], "to", leave["to"])
        st.write("📝 Reason:", leave["reason"])

        col1, col2 = st.columns(2)

        # ✅ APPROVE
        if col1.button("✅ Approve", key=f"pa_{leave['id']}"):
            msg = handle_approval("PRINCIPAL_APPROVE", leave)
            logger.info(msg)
            st.success(msg)
            st.rerun()

        # ❌ REJECT
        if col2.button("❌ Reject", key=f"pr_{leave['id']}"):
            msg = handle_approval("PRINCIPAL_REJECT", leave)
            logger.warning(msg)
            st.error(msg)
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)