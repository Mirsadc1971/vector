#!/usr/bin/env python3
import os
import re

def fix_colors_properly(content):
    """Fix colors the right way"""

    # 1. Popular Service Areas heading - GOLD text
    content = re.sub(
        r'(<h2[^>]*>)(.*?Popular Service Areas.*?)(</h2>)',
        r'<h2 style="color: #F4A261 !important;">\2</h2>',
        content,
        flags=re.IGNORECASE
    )

    # 2. Service area buttons - GOLD text on dark background
    content = re.sub(
        r'\.service-area-button\s*\{[^}]*\}',
        '''.service-area-button {
    background: #2C3E50 !important;
    color: #F4A261 !important;
    border: 2px solid #F4A261 !important;
    padding: 15px 20px !important;
    text-decoration: none !important;
    display: block !important;
    text-align: center !important;
}''',
        content,
        flags=re.DOTALL
    )

    # 3. View All Areas button - DARK text on GOLD background
    content = re.sub(
        r'(<a[^>]*(?:view-all|View All)[^>]*>)(.*?)(</a>)',
        lambda m: '<a href="/property-management/" style="background: #F4A261 !important; color: #1f2937 !important; padding: 15px 30px !important; display: inline-block !important; font-weight: bold !important; text-decoration: none !important; border-radius: 8px !important;">' + m.group(2) + '</a>',
        content,
        flags=re.IGNORECASE | re.DOTALL
    )

    # 4. Areas We Serve in gold cards - DARK text
    if '.promise-card' in content:
        content = re.sub(
            r'(\.promise-card\s*\{[^}]*)',
            lambda m: m.group(1) + '\n    color: #1f2937 !important;' if 'color: #1f2937' not in m.group(1) else m.group(1),
            content,
            flags=re.DOTALL
        )

    return content

# Process all HTML files
print("Fixing colors correctly...")

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
        content = fix_colors_properly(content)
        with open(page, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {page}")

# Fix property-management index
pm_index = 'property-management/index.html'
if os.path.exists(pm_index):
    with open(pm_index, 'r', encoding='utf-8') as f:
        content = f.read()
    content = fix_colors_properly(content)
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
        content = fix_colors_properly(content)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {directory}")

print("\nColors fixed correctly - service buttons gold text, View All dark on gold!")