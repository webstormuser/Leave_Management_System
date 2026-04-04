// ================= DATA =================
const staffByDepartment = {
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
    ],
    "Chemical Engineering": [
        "Dr. Sandeep A. Thakur (HOD)",
        "Ms. Manasi Shashikant Nhalade",
        "Mrs. Sarika S. Pawar",
        "Mr. Vijay P. Sangore"
    ],
    "Electrical Engineering": [
        "Mr. M. Mujtahid Ansari (HOD)",
        "Mr. Vijay S. Pawar",
        "Dr. Suhas M. Shembekar",
        "Mr. Muqueem M. Khan",
        "Mr. Tanveer Husain",
        "Mr. Vijay A. Shinde",
        "Ms. Shaikh Uzma Sabir",
        "Dr. R. R. Karhe"
    ],
    "Mechanical Engineering": [
        "Mr. Navneet K. Patil",
        "Dr. Krishna S. Shrivastava",
        "Dr. Prajitsen G. Damle (HOD)",
        "Dr. Devendra B. Sadaphale",
        "Dr. Pradeep M. Solanki",
        "Dr. Ajay R. Bhardwaj",
        "Dr. Dipak C. Talele"
    ],
    "First Year Engineering": [
        "Dr. Sandip S. Patil (HOD)",
        "Dr. Kiran S. Patil",
        "Dr. Sunita S. Patil",
        "Mr. Y. K. Chitte",
        "Dr. Prashant N. Ulhe",
        "Dr. A. C. Wani",
        "Ms. Priti R. Sharma",
        "Dr. Chandrashekhar U. Nikam",
        "Dr. Pravin D. Patil",
        "Mr. Mahendra B. Patil",
        "Ms. Meera V. Kulkarni",
        "Ms. Dhanashree S. Tayade",
        "Mr. Ujwalsingh T. Patil",
        "Ms. Tanuja Y. Chouhan",
        "Ms. Jayshree R. Tayade",
        "Mr. Sachin Bhalerao",
        "Dr. Devendra B. Sadaphale",
        "Ms. Siddhi Neve",
        "Ms. Anjali Jain"
    ]
};


// ================= INIT =================
document.addEventListener("DOMContentLoaded", function () {
    const deptSelect = document.getElementById("department");

    if (deptSelect && deptSelect.options.length <= 1) {
        Object.keys(staffByDepartment).forEach(dept => {
            deptSelect.add(new Option(dept, dept));
        });
    }
});


// ================= UPDATE FACULTY =================
function updateFaculty() {
    const dept = document.getElementById("department")?.value;
    const nameSelect = document.getElementById("name");
    const altStaff = document.getElementById("altStaff");

    if (!nameSelect || !altStaff) return;

    nameSelect.innerHTML = `<option value="">-- Select Name --</option>`;
    altStaff.innerHTML = `<option value="">-- Select Alternate Staff --</option>`;

    if (!staffByDepartment[dept]) return;

    staffByDepartment[dept].forEach(name => {
        nameSelect.add(new Option(name, name));
        altStaff.add(new Option(name, name));
    });
}


// ================= EMAIL AUTO =================
function autoFillEmail() {
    let name = document.getElementById("name")?.value;
    let emailField = document.getElementById("email");

    if (!name || !emailField) return;

    name = name.replace(/\(HOD\)/g, "")
               .replace(/Dr\.|Mr\.|Ms\.|Mrs\./g, "")
               .trim()
               .toLowerCase()
               .replace(/\s+/g, ".");

    emailField.value = name + "@sscoetjalgaon.ac.in";
}


// ================= SUBMIT =================
function submitLeave() {

    const department = document.getElementById("department")?.value;
    const name = document.getElementById("name")?.value;
    const altStaff = document.getElementById("altStaff")?.value;
    const leaveType = document.getElementById("leaveType")?.value;

    if (!department || !name) {
        alert("Please select Department and Name ❌");
        return;
    }

    if (name === altStaff) {
        alert("Alternate staff cannot be same ❌");
        return;
    }

    const fromDate = document.getElementById("fromDate")?.value;
    const toDate = document.getElementById("toDate")?.value;

    if (!fromDate || !toDate) {
        alert("Please select dates ❌");
        return;
    }

    const proofFile = document.getElementById("proof")?.files[0];

    if ((leaveType === "ML" || leaveType === "DL") && !proofFile) {
        alert("Proof is required for ML / DL ❌");
        return;
    }

    const formData = new FormData();

    formData.append("department", department);
    formData.append("name", name);
    formData.append("designation", document.getElementById("designation")?.value);
    formData.append("email", document.getElementById("email")?.value);
    formData.append("mobile", document.getElementById("mobile")?.value);
    formData.append("fromDate", fromDate);
    formData.append("toDate", toDate);
    formData.append("leaveType", leaveType);
    formData.append("reason", document.getElementById("reason")?.value);
    formData.append("altStaff", altStaff);

    if (proofFile) {
        formData.append("proof", proofFile);
    }

    fetch("/submit", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(res => {
        if (res.status === "success") {
            alert("Submitted ID: " + res.request_id);
            location.reload();
        } else {
            alert(res.message || "Submission failed ❌");
        }
    })
    .catch(err => {
        alert("Submission failed ❌");
        console.error(err);
    });
}


// ================= APPROVE =================
function approveLeave(id) {

    let url = window.location.pathname.includes("principal")
        ? "/principal/approve"
        : "/hod/approve";

    fetch(url, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ id })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message || "Done");
        location.reload();
    })
    .catch(err => console.error(err));
}


// ================= REJECT =================
function rejectLeave(id) {

    let url = window.location.pathname.includes("principal")
        ? "/principal/reject"
        : "/hod/reject";

    fetch(url, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ id })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message || "Rejected");
        location.reload();
    })
    .catch(err => console.error(err));
}


// ================= MARK PROOF VIEWED =================
function markProofViewed(leaveId) {

    fetch("/principal/mark_viewed", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ id: leaveId })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "ok") {
            let btn = document.getElementById("approveBtn-" + leaveId);
            if (btn) {
                btn.disabled = false;
                btn.classList.remove("disabled-btn");
                btn.innerText = "✅ Approve";
            }
        }
    })
    .catch(err => console.error(err));
}