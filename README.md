

---

# Finance Management System (Backend)
**Candidate:** Sowmya Indurthi  
**Email:** sowmyaindurthi1406@gmail.com  
**Role:** Python Developer Intern Submission  

## 📘 Project Overview
This project is a high-performance, secure backend built with **FastAPI** and **MySQL** designed to manage personal financial ecosystems. Beyond simple data entry, the system serves as a secure vault for financial records, providing automated analytics and enforcing strict **Role-Based Access Control (RBAC)** to ensure data privacy and integrity.

---
## 🛠 Tech Stack & Architecture
The application is built on the principle of **Separation of Concerns**, ensuring the code is modular and easy to scale.

* **Framework:** FastAPI (High-performance Python framework with asynchronous support).
* **Database:** MySQL (Relational persistence layer for structured data).
* **ORM:** SQLAlchemy (Object-Relational Mapping for clean database interactions).
* **Validation:** Pydantic (Strict data schemas to ensure 100% data integrity).
* **Security:** JWT (JSON Web Tokens) with Bcrypt password hashing.
* **Testing:** Pytest (Automated unit testing suite for reliability).

### Folder Structure & Module Responsibilities:
```text
FINANCE_SYSTEM_BACKEND/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/   # API Routes (analytics.py, auth.py, transactions.py)
│   │   └── deps.py          # Dependency injection (Database & Auth sessions)
│   ├── core/                # Configuration and Security settings (config.py)
│   ├── db/                  # Database session management (session.py)
│   ├── models/              # SQLAlchemy Database models (user.py, transaction.py)
│   ├── schemas/             # Pydantic data validation (user.py, transaction.py)
│   ├── services/            # Business logic and Math (transaction_service.py)
│   ├── utils/               # Helper functions and hashing (security.py)
│   ├── __init__.py
│   └── main.py              # Entry point for the FastAPI application
├── tests/                   # Automated Pytest suite
│   ├── test_auth.py         # Registration and Login security tests
│   └── test_transactions.py # RBAC and Transaction logic tests
├── venv/                    # Virtual Environment (Local only)
├── .env                     # Environment variables (Private)
├── README.md                # Project documentation
└── requirements.txt         # Project dependencies list
```

---

## 🛠 Architecture Design & Approach
The application is built on the principle of **Separation of Concerns**. Instead of a monolithic block of code, the system is decomposed into specialized layers:

* **API Layer (`app/api/`):** Acts as the interface, handling HTTP requests and returning standardized JSON responses.
* **Service Layer (`app/services/`):** The "Brain" of the application. All business logic, mathematical calculations for analytics, and permission checks are centralized here.
* **Data Layer (`app/models/` & `app/db/`):** Manages the persistent state of the application using SQLAlchemy ORM.
* **Validation Layer (`app/schemas/`):** Uses Pydantic to ensure that no "bad data" ever reaches the business logic.

### Module Breakdown:
* **`core/`**: Houses global security configurations, JWT secret keys, and environment settings.
* **`utils/`**: Contains reusable helper functions (e.g., password hashing and date formatters).
* **`main.py`**: The entry point that initializes the FastAPI app and includes the modular routers.

---

## 🚀 Key Features & Implementation Logic

### 1. Secure Authentication & User Identity
* **Why:** To ensure financial data is private.
* **Implementation:** Developed a JWT-based authentication system. Passwords are never stored in plain text; they are hashed using **Bcrypt** for industry-standard security.

### 2. Intelligent Financial Analytics
* **Why:** To provide value beyond storage.
* **Implementation:** Created specialized endpoints that process raw transaction data into meaningful summaries including Total Balance, Income-to-Expense ratios, and Category breakdowns.

### 3. Role-Based Access Control (RBAC)
* **Why:** To simulate real-world corporate data hierarchies.
* **Implementation:** * **Viewer:** Read-only access.
    * **Analyst:** Access to advanced insights and filtering.
    * **Admin:** Full authority to manage (Create/Update/Delete) records.

### 4. Optional Enhancements ("Super Dream" Features)
* **CSV Export:** A dedicated route to stream database records directly into an Excel-compatible CSV file.
* **Pagination & Search:** Implemented `skip` and `limit` logic to ensure the API remains fast as the database grows, alongside keyword search for transaction notes.

