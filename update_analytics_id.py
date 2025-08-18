import os
import re
from pathlib import Path

def update_analytics_id(file_path):
    """Update Google Analytics ID in HTML files"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes_made = False
    
    # Replace the placeholder GA ID with the real one
    old_id = 'G-YOUR-ID-HERE'
    new_id = 'G-LCX4DTB57C'
    
    if old_id in content:
        content = content.replace(old_id, new_id)
        changes_made = True
    
    # Also check for any other variations that might exist
    # Pattern for gtag config line
    gtag_pattern = r"gtag\('config', '([^']+)'\)"
    gtag_matches = re.findall(gtag_pattern, content)
    
    for match in gtag_matches:
        if match != new_id and match.startswith('G-'):
            content = content.replace(f"gtag('config', '{match}')", f"gtag('config', '{new_id}')")
            changes_made = True
    
    # Pattern for GA script src
    script_pattern = r'googletagmanager\.com/gtag/js\?id=([^"\']+)'
    script_matches = re.findall(script_pattern, content)
    
    for match in script_matches:
        if match != new_id and match.startswith('G-'):
            content = content.replace(f'googletagmanager.com/gtag/js?id={match}', f'googletagmanager.com/gtag/js?id={new_id}')
            changes_made = True
    
    # Write back if changes were made
    if changes_made:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Process all HTML files
html_files = []

# Get all HTML files in root
for file in Path('.').glob('*.html'):
    html_files.append(str(file))

# Get all HTML files in subdirectories
for file in Path('.').rglob('*/index.html'):
    html_files.append(str(file))

print(f"Updating Google Analytics ID in {len(html_files)} HTML files")
print(f"New GA4 ID: G-LCX4DTB57C")
print("-" * 50)

updated = 0
skipped = 0
errors = 0

for file in html_files:
    try:
        if update_analytics_id(file):
            print(f"[UPDATED] {file}")
            updated += 1
        else:
            skipped += 1
    except Exception as e:
        errors += 1
        print(f"[ERROR] {file}: {str(e)}")

print("-" * 50)
print(f"\n[COMPLETE] Google Analytics ID update complete!")
print(f"\nResults:")
print(f"  Files updated: {updated}")
print(f"  Files unchanged: {skipped}")
print(f"  Errors: {errors}")