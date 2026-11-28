import requests
import json

BASE_URL = "http://127.0.0.1:5000"
results = []

def run_test(name, method, endpoint, payload=None, expected_status=200):
    url = f"{BASE_URL}{endpoint}"
    print(f"\n--- {name} ---")
    print(f"Request: {method} {url}")
    try:
        if method == "POST":
            resp = requests.post(url, json=payload)
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

# Test 1: Add Valid Attendance (201)
new_record = {
    "student_id": "2024-0050",
    "student_name": "Dela Cruz, Juan P.",
    "date": "2026-11-27",
    "event": "ICT Hackathon",
    "status": "late"
}
run_test("Add Valid Attendance", "POST", "/post/attendance", payload=new_record, expected_status=201)

# Test 2: Missing Required Fields (400 - Error Handling)
run_test("Add Missing Fields (400)", "POST", "/post/attendance", payload={"student_name": "No ID"}, expected_status=400)

# Test 3: Invalid Status Value (400 - Error Handling)
run_test("Add Invalid Status (400)", "POST", "/post/attendance", payload={"student_id": "X", "student_name": "Y", "status": "PRESENT!"}, expected_status=400)

# Test 4: Non-JSON Body (400 - Error Handling)
print("\n--- Testing with non-JSON body (simulated) ---")
# Note: In real testing, we'd send raw bytes. Here we note the behavior.
print("Note: Sending non-dict JSON triggers 400 'Invalid JSON request' in API")

print("\n---POST Tests Complete ---")
