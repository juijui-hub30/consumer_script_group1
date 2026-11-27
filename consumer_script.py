import requests
import json

# ============================================================
# GROUP 1 - CONSUMER SCRIPT
# Target: Group 6 (Campus Event Attendance API)
# Repository: https://github.com/lovendinjademontero12/API_Creation_Group6
# ============================================================

BASE_URL = "http://127.0.0.1:5000"

# Track results for the summary report
results = []

def log(method, endpoint, status, expected, passed):
    """Store each test result."""
    results.append({
        "method": method,
        "endpoint": endpoint,
        "status": status,
        "expected": expected,
        "passed": passed
    })

def run_test(name, method, endpoint, payload=None, expected_status=200):
    """Send a request and check if the response matches expectations."""
    url = f"{BASE_URL}{endpoint}"
    print(f"\n--- {name} ---")
    print(f"Request: {method} {url}")

    try:
        if method == "GET":
            resp = requests.get(url)
        elif method == "POST":
            resp = requests.post(url, json=payload)
        elif method == "PUT":
            resp = requests.put(url, json=payload)
        elif method == "DELETE":
            resp = requests.delete(url)

        # Try to parse JSON response
        try:
            body = resp.json()
        except Exception:
            body = {"raw": resp.text}

        passed = (resp.status_code == expected_status)
        label = "PASS" if passed else "FAIL"

        print(f"Status Code: {resp.status_code} (Expected: {expected_status}) [{label}]")
        print(f"Response: {json.dumps(body)[:200]}")

        log(method, endpoint, resp.status_code, expected_status, passed)
        return resp.status_code, body

    except requests.exceptions.ConnectionError:
        print("[ERROR] Cannot connect. Is Group 6's app.py running?")
        log(method, endpoint, "N/A", expected_status, False)
        return None, None


# ================= TEST SEQUENCE =================

print("=" * 50)
print("GROUP 1 CONSUMER SCRIPT")
print("Testing Group 6 Campus Event Attendance API")
print("=" * 50)

# 1. Health Check
run_test("Health Check", "GET", "/", expected_status=200)

# 2. GET all attendance records
run_test("Get All Attendance", "GET", "/attendance", expected_status=200)

# 3. GET by student ID (valid)
run_test("Get Student by ID (Valid)", "GET", "/attendance/2024-0001", expected_status=200)

# 4. ERROR HANDLING: GET by student ID (invalid -> 404)
run_test("Get Student by ID (Invalid - Error Handling)",
         "GET", "/attendance/9999-FAKE", expected_status=404)

# 5. POST new attendance record (valid -> 201)
new_record = {
    "student_id": "2024-0050",
    "student_name": "Dela Cruz, Juan P.",
    "date": "2026-11-27",
    "event": "ICT Hackathon",
    "status": "late"
}
code, body = run_test("Add New Attendance",
                      "POST", "/post/attendance",
                      payload=new_record, expected_status=201)

# Save the new record's ID for update/delete tests
record_id = body["attendance"]["id"] if code == 201 else None

# 6. PUT update status (valid -> 200)
if record_id:
    run_test("Update Status to Present",
             "PUT", f"/attendance/{record_id}",
             payload={"status": "present"}, expected_status=200)

# 7. ERROR HANDLING: PUT with invalid status (-> 400)
if record_id:
    run_test("Update with Invalid Status (Error Handling)",
             "PUT", f"/attendance/{record_id}",
             payload={"status": "excused"}, expected_status=400)

# 8. ERROR HANDLING: PUT on non-existent record (-> 404)
run_test("Update Non-Existent Record (Error Handling)",
         "PUT", "/attendance/99999",
         payload={"status": "late"}, expected_status=404)

# 9. DELETE record (valid -> 200)
if record_id:
    run_test("Delete Attendance Record",
             "DELETE", f"/attendance/{record_id}",
             expected_status=200)

# 10. ERROR HANDLING: DELETE already-deleted record (-> 404)
if record_id:
    run_test("Delete Already-Deleted Record (Error Handling)",
             "DELETE", f"/attendance/{record_id}",
             expected_status=404)


# ================= SUMMARY REPORT =================

print("\n" + "=" * 50)
print("SUMMARY REPORT")
print("=" * 50)

total = len(results)
passed_count = sum(1 for r in results if r["passed"])
failed_count = total - passed_count

print(f"{'Method':<8} {'Endpoint':<25} {'Got':<6} {'Expected':<10} {'Result'}")
print("-" * 70)

for r in results:
    verdict = "PASS" if r["passed"] else "FAIL"
    print(f"{r['method']:<8} {r['endpoint']:<25} {str(r['status']):<6} {str(r['expected']):<10} {verdict}")

print("-" * 70)
print(f"TOTAL TESTS : {total}")
print(f"PASSED      : {passed_count}")
print(f"FAILED      : {failed_count}")
print(f"SUCCESS RATE: {(passed_count / total * 100):.1f}%")
print("=" * 50)
