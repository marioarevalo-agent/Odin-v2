import re

with open(r'C:\Users\Usuario\.gemini\antigravity-ide\scratch\Onyx\index_v117_good.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f'Original lines: {len(lines)}')

# Find the USB PORT MONITORING HTML card to remove
start_html = None
end_html = None
for i, line in enumerate(lines):
    if 'USB PORT MONITORING' in line and 'Full width' in line:
        start_html = i - 1  # include blank line before
        print(f'Found USB HTML card start at line {i+1}')
    if start_html is not None and i > start_html and '</div>' in line:
        stripped = line.strip()
        if stripped == '</div>' and i > start_html + 15:
            end_html = i + 1
            print(f'Found USB HTML card end at line {i+1}')
            break

# Manual check: find exact boundaries
start_html = None
end_html = None
for i, line in enumerate(lines):
    if '<!-- USB PORT MONITORING' in line:
        start_html = i
        print(f'USB HTML start: line {i+1}: {line.strip()[:60]}')
    if start_html is not None and i > start_html and 'secUsbPortsPanel' in line:
        print(f'USB panel div at line {i+1}')
        # Count closing divs
        depth = 0
        for j in range(start_html, min(start_html + 25, len(lines))):
            depth += lines[j].count('<div')
            depth -= lines[j].count('</div>')
            if depth <= 0 and j > start_html + 5:
                end_html = j + 1
                print(f'USB HTML end: line {j+1}')
                break
        break

if start_html is not None and end_html is not None:
    print(f'Removing HTML lines {start_html+1}-{end_html}')
    del lines[start_html:end_html]
    print(f'Removed {end_html - start_html} HTML lines')
else:
    print('WARNING: Could not find USB HTML block!')

# Re-join to work with text
text = ''.join(lines)

# Find and remove USB PORTS JS rendering block
js_start_marker = '// ── USB PORTS RENDERING ──'
js_end_marker = 'usbPanel.innerHTML = usbHtml;'

js_start_idx = text.find(js_start_marker)
if js_start_idx >= 0:
    js_end_idx = text.find(js_end_marker, js_start_idx)
    if js_end_idx >= 0:
        # Find the closing brace after usbPanel.innerHTML
        closing = text.find('}', js_end_idx + len(js_end_marker))
        if closing >= 0:
            # Remove from js_start to closing + 1
            removed = text[js_start_idx:closing+1]
            text = text[:js_start_idx] + text[closing+1:]
            removed_lines = removed.count('\n')
            print(f'Removed USB JS block ({removed_lines} lines)')
    else:
        print('WARNING: Could not find JS end marker')
else:
    print('WARNING: Could not find JS start marker')

# Apply USB parse fix for Por Equipo tab
old_ports = 'const ports = data.usb_ports;'
new_ports = """var ports = data.usb_ports;
  if (typeof ports === 'string') {
    try { ports = JSON.parse(ports); } catch(e) { ports = null; }
  }"""
if old_ports in text:
    text = text.replace(old_ports, new_ports)
    print('Applied USB JSON parse fix')

# Fix ports array check
old_check = 'if (!ports || !ports.length) {'
new_check = 'if (!ports || !Array.isArray(ports) || !ports.length) {'
if old_check in text:
    text = text.replace(old_check, new_check)
    print('Applied ports array check fix')

# Apply status label changes: Sistema -> Disponible, remove Conectado mapping
old_status = "'Sistema':      { color: '#6C9FFF', icon: '⚙', label: 'SISTEMA'"
if old_status in text:
    text = text.replace(
        "'Sistema':      { color: '#6C9FFF', icon: '⚙', label: 'SISTEMA',     bg: '#6C9FFF12', border: '2px solid #6C9FFF55', glow: 'none' },",
        "'Disponible':   { color: '#FBBF24', icon: '○', label: 'DISPONIBLE',   bg: '#FBBF2410', border: '2px dashed #FBBF2466', glow: 'none' },"
    )
    print('Applied status label: Sistema -> Disponible')

# Remove Conectado entry
old_conectado = "'Conectado':    { color: '#10B981', icon: '●', label: 'EN USO',       bg: '#10B98112', border: '2px solid #10B981', glow: '0 0 12px #10B98130' }"
if old_conectado in text:
    text = text.replace("\n    " + old_conectado, "")
    print('Removed Conectado status entry')

# Add resolveStatus function after statusCfg
resolve_func = """
  // Resolve any status to En Uso or Disponible
  function resolveStatus(p) {
    if (p.status === 'Bloqueado') return 'Bloqueado';
    if (p.status === 'Desconectado') return 'Desconectado';
    return (p.category === 'Controlador' || p.category === 'Hub') ? 'Disponible' : 'En Uso';
  }"""

# Insert after the statusCfg closing brace
status_end = "  };\n  var catIcons2"
if status_end in text and 'resolveStatus' not in text:
    text = text.replace(status_end, "  };" + resolve_func + "\n  var catIcons2")
    print('Added resolveStatus function')

# Update classification filters to use resolveStatus
old_filter1 = "var userDevices = ports.filter(function(p){ return p.status === 'En Uso' || (p.status === 'Conectado' && p.category !== 'Controlador' && p.category !== 'Hub'); });"
new_filter1 = "var userDevices = ports.filter(function(p){ return resolveStatus(p) === 'En Uso'; });"
if old_filter1 in text:
    text = text.replace(old_filter1, new_filter1)
    print('Updated userDevices filter')

old_filter2 = "var sysComponents = ports.filter(function(p){ return p.status === 'Sistema' || (p.status === 'Conectado' && (p.category === 'Controlador' || p.category === 'Hub')); });"
new_filter2 = "var availPorts = ports.filter(function(p){ return resolveStatus(p) === 'Disponible'; });"
if old_filter2 in text:
    text = text.replace(old_filter2, new_filter2)
    print('Updated sysComponents -> availPorts filter')

# Update all sysComponents references to availPorts
text = text.replace('sysComponents.length', 'availPorts.length')
text = text.replace('sysComponents)', 'availPorts)')
text = text.replace("pctSys", "pctAvail")
text = text.replace("sistema", "disponibles")
text = text.replace("#6C9FFF", "#FBBF24")  # Only in the bar summary context - too broad, skip this

# Fix status resolution in port rendering
old_resolve = "var st = port.status || 'Desconectado';\n    if (st === 'Conectado') { st = (port.category === 'Controlador' || port.category === 'Hub') ? 'Sistema' : 'En Uso'; }"
new_resolve = "var st = resolveStatus(port);"
if old_resolve in text:
    text = text.replace(old_resolve, new_resolve)
    print('Updated port status resolution')

old_sys_check = "var isSys = (st === 'Sistema');"
new_avail_check = "var isAvail = (st === 'Disponible');"
if old_sys_check in text:
    text = text.replace(old_sys_check, new_avail_check)
    print('Updated isSys -> isAvail')

# Update isSys references
text = text.replace("else if (isSys) h += '⚙️'", "else if (isAvail) h += '<div style=\"width:10px;height:10px;border-radius:50%;border:2px dashed #FBBF2488\"></div>'")

# Update sorted array
text = text.replace('.concat(sysComponents)', '.concat(availPorts)')

# Update table status resolution
old_table_st = """var st2 = port.status || 'Desconectado';
    if (st2 === 'Conectado') st2 = (port.category === 'Controlador' || port.category === 'Hub') ? 'Sistema' : 'En Uso';"""
new_table_st = "var st2 = resolveStatus(port);"
if old_table_st in text:
    text = text.replace(old_table_st, new_table_st)
    print('Updated table status resolution')

# Verify
if 'secUsbPortsPanel' in text:
    print('WARNING: secUsbPortsPanel still present!')
else:
    print('OK: USB panel removed from Monitoreo')

if 'resolveStatus' in text:
    print('OK: resolveStatus present')

if 'Distribución' in text:
    print('OK: accents correct')

if '🔌' in text:
    print('OK: emojis present')

replacement_count = text.count('\ufffd')
print(f'Replacement chars: {replacement_count}')

# Save
with open(r'C:\Users\Usuario\.gemini\antigravity-ide\scratch\Onyx\index.html', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(text)
print('DONE: Saved index.html')
