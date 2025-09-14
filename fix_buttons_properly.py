#!/usr/bin/env python3
import os
import re

def fix_buttons_properly(content):
    """Fix the 3 buttons HTML structure properly"""

    # Find and fix the broken button structure
    # Look for the pattern with the three buttons
    pattern = r'<div style="display: flex.*?>(.*?🚗.*?Get Directions.*?🔍.*?Find on Google.*?⭐.*?Leave Review.*?)</div>'

    def replace_buttons(match):
        # Extract the content
        inner = match.group(1)

        # Clean up the messy structure and rebuild properly
        return '''<div style="display: flex !important; gap: 15px !important; justify-content: center !important; align-items: center !important; flex-wrap: wrap !important; margin: 30px 0 !important;">
                        <a href="https://www.google.com/maps/dir//Manage369+Property+Management+1400+Patriot+Boulevard+357+Glenview+IL+60026"
                           target="_blank"
                           style="background: #4285f4; color: white; padding: 12px 24px; text-decoration: none; border-radius: 8px; font-weight: 600; display: inline-flex; align-items: center; gap: 8px;">
                           <span>🚗</span> Get Directions
                        </a>
                        <a href="https://www.google.com/search?q=manage369+property+management+glenview"
                           target="_blank"
                           style="background: #ea4335; color: white; padding: 12px 24px; text-decoration: none; border-radius: 8px; font-weight: 600; display: inline-flex; align-items: center; gap: 8px;">
                           <span>🔍</span> Find on Google
                        </a>
                        <a href="https://g.page/r/CSoD1LAaEIuOEB0/review"
                           target="_blank"
                           style="background: #fbbc04; color: #1f2937; padding: 12px 24px; text-decoration: none; border-radius: 8px; font-weight: 600; display: inline-flex; align-items: center; gap: 8px;">
                           <span>⭐</span> Leave Review
                        </a>
                    </div>'''

    content = re.sub(pattern, replace_buttons, content, flags=re.DOTALL)

    # Also clean up any duplicate or nested flex divs
    content = re.sub(
        r'<div style="display: flex[^>]*>[\s]*<div style="display: flex',
        '<div style="display: flex',
        content
    )

    return content

# Process all HTML files
print("Fixing button HTML structure properly...")

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
        content = fix_buttons_properly(content)
        with open(page, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {page}")

# Fix property-management index
pm_index = 'property-management/index.html'
if os.path.exists(pm_index):
    with open(pm_index, 'r', encoding='utf-8') as f:
        content = f.read()
    content = fix_buttons_properly(content)
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
        content = fix_buttons_properly(content)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {directory}")

print("\nButton structure fixed properly!")