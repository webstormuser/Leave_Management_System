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
window.onload = function () {

    const deptSelect = document.getElementById("department");

    if (deptSelect) {
        deptSelect.innerHTML = `<option value="">-- Select Department --</option>`;

        Object.keys(staffByDepartment).forEach(dept => {
            deptSelect.add(new Option(dept, dept));
        });
    }
};


// ================= UPDATE FACULTY =================
function updateFaculty() {

    const dept = document.getElementById("department")?.value;
    const nameSelect = document.getElementById("name");
    const altStaff = document.getElementById("altStaff");

    if (!nameSelect || !altStaff) return;

    nameSelect.innerHTML = "";
    altStaff.innerHTML = "";

    if (!staffByDepartment[dept]) return;

    nameSelect.add(new Option("-- Select Name --", ""));
    altStaff.add(new Option("-- Select Alternate Staff --", ""));

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

    if (!department || !name) {
        alert("Please select Department and Name ❌");
        return;
    }

    if (name === altStaff) {
        alert("Alternate staff cannot be same ❌");
        return;
    }

    const data = {
        department,
        name,
        designation: document.getElementById("designation")?.value,
        email: document.getElementById("email")?.value,
        mobile: document.getElementById("mobile")?.value,
        fromDate: document.getElementById("fromDate")?.value,
        toDate: document.getElementById("toDate")?.value,
        leaveType: document.getElementById("leaveType")?.value,
        reason: document.getElementById("reason")?.value,
        altStaff
    };

    fetch("/submit", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(res => {
        alert("Submitted ID: " + res.request_id);
        location.reload();
    });
}


// ================= MONTH FILTER (FIXED) =================
function filterByMonth() {

    const month = document.getElementById("monthSelect")?.value;
    const year = document.getElementById("yearSelect")?.value;

    if (!month || !year) {
        alert("Select month and year");
        return;
    }

    let count = 0;
    const selected = year + "-" + month;

    // ✅ ONLY FILTER RECORDS
    document.querySelectorAll(".record-card").forEach(card => {

        let fromDate = card.getAttribute("data-from");
        let toDate = card.getAttribute("data-to");

        if (!fromDate || !toDate) {
            card.style.display = "block";
            count++;
            return;
        }

        let f = fromDate.split("-");
        let t = toDate.split("-");

        let fromVal = f[0] + "-" + f[1].padStart(2, "0");
        let toVal = t[0] + "-" + t[1].padStart(2, "0");

        if (selected >= fromVal && selected <= toVal) {
            card.style.display = "block";
            count++;
        } else {
            card.style.display = "none";
        }

    });

    document.getElementById("filterResult").innerText =
        "Showing " + count + " record(s)";
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
function approveLeave(id, btn) {

    fetch("/hod/approve", {
        method: "POST",
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
function rejectLeave(id, btn) {

    fetch("/hod/reject", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ id })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        location.reload();
    });
}