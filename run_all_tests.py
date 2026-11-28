import requests
import json

BASE_URL = "http://127.0.0.1:5000"
results = []

def run_test(name, method, endpoint, payload=None, expected_status=200):
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "GET":
            resp = requests.get(url)
        elif method == "POST":
            resp = requests.post(url, json=payload)
        elif method == "PUT":
            resp = requests.put(url, json=payload)
        elif method == "DELETE":
            resp = requests.delete(url)
        passed = (resp.status_code == expected_status)
        label = "PASS" if passed else "FAIL"
        try:
            body = resp.json()
        except:
            body = {"raw": resp.text}
        results.append({"method": method, "endpoint": endpoint, "status": resp.status_code, "expected": expected_status, "passed": passed})
        return resp.status_code, body
    except requests.exceptions.ConnectionError:
        print("[ERROR] Cannot connect to API")
        return None, None

print("=" * 60)
print("GROUP 1 - FULL CONSUMER SCRIPT")
print("Testing Group 6 Campus Event Attendance API")
print("=" * 60)

# ALL TESTS
run_test("Health Check", "GET", "/", expected_status=200)
run_test("Get All", "GET", "/attendance", expected_status=200)
run_test("Get Student (Valid)", "GET", "/attendance/2024-0001", expected_status=200)
run_test("Get Student (Invalid)", "GET", "/attendance/9999-FAKE", expected_status=404)

new_record = {"student_id": "2024-0077", "student_name": "Test, Full User", "date": "2026-11-27", "event": "Full Test", "status": "late"}
code, body = run_test("Add Record", "POST", "/post/attendance", payload=new_record, expected_status=201)
rid = body["attendance"]["id"] if code == 201 else None

if rid:
    run_test("Update Status", "PUT", f"/attendance/{rid}", payload={"status": "present"}, expected_status=200)
    run_test("Update Bad Status", "PUT", f"/attendance/{rid}", payload={"status": "excused"}, expected_status=400)
    run_test("Update Missing ID", "PUT", "/attendance/99999", payload={"status": "late"}, expected_status=404)
    run_test("Delete Record", "DELETE", f"/attendance/{rid}", expected_status=200)
    run_test("Delete Again", "DELETE", f"/attendance/{rid}", expected_status=404)

# SUMMARY REPORT
print("\n" + "=" * 60)
print("SUMMARY REPORT")
print("=" * 60)
total = len(results)
passed = sum(1 for r in results if r["passed"])
failed = total - passed

print(f"{'Method':<8} {'Endpoint':<25} {'Got':<6} {'Expected':<10} {'Result'}")
print("-" * 65)
for r in results:
    print(f"{r['method']:<8} {r['endpoint']:<25} {str(r['status']):<6} {str(r['expected']):<10} {'PASS' if r['passed'] else 'FAIL'}")
print("-" * 65)
print(f"TOTAL     : {total}")
print(f"PASSED    : {passed}")
print(f"FAILED    : {failed}")
print(f"SUCCESS   : {(passed/total*100):.1f}%")
print("=" * 60)
