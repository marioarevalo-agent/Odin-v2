import urllib.request, json

ips = ['186.29.176.151', '186.155.18.95']

for ip in ips:
    print(f'\n=== {ip} ===')
    
    # ipinfo.io
    try:
        req = urllib.request.Request(f'https://ipinfo.io/{ip}/json',
            headers={'User-Agent': 'EIQ/1.0', 'Accept': 'application/json'})
        resp = urllib.request.urlopen(req, timeout=5)
        data = json.loads(resp.read())
        print(f'  ipinfo.io: city={data.get("city")}, region={data.get("region")}, loc={data.get("loc")}, org={data.get("org")}')
    except Exception as e:
        print(f'  ipinfo.io error: {e}')
    
    # ip-api.com
    try:
        req = urllib.request.Request(f'http://ip-api.com/json/{ip}?fields=status,country,regionName,city,lat,lon,isp,zip,timezone',
            headers={'User-Agent': 'EIQ/1.0'})
        resp = urllib.request.urlopen(req, timeout=5)
        data = json.loads(resp.read())
        print(f'  ip-api.com: city={data.get("city")}, region={data.get("regionName")}, lat={data.get("lat")}, lon={data.get("lon")}, zip={data.get("zip")}, isp={data.get("isp")}')
    except Exception as e:
        print(f'  ip-api.com error: {e}')
    
    # ipwhois.app  
    try:
        req = urllib.request.Request(f'https://ipwho.is/{ip}',
            headers={'User-Agent': 'EIQ/1.0'})
        resp = urllib.request.urlopen(req, timeout=5)
        data = json.loads(resp.read())
        print(f'  ipwho.is: city={data.get("city")}, region={data.get("region")}, lat={data.get("latitude")}, lon={data.get("longitude")}, isp={data.get("connection",{}).get("isp")}')
    except Exception as e:
        print(f'  ipwho.is error: {e}')
