# 📋 Leave Management System

A **Flask APP -based Leave Management System** designed for academic institutions to manage faculty leave applications efficiently through a structured approval workflow.

---

## 🚀 Features

### 👨‍🏫 Faculty

* Apply for leave (CL, ML, EL, DL, etc.)
* Select department and alternate staff
* View leave balance (CL & ML)
* Track request status

### 🧑‍💼 HOD (Head of Department)

* View department-wise leave requests
* Approve / Reject leave applications
* Forward selected leaves to Principal
* Dashboard with analytics and KPIs

### 🏛️ Principal

* Final approval authority
* View HOD-approved requests
* Approve / Reject leaves
* Dashboard with summary metrics

---

## 🔄 Workflow

Faculty → Submit Leave
⬇
HOD → Approve / Reject
⬇
Principal → Final Approval
⬇
Email Notification to Applicant

---

## 📊 Dashboard Features

* 📈 KPI Cards (Total, Approved, Pending, Rejected)
* 📉 Analytics Charts (leave type, department-wise)
* 💎 Glassmorphism UI (modern design)
* 📂 Sidebar Navigation with role-based access

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **Backend:** Python
* **Database:** SQLite
* **Visualization:** Pandas, Streamlit Charts
* **Email Service:** Yagmail (SMTP)
* **Logging:** Custom Logger

---

## 📁 Project Structure

```
leave_management_system/
│
├── app.py
├── pages/
│   ├── 1_Faculty.py
│   ├── 2_HOD.py
│   └── 3_Principal.py
│
├── database/
│   ├── db.py
│   ├── leave_db.py
│   └── faculty_db.py
│
├── services/
│   ├── approval_service.py
│   └── email_service.py
│
├── utils/
│   ├── logger.py
│   ├── style.py
│   └── sidebar.py
│
├── analytics/
│   └── charts.py
│
├── assets/
│   └── styles.css
│
└── config/
    └── config.py
```

---

## 🔐 Authentication

* Role-based login:

  * Faculty
  * HOD (email-based credentials)
  * Principal
* Session-based access control

---

## 📬 Email Notifications

* Sent to:

  * HOD for approval
  * Principal for final approval
  * Applicant for status updates
* Async (non-blocking) email system

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/your-repo.git
cd leave_management_system
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run Application

```bash
streamlit run app.py
```

---

## 🌐 Deployment

This project can be deployed on:

* Streamlit Cloud
* Local Server
* College Intranet

---

## 📌 Future Enhancements

* Leave balance auto-deduction
* Role-based analytics filters
* Mobile responsive UI
* Export reports (PDF/Excel)
* AI-based leave prediction (advanced)

---

## 👨‍💻 Author

Developed by **Ashwini Kakde**
Assistant Professor, Computer Department

---

## ⭐ Acknowledgment

This project is developed for academic and institutional use to streamline leave approval processes.

---

## 📜 License

This project is for educational purposes.
