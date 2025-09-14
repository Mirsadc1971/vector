#!/usr/bin/env python3
import os
import re

def fix_cards_correctly(content):
    """Fix cards to have DARK background with GOLD text"""

    # Fix promise cards - DARK background, GOLD text
    content = re.sub(
        r'\.promise-card\s*\{([^}]*)\}',
        lambda m: '.promise-card {' + re.sub(r'background:[^;]*;', '', re.sub(r'color:[^;]*;', '', m.group(1))) + '\n    background: rgba(44, 62, 80, 0.3) !important;\n    color: #F4A261 !important;\n    border: 1px solid rgba(244, 162, 97, 0.3) !important;\n}',
        content,
        flags=re.DOTALL
    )

    # Fix promise card headings and paragraphs - GOLD text
    content = re.sub(
        r'\.promise-card h3[^{]*\{[^}]*\}',
        '.promise-card h3 {\n    color: #F4A261 !important;\n}',
        content,
        flags=re.DOTALL
    )

    content = re.sub(
        r'\.promise-card p[^{]*\{[^}]*\}',
        '.promise-card p {\n    color: #F4A261 !important;\n}',
        content,
        flags=re.DOTALL
    )

    # Fix service cards too - DARK background, GOLD text for headings
    content = re.sub(
        r'\.service-card\s*\{([^}]*)\}',
        lambda m: '.service-card {' + re.sub(r'background:[^;]*;', '', m.group(1)) + '\n    background: rgba(44, 62, 80, 0.3) !important;\n    border: 1px solid rgba(244, 162, 97, 0.3) !important;\n}' if 'background: rgba(44, 62, 80' not in m.group(1) else m.group(0),
        content,
        flags=re.DOTALL
    )

    return content

# Process all HTML files
print("Fixing cards - DARK background with GOLD text...")

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
        content = fix_cards_correctly(content)
        with open(page, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {page}")

# Fix property-management index
pm_index = 'property-management/index.html'
if os.path.exists(pm_index):
    with open(pm_index, 'r', encoding='utf-8') as f:
        content = f.read()
    content = fix_cards_correctly(content)
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
        content = fix_cards_correctly(content)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {directory}")

print("\nFixed - cards now have DARK background with GOLD text!")