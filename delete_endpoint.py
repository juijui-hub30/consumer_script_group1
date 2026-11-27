import requests
import json

BASE_URL = "http://127.0.0.1:5000"
results = []

def run_test(name, method, endpoint, expected_status=200):
    url = f"{BASE_URL}{endpoint}"
    print(f"\n--- {name} ---")
    print(f"Request: {method} {url}")
    try:
        if method == "DELETE":
            resp = requests.delete(url)
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

# First, create a record to delete
print("--- Creating a test record to delete ---")
create_resp = requests.post(f"{BASE_URL}/post/attendance", json={
    "student_id": "2024-0088",
    "student_name": "Test, Delete User",
    "date": "2026-11-27",
    "event": "DELETE Test Event",
    "status": "present"
})
create_body = create_resp.json()
record_id = create_body["attendance"]["id"] if create_resp.status_code == 201 else None

if record_id:
    # Test 1: Delete Valid Record (200)
    run_test("Delete Valid Record", "DELETE", f"/attendance/{record_id}", expected_status=200)

    # Test 2: Delete Already-Deleted Record (404 - Error Handling)
    run_test("Delete Already-Deleted Record (404)", "DELETE", f"/attendance/{record_id}", expected_status=404)

    # Test 3: Delete Non-Existent Record (404 - Error Handling)
    run_test("Delete Non-Existent Record (404)", "DELETE", "/attendance/99999", expected_status=404)
else:
    print("[SKIP] Could not create record for DELETE tests")

print("\n---DELETE Tests Complete ---")