import re
import sys

def verify_js_syntax(code, filename="code"):
    print(f"--- Verifying {filename} ---")
    i = 0
    line_num = 1
    line_start_idx = 0
    
    # State stack. Start in NORMAL mode.
    # Each item is a dict: { "state": state, "line": line, "col": col, "brace_count": 0 }
    state_stack = [{"state": "NORMAL", "line": 1, "col": 1, "brace_count": 0}]
    
    # Track overall delimiters for reporting
    open_braces = []  # stores (line, col)
    open_parens = []  # stores (line, col)
    open_brackets = [] # stores (line, col)
    
    escaped = False
    
    # Helper to track last non-whitespace char for regex heuristic
    last_char = ""
    
    while i < len(code):
        c = code[i]
        
        # Track line number and column
        if c == '\n':
            line_num += 1
            line_start_idx = i + 1
            # Auto-close single-line comment on newline
            if state_stack[-1]["state"] == "COMMENT_SL":
                state_stack.pop()
                last_char = ""
        
        col = i - line_start_idx + 1
        current_state = state_stack[-1]["state"]
        
        if current_state == "NORMAL":
            if escaped:
                escaped = False
                i += 1
                continue
            
            # Check comments
            if code[i:i+2] == "//":
                state_stack.append({"state": "COMMENT_SL", "line": line_num, "col": col})
                i += 2
                continue
            elif code[i:i+2] == "/*":
                state_stack.append({"state": "COMMENT_ML", "line": line_num, "col": col})
                i += 2
                continue
            
            # Check strings/template literals
            elif c == "'":
                state_stack.append({"state": "SINGLE_QUOTE", "line": line_num, "col": col})
                escaped = False
                i += 1
                continue
            elif c == '"':
                state_stack.append({"state": "DOUBLE_QUOTE", "line": line_num, "col": col})
                escaped = False
                i += 1
                continue
            elif c == '`':
                state_stack.append({"state": "TEMPLATE_LITERAL", "line": line_num, "col": col})
                escaped = False
                i += 1
                continue
                
            # Check regex heuristic
            elif c == "/":
                if last_char in ("", "=", ":", "(", "[", "{", ";", ",", "&", "|", "!", "?", "+", "-", "*", "%", "^", ">", "<"):
                    state_stack.append({"state": "REGEX", "line": line_num, "col": col})
                    escaped = False
                    i += 1
                    continue
                else:
                    last_char = "/"
            
            elif c in (" ", "\t", "\r", "\n"):
                pass
            else:
                last_char = c
                
            # Delimiters
            if c == '{':
                state_stack[-1]["brace_count"] += 1
                open_braces.append((line_num, col))
            elif c == '}':
                # Check if this closes a template literal interpolation ${...}
                if state_stack[-1]["brace_count"] == 0:
                    # We have a unmatched '}'. If the parent state is TEMPLATE_LITERAL, this closes the interpolation!
                    if len(state_stack) > 1 and state_stack[-2]["state"] == "TEMPLATE_LITERAL":
                        state_stack.pop() # pop NORMAL state
                        i += 1
                        continue
                    else:
                        print(f"Error: Extra '}}' at line {line_num}, col {col}")
                else:
                    state_stack[-1]["brace_count"] -= 1
                    if open_braces:
                        open_braces.pop()
                    else:
                        print(f"Error: Extra '}}' at line {line_num}, col {col}")
                        
            elif c == '(':
                open_parens.append((line_num, col))
            elif c == ')':
                if open_parens:
                    open_parens.pop()
                else:
                    print(f"Error: Extra ')' at line {line_num}, col {col}")
                    
            elif c == '[':
                open_brackets.append((line_num, col))
            elif c == ']':
                if open_brackets:
                    open_brackets.pop()
                else:
                    print(f"Error: Extra ']' at line {line_num}, col {col}")
                    
        elif current_state == "TEMPLATE_LITERAL":
            if escaped:
                escaped = False
            elif c == "\\":
                escaped = True
            elif code[i:i+2] == "${":
                # Start interpolation: push a new NORMAL state context
                state_stack.append({"state": "NORMAL", "line": line_num, "col": col, "brace_count": 0})
                i += 2
                continue
            elif c == '`':
                state_stack.pop() # pop TEMPLATE_LITERAL
                last_char = '`'
                
        elif current_state in ("SINGLE_QUOTE", "DOUBLE_QUOTE", "REGEX"):
            if escaped:
                escaped = False
            elif c == "\\":
                escaped = True
            elif (current_state == "SINGLE_QUOTE" and c == "'") or \
                 (current_state == "DOUBLE_QUOTE" and c == '"') or \
                 (current_state == "REGEX" and c == "/"):
                state_stack.pop()
                last_char = c
                
        elif current_state == "COMMENT_ML":
            if code[i:i+2] == "*/":
                state_stack.pop()
                i += 2
                continue
                
        i += 1
        
    print(f"Parsing finished.")
    # Check states left in stack
    if len(state_stack) > 1:
        print(f"Error: Unclosed states in stack:")
        for s in state_stack[1:]:
            print(f"  - State '{s['state']}' opened at line {s['line']}, col {s['col']}")
            
    if open_braces:
        print(f"Error: {len(open_braces)} unmatched '{{' open. Deepest at line {open_braces[-1][0]}, col {open_braces[-1][1]}")
        print("First 5 open braces:", open_braces[:5])
    if open_parens:
        print(f"Error: {len(open_parens)} unmatched '(' open. Deepest at line {open_parens[-1][0]}, col {open_parens[-1][1]}")
        print("First 5 open parens:", open_parens[:5])
    if open_brackets:
        print(f"Error: {len(open_brackets)} unmatched '[' open. Deepest at line {open_brackets[-1][0]}, col {open_brackets[-1][1]}")
        print("First 5 open brackets:", open_brackets[:5])
        
    if len(state_stack) == 1 and not open_braces and not open_parens and not open_brackets:
        print("Success: All delimiters matched perfectly!")
        return True
    return False

def check_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    script_pattern = re.compile(r'<script[^>]*>(.*?)</script>', re.DOTALL)
    scripts = list(script_pattern.finditer(html))
    
    all_ok = True
    for idx, m in enumerate(scripts):
        code = m.group(1)
        start_line = html[:m.start()].count('\n') + 1
        # Reconstruct line spacing
        prefix_newlines = "\n" * (start_line - 1)
        full_code = prefix_newlines + code
        ok = verify_js_syntax(full_code, f"{filepath} (Script block {idx+1} starting at line {start_line})")
        if not ok:
            all_ok = False
            
    return all_ok

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "index.html"
    check_html_file(target)
