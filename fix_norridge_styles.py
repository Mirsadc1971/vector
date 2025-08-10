import re

# Read the Norridge file
with open(r'C:\Users\mirsa\manage369-live\property-management\norridge\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the position of the broken style content
# We need to remove everything from line 111 until </style>
lines = content.split('\n')

# Find where the broken style section starts and ends
new_lines = []
in_broken_style = False
for i, line in enumerate(lines):
    # Start of broken section (around line 111)
    if 'position: fixed;' in line and 'top: 0;' in lines[i+1] if i+1 < len(lines) else False:
        in_broken_style = True
        continue
    # End of broken section
    elif '</style>' in line and in_broken_style:
        in_broken_style = False
        continue
    # Skip lines in broken section
    elif in_broken_style:
        continue
    # Keep all other lines
    else:
        new_lines.append(line)

# Write back
with open(r'C:\Users\mirsa\manage369-live\property-management\norridge\index.html', 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines))

print("Fixed Norridge page by removing broken inline styles")