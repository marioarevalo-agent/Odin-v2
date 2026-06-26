import re

f=open(r'C:\Users\Usuario\.gemini\antigravity-ide\scratch\Onyx\index.html','r',encoding='utf-8')
t=f.read()
f.close()

# Extract main script block
scripts = re.findall(r'<script[^>]*>(.*?)</script>', t, re.DOTALL)
script = scripts[0]

# Find the Google Maps JS section and check its brace balance
gmap_start = script.find('// ── Google Maps Rendering ──')
gmap_end = script.find('// Device cards overlay', gmap_start) + 500
gmap_section = script[gmap_start:gmap_end+200]

opens = gmap_section.count('{')
closes = gmap_section.count('}')
print(f'Google Maps section: {{ {opens} vs }} {closes} (delta {opens-closes})')

# Find the loadGoogleMapsScript function end
load_start = script.find('function loadGoogleMapsScript')
load_snippet = script[load_start:load_start+800]
opens2 = load_snippet.count('{')
closes2 = load_snippet.count('}')
print(f'loadGoogleMapsScript: {{ {opens2} vs }} {closes2}')
print(repr(load_snippet[-200:]))

# Find what comes right after the map JS section
after_map = script.find('// Device cards overlay', gmap_start)
print(f'\nContext around device cards overlay (char {after_map}):')
print(repr(script[after_map:after_map+500]))
