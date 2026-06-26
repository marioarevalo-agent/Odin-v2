"""
Script to replace the canvas-based world map with Google Maps implementation.
Preserves all other content and encoding.
"""

with open(r'C:\Users\Usuario\.gemini\antigravity-ide\scratch\Onyx\index_v117_good.html', 'r', encoding='utf-8') as f:
    text = f.read()

print(f'Loaded {len(text)} chars')

# ── 1. Find and replace the map HTML container ──
old_map_html = '''<div style="position:relative;width:100%;aspect-ratio:2/1;min-height:320px;overflow:hidden;background:#040d21" id="secWorldMapContainer">
                  <!-- Canvas for world map -->
                  <canvas id="secWorldCanvas" style="position:absolute;top:0;left:0;width:100%;height:100%"></canvas>
                  <!-- SVG overlay for pins -->
                  <svg viewBox="0 0 1000 500" preserveAspectRatio="xMidYMid meet" width="100%" height="100%" id="secWorldMapSvg" style="position:absolute;top:0;left:0;z-index:2">
                    <defs>
                      <radialGradient id="glowG" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#10B981" stop-opacity="0.8"/><stop offset="100%" stop-color="#10B981" stop-opacity="0"/></radialGradient>
                      <radialGradient id="glowB" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#FBBF24" stop-opacity="0.8"/><stop offset="100%" stop-color="#FBBF24" stop-opacity="0"/></radialGradient>
                      <radialGradient id="glowY" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#FBBF24" stop-opacity="0.8"/><stop offset="100%" stop-color="#FBBF24" stop-opacity="0"/></radialGradient>
                      <radialGradient id="glowR" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#EF4444" stop-opacity="0.8"/><stop offset="100%" stop-color="#EF4444" stop-opacity="0"/></radialGradient>
                    </defs>
                  </svg>
                  <!-- Scan line -->
                  <div style="position:absolute;top:0;left:0;width:100%;height:3px;background:linear-gradient(90deg,transparent,rgba(16,185,129,0.5),transparent);z-index:3;animation:mapScan 5s linear infinite"></div>
                  <style>@keyframes mapScan{0%{transform:translateY(0)}100%{transform:translateY(100%)}}@keyframes pinPulse{0%,100%{transform:scale(1);opacity:0.6}50%{transform:scale(1.8);opacity:0}}</style>
                  <!-- Tooltip -->
                  <div id="secMapTooltip" style="display:none;position:absolute;z-index:10;background:rgba(4,13,33,0.95);border:1px solid rgba(108,159,255,0.35);border-radius:10px;padding:12px 16px;pointer-events:none;backdrop-filter:blur(12px);min-width:180px;box-shadow:0 12px 40px rgba(0,0,0,0.6)">
                    <div id="secMapTooltipContent"></div>
                  </div>
                  <!-- Legend -->
                  <div style="position:absolute;top:12px;right:12px;background:rgba(4,13,33,0.9);border:1px solid rgba(108,159,255,0.2);border-radius:10px;padding:10px 14px;z-index:4">
                    <div style="color:#64748B;font-size:8px;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:6px">ESTADO DE RED</div>
                    <div style="display:flex;align-items:center;gap:6px;margin-bottom:4px"><div style="width:9px;height:9px;border-radius:50%;background:#10B981;box-shadow:0 0 10px #10B98199"></div><span style="color:#CBD5E1;font-size:10px">Conectado</span></div>
                    <div style="display:flex;align-items:center;gap:6px"><div style="width:9px;height:9px;border-radius:50%;background:#EF4444;box-shadow:0 0 10px #EF444499"></div><span style="color:#CBD5E1;font-size:10px">Desconectado</span></div>
                  </div>
                  <!-- Device cards -->
                  <div id="secMapDeviceCards" style="position:absolute;bottom:12px;left:12px;display:flex;gap:10px;flex-wrap:wrap;z-index:4"></div>
                </div>'''

