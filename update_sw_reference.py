import os
import re

# Update all HTML files to use minified service worker
html_files = ['index.html']

# Add all property management pages
property_dirs = os.listdir('property-management')
for d in property_dirs:
    if os.path.isdir(f'property-management/{d}'):
        html_files.append(f'property-management/{d}/index.html')

updated = 0
for file_path in html_files:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update service worker reference
        if "register('/sw.js')" in content:
            content = content.replace("register('/sw.js')", "register('/sw-min.js')")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            updated += 1
            print(f"[OK] Updated {file_path}")

print(f"\nUpdated {updated} files to use minified service worker")