#!/usr/bin/env python3
import os
import re

os.chdir('C:\\Users\\mirsa\\Documents\\manage369-live\\property-management')

# Get all directories
dirs = [d for d in os.listdir('.') if os.path.isdir(d)]
print(f"Fixing card alignment in {len(dirs)} pages...")

for directory in dirs:
    file_path = os.path.join(directory, 'index.html')
    if not os.path.exists(file_path):
        continue

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix services grid alignment
    content = re.sub(
        r'\.services-grid\s*{\s*display:\s*grid;\s*grid-template-columns:\s*repeat\(auto-fit,\s*minmax\(\d+px,\s*1fr\)\);',
        '.services-grid {\n    display: grid;\n    grid-template-columns: repeat(3, 1fr);',
        content
    )

    # Fix promise grid alignment
    content = re.sub(
        r'\.promise-grid\s*{\s*display:\s*grid;\s*grid-template-columns:\s*repeat\(auto-fit,\s*minmax\(\d+px,\s*1fr\)\);',
        '.promise-grid {\n    display: grid;\n    grid-template-columns: repeat(3, 1fr);',
        content
    )

    # Fix trust stats alignment
    content = re.sub(
        r'grid-template-columns:\s*repeat\(auto-fit,\s*minmax\(250px,\s*1fr\)\)',
        'grid-template-columns: repeat(4, 1fr)',
        content
    )

    # Fix any inline grid styles with auto-fit
    content = re.sub(
        r'grid-template-columns:\s*repeat\(auto-fit,\s*minmax\(\d+px,\s*1fr\)\)',
        'grid-template-columns: repeat(3, 1fr)',
        content
    )

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Fixed {directory}")

print("\nAll pages now have perfect card alignment!")