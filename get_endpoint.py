import requests
import json

BASE_URL = "http://127.0.0.1:5000"
results = []

def run_test(name, method, endpoint, expected_status=200):
    url = f"{BASE_URL}{endpoint}"
    print(f"\n--- {name} ---")
    print(f"Request: {method} {url}")
    try:
        resp = requests.get(url)
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

# Test 1: Health Check
run_test("Health Check", "GET", "/", expected_status=200)

# Test 2: Get All Attendance
run_test("Get All Attendance", "GET", "/attendance", expected_status=200)

# Test 3: Get by Student ID (Valid)
run_test("Get Student by ID (Valid)", "GET", "/attendance/2024-0001", expected_status=200)

# Test 4: Get by Student ID (Invalid - Error Handling)
run_test("Get Student by ID (Invalid - 404)", "GET", "/attendance/9999-FAKE", expected_status=404)

print("\n---GET Tests Complete ---")