with open(r'C:\Users\Usuario\.gemini\antigravity-ide\scratch\Onyx\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

lines = html.split('\n')
in_script = False
paren_stack = []
brace_stack = []
script_start = 0

for i, line in enumerate(lines):
    ln = i + 1
    if '<script>' in line.lower():
        in_script = True
        script_start = ln
        continue
    if '</script>' in line.lower():
        if in_script and len(paren_stack) != 0:
            print(f"Script ending at L{ln}: Unmatched parens: {len(paren_stack)}")
            for pos in paren_stack[-5:]:
                print(f"  Unmatched ( at L{pos}")
        in_script = False
        paren_stack = []
        continue
    if not in_script:
        continue
    
    # Skip string contents (rough approximation)
    in_single = False
    in_double = False
    in_template = False
    j = 0
    while j < len(line):
        c = line[j]
        # Skip escaped chars
        if j > 0 and line[j-1] == '\\':
            j += 1
            continue
        if c == "'" and not in_double and not in_template:
            in_single = not in_single
        elif c == '"' and not in_single and not in_template:
            in_double = not in_double
        elif c == '`' and not in_single and not in_double:
            in_template = not in_template
        elif not in_single and not in_double and not in_template:
            if c == '(':
                paren_stack.append(ln)
            elif c == ')':
                if paren_stack:
                    paren_stack.pop()
                else:
                    print(f"L{ln}: Extra ) without matching (")
        j += 1
