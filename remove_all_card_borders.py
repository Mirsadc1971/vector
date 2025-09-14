#!/usr/bin/env python3
import os
import re

def remove_all_borders(content):
    """Remove ALL colored borders from cards - completely"""

    # Remove all border-left, border-right, border-top, border-bottom
    content = re.sub(r'border-left:[^;]*;', '', content)
    content = re.sub(r'border-right:[^;]*;', '', content)
    content = re.sub(r'border-top:[^;]*;', '', content)
    content = re.sub(r'border-bottom:[^;]*;', '', content)

    # Replace all card borders with subtle gold border
    content = re.sub(
        r'(\.service-card\s*\{[^}]*?)border:[^;]*;',
        r'\1border: 1px solid rgba(244, 162, 97, 0.2);',
        content,
        flags=re.DOTALL
    )

    content = re.sub(
        r'(\.promise-card\s*\{[^}]*?)border:[^;]*;',
        r'\1border: 1px solid rgba(244, 162, 97, 0.2);',
        content,
        flags=re.DOTALL
    )

    # Remove any inline style borders with colors
    content = re.sub(r'style="[^"]*border-left:[^;]*;[^"]*"', lambda m: m.group(0).replace(re.search(r'border-left:[^;]*;', m.group(0)).group(0), '') if re.search(r'border-left:[^;]*;', m.group(0)) else m.group(0), content)
    content = re.sub(r'style="[^"]*border-right:[^;]*;[^"]*"', lambda m: m.group(0).replace(re.search(r'border-right:[^;]*;', m.group(0)).group(0), '') if re.search(r'border-right:[^;]*;', m.group(0)) else m.group(0), content)
    content = re.sub(r'style="[^"]*border-top:[^;]*;[^"]*"', lambda m: m.group(0).replace(re.search(r'border-top:[^;]*;', m.group(0)).group(0), '') if re.search(r'border-top:[^;]*;', m.group(0)) else m.group(0), content)
    content = re.sub(r'style="[^"]*border-bottom:[^;]*;[^"]*"', lambda m: m.group(0).replace(re.search(r'border-bottom:[^;]*;', m.group(0)).group(0), '') if re.search(r'border-bottom:[^;]*;', m.group(0)) else m.group(0), content)

    return content

# Process all HTML files
print("Removing ALL colored borders from card sides...")

# Fix main pages
main_pages = [
    'index.html',
    'services.html',
    'contact.html',
    'pay-dues.html',
    'payment-methods.html',
    'forms.html',
    'leave-review.html',
    'privacy-policy.html',
    'terms-of-service.html',
    'legal-disclaimers.html',
    'accessibility.html',
    'property-management-near-me.html'
]

for page in main_pages:
    if os.path.exists(page):
        with open(page, 'r', encoding='utf-8') as f:
            content = f.read()
        content = remove_all_borders(content)
        with open(page, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {page}")

# Fix property-management index
pm_index = 'property-management/index.html'
if os.path.exists(pm_index):
    with open(pm_index, 'r', encoding='utf-8') as f:
        content = f.read()
    content = remove_all_borders(content)
    with open(pm_index, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed {pm_index}")

# Fix all area pages
os.chdir('property-management')
dirs = [d for d in os.listdir('.') if os.path.isdir(d)]

for directory in dirs:
    file_path = os.path.join(directory, 'index.html')
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        content = remove_all_borders(content)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {directory}")

print("\nALL colored borders removed from cards!")