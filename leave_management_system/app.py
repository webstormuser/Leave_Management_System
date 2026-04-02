from flask import Flask, render_template, session, request, redirect, jsonify
from database.db import init_db, get_connection
from database.leave_db import get_leaves, get_leave_by_id
from services.approval_service import handle_approval
from config.config import HOD_CREDENTIALS, HOD_DEPARTMENT, PRINCIPAL

from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = "secret123"

# ================= INIT DB =================
init_db()


# ================= HOME =================
@app.route("/")
def home():
    return render_template("index.html")


# ================= LOGIN =================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        role = request.form["role"]
        username = request.form["username"]
        password = request.form["password"]

        # ===== FACULTY =====
        if role == "Faculty" and username == "faculty" and password == "123":
            session["role"] = "Faculty"
            session["user"] = username
            return redirect("/faculty")

        # ===== HOD =====
        elif role == "HOD":
            if username in HOD_CREDENTIALS and password == HOD_CREDENTIALS[username]:
                session["role"] = "HOD"
                session["user"] = username
                return redirect("/hod")
            else:
                return render_template("login.html", error="Invalid HOD credentials ❌")

        # ===== PRINCIPAL =====
        elif role == "Principal":
            if username == PRINCIPAL and password == HOD_CREDENTIALS.get(username):
                session["role"] = "Principal"
                session["user"] = username
                return redirect("/principal")
            else:
                return render_template("login.html", error="Invalid Principal credentials ❌")

    return render_template("login.html")


# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ================= FACULTY =================
@app.route("/faculty")
def faculty():

    if session.get("role") != "Faculty":
        return redirect("/login")

    return render_template("faculty.html", user=session.get("user"))


