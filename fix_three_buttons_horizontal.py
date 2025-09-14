#!/usr/bin/env python3
import os
import re

def fix_three_buttons(content):
    """Fix the 3 buttons (Get Directions, Find on Google, Leave Review) to be horizontal"""

    # Find the section with the 3 buttons
    pattern = r'(🚗.*?Get Directions.*?</a>)(.*?)(🔍.*?Find on Google.*?</a>)(.*?)(⭐.*?Leave.*?Review.*?</a>)'

    def replace_buttons(match):
        button1 = match.group(1)
        button2 = match.group(3)
        button3 = match.group(5)

        # Wrap in a flex container
        return f'''<div style="display: flex !important; gap: 15px !important; justify-content: center !important; align-items: center !important; flex-wrap: wrap !important; margin: 30px 0 !important;">
                        {button1}
                        {button2}
                        {button3}
                    </div>'''

    content = re.sub(pattern, replace_buttons, content, flags=re.DOTALL)

    # Also add CSS for button-group class if it exists
    if '</style>' in content:
        if '.button-group' not in content:
            content = content.replace('</style>', '''
.button-group {
    display: flex !important;
    gap: 15px !important;
    justify-content: center !important;
    align-items: center !important;
    flex-wrap: wrap !important;
    margin: 30px 0 !important;
}

.button-group a {
    display: inline-flex !important;
    align-items: center !important;
    white-space: nowrap !important;
}
</style>''')
        else:
            # Update existing button-group CSS
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

    return content

# Process all HTML files
print("Fixing 3 buttons to be horizontal...")

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
        content = fix_three_buttons(content)
        with open(page, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {page}")

# Fix property-management index
pm_index = 'property-management/index.html'
if os.path.exists(pm_index):
    with open(pm_index, 'r', encoding='utf-8') as f:
        content = f.read()
    content = fix_three_buttons(content)
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
        content = fix_three_buttons(content)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {directory}")

print("\n3 buttons now horizontal!")