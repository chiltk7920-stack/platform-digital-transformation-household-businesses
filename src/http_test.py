import requests

base='http://127.0.0.1:6868'
try:
    r = requests.post(f"{base}/api/auth/login", json={'user_name':'emp_kc1015','password':'58997'}, timeout=5)
    print('login', r.status_code)
    print(r.text)
    token = r.json().get('token') if r.status_code==200 else None
    if token:
        headers={'Authorization': f'Bearer {token}'}
        r2 = requests.get(f"{base}/api/employee/customers/", headers=headers, timeout=5)
        print('get', r2.status_code)
        print(r2.text)
except Exception as e:
    print('ERR', e)
