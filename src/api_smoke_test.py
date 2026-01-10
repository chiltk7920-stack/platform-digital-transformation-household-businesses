import os
import requests
import json

BASE = os.environ.get('API_BASE', 'http://127.0.0.1:6868')
TIMEOUT = 5

def login(user_name, password):
    url = f"{BASE}/api/auth/login"
    try:
        r = requests.post(url, json={'user_name': user_name, 'password': password}, timeout=TIMEOUT)
    except Exception as e:
        print(f"[ERROR] login {user_name}: {e}")
        return None
    print(f"login {user_name}: {r.status_code}")
    if r.status_code != 200:
        print(r.text)
        return None
    data = r.json()
    return data.get('token')

def call_get(path, token=None):
    url = f"{BASE}{path}"
    headers = {}
    if token:
        headers['Authorization'] = f"Bearer {token}"
    try:
        r = requests.get(url, headers=headers, timeout=TIMEOUT)
    except Exception as e:
        print(f"[ERROR] GET {path}: {e}")
        return None, None
    try:
        body = r.json()
    except Exception:
        body = r.text
    return r.status_code, body

def pretty(obj):
    try:
        print(json.dumps(obj, indent=2, ensure_ascii=False))
    except Exception:
        print(obj)

def run_smoke():
    print('--- Owner (kc1015) login and calls ---')
    owner_token = login('kc1015', '58997')
    code, body = call_get('/api/owner/employees/', owner_token)
    print('/api/owner/employees/ ->', code)
    pretty(body)

    code, body = call_get('/api/owner/sellers/', owner_token)
    print('/api/owner/sellers/ ->', code)
    pretty(body)

    print('\n--- Employee (emp_kc1015) login and calls ---')
    emp_token = login('emp_kc1015', '58997')
    code, body = call_get('/api/employee/customers/', emp_token)
    print('/api/employee/customers/ ->', code)
    pretty(body)

    # Also test employee cannot call owner endpoints
    code, body = call_get('/api/owner/employees/', emp_token)
    print('/api/owner/employees/ (as employee) ->', code)
    pretty(body)

if __name__ == '__main__':
    run_smoke()
