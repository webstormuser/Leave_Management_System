import streamlit as st
import pandas as pd
from database.leave_db import get_leaves
from utils.logger import get_logger

logger = get_logger("analytics")


def show_analytics():

    st.title("📊 Advanced Leave Analytics")

    data = get_leaves()

    if not data:
        st.warning("No data available")
        return

    # ================= HANDLE OLD + NEW DB =================
    if len(data[0]) == 9:
        df = pd.DataFrame(data, columns=[
            "id", "name", "department", "leave_type",
            "from", "to", "reason", "status", "email"
        ])
        df["days"] = 1  # fallback for old records
    else:
        df = pd.DataFrame(data, columns=[
            "id", "name", "department", "leave_type",
            "from", "to", "reason", "status", "email", "days"
        ])

    # ================= FILTER APPROVED =================
    approved_df = df[df["status"].isin([
        "Approved by HOD",
        "Approved by Principal"
    ])]

    if approved_df.empty:
        st.warning("No approved leave data available")
        return

    # ================= DEPARTMENT CHART =================
    st.subheader("📌 Leaves by Department (Days)")
    dept_days = approved_df.groupby("department")["days"].sum()
    st.bar_chart(dept_days)

    # ================= FACULTY CHART =================
    st.subheader("👨‍🏫 Leaves by Faculty (Days)")
    faculty_days = approved_df.groupby("name")["days"].sum()
    st.bar_chart(faculty_days)

    # ================= MONTHLY TREND =================
    st.subheader("📈 Monthly Leave Trend")

    try:
        approved_df["from"] = pd.to_datetime(approved_df["from"])
        monthly = approved_df.groupby(approved_df["from"].dt.month)["days"].sum()
        st.line_chart(monthly)
    except Exception as e:
        st.warning("Date conversion issue in monthly chart")

    # ================= LEAVE BALANCE =================
    st.subheader("📋 Leave Balance (CL / ML in Days)")

    leave_df = approved_df[approved_df["leave_type"].isin(["CL", "ML"])]

    if leave_df.empty:
        st.info("No CL/ML data available")
        return

    pivot = leave_df.pivot_table(
        index="name",
        columns="leave_type",
        values="days",
        aggfunc="sum",
        fill_value=0
    )

    # Ensure both columns exist
    if "CL" not in pivot.columns:
        pivot["CL"] = 0
    if "ML" not in pivot.columns:
        pivot["ML"] = 0

    # Leave limits
    pivot["Total CL"] = 11
    pivot["Used CL"] = pivot["CL"]
    pivot["Remaining CL"] = pivot["Total CL"] - pivot["Used CL"]

    pivot["Total ML"] = 11
    pivot["Used ML"] = pivot["ML"]
    pivot["Remaining ML"] = pivot["Total ML"] - pivot["Used ML"]

    final_df = pivot[[
        "Total CL", "Used CL", "Remaining CL",
        "Total ML", "Used ML", "Remaining ML"
    ]]

    st.dataframe(final_df)

    logger.info("Analytics displayed successfully")