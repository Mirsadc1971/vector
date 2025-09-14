#!/usr/bin/env python3
import os
import re

def fix_popular_areas_text(content):
    """Fix Popular Service Areas text to be gold"""

    # Fix any h2 or h3 containing "Popular Service Areas"
    content = re.sub(
        r'(<h[23][^>]*>)(.*?Popular Service Areas.*?)(</h[23]>)',
        lambda m: m.group(1) + m.group(2) + m.group(3),
        content,
        flags=re.IGNORECASE
    )

    # Add CSS to ensure the heading is gold
    if 'Popular Service Areas' in content or 'popular service areas' in content.lower():
        # Add CSS for the section heading
        if '</style>' in content:
            css_addition = '''
/* Popular Service Areas heading - GOLD */
h2:has(+ .service-areas),
h2:has(+ .area-grid),
h2:has(+ [class*="area"]),
h2 {
    color: #F4A261 !important;
}

.service-areas-section h2,
.popular-areas h2,
h2:contains("Popular Service Areas"),
h2:contains("Service Areas") {
    color: #F4A261 !important;
    text-align: center;
    margin-bottom: 2rem;
}
'''
            if 'Popular Service Areas heading' not in content:
                content = content.replace('</style>', css_addition + '</style>')

    return content

# Process all HTML files
print("Fixing 'Popular Service Areas' text color to gold...")

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
        content = fix_popular_areas_text(content)
        with open(page, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {page}")

# Fix property-management index
pm_index = 'property-management/index.html'
if os.path.exists(pm_index):
    with open(pm_index, 'r', encoding='utf-8') as f:
        content = f.read()
    content = fix_popular_areas_text(content)
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
        content = fix_popular_areas_text(content)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {directory}")

print("\nAll 'Popular Service Areas' text now gold!")