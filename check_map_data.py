import urllib.request, json

# Login first
login_data = json.dumps({"email": "admin@proy-anla-poc.local", "password": "Admin2026!"}).encode()
login_req = urllib.request.Request(
    'https://proy-anla-poc-175647544738.us-central1.run.app/api/auth/login',
    data=login_data,
    headers={'Content-Type': 'application/json'}
)
login_resp = urllib.request.urlopen(login_req, timeout=10)
# Get cookie
cookie = login_resp.getheader('Set-Cookie')
print(f'Cookie: {cookie[:60]}...')

# Now fetch seguridad with cookie
req = urllib.request.Request(
    'https://proy-anla-poc-175647544738.us-central1.run.app/api/seguridad',
    headers={'Cookie': cookie.split(';')[0] if cookie else ''}
)
resp = urllib.request.urlopen(req, timeout=10)
data = json.loads(resp.read())

cmap = data.get('connection_map', [])
print(f'\nDevices in connection_map: {len(cmap)}')
for d in cmap:
    name = d.get('name', '?')
    ip = d.get('ip', 'N/A')
    lat = d.get('lat', 0)
    lon = d.get('lon', 0)
    city = d.get('city', '?')
    country = d.get('country', '?')
    status = d.get('status', '?')
    isp = d.get('isp', '?')
    print(f'  {name:20s} IP={ip:18s} lat={lat:8.4f} lon={lon:9.4f} city={city:15s} country={country:10s} status={status} isp={isp}')
