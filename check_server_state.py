import urllib.request, json, hashlib

# Login
login_data = json.dumps({"email": "admin@proy-anla-poc.local", "password": "Admin2026!"}).encode()
login_req = urllib.request.Request(
    'https://proy-anla-poc-175647544738.us-central1.run.app/api/auth/login',
    data=login_data, headers={'Content-Type': 'application/json'})
login_resp = urllib.request.urlopen(login_req, timeout=10)
cookie = login_resp.getheader('Set-Cookie').split(';')[0]

# Check server version
req = urllib.request.Request(
    'https://proy-anla-poc-175647544738.us-central1.run.app/api/agent-version',
    headers={'Cookie': cookie})
resp = urllib.request.urlopen(req, timeout=10)
ver = json.loads(resp.read())
print("Agent version info from server:")
for k, v in ver.items():
    print(f"  {k}: {v}")

# Check available API endpoints to find what changed
endpoints = ['/api/seguridad', '/api/kpis', '/api/devices', '/api/productivity']
for ep in endpoints:
    try:
        req = urllib.request.Request(
            f'https://proy-anla-poc-175647544738.us-central1.run.app{ep}',
            headers={'Cookie': cookie})
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read())
        if isinstance(data, dict):
            keys = list(data.keys())
            print(f"\n{ep} -> keys: {keys}")
        elif isinstance(data, list):
            print(f"\n{ep} -> list of {len(data)} items")
            if data:
                print(f"  first item keys: {list(data[0].keys()) if isinstance(data[0], dict) else 'not dict'}")
    except Exception as e:
        print(f"\n{ep} -> Error: {e}")
