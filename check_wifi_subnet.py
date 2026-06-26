import urllib.request, json

login_data = json.dumps({"email": "admin@proy-anla-poc.local", "password": "Admin2026!"}).encode()
login_req = urllib.request.Request(
    'https://proy-anla-poc-175647544738.us-central1.run.app/api/auth/login',
    data=login_data, headers={'Content-Type': 'application/json'})
login_resp = urllib.request.urlopen(login_req, timeout=10)
cookie = login_resp.getheader('Set-Cookie').split(';')[0]

# Fetch devices to get network info
req = urllib.request.Request(
    'https://proy-anla-poc-175647544738.us-central1.run.app/api/devices',
    headers={'Cookie': cookie})
resp = urllib.request.urlopen(req, timeout=10)
devices = json.loads(resp.read())

for d in devices:
    did = d.get('device_id', '?')
    net_raw = d.get('network_info', '')
    if isinstance(net_raw, str) and net_raw:
        try:
            net = json.loads(net_raw)
        except:
            net = {}
    elif isinstance(net_raw, dict):
        net = net_raw
    else:
        net = {}
    
    wifi = net.get('wifi_ssid', 'N/A')
    local_ip = ''
    for iface in net.get('interfaces', []):
        if iface.get('type') == 'WiFi':
            local_ip = iface.get('ip', '')
            break
    subnet = '.'.join(local_ip.split('.')[:3]) if local_ip else 'none'
    print(f'{did:40s} wifi={wifi:25s} local_ip={local_ip:18s} subnet={subnet}')