---
## 🔐 Security & Authorization Flow
### How Credentials Work
I have implemented a **Stateful Security Layer** using JWT. When a user logs in, the server issues a unique, encrypted "Access Token." 

### The "Authorize" Button (Swagger UI)
To make testing easy for evaluators, I have integrated the **OAuth2 Password Flow** into the Swagger UI (`/docs`):
1.  Click the **"Authorize"** padlock button at the top right of the Swagger page.
2.  Enter a registered `username` and `password`.
3.  The browser securely stores the token and automatically attaches it to the `Authorization: Bearer <token>` header for all subsequent API calls.

---

## 👥 User Roles & Permissions
The system identifies three distinct user types, each with specific capabilities:

| Feature | **Viewer** | **Analyst** | **Admin** |
| :--- | :---: | :---: | :---: |
| View Own Transactions | ✅ | ✅ | ✅ |
| Access Financial Analytics | ✅ | ✅ | ✅ |
| Filter & Search Records | ❌ | ✅ | ✅ |
| Create New Transactions | ❌ | ❌ | ✅ |
| Update/Edit Transactions | ❌ | ❌ | ✅ |
| Delete Transactions | ❌ | ❌ | ✅ |
| Export Data to CSV | ✅ | ✅ | ✅ |

---

## 🧪 Automated Testing & Reliability
I have prioritized reliability by implementing a testing suite using **Pytest**.
* **Benefit:** These tests act as a "Security Safety Net." They automatically verify that a **Viewer** cannot delete data and that **Unauthorized Users** are blocked from the system entirely.
* **Validation:** Every input (amount, date, category) is validated by Pydantic. If a user provides invalid data, the system returns a clear `422 Unprocessable Entity` status instead of crashing.

---

## ✅ Technical Self-Evaluation

### 1. Python Proficiency & Code Quality
The code utilizes modern Python 3.x features, including **Type Hinting** for error reduction and **Asynchronous I/O** for high-concurrency performance. Naming conventions follow **PEP 8** to ensure the code is readable and maintainable for team environments.

### 2. Data Handling & Persistence
Utilized **MySQL** for robust relational data management. I designed the schema with indexed foreign keys (linking Transactions to Users) to ensure queries remain efficient and data remains consistent.

### 3. Validation & Reliability
Every endpoint is protected by **Pydantic Schemas**. The system is designed to fail gracefully; if a user provides an invalid amount or an incorrect date, the system returns a clear `422 Unprocessable Entity` status with a descriptive error message, preventing application crashes.

---

## 🧪 Automated Testing Suite
I have prioritized reliability by implementing a testing suite using **Pytest**. This provides a "Safety Net" for the application.

* **Tests Implemented:** 1.  **Identity Verification:** Ensures the registration and login flows work.
    2.  **Security Blocking:** Confirms that incorrect passwords result in `401 Unauthorized`.
    3.  **RBAC Enforcement:** Specifically tests that a **Viewer** is strictly forbidden (`403`) from deleting transactions.
    4.  **Header Verification:** Ensures the CSV Export route returns the correct media type.
* **Benefit:** These tests allow for continuous integration; any future changes to the code can be verified instantly to ensure security rules haven't been "broken."

---

## ⚙️ Setup & Installation

### 1. Environment Setup
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
```

### 2. Database Configuration
Create a `.env` file in the root directory:
```env
DATABASE_URL=mysql+pymysql://USER:PASSWORD@localhost:3306/finance_db
SECRET_KEY=your_secure_random_string
ALGORITHM=HS256
```

### 3. Execution & Testing
* **Run Server:** `uvicorn app.main:app --reload`
* **Run Tests:** `python -m pytest`
* **API Docs:** Access `http://127.0.0.1:8000/docs` for the interactive Swagger UI.

---

## 📝 Important Notes & Assumptions
* **Data Ownership:** Each transaction is hard-linked to a specific `user_id`. No user can access or modify another user’s records.
* **Destructive Actions:** I assumed a strict security policy where only **Admins** can delete records to prevent accidental data loss in a financial context.
* **Scalability:** The architecture is "Cloud-Ready," meaning it can be easily containerized (Docker) or scaled across multiple servers.

---
**© 2026 Sowmya Indurthi | Python Developer Assignment Submission**