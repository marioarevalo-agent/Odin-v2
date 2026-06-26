with open(r'C:\Users\Usuario\.gemini\antigravity-ide\scratch\Onyx\index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f'Lines before: {len(lines)}')

# Find the old Google Maps code that's left over
start_remove = None
end_remove = None

for i, line in enumerate(lines):
    if 'function initGoogleMapSection(devices)' in line:
        start_remove = i
        print(f'Found old initGoogleMapSection at line {i+1}')
        break

if start_remove is not None:
    # Find where the old loadGoogleMapsScript ends  
    for i in range(start_remove, min(start_remove + 200, len(lines))):
        if 'function loadGoogleMapsScript(devices)' in lines[i]:
            print(f'Found loadGoogleMapsScript at line {i+1}')
        if 'loadGoogleMapsScript(data.connection_map)' in lines[i]:
            print(f'Found old loadGoogleMapsScript call at line {i+1}')
            # Find next closing braces
            for j in range(i, min(i+5, len(lines))):
                if lines[j].strip() == '}':
                    end_remove = j + 1
                    break
            break

if start_remove is not None and end_remove is not None:
    # Also scan back to see if there's duplicate device cards
    for i in range(start_remove, end_remove):
        if 'secMapDeviceCards' in lines[i]:
            print(f'  Also removing duplicate DeviceCards at line {i+1}')
    
    print(f'Removing lines {start_remove+1} to {end_remove}')
    lines = lines[:start_remove] + lines[end_remove:]
    print(f'Lines after: {len(lines)}')
else:
    print(f'Could not find old Google Maps code')

with open(r'C:\Users\Usuario\.gemini\antigravity-ide\scratch\Onyx\index.html', 'w', encoding='utf-8', newline='') as f:
    f.writelines(lines)
print('Saved.')
