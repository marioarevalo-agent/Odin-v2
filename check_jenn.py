import urllib.request, json

# Login
login_data = json.dumps({"email": "admin@proy-anla-poc.local", "password": "Admin2026!"}).encode()
login_req = urllib.request.Request(
    'https://proy-anla-poc-175647544738.us-central1.run.app/api/auth/login',
    data=login_data, headers={'Content-Type': 'application/json'})
login_resp = urllib.request.urlopen(login_req, timeout=10)
cookie = login_resp.getheader('Set-Cookie').split(';')[0]

# Check agent version on server
req = urllib.request.Request(
    'https://proy-anla-poc-175647544738.us-central1.run.app/api/agent-version',
    headers={'Cookie': cookie})
resp = urllib.request.urlopen(req, timeout=10)
ver = json.loads(resp.read())
print("Server agent version:", ver)

# Check Jenn's device details
req2 = urllib.request.Request(
    'https://proy-anla-poc-175647544738.us-central1.run.app/api/devices',
    headers={'Cookie': cookie})
resp2 = urllib.request.urlopen(req2, timeout=10)
devices = json.loads(resp2.read())

for d in devices:
    if 'jenn' in d.get('device_id', '').lower():
        print(f"\n=== Jennifer's device: {d['device_id']} ===")
        print(f"  Status: {d['status']}")
        print(f"  Last sync: {d['last_sync']}")
        print(f"  CPU: {d['cpu_usage']}%, RAM: {d['ram_usage']}%")
        print(f"  Battery: {d.get('battery_percent')}% ({d.get('battery_status')})")
        print(f"  Last IP: {d.get('last_ip')}")
        
        # Check event logs for errors
        events_raw = d.get('event_logs', '')
        if isinstance(events_raw, str) and events_raw:
            try:
                events = json.loads(events_raw)
                print(f"\n  Event logs ({len(events)} entries):")
                for e in events[:10]:
                    sev = e.get('severity', '?')
                    src = e.get('source', '?')
                    msg = e.get('message', '')[:100]
                    print(f"    [{sev}] {src}: {msg}")
            except:
                print(f"  Event logs (raw, first 200): {events_raw[:200]}")
        
        # Check top processes
        tp_raw = d.get('top_processes', '')
        if isinstance(tp_raw, str) and tp_raw:
            try:
                tp = json.loads(tp_raw)
                print(f"\n  Top processes:")
                for p in tp[:5]:
                    print(f"    {p.get('name','?'):30s} CPU:{p.get('cpu',0):6.1f}% MEM:{p.get('mem',0):5.1f}%")
            except:
                pass
        elif isinstance(tp_raw, list):
            print(f"\n  Top processes:")
            for p in tp_raw[:5]:
                print(f"    {p.get('name','?'):30s} CPU:{p.get('cpu',0):6.1f}% MEM:{p.get('mem',0):5.1f}%")
        
        # Check cause
        cr = d.get('cause_root', '')
        cp = d.get('cause_process', '')
        if cr:
            print(f"\n  Root cause: {cr}")
            print(f"  Cause process: {cp}")
