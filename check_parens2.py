import re

with open(r'C:\Users\Usuario\.gemini\antigravity-ide\scratch\Onyx\index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find main script block
in_script = False
script_lines = []
script_line_nums = []

for i, line in enumerate(lines):
    ln = i + 1
    if '<script>' in line.lower() and '</script>' not in line.lower():
        in_script = True
        continue
    if '</script>' in line.lower():
        if in_script:
            break
        continue
    if in_script:
        script_lines.append(line)
        script_line_nums.append(ln)

# Simple paren counter - just track cumulative balance
# ignoring strings/regex (rough but useful)
balance = 0
for idx, (line, ln) in enumerate(zip(script_lines, script_line_nums)):
    for c in line:
        if c == '(':
            balance += 1
        elif c == ')':
            balance -= 1
    # Check if balance dips below a suspiciously low point
    if ln >= 4930 and ln <= 4970:
        print(f"L{ln}: balance={balance}  {line.rstrip()[:80]}")

print(f"\nFinal balance: {balance}")

# Also count the specific line 4956 to see if the regex is causing issues
for idx, (line, ln) in enumerate(zip(script_lines, script_line_nums)):
    if ln == 4956:
        opens = line.count('(')
        closes = line.count(')')
        print(f"\nL{ln}: opens={opens} closes={closes} diff={opens-closes}")
        print(f"Content: {line.rstrip()[:200]}")
