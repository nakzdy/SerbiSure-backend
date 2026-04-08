import subprocess
import json

def run_http_command(cmd_args):
    print(f"\n=======================================================")
    print(f"Running: http {' '.join(cmd_args)}")
    print(f"=======================================================")
    try:
        result = subprocess.run(
            ['venv\\Scripts\\http'] + cmd_args,
            capture_output=True,
            text=True,
            shell=True
        )
        print(f"{result.stdout}")
        if result.stderr:
            print(f"Stderr:\n{result.stderr}")
        return result.stdout
    except Exception as e:
        print(f"Failed to run command: {e}")

# 1. Login and get token
out = run_http_command([
    'POST', 'http://127.0.0.1:8000/api/auth/login/',
    'email=homeowner@test.com', 'password=pass1234'
])

token = None
try:
    idx = out.find('{')
    if idx != -1:
        data = json.loads(out[idx:])
        token = data.get('data', {}).get('token')
except:
    pass

print(f"\n[Extracted Token: {token}]")

# 2. Get all services (public)
run_http_command(['GET', 'http://127.0.0.1:8000/api/services/'])

if token:
    # 3. Create a booking (authenticated)
    out = run_http_command([
        'POST', 'http://127.0.0.1:8000/api/bookings/',
        f'Authorization:Token {token}',
        'service=1', 'scheduled_date=2026-05-10'
    ])
    
    # 4. Get bookings for logged-in user
    run_http_command([
        'GET', 'http://127.0.0.1:8000/api/bookings/',
        f'Authorization:Token {token}'
    ])
