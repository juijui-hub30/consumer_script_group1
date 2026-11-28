import requests
import json

BASE_URL = "http://127.0.0.1:5000"
results = []

def run_test(name, method, endpoint, payload=None, expected_status=200):
    url = f"{BASE_URL}{endpoint}"
    print(f"\n--- {name} ---")
    print(f"Request: {method} {url}")
    try:
        if method == "PUT":
            resp = requests.put(url, json=payload)
        passed = (resp.status_code == expected_status)
        label = "PASS" if passed else "FAIL"
        print(f"Status: {resp.status_code} (Expected: {expected_status}) [{label}]")
        try:
            body = resp.json()
        except:
            body = {"raw": resp.text}
        print(f"Response: {json.dumps(body)[:200]}")
        results.append({"method": method, "endpoint": endpoint, "status": resp.status_code, "expected": expected_status, "passed": passed})
        return resp.status_code, body
    except requests.exceptions.ConnectionError:
        print("[ERROR] Cannot connect. Is Group 6's app.py running?")
        results.append({"method": method, "endpoint": endpoint, "status": "N/A", "expected": expected_status, "passed": False})
        return None, None

# First, create a record to update
print("--- Creating a test record to update ---")
create_resp = requests.post(f"{BASE_URL}/post/attendance", json={
    "student_id": "2024-0099",
    "student_name": "Test, Update User",
    "date": "2026-11-27",
    "event": "PUT Test Event",
    "status": "present"
})
create_body = create_resp.json()
record_id = create_body["attendance"]["id"] if create_resp.status_code == 201 else None

if record_id:
    # Test 1: Update Status (200)
    run_test("Update Status to Late", "PUT", f"/attendance/{record_id}", payload={"status": "late"}, expected_status=200)

    # Test 2: Update with Invalid Status (400 - Error Handling)
    run_test("Update with Invalid Status (400)", "PUT", f"/attendance/{record_id}", payload={"status": "excused"}, expected_status=400)

    # Test 3: Update Non-Existent Record (404 - Error Handling)
    run_test("Update Non-Existent Record (404)", "PUT", "/attendance/99999", payload={"status": "late"}, expected_status=404)
else:
    print("[SKIP] Could not create record for PUT tests")

print("\n---PUT Tests Complete ---")
