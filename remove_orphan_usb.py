with open(r'C:\Users\Usuario\.gemini\antigravity-ide\scratch\Onyx\index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f'Lines before: {len(lines)}')

# Find the orphaned USB block start (line 3915 = index 3914)
# It starts with "        // Global summary bar" after the map section
start_remove = None
end_remove = None

for i, line in enumerate(lines):
    if '// Global summary bar' in line and 'usbHtml' in lines[i+1] if i+1 < len(lines) else False:
        start_remove = i
        print(f'Found orphaned USB start at line {i+1}: {line.strip()[:60]}')
        break

if start_remove is None:
    # Alternative: find after "loadGoogleMapsScript" call
    for i, line in enumerate(lines):
        if 'loadGoogleMapsScript(data.connection_map)' in line:
            # Check next non-empty lines
            for j in range(i+1, min(i+5, len(lines))):
                stripped = lines[j].strip()
                if stripped and stripped != '' and 'Global summary' in stripped:
                    start_remove = j
                    print(f'Found via loadGoogleMapsScript at line {j+1}')
                    break
            if start_remove:
                break

# Find end: "usbPanel.innerHTML = usbHtml;" followed by closing braces and })
if start_remove:
    for i in range(start_remove, min(start_remove + 150, len(lines))):
        if 'usbPanel.innerHTML = usbHtml' in lines[i]:
            # Find the closing brace of the if block
            for j in range(i+1, min(i+5, len(lines))):
                if lines[j].strip() == '}':
                    end_remove = j + 1
                    print(f'Found orphaned USB end at line {j+1}')
                    break
            break

print(f'Removing lines {start_remove+1} to {end_remove}')
if start_remove and end_remove:
    removed_lines = lines[start_remove:end_remove]
    print(f'Removing {len(removed_lines)} lines')
    lines = lines[:start_remove] + lines[end_remove:]
    print(f'Lines after: {len(lines)}')
else:
    print(f'ERROR: Could not determine range. start={start_remove}, end={end_remove}')
    # Debug: show lines around line 3915
    for i in range(3913, 3920):
        print(f'Line {i+1}: {lines[i].strip()[:80]}')

with open(r'C:\Users\Usuario\.gemini\antigravity-ide\scratch\Onyx\index.html', 'w', encoding='utf-8', newline='') as f:
    f.writelines(lines)
print('Saved.')
