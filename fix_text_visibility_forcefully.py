#!/usr/bin/env python3
import os
import re

def fix_visibility(content):
    """Fix text visibility issues forcefully"""

    # Fix Popular Service Areas heading - make it GOLD with inline styles
    content = re.sub(
        r'(<h2[^>]*>)(.*?Popular Service Areas.*?)(</h2>)',
        r'<h2 style="color: #F4A261 !important; text-align: center;">\2</h2>',
        content,
        flags=re.IGNORECASE
    )

    # Fix View All Areas button - dark text on gold background
    content = re.sub(
        r'(<a[^>]*class="[^"]*view-all[^"]*"[^>]*>)(.*?View All.*?Areas.*?)(</a>)',
        r'<a class="view-all-btn" href="/property-management/" style="background: #F4A261 !important; color: #1f2937 !important; padding: 15px 30px !important; display: inline-block !important; font-weight: bold !important; text-decoration: none !important; border-radius: 8px !important;">\2</a>',
        content,
        flags=re.IGNORECASE | re.DOTALL
    )

    # Also fix if it's a button element
    content = re.sub(
        r'(<button[^>]*>)(.*?View All.*?Areas.*?)(</button>)',
        r'<button style="background: #F4A261 !important; color: #1f2937 !important; padding: 15px 30px !important; font-weight: bold !important; border: none !important; border-radius: 8px !important; cursor: pointer !important;">\2</button>',
        content,
        flags=re.IGNORECASE | re.DOTALL
    )

    # Fix service area button text to be gold
    content = re.sub(
        r'\.service-area-button\s*\{([^}]*)\}',
        '''.service-area-button {
    background: #2C3E50 !important;
    color: #F4A261 !important;
    border: 2px solid #F4A261 !important;
    padding: 15px 20px !important;
    text-decoration: none !important;
    display: block !important;
    text-align: center !important;
    transition: all 0.3s ease !important;
}''',
        content,
        flags=re.DOTALL
    )

    return content

# Process all HTML files
print("Forcefully fixing text visibility issues...")

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
        content = fix_visibility(content)
        with open(page, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {page}")

# Fix property-management index
pm_index = 'property-management/index.html'
if os.path.exists(pm_index):
    with open(pm_index, 'r', encoding='utf-8') as f:
        content = f.read()
    content = fix_visibility(content)
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
        content = fix_visibility(content)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {directory}")

print("\nAll visibility issues fixed with inline styles!")