#!/usr/bin/env python3
import os
import glob
import re

def fix_control_chars(file_path):
    """Remove control characters and fix formatting"""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original = content
    
    # Remove any control characters (except newlines and tabs)
    content = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', content)
    
    # Fix the indentation of </header> tag if it exists
    content = re.sub(r'\s+</header>', '\n    </header>', content)
    
    # Remove excessive blank lines (more than 2 consecutive)
    content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
    
    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Get all property management HTML files
property_files = glob.glob(r"C:\Users\mirsa\manage369-live\property-management\*\index.html")

print(f"Checking {len(property_files)} property pages for control characters...\n")

fixed = []
for file_path in property_files:
    dir_name = os.path.basename(os.path.dirname(file_path))
    if fix_control_chars(file_path):
        fixed.append(dir_name)
        print(f"Fixed: {dir_name}")

print(f"\nTotal fixed: {len(fixed)} pages")
if fixed:
    print("Pages cleaned:")
    for page in fixed:
        print(f"  - {page}")