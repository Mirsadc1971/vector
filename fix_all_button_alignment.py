#!/usr/bin/env python3
import os
import re

def fix_buttons_in_file(file_path):
    """Fix button alignment in a single file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix 3-button group alignment (Get Directions, Find on Google, Leave Review)
    if 'button-group' in content:
        # Ensure button group uses flexbox
        if '.button-group {' in content:
            content = re.sub(
                r'\.button-group\s*\{[^}]*\}',
                '''.button-group {
    display: flex !important;
    gap: 15px !important;
    justify-content: center !important;
    align-items: center !important;
    flex-wrap: wrap !important;
    margin: 30px 0 !important;
}''',
                content,
                flags=re.DOTALL
            )
        else:
            # Add button-group CSS if missing
            content = content.replace('</style>', '''
.button-group {
    display: flex !important;
    gap: 15px !important;
    justify-content: center !important;
    align-items: center !important;
    flex-wrap: wrap !important;
    margin: 30px 0 !important;
}
</style>''')

    # Fix service area buttons alignment
    if 'service-areas' in content or 'area-grid' in content:
        # Ensure area grid uses proper grid
        if '.area-grid {' not in content and '.service-areas' in content:
            content = content.replace('</style>', '''
.service-areas {
    display: grid !important;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)) !important;
    gap: 15px !important;
    margin: 40px 0 !important;
}

.service-area-button, .area-link {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    padding: 15px 20px !important;
    min-height: 50px !important;
    text-align: center !important;
}
</style>''')

    # Fix CTA buttons alignment
    if '.cta-button' in content:
        content = re.sub(
            r'\.cta-button\s*\{([^}]*)\}',
            lambda m: '.cta-button {' + m.group(1) + '''
    display: inline-block !important;
    text-align: center !important;
    min-width: 200px !important;
}''',
            content,
            flags=re.DOTALL
        )

    # Fix general button alignment
    content = re.sub(
        r'(\.btn[^{]*\{[^}]*)',
        lambda m: m.group(1) + '''
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;''',
        content,
        flags=re.DOTALL
    )

    return content

# Process all HTML files
print("Fixing button alignment across entire site...")

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
        content = fix_buttons_in_file(page)
        with open(page, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {page}")

# Fix property-management index
pm_index = 'property-management/index.html'
if os.path.exists(pm_index):
    content = fix_buttons_in_file(pm_index)
    with open(pm_index, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed {pm_index}")

# Fix all area pages
os.chdir('property-management')
dirs = [d for d in os.listdir('.') if os.path.isdir(d)]

for directory in dirs:
    file_path = os.path.join(directory, 'index.html')
    if os.path.exists(file_path):
        content = fix_buttons_in_file(file_path)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {directory}")

print("\nAll button alignment fixed across entire site!")