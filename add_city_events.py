import re

with open(r'C:\Users\Usuario\.gemini\antigravity-ide\scratch\Onyx\server.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find events.append blocks that are inside the connection_map loop
# (between "# CPU alerts" and the end of the device loop)
# We need to add "city": current_city to each events.append

# Pattern: events.append({...}) without "city" key, inside the per-device loop
# We'll add "city": current_city right before the closing })

# Find the region between "# CPU alerts" and the next major section
start_marker = '# CPU alerts'
start_idx = content.find(start_marker)
print(f'Found CPU alerts at char {start_idx}')

# Count events.append calls in the section
section = content[start_idx:start_idx+3000]
appends = [m.start() for m in re.finditer(r'events\.append\(', section)]
print(f'Found {len(appends)} events.append calls in section')

# Replace each events.append that doesn't have "city" - add it before closing })\n
# We need to be careful to only add within the right scope
# Strategy: after "category": "xxx"}) add , "city": current_city
count = 0
result = content[:start_idx]
remaining = content[start_idx:]

# Replace pattern: 'category": "xxx"})' -> 'category": "xxx", "city": current_city})'
pattern = r'("category":\s*"[^"]+"\})\)'
def add_city(m):
    global count
    inner = m.group(1)
    if '"city"' not in inner:
        count += 1
        return inner[:-1] + ', "city": current_city})'
    return m.group(0)

# Only apply within the first 3000 chars of remaining (within the device loop)
chunk = remaining[:3000]
rest = remaining[3000:]
chunk_new = re.sub(pattern, add_city, chunk)
result += chunk_new + rest

print(f'Added city to {count} events.append calls')

with open(r'C:\Users\Usuario\.gemini\antigravity-ide\scratch\Onyx\server.py', 'w', encoding='utf-8', newline='') as f:
    f.write(result)
print('Saved.')
