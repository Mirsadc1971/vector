#!/usr/bin/env python3
import os
import re

def restore_buttons(content):
    """Restore the 3 buttons at the bottom before footer"""

    # Find the footer
    footer_match = re.search(r'(<footer)', content)
    if not footer_match:
        return content

    footer_pos = footer_match.start()

    # The 3 buttons HTML to insert
    buttons_html = '''
    <!-- Three Action Buttons Section -->
    <section style="background: #1f2937; padding: 3rem 1.5rem;">
        <div style="max-width: 1200px; margin: 0 auto; text-align: center;">
            <h2 style="color: #F4A261; font-size: 2rem; margin-bottom: 2rem;">Quick Actions</h2>
            <div style="display: flex !important; gap: 15px !important; justify-content: center !important; align-items: center !important; flex-wrap: wrap !important;">
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
            </div>
        </div>
    </section>

    '''

    # Insert buttons before footer
    content = content[:footer_pos] + buttons_html + content[footer_pos:]

    return content

# Process all pages
print("Restoring 3 buttons at bottom of pages...")

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
        # Only add if buttons don't exist
        if '🚗' not in content:
            content = restore_buttons(content)
            with open(page, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Restored buttons in {page}")

# Fix property-management index
pm_index = 'property-management/index.html'
if os.path.exists(pm_index):
    with open(pm_index, 'r', encoding='utf-8') as f:
        content = f.read()
    if '🚗' not in content:
        content = restore_buttons(content)
        with open(pm_index, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Restored buttons in {pm_index}")

# Fix all area pages
os.chdir('property-management')
dirs = [d for d in os.listdir('.') if os.path.isdir(d)]

for directory in dirs:
    file_path = os.path.join(directory, 'index.html')
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if '🚗' not in content:
            content = restore_buttons(content)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Restored buttons in {directory}")

print("\n3 buttons restored at bottom of all pages!")