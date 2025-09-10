import os
import re

def update_certifications_color(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to find the certifications div with gold color
    pattern = r'(<div style="font-size: 0\.75rem; color: #F4A261;[^>]*>)(.*?CAI National Member.*?License: 291\.000211.*?)(</div>)'
    
    # Replace with white color (#e5e7eb)
    replacement = r'<div style="font-size: 0.75rem; color: #e5e7eb; line-height: 1.4; margin-bottom: 0.5rem;">\2\3'
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    if content != new_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

# Update all HTML files
updated_count = 0
for root, dirs, files in os.walk('.'):
    # Skip node_modules and .git directories
    if 'node_modules' in root or '.git' in root:
        continue
    
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            if update_certifications_color(filepath):
                updated_count += 1
                print(f"Updated: {filepath}")

print(f"\nTotal files updated: {updated_count}")