# ================= SUBMIT LEAVE =================
@app.route("/submit", methods=["POST"])
def submit_leave():

    if session.get("role") != "Faculty":
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

    try:
        data = request.get_json()

        from_date = datetime.strptime(data['fromDate'], "%Y-%m-%d")
        to_date = datetime.strptime(data['toDate'], "%Y-%m-%d")

        if from_date > to_date:
            return jsonify({"status": "error", "message": "Invalid date range"})

        days = (to_date - from_date).days + 1
        leave_id = str(uuid.uuid4())[:8]

        conn = get_connection()
        c = conn.cursor()

        c.execute("""
        INSERT INTO leaves (
            id, name, department, designation, email, mobile,
            leave_type, from_date, to_date, days,
            reason, alt_staff, status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            leave_id,
            data.get("name"),
            data.get("department"),
            data.get("designation"),
            data.get("email"),
            data.get("mobile"),
            data.get("leaveType"),
            data.get("fromDate")[:10],
            data.get("toDate")[:10],
            days,
            data.get("reason"),
            data.get("altStaff"),
            "Pending Approval"
        ))

        conn.commit()
        conn.close()

        return jsonify({
            "status": "success",
            "request_id": leave_id
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"status": "error", "message": str(e)}), 500


# ================= HOD =================
@app.route("/hod")
def hod():

    if session.get("role") != "HOD":
        return redirect("/login")

    user = session.get("user")
    dept = HOD_DEPARTMENT.get(user)

    data = get_leaves()

    pending_leaves = []
    all_leaves = []

    total = approved = rejected = pending = 0

    for row in data:

        leave = {
        "id": row["id"],
        "name": row["name"],
        "department": row["department"],
        "leave_type": row["leave_type"],
        "from_date": row["from_date"],
        "to_date": row["to_date"],
        "reason": row["reason"],
        "status": row["status"],
        "email": row["email"]
        }

        # ✅ Flexible match (fixes 0 records issue)
        if dept and leave["department"] and dept.lower() in leave["department"].lower():

            total += 1
            all_leaves.append(leave)

            if leave["status"] == "Pending Approval":
                pending += 1
                pending_leaves.append(leave)

            elif "Approved" in leave["status"]:
                approved += 1

            elif "Rejected" in leave["status"]:
                rejected += 1

    return render_template(
        "hod.html",
        user=user,
        department=dept,
        leaves=pending_leaves,
        all_leaves=all_leaves,
        total=total,
        approved=approved,
        rejected=rejected,
        pending=pending
    )


# ================= PRINCIPAL =================
@app.route("/principal")
def principal():

    if session.get("role") != "Principal":
        return redirect("/login")

    data = get_leaves()

    leaves = []
    total = approved = rejected = pending = 0

    for row in data:

        leave = {
            "id": row["id"],
            "name": row["name"],
            "department": row["department"],
            "leave_type": row["leave_type"],
            "from_date": row["from_date"],
            "to_date": row["to_date"],
            "reason": row["reason"],
            "status": row["status"],
            "email": row["email"]
        }

        total += 1

        if leave["status"] == "Pending Principal Approval":
            pending += 1
            leaves.append(leave)

        elif "Approved" in leave["status"]:
            approved += 1

        elif "Rejected" in leave["status"]:
            rejected += 1

    return render_template(
        "principal.html",
        user=session.get("user"),
        leaves=leaves,
        total=total,
        approved=approved,
        rejected=rejected,
        pending=pending
    )


# ================= HOD APPROVAL =================
@app.route("/hod/approve", methods=["POST"])
def hod_approve():

    if session.get("role") != "HOD":
        return jsonify({"message": "Unauthorized"}), 403

    leave_id = request.json.get("id")
    leave = get_leave_by_id(leave_id)

    if not leave:
        return jsonify({"message": "Leave not found ❌"})

    leave = dict(leave)

    leave["from_date"] = leave.get("from_date") or leave.get("from")
    leave["to_date"] = leave.get("to_date") or leave.get("to")

    msg = handle_approval("HOD_APPROVE", leave)
    return jsonify({"message": msg})


@app.route("/hod/reject", methods=["POST"])
def hod_reject():

    if session.get("role") != "HOD":
        return jsonify({"message": "Unauthorized"}), 403

    leave_id = request.json.get("id")
    leave = get_leave_by_id(leave_id)

    if not leave:
        return jsonify({"message": "Leave not found ❌"})

    leave = dict(leave)

    leave["from_date"] = leave.get("from_date") or leave.get("from")
    leave["to_date"] = leave.get("to_date") or leave.get("to")

    msg = handle_approval("HOD_REJECT", leave)
    return jsonify({"message": msg})


# ================= PRINCIPAL APPROVAL =================
@app.route("/principal/approve", methods=["POST"])
def principal_approve():

    # ================= AUTH =================
    if session.get("role") != "Principal":
        return jsonify({"message": "Unauthorized"}), 403

    leave_id = request.json.get("id")
    leave = get_leave_by_id(leave_id)

    # ================= VALIDATION =================
    if not leave:
        return jsonify({"message": "Leave not found ❌"}), 404

    # ✅ Convert to dict FIRST (IMPORTANT)
    leave = dict(leave)

    leave_type = leave.get("leave_type")
    proof = leave.get("proof")
    proof_viewed = leave.get("proof_viewed")

    # ================= ML / DL RULE =================
    if leave_type in ["ML", "DL"]:

        # ❌ No proof uploaded
        if not proof:
            return jsonify({"message": "Proof required ❌"}), 400

        # ❌ Proof not viewed
        if not proof_viewed:
            return jsonify({"message": "Please view proof before approval ❌"}), 400

    # ================= DATE FIX =================
    leave["from_date"] = leave.get("from_date") or leave.get("from")
    leave["to_date"] = leave.get("to_date") or leave.get("to")

    # ================= FINAL APPROVAL =================
    msg = handle_approval("PRINCIPAL_APPROVE", leave)

    return jsonify({"message": msg})

@app.route("/principal/mark_viewed", methods=["POST"])
def mark_viewed():

    if session.get("role") != "Principal":
        return jsonify({"status": "unauthorized"}), 403

    leave_id = request.json.get("id")

    conn = get_connection()
    c = conn.cursor()

    c.execute("UPDATE leaves SET proof_viewed = 1 WHERE id = ?", (leave_id,))
    conn.commit()
    conn.close()

    return jsonify({"status": "ok"})

@app.route("/principal/reject", methods=["POST"])
def principal_reject():

    if session.get("role") != "Principal":
        return jsonify({"message": "Unauthorized"}), 403

    leave_id = request.json.get("id")
    leave = get_leave_by_id(leave_id)

    if not leave:
        return jsonify({"message": "Leave not found ❌"})

    leave = dict(leave)

    leave["from_date"] = leave.get("from_date") or leave.get("from")
    leave["to_date"] = leave.get("to_date") or leave.get("to")

    msg = handle_approval("PRINCIPAL_REJECT", leave)
    return jsonify({"message": msg})


# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)