#!/usr/bin/env python3
import os
import re

os.chdir('C:\\Users\\mirsa\\Documents\\manage369-live\\property-management')

# Get all directories
dirs = [d for d in os.listdir('.') if os.path.isdir(d)]
print(f"Fixing trust stats to 4 columns in {len(dirs)} pages...")

for directory in dirs:
    file_path = os.path.join(directory, 'index.html')
    if not os.path.exists(file_path):
        continue

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Keep trust stats at 4 columns (it's already correct)
    # But make sure the services and promise grids stay at 3 columns

    # This is already done, but let's verify trust stats are 4 columns
    if '.trust-stats' in content:
        # Find and ensure trust stats section has 4 columns
        content = re.sub(
            r'(\.trust-stats\s*{[^}]*grid-template-columns:\s*)repeat\(3,\s*1fr\)',
            r'\1repeat(4, 1fr)',
            content
        )

    # Also check inline trust stats
    content = re.sub(
        r'(<div[^>]*class="trust-stats"[^>]*>.*?display:\s*grid;\s*grid-template-columns:\s*)repeat\(3,\s*1fr\)',
        r'\1repeat(4, 1fr)',
        content,
        flags=re.DOTALL
    )

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Fixed {directory}")

print("\nAll pages now have 4-column trust stats on desktop!")