new_map_html = '''<div style="position:relative;width:100%;height:420px;overflow:hidden;border-radius:0 0 12px 12px" id="secWorldMapContainer">
                  <!-- Google Maps container -->
                  <div id="secGoogleMap" style="width:100%;height:100%"></div>
                  <!-- Overlay legend -->
                  <div id="secMapLegend" style="position:absolute;top:12px;right:12px;background:rgba(4,13,33,0.92);border:1px solid rgba(108,159,255,0.3);border-radius:12px;padding:12px 16px;z-index:10;backdrop-filter:blur(12px);box-shadow:0 8px 32px rgba(0,0,0,0.5)">
                    <div style="color:#64748B;font-size:8px;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:8px">🌐 ESTADO DE RED</div>
                    <div style="display:flex;align-items:center;gap:6px;margin-bottom:5px"><div style="width:10px;height:10px;border-radius:50%;background:#10B981;box-shadow:0 0 10px #10B98199"></div><span style="color:#CBD5E1;font-size:11px;font-weight:500">Conectado</span></div>
                    <div style="display:flex;align-items:center;gap:6px;margin-bottom:5px"><div style="width:10px;height:10px;border-radius:50%;background:#FBBF24;box-shadow:0 0 10px #FBBF2499"></div><span style="color:#CBD5E1;font-size:11px;font-weight:500">Alerta</span></div>
                    <div style="display:flex;align-items:center;gap:6px"><div style="width:10px;height:10px;border-radius:50%;background:#EF4444;box-shadow:0 0 10px #EF444499"></div><span style="color:#CBD5E1;font-size:11px;font-weight:500">Desconectado</span></div>
                  </div>
                  <!-- Device cards -->
                  <div id="secMapDeviceCards" style="position:absolute;bottom:12px;left:12px;display:flex;gap:10px;flex-wrap:wrap;z-index:10;max-width:calc(100% - 180px)"></div>
                  <!-- Loading overlay -->
                  <div id="secMapLoading" style="position:absolute;inset:0;background:#040d21;display:flex;align-items:center;justify-content:center;z-index:20">
                    <div style="text-align:center">
                      <div style="font-size:32px;margin-bottom:12px">🗺️</div>
                      <div style="color:#94A3B8;font-size:13px">Cargando mapa...</div>
                    </div>
                  </div>
                </div>'''

if old_map_html in text:
    text = text.replace(old_map_html, new_map_html)
    print('Replaced map HTML container')
else:
    # Try to find a simpler match
    old_simple = 'id="secWorldMapContainer">'
    new_simple = 'id="secWorldMapContainer" style="height:420px">'
    print('WARNING: Could not find exact HTML match, trying to find key parts...')
    
    # Find and report what's there
    idx = text.find('secWorldMapContainer')
    if idx >= 0:
        print(f'Found secWorldMapContainer at char {idx}')
        snippet = text[idx-200:idx+300]
        print(repr(snippet[:300]))

# ── 2. Find and remove the old canvas/SVG JS rendering block ──
# Find the JS block that draws the canvas map
old_js_start = 'const mapCanvas = document.getElementById(\'secWorldCanvas\');'
old_js_end = '// Device cards\n        if (mapCards) {'

start_idx = text.find(old_js_start)
if start_idx >= 0:
    print(f'Found old canvas JS at char {start_idx}')
else:
    # Try with double quotes  
    old_js_start = 'const mapCanvas = document.getElementById("secWorldCanvas");'
    start_idx = text.find(old_js_start)
    print(f'Found canvas JS (double quotes) at: {start_idx}')

# ── 3. Replace the entire map JavaScript section ──
# Find start of the map rendering function area
map_js_marker_start = "const mapCanvas = document.getElementById('secWorldCanvas');"
map_js_marker_end = "// Device cards\n        if (mapCards) {"

start = text.find(map_js_marker_start)
end = text.find(map_js_marker_end)

