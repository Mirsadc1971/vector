#!/usr/bin/env python3
import os
import re

def fix_gold_on_gold(content):
    """Fix gold on gold text issues"""

    # Fix promise cards - ensure dark text on gold background
    content = re.sub(
        r'\.promise-card\s*\{([^}]*)\}',
        lambda m: '.promise-card {' + re.sub(r'color:[^;]*;', '', m.group(1)) + '\n    color: #1f2937 !important;\n    background: linear-gradient(135deg, #F4A261, #e8974f) !important;\n}',
        content,
        flags=re.DOTALL
    )

    # Fix promise card headings and paragraphs
    if '.promise-card h3' in content:
        content = re.sub(
            r'\.promise-card h3[^{]*\{[^}]*\}',
            '.promise-card h3 {\n    color: #1f2937 !important;\n}',
            content,
            flags=re.DOTALL
        )

    if '.promise-card p' in content:
        content = re.sub(
            r'\.promise-card p[^{]*\{[^}]*\}',
            '.promise-card p {\n    color: #1f2937 !important;\n}',
            content,
            flags=re.DOTALL
        )

    # Add CSS if not present
    if '.promise-card' in content and 'promise-card h3' not in content:
        content = content.replace('</style>', '''
.promise-card,
.promise-card h3,
.promise-card p,
.promise-card * {
    color: #1f2937 !important;
}
</style>''')

    return content

# Process all HTML files
print("Fixing gold on gold text issues...")

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
        content = fix_gold_on_gold(content)
        with open(page, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {page}")

# Fix property-management index
pm_index = 'property-management/index.html'
if os.path.exists(pm_index):
    with open(pm_index, 'r', encoding='utf-8') as f:
        content = f.read()
    content = fix_gold_on_gold(content)
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
        content = fix_gold_on_gold(content)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {directory}")

print("\nFixed gold on gold - promise cards now have dark text!")