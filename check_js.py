import re
f=open(r'C:\Users\Usuario\.gemini\antigravity-ide\scratch\Onyx\index.html','r',encoding='utf-8')
t=f.read()
f.close()

scripts = re.findall(r'<script[^>]*>(.*?)</script>', t, re.DOTALL)
print(f'Found {len(scripts)} script blocks')
for i, s in enumerate(scripts):
    opens = s.count('{')
    closes = s.count('}')
    parens_o = s.count('(')
    parens_c = s.count(')')
    print(f'Script {i+1}: {len(s)} chars, braces {{ {opens} vs }} {closes} (delta {opens-closes}), parens {parens_o} vs {parens_c}')
    if abs(opens-closes) > 5:
        print(f'  *** WARNING: Brace mismatch! ***')

# Also check if the map JS functions have syntax issues
if 'initGoogleMapSection' in t:
    idx = t.find('initGoogleMapSection')
    snippet = t[idx:idx+200]
    print(f'\ninitGoogleMapSection found at char {idx}')
    print(repr(snippet[:100]))

# Check showApp function
if 'function showApp' in t:
    idx = t.find('function showApp')
    snippet = t[idx:idx+300]
    print(f'\nshowApp found at char {idx}')
    # Count braces in just this function (first 500 chars)
    b_open = snippet[:500].count('{')
    b_close = snippet[:500].count('}')
    print(f'showApp first 500 chars braces: {{ {b_open} vs }} {b_close}')
