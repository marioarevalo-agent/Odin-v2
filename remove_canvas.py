with open(r'C:\Users\Usuario\.gemini\antigravity-ide\scratch\Onyx\index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f'Lines before: {len(lines)}')

# Find and remove the old canvas/SVG block
# These are the remnant lines after our new div was inserted
start_remove = None
end_remove = None

for i, line in enumerate(lines):
    stripped = line.strip()
    if '<!-- Canvas for world map -->' in stripped and start_remove is None:
        start_remove = i
        print(f'Found canvas start at line {i+1}')
    if start_remove is not None and 'id="secMapDeviceCards"' in stripped and i > start_remove:
        # Find the closing divs after this
        for j in range(i, min(i+5, len(lines))):
            if '</div>' in lines[j] and 'secMapDeviceCards' not in lines[j]:
                end_remove = j + 1
                print(f'Found canvas end at line {j+1}')
                break
        break

if start_remove is not None and end_remove is not None:
    removed = lines[start_remove:end_remove]
    print(f'Removing {end_remove - start_remove} lines:')
    for l in removed:
        print(f'  REMOVING: {l.strip()[:60]}')
    lines = lines[:start_remove] + lines[end_remove:]
    print(f'Lines after: {len(lines)}')
else:
    print(f'WARNING: start={start_remove}, end={end_remove}')
    # Show context around canvas
    for i, l in enumerate(lines):
        if 'secWorldCanvas' in l or 'Canvas for world' in l:
            print(f'  Line {i+1}: {l.strip()[:80]}')

with open(r'C:\Users\Usuario\.gemini\antigravity-ide\scratch\Onyx\index.html', 'w', encoding='utf-8', newline='') as f:
    f.writelines(lines)
print('Saved.')
