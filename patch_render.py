#!/usr/bin/env python3
"""
Patch index.html to add rendering code for prodWebPagesCards and prodDesktopApps
inside the loadUserProductivity function.
"""
import sys

INPUT_FILE = "index_v81.html"
OUTPUT_FILE = "index.html"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    content = f.read()

print(f"Read {len(content)} bytes from {INPUT_FILE}")

# The marker is the closing of the loadUserProductivity function.
# We need to find the pattern:  
#     });
#   }
# }
#
# function exportProductivityCSV()
#
# And insert the render code BEFORE the last } of loadUserProductivity

MARKER = """    });
  }
}

function exportProductivityCSV()"""

REPLACEMENT = """    });
  }

  // == Render Web Pages (Detalle de Navegacion) ==
  const wpContainer = document.getElementById('prodWebPagesCards');
  if (wpContainer) {
    if (filteredWebPages && filteredWebPages.length > 0) {
      const catIcons = {'Trabajo':'\\uD83D\\uDCBC','Comun.':'\\uD83D\\uDCAC','Ocio':'\\uD83C\\uDFAE','Web':'\\uD83C\\uDF10'};
      const catColors = {'Trabajo':'#3B82F6','Comun.':'#10B981','Ocio':'#EF4444','Web':'#8B5CF6'};
      let wpHtml = '';
      filteredWebPages.forEach(function(page) {
        const icon = catIcons[page.category] || '\\uD83C\\uDF10';
        const color = catColors[page.category] || '#8B5CF6';
        wpHtml += '<div style="background:var(--surface2);border-radius:10px;padding:12px 14px;display:flex;align-items:center;gap:12px;border:1px solid var(--border)">' +
          '<div style="width:32px;height:32px;border-radius:8px;background:' + color + '18;display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0">' + icon + '</div>' +
          '<div style="flex:1;min-width:0"><div style="font-size:12px;font-weight:700;color:var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis">' + page.domain + '</div>' +
          '<div style="display:flex;gap:8px;margin-top:3px;font-size:10px"><span class="cat-pill ' + page.cat_class + '" style="font-size:9px;padding:1px 6px">' + page.category + '</span>' +
          '<span style="color:var(--text3)">' + page.time + '</span><span style="color:var(--text3)">' + page.visits + ' visitas</span></div></div></div>';
      });
      wpContainer.innerHTML = wpHtml;
    } else {
      wpContainer.innerHTML = '<div style="color:var(--text3);font-size:12px;text-align:center;padding:30px 10px"><div style="font-size:24px;margin-bottom:8px">\\uD83C\\uDF10</div><div style="font-weight:600;margin-bottom:4px">Sin datos de navegacion</div><div style="font-size:10px;opacity:0.7">El agente reportara historial en la proxima actualizacion</div></div>';
    }
  }

  // == Render Desktop Apps ==
  const daContainer = document.getElementById('prodDesktopApps');
  if (daContainer) {
    if (filteredDesktopApps && filteredDesktopApps.length > 0) {
      let daHtml = '';
      filteredDesktopApps.forEach(function(app) {
        daHtml += '<div style="background:var(--surface2);border-radius:10px;padding:10px 14px;display:flex;align-items:center;gap:10px;border:1px solid var(--border);min-width:180px">' +
          '<div style="width:30px;height:30px;border-radius:8px;background:' + (app.color || '#64748B') + '18;display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0">' + (app.icon || '\\u2699\\uFE0F') + '</div>' +
          '<div style="flex:1;min-width:0"><div style="font-size:11px;font-weight:700;color:var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis">' + app.name + '</div>' +
          '<div style="font-size:10px;color:var(--text3)">' + (app.hours || '') + ' \\u00B7 ' + (app.pct_label || app.pct + '%') + '</div></div></div>';
      });
      daContainer.innerHTML = daHtml;
    } else {
      daContainer.innerHTML = '<div style="color:var(--text3);font-size:12px;padding:12px">Sin datos de apps de escritorio</div>';
    }
  }
}

function exportProductivityCSV()"""

count = content.count(MARKER)
print(f"Marker found {count} time(s)")

if count == 1:
    content = content.replace(MARKER, REPLACEMENT)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Wrote {len(content)} bytes to {OUTPUT_FILE}")
    print("SUCCESS: Render code injected!")
else:
    print(f"ERROR: Marker found {count} times, expected 1. Aborting.")
    sys.exit(1)
