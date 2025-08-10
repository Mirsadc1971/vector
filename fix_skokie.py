#!/usr/bin/env python3
import re

file_path = r"C:\Users\mirsa\manage369-live\property-management\skokie\index.html"

# Read the file
with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Remove any control characters and fix the header structure
# Remove any non-printable characters except newlines and tabs
cleaned = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', content)

# Fix the indentation of </header> tag
cleaned = re.sub(r'\s+</header>', '\n    </header>', cleaned)

# Remove extra blank lines between </div> and </header>
cleaned = re.sub(r'(</div>)\s*\n\s*\n\s*\n\s*(</header>)', r'\1\n    \2', cleaned)

# Write the fixed content back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(cleaned)

print(f"Fixed Skokie page - removed control characters and fixed formatting")