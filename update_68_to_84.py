#!/usr/bin/env python3
import os
import re

# Update main index.html
files_to_update = [
    'index.html',
    'property-management-near-me.html'
]

for file in files_to_update:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update various references
        content = content.replace('68 total service areas', '84 total service areas')
        content = content.replace('View All 68 Areas', 'View All 84 Areas')
        content = content.replace('68 areas covered', '84 areas covered')
        content = content.replace('60+ other communities across 68 total', '75+ other communities across 84 total')

        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {file}")

# Update all area pages
os.chdir('property-management')

for directory in os.listdir('.'):
    if os.path.isdir(directory):
        file_path = os.path.join(directory, 'index.html')
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Update references
            content = content.replace('View all 68 service areas', 'View all 84 service areas')
            content = content.replace('all 68 service', 'all 84 service')

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {directory}")

# Update index-old.html if exists
if os.path.exists('index-old.html'):
    with open('index-old.html', 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace('68 Chicago', '84 Chicago')
    content = content.replace('68 North Shore', '84 North Shore')
    content = content.replace('68 Communities', '84 Communities')
    content = content.replace('68 Premium', '84 Premium')
    content = content.replace('across 68 Chicago', 'across 84 Chicago')

    with open('index-old.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated index-old.html")

print("\nAll references updated from 68 to 84!")