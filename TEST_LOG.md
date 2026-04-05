

---

### Create file: `TEST_LOG.md`
**Copy and paste this text:**

# System Verification & Terminal Execution Log
**Candidate:** Sowmya Indurthi  
**Date:** April 5, 2026

This document provides proof of system stability and functional verification through actual terminal outputs captured during the testing phase.

## 1. Server Initialization & Swagger Access
The following logs confirm that the FastAPI server started correctly and that the documentation endpoints (`/docs` and `/openapi.json`) were accessible.

**Terminal Trace:**
```text
INFO: Started server process [16000]
INFO: Waiting for application startup.
INFO: Application startup complete.
INFO: 127.0.0.1 - "GET / HTTP/1.1" 200 OK
INFO: 127.0.0.1 - "GET /docs HTTP/1.1" 200 OK
INFO: 127.0.0.1 - "GET /openapi.json HTTP/1.1" 200 OK
```
*Note: I observed a trapped `AttributeError` regarding the bcrypt version. This is a known compatibility warning between Passlib and newer bcrypt versions in Python 3.7 environments, but as shown below, it did not prevent successful user registration or login.*

---

## 2. End-to-End Functional Testing
I performed a sequential test of the core business requirements. Each status code below validates a specific logic layer.

### Phase 1: Authentication (RBAC Setup)
I created three users to verify the Role-Based Access Control logic.
* **POST /api/v1/auth/register** -> `201 Created` (x3 users created)
* **POST /api/v1/auth/login** -> `200 OK` (Admin login successful)

### Phase 2: Transaction & Analytics Logic
I posted three records (1 Income, 2 Expenses) to test the calculation engine.
* **POST /api/v1/transactions/** -> `201 Created` (Records persisted)
* **GET /api/v1/analytics/summary** -> `200 OK` (Math verified)

### Phase 3: Security & Authorization Handling
This trace shows the system correctly handling different security scenarios:
1. **Unauthorized Access:** Blocked an unauthenticated request.
2. **Success:** Authorized a valid request for transaction history.
3. **Forbidden (RBAC):** Blocked a non-Admin user from deleting a record.
4. **Not Found:** Correctly handled a request for a non-existent transaction ID.

**Verified Terminal Logs:**
```text
INFO: 127.0.0.1 - "GET /api/v1/transactions/?skip=0&limit=10 HTTP/1.1" 401 Unauthorized
INFO: 127.0.0.1 - "GET /api/v1/transactions/?skip=0&limit=10 HTTP/1.1" 200 OK
INFO: 127.0.0.1 - "DELETE /api/v1/transactions/5 HTTP/1.1" 403 Forbidden
INFO: 127.0.0.1 - "DELETE /api/v1/transactions/5 HTTP/1.1" 404 Not Found
```

---

## 3. Automated Test Execution
Finally, I ran the `pytest` suite to ensure no regressions were introduced during the logic updates.

```text
============================= test session starts =============================
platform win32 -- Python 3.7.4, pytest-7.4.4
tests\test_auth.py ..                                                    [ 50%]
tests\test_transactions.py ..                                             [100%]
======================== 4 passed, 4 warnings in 3.82s ========================
```

## Final Conclusion
The terminal logs confirm that the system handles **Success (200/201)**, **Security (401/403)**, and **Edge Cases (404)** exactly as intended. The application is robust and ready for evaluation.

---