if start >= 0 and end >= 0:
    # Find the closing of the device cards block
    end2 = text.find('});\n        }', end)
    if end2 < 0:
        end2 = text.find('}\n      })', end)
    print(f'Found JS block: chars {start} to {end2}')
    
    # Define the replacement Google Maps JS
    new_map_js = """// ── Google Maps Rendering ──
      var _gMapInstance = null;
      var _gMapMarkers = [];

      function initGoogleMapSection(devices) {
        var mapDiv = document.getElementById('secGoogleMap');
        var loadingDiv = document.getElementById('secMapLoading');
        if (!mapDiv) return;
        if (!devices || devices.length === 0) {
          if (loadingDiv) loadingDiv.innerHTML = '<div style="text-align:center"><div style="font-size:28px;margin-bottom:10px">📡</div><div style="color:#64748B;font-size:12px">Sin dispositivos en el mapa</div></div>';
          return;
        }

        // Dark style for Google Maps
        var darkStyle = [
          {elementType:'geometry',stylers:[{color:'#0a0f1e'}]},
          {elementType:'labels.text.fill',stylers:[{color:'#4a6fa5'}]},
          {elementType:'labels.text.stroke',stylers:[{color:'#050b17'}]},
          {featureType:'administrative',elementType:'geometry',stylers:[{color:'#1a2a4a'}]},
          {featureType:'administrative.country',elementType:'labels.text.fill',stylers:[{color:'#6c9fff'}]},
          {featureType:'administrative.locality',elementType:'labels.text.fill',stylers:[{color:'#8ab4f8'}]},
          {featureType:'poi',stylers:[{visibility:'off'}]},
          {featureType:'road',stylers:[{visibility:'off'}]},
          {featureType:'transit',stylers:[{visibility:'off'}]},
          {featureType:'water',elementType:'geometry',stylers:[{color:'#020a18'}]},
          {featureType:'water',elementType:'labels.text.fill',stylers:[{color:'#1a3a6a'}]},
          {featureType:'landscape',elementType:'geometry',stylers:[{color:'#0d1b2e'}]},
          {featureType:'landscape.natural',elementType:'geometry',stylers:[{color:'#0f2035'}]},
          {featureType:'administrative.country',elementType:'geometry.stroke',stylers:[{color:'#1e3a6e'},{weight:0.8}]}
        ];

        var center = {lat: 4.71, lng: -74.07}; // Bogotá default
        if (devices.length === 1) {
          center = {lat: devices[0].lat || 4.71, lng: devices[0].lon || -74.07};
        }

        var mapOptions = {
          zoom: devices.length === 1 ? 11 : 5,
          center: center,
          styles: darkStyle,
          disableDefaultUI: true,
          zoomControl: true,
          zoomControlOptions: {position: 7},
          gestureHandling: 'cooperative',
          backgroundColor: '#0a0f1e'
        };

        if (!_gMapInstance) {
          _gMapInstance = new google.maps.Map(mapDiv, mapOptions);
        }

        // Clear old markers
        _gMapMarkers.forEach(function(m) { m.marker.setMap(null); });
        _gMapMarkers = [];

        var bounds = new google.maps.LatLngBounds();
        var pinColors = ['#10B981','#6C9FFF','#A78BFA','#F59E0B','#EC4899'];
        var infoWindows = [];

        devices.forEach(function(dev, i) {
          var lat = dev.lat || 4.71;
          var lon = dev.lon || -74.07;
          var isOnline = dev.status === 'online';
          var isAlert = dev.status === 'alert';
          var markerColor = isOnline ? (pinColors[i % pinColors.length]) : (isAlert ? '#FBBF24' : '#EF4444');
          var glowColor = isOnline ? '#10B981' : (isAlert ? '#FBBF24' : '#EF4444');
          var statusText = isOnline ? 'Conectado' : (isAlert ? 'Alerta' : 'Desconectado');
          var statusEmoji = isOnline ? '🟢' : (isAlert ? '🟡' : '🔴');

          var pos = {lat: lat, lng: lon};
          bounds.extend(pos);

          // Custom SVG marker
          var svgMarker = {
            path: 'M12 0C7.6 0 4 3.6 4 8c0 5.5 8 14 8 14s8-8.5 8-14c0-4.4-3.6-8-8-8zm0 10.5c-1.4 0-2.5-1.1-2.5-2.5S10.6 5.5 12 5.5s2.5 1.1 2.5 2.5S13.4 10.5 12 10.5z',
            fillColor: markerColor,
            fillOpacity: 1,
            strokeWeight: 2,
            strokeColor: 'rgba(255,255,255,0.9)',
            scale: 1.8,
            anchor: new google.maps.Point(12, 22)
          };

          var marker = new google.maps.Marker({
            position: pos,
            map: _gMapInstance,
            icon: svgMarker,
            title: dev.name,
            zIndex: isOnline ? 10 : 5,
            animation: google.maps.Animation.DROP
          });

          // Info window (custom styled)
          var infoContent = '<div style="background:#0d1b2e;border:1px solid ' + markerColor + '44;border-radius:10px;padding:14px 18px;min-width:220px;font-family:Inter,sans-serif">' +
            '<div style="font-weight:700;font-size:14px;margin-bottom:10px;color:' + markerColor + ';display:flex;align-items:center;gap:6px">' + statusEmoji + ' ' + dev.name + '</div>' +
            '<div style="display:grid;grid-template-columns:auto 1fr;gap:4px 12px;font-size:11px">' +
            '<span style="color:#4a6fa5">IP:</span><span style="color:#8ab4f8;font-family:monospace">' + (dev.ip || 'N/A') + '</span>' +
            '<span style="color:#4a6fa5">Ciudad:</span><span style="color:#cbd5e1">' + (dev.city || 'Bogotá') + '</span>' +
            '<span style="color:#4a6fa5">País:</span><span style="color:#cbd5e1">' + (dev.country || 'Colombia') + '</span>' +
            '<span style="color:#4a6fa5">ISP:</span><span style="color:#cbd5e1">' + (dev.isp || '—') + '</span>' +
            '<span style="color:#4a6fa5">Estado:</span><span style="color:' + markerColor + ';font-weight:700">' + statusText + '</span>' +
            '</div></div>';

          var infoWindow = new google.maps.InfoWindow({
            content: infoContent,
            disableAutoPan: false
          });
          infoWindows.push(infoWindow);

          marker.addListener('click', function() {
            infoWindows.forEach(function(iw) { iw.close(); });
            infoWindow.open(_gMapInstance, marker);
          });

          _gMapMarkers.push({marker: marker, dev: dev, color: markerColor});
        });

        // Fit bounds
        if (devices.length > 1) {
          _gMapInstance.fitBounds(bounds, {top: 40, right: 40, bottom: 60, left: 40});
          var zoomListener = google.maps.event.addListenerOnce(_gMapInstance, 'idle', function() {
            if (_gMapInstance.getZoom() > 12) _gMapInstance.setZoom(12);
            if (_gMapInstance.getZoom() < 3) _gMapInstance.setZoom(4);
          });
        }

        // Add pulsing circles (custom overlay)
        _gMapMarkers.forEach(function(item) {
          var circle = new google.maps.Circle({
            strokeColor: item.color,
            strokeOpacity: 0,
            strokeWeight: 2,
            fillColor: item.color,
            fillOpacity: 0.12,
            map: _gMapInstance,
            center: item.marker.getPosition(),
            radius: 15000
          });
          item.circle = circle;
        });

        if (loadingDiv) loadingDiv.style.display = 'none';
      }

      // Load Google Maps API
      function loadGoogleMapsScript(devices) {
        if (window.google && window.google.maps) {
          initGoogleMapSection(devices);
          return;
        }
        window._gMapDevices = devices;
        window.initGMapCallback = function() { initGoogleMapSection(window._gMapDevices); };
        var script = document.createElement('script');
        script.src = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyD-9tSrke72PouQMnMX-a7eZSW0jkFMBWY&callback=initGMapCallback&loading=async';
        script.async = true;
        script.defer = true;
        document.head.appendChild(script);
      }

      // Device cards (bottom left overlay)
      const mapCards = document.getElementById('secMapDeviceCards');"""
    
    # Also find and update the device cards rendering
    device_cards_block_start = old_js_marker_end = "// Device cards\n        if (mapCards) {"
    device_cards_block_end_marker = "setTimeout"
    
    # Find end of device cards block
    dc_start = end  # we already have end pointing to "// Device cards"
    dc_end = text.find('});\n        }', dc_start)
    if dc_end < 0:
        dc_end = text.find('\n        }\n      })', dc_start)
    if dc_end >= 0:
        dc_end = dc_end + 15
    
    print(f'Device cards block: {dc_start} to {dc_end}')
    
    old_js_full = text[start:dc_end]
    print(f'Replacing {len(old_js_full)} chars of old JS')
    
    new_device_cards_js = """
        // Device cards overlay
        if (mapCards && data.connection_map) {
          var pinColors2 = ['#10B981','#6C9FFF','#A78BFA','#F59E0B','#EC4899'];
          mapCards.innerHTML = data.connection_map.map(function(dev, i) {
            var isOnline = dev.status === 'online';
            var isAlert = dev.status === 'alert';
            var color = isOnline ? pinColors2[i % pinColors2.length] : (isAlert ? '#FBBF24' : '#EF4444');
            var dot = isOnline ? '🟢' : (isAlert ? '🟡' : '🔴');
            return '<div style="background:rgba(10,15,30,0.92);border:1px solid ' + color + '44;border-radius:10px;padding:10px 14px;min-width:130px;backdrop-filter:blur(8px);box-shadow:0 4px 20px rgba(0,0,0,0.5)">' +
              '<div style="display:flex;align-items:center;gap:6px;margin-bottom:4px">' +
              '<div style="width:8px;height:8px;border-radius:50%;background:' + color + ';box-shadow:0 0 8px ' + color + '88"></div>' +
              '<span style="color:#F1F5F9;font-weight:700;font-size:12px">' + dev.name + '</span></div>' +
              '<div style="color:#4a6fa5;font-family:monospace;font-size:9px">' + (dev.ip || 'N/A') + '</div>' +
              '<div style="color:#94A3B8;font-size:9px;margin-top:2px">' + (dev.city || 'Bogotá') + ' · ' + (dev.country || 'Colombia') + '</div>' +
              '</div>';
          }).join('');
        }

        // Initialize Google Maps with devices
        if (data.connection_map && data.connection_map.length > 0) {
          loadGoogleMapsScript(data.connection_map);
        }"""
    
    replacement = new_map_js + new_device_cards_js
    text = text[:start] + replacement + text[dc_end:]
    print(f'Replaced map JS successfully')
