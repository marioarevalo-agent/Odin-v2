import urllib.request, json

# Login
login_data = json.dumps({"email": "admin@proy-anla-poc.local", "password": "Admin2026!"}).encode()
login_req = urllib.request.Request(
    'https://proy-anla-poc-175647544738.us-central1.run.app/api/auth/login',
    data=login_data,
    headers={'Content-Type': 'application/json'}
)
login_resp = urllib.request.urlopen(login_req, timeout=10)
cookie = login_resp.getheader('Set-Cookie').split(';')[0]

# Fetch device details
req = urllib.request.Request(
    'https://proy-anla-poc-175647544738.us-central1.run.app/api/devices',
    headers={'Cookie': cookie}
)
resp = urllib.request.urlopen(req, timeout=10)
devices = json.loads(resp.read())

print(f'=== {len(devices)} devices ===\n')
for d in devices:
    did = d.get('device_id', '?')
    print(f'--- {did} ---')
    # Print all keys and values (first 200 chars)
    for k, v in d.items():
        vs = str(v)
        if len(vs) > 200:
            vs = vs[:200] + '...'
        print(f'  {k}: {vs}')
    print()

# Also check per-device endpoint
for d in devices[:3]:
    did = d.get('device_id', '')
    if not did:
        continue
    try:
        req2 = urllib.request.Request(
            f'https://proy-anla-poc-175647544738.us-central1.run.app/api/devices/{did}',
            headers={'Cookie': cookie}
        )
        resp2 = urllib.request.urlopen(req2, timeout=10)
        detail = json.loads(resp2.read())
        lm = detail.get('latest_metrics', {})
        if lm:
            print(f'\n=== Latest metrics for {did} ===')
            for k in ['device_id', 'device_type', 'hostname', 'os_info', 'local_ip', 'public_ip', 
                       'network_info', 'timezone', 'wifi_ssid', 'location', 'geo_location',
                       'system_info', 'username']:
                v = lm.get(k)
                if v:
                    vs = str(v)[:200]
                    print(f'  {k}: {vs}')
    except Exception as e:
        print(f'Error fetching {did}: {e}')
