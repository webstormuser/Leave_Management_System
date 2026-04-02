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

    if (!emailField.value) {
                emailField.value = name + "@sscoetjalgaon.ac.in";
            }emailField.value = name + "@sscoetjalgaon.ac.in";
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

    // ✅ PROOF VALIDATION
    const proofFile = document.getElementById("proof")?.files[0];

    if ((leaveType === "ML" || leaveType === "DL") && !proofFile) {
        alert("Proof is required for ML / DL ❌");
        return;
    }

    // ✅ USE FORMDATA (IMPORTANT)
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
        credentials: "same-origin",
        body: formData
    })
    .then(res => res.json())
    .then(res => {
        alert("Submitted ID: " + res.request_id);
        location.reload();
    })
    .catch(err => {
        alert("Submission failed ❌");
        console.error(err);
    });
}


// ================= FILTER =================
function filterByMonth() {
    const month = document.getElementById("monthSelect")?.value;
    const year = document.getElementById("yearSelect")?.value;

    const cards = document.querySelectorAll(".record-card");
    let count = 0;

    cards.forEach(card => {
        const fromDate = card.getAttribute("data-from");

        if (!fromDate) {
            card.style.display = "none";
            return;
        }

        const [cardYear, cardMonth] = fromDate.split("-");

        if (
            (month === "" || cardMonth === month) &&
            (year === "" || cardYear === year)
        ) {
            card.style.display = "block";
            count++;
        } else {
            card.style.display = "none";
        }
    });

    document.getElementById("filterResult").innerText =
        count === 0
        ? "No records found ❌"
        : count + " record(s) found ✅";
}


// ================= RESET =================
function resetFilter() {
    document.getElementById("monthSelect").value = "";
    document.getElementById("yearSelect").value = "";

    document.querySelectorAll(".record-card").forEach(card => {
        card.style.display = "block";
    });

    document.getElementById("filterResult").innerText = "";
}


// ================= APPROVE =================
function approveLeave(id) {
    let url = window.location.pathname.includes("principal")
        ? "/principal/approve"
        : "/hod/approve";

    fetch(url, {
        method: "POST",
        credentials: "same-origin",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ id })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        location.reload();
    });
}


// ================= REJECT =================
function rejectLeave(id) {
    let url = window.location.pathname.includes("principal")
        ? "/principal/reject"
        : "/hod/reject";

    fetch(url, {
        method: "POST",
        credentials: "same-origin",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ id })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        location.reload();
    });
}
//==============================
function markProofViewed(leaveId) {

    fetch("/principal/mark_viewed", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ id: leaveId })
    })
    .then(res => res.json())
    .then(data => {

        if (data.status === "ok") {
            let btn = document.getElementById("approveBtn-" + leaveId);
            btn.disabled = false;
            btn.classList.remove("disabled-btn");
        }
    });
}