else:
    print(f'WARNING: Could not locate JS block. start={start}, end={end}')

# ── 4. Also remove the old setTimeout pin animation if any ──
old_timeout = "setTimeout(() => { g.style.opacity = '1'; }, 150);\n        });\n        \n        // Device cards"
if old_timeout in text:
    text = text.replace(old_timeout, "// Device cards")
    print('Removed old animation setTimeout')

# ── 5. Verify ──
if 'secGoogleMap' in text:
    print('OK: Google Maps div present')
if 'initGoogleMapSection' in text:
    print('OK: initGoogleMapSection function present')
if 'Distribución' in text:
    print('OK: accents correct')
if '🗺️' in text:
    print('OK: emojis present')
replacement_count = text.count('\ufffd')
print(f'Replacement chars: {replacement_count}')
print(f'Final size: {len(text)} chars')

# ── 6. Apply USB panel removal (same as before) ──
# Remove USB PORT MONITORING card from Monitoreo tab
usb_html_start = text.find('<!-- USB PORT MONITORING')
candidates = []
while usb_html_start >= 0:
    candidates.append(usb_html_start)
    usb_html_start = text.find('<!-- USB PORT MONITORING', usb_html_start + 1)
print(f'Found {len(candidates)} USB PORT MONITORING markers')

