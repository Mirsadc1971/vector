#!/usr/bin/env python3
import os
import re

def fix_areas_we_serve(content):
    """Fix Areas We Serve text to be dark on gold background"""

    # Fix Areas We Serve heading - dark text on gold cards
    content = re.sub(
        r'(<h[23][^>]*>)(.*?Areas We Serve.*?)(</h[23]>)',
        r'<\1 style="color: #1f2937 !important;">\2</\3>',
        content,
        flags=re.IGNORECASE
    )

    # If it's in a gold card/section, ensure the text is dark
    if '.promise-card' in content:
        content = re.sub(
            r'(\.promise-card\s*\{[^}]*)',
            r'\1    color: #1f2937 !important;\n',
            content,
            flags=re.DOTALL
        )

    # Fix any gold background sections to have dark text
    content = re.sub(
        r'(background:\s*#F4A261[^}]*\})',
        lambda m: m.group(1).replace('}', '    color: #1f2937 !important;\n}') if 'color:' not in m.group(1) else m.group(1),
        content
    )

    # Specifically target areas-we-serve section
    if '</style>' in content and 'areas-we-serve' not in content.lower():
        css_addition = '''
/* Areas We Serve - dark text on gold */
.areas-we-serve h2,
.areas-we-serve h3,
h2:contains("Areas We Serve"),
h3:contains("Areas We Serve") {
    color: #1f2937 !important;
}

.promise-card h3,
.promise-card p,
.promise-card {
    color: #1f2937 !important;
}
'''
        content = content.replace('</style>', css_addition + '</style>')

    return content

# Process all HTML files
print("Fixing 'Areas We Serve' text color...")

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
        content = fix_areas_we_serve(content)
        with open(page, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {page}")

# Fix property-management index
pm_index = 'property-management/index.html'
if os.path.exists(pm_index):
    with open(pm_index, 'r', encoding='utf-8') as f:
        content = f.read()
    content = fix_areas_we_serve(content)
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
        content = fix_areas_we_serve(content)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {directory}")

print("\nAll 'Areas We Serve' text fixed - dark on gold!")