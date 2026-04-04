from flask import Flask, render_template, session, request, redirect, jsonify
from database.db import init_db, get_connection
from database.leave_db import get_leaves, get_leave_by_id
from services.approval_service import handle_approval
from config.config import HOD_CREDENTIALS, HOD_DEPARTMENT, PRINCIPAL
import os
from werkzeug.utils import secure_filename
from datetime import datetime

from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = "secret123"

# ================= INIT DB =================
init_db()

# ================= CONFIG =================
UPLOAD_FOLDER = "static/uploads"


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

        if role == "Faculty" and username == "faculty" and password == "123":
            session["role"] = "Faculty"
            session["user"] = username
            return redirect("/faculty")

        elif role == "HOD":
            if username in HOD_CREDENTIALS and password == HOD_CREDENTIALS[username]:
                session["role"] = "HOD"
                session["user"] = username
                return redirect("/hod")
            else:
                return render_template("login.html", error="Invalid HOD credentials ❌")

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
        data = request.form
        file = request.files.get("proof")

        from_date = datetime.strptime(data['fromDate'], "%Y-%m-%d")
        to_date = datetime.strptime(data['toDate'], "%Y-%m-%d")

        if from_date > to_date:
            return jsonify({"status": "error", "message": "Invalid date range"})

        days = (to_date - from_date).days + 1
        leave_id = str(uuid.uuid4())[:8]

        # ================= FILE HANDLING =================
        # ================= FILE HANDLING =================
    proof_path = None

    if file and file.filename != "":
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        # 🔹 Original filename
        original_name = secure_filename(file.filename)

        # 🔹 Split extension
        name, ext = os.path.splitext(original_name)

        # 🔹 Clean faculty name
        faculty_name = data.get("name", "faculty")
        faculty_name = faculty_name.replace("(HOD)", "")
        faculty_name = faculty_name.replace("Dr.", "").replace("Mr.", "").replace("Ms.", "").replace("Mrs.", "")
        faculty_name = faculty_name.strip().replace(" ", "_").replace(".", "")

        # 🔹 Leave type
        leave_type = data.get("leaveType", "Leave")

        # 🔹 Timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # 🔹 FINAL NAME (ONLY THIS NAME USED)
        final_name = f"{faculty_name}_{leave_type}_{timestamp}{ext}"

        # 🔹 Save file
        file_path = os.path.join(UPLOAD_FOLDER, final_name)
        file.save(file_path)

        # 🔹 Store RELATIVE path (IMPORTANT)
        proof_path = f"static/uploads/{final_name}"

        # ================= DB INSERT =================
        conn = get_connection()
        c = conn.cursor()

        c.execute("""
        INSERT INTO leaves (
            id, name, department, designation, email, mobile,
            leave_type, from_date, to_date, days,
            reason, alt_staff, status, proof
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            leave_id,
            data.get("name"),
            data.get("department"),
            data.get("designation"),
            data.get("email"),
            data.get("mobile"),
            data.get("leaveType"),
            data.get("fromDate"),
            data.get("toDate"),
            days,
            data.get("reason"),
            data.get("altStaff"),
            "Pending Approval",
            proof_path
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

        leave = dict(row)

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

        leave = dict(row)

        total += 1

        if leave["status"] in ["Pending Approval", "Pending Principal Approval"]:
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


# ================= PRINCIPAL APPROVAL =================
@app.route("/principal/approve", methods=["POST"])
def principal_approve():

    if session.get("role") != "Principal":
        return jsonify({"message": "Unauthorized"}), 403

    leave_id = request.json.get("id")
    leave = get_leave_by_id(leave_id)

    if not leave:
        return jsonify({"message": "Leave not found ❌"}), 404

    leave = dict(leave)

    leave_type = leave.get("leave_type")
    proof = leave.get("proof")

    # ✅ FIX BOOLEAN ISSUE
    proof_viewed = int(leave.get("proof_viewed") or 0)

    if leave_type in ["ML", "DL"]:

        if not proof:
            return jsonify({"message": "Proof required ❌"}), 400

        if not proof_viewed:
            return jsonify({"message": "Please view proof before approval ❌"}), 400

    msg = handle_approval("PRINCIPAL_APPROVE", leave)

    return jsonify({"message": msg})


# ================= MARK PROOF VIEWED =================
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


# ================= PRINCIPAL REJECT =================
@app.route("/principal/reject", methods=["POST"])
def principal_reject():

    if session.get("role") != "Principal":
        return jsonify({"message": "Unauthorized"}), 403

    leave_id = request.json.get("id")
    leave = get_leave_by_id(leave_id)

    if not leave:
        return jsonify({"message": "Leave not found ❌"})

    leave = dict(leave)

    msg = handle_approval("PRINCIPAL_REJECT", leave)

    return jsonify({"message": msg})


# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)