# The second one is the global panel in Monitoreo tab
if len(candidates) >= 2:
    block_start = candidates[1]
    # Find the closing </div> for this card (depth counting)
    depth = 0
    pos = block_start
    while pos < len(text):
        if text[pos:pos+4] == '<div':
            depth += 1
        elif text[pos:pos+6] == '</div>':
            depth -= 1
            if depth <= 0:
                block_end = pos + 6
                break
        pos += 1
    text = text[:block_start] + text[block_end:]
    print(f'Removed USB HTML global panel')

# Remove USB PORTS RENDERING JS
js_start = text.find('// ── USB PORTS RENDERING ──')
if js_start >= 0:
    js_end = text.find('usbPanel.innerHTML = usbHtml;', js_start)
    if js_end >= 0:
        closing = text.find('}', js_end + 30)
        text = text[:js_start] + text[closing+1:]
        print('Removed USB JS block')

# Apply USB parse fix
old_ports = "const ports = data.usb_ports;"
new_ports = """var ports = data.usb_ports;
  if (typeof ports === 'string') {
    try { ports = JSON.parse(ports); } catch(e) { ports = null; }
  }"""
if old_ports in text:
    text = text.replace(old_ports, new_ports)
    print('Applied USB JSON parse fix')

# ── 7. Save ──
with open(r'C:\Users\Usuario\.gemini\antigravity-ide\scratch\Onyx\index.html', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(text)
print('DONE: Saved index.html with Google Maps')
