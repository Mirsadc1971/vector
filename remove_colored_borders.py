#!/usr/bin/env python3
import os
import re

def remove_colored_borders(content):
    """Remove red and green borders from cards"""

    # Remove any red borders
    content = re.sub(r'border:\s*[^;]*red[^;]*;', 'border: 1px solid rgba(244, 162, 97, 0.3);', content, flags=re.IGNORECASE)
    content = re.sub(r'border:\s*[^;]*#ff0000[^;]*;', 'border: 1px solid rgba(244, 162, 97, 0.3);', content, flags=re.IGNORECASE)
    content = re.sub(r'border:\s*[^;]*#f00[^;]*;', 'border: 1px solid rgba(244, 162, 97, 0.3);', content, flags=re.IGNORECASE)

    # Remove any green borders
    content = re.sub(r'border:\s*[^;]*green[^;]*;', 'border: 1px solid rgba(244, 162, 97, 0.3);', content, flags=re.IGNORECASE)
    content = re.sub(r'border:\s*[^;]*#00ff00[^;]*;', 'border: 1px solid rgba(244, 162, 97, 0.3);', content, flags=re.IGNORECASE)
    content = re.sub(r'border:\s*[^;]*#0f0[^;]*;', 'border: 1px solid rgba(244, 162, 97, 0.3);', content, flags=re.IGNORECASE)
    content = re.sub(r'border:\s*[^;]*#008000[^;]*;', 'border: 1px solid rgba(244, 162, 97, 0.3);', content, flags=re.IGNORECASE)

    # Remove any thick colored borders (3px or more)
    content = re.sub(r'border:\s*[3-9]px[^;]*;', 'border: 1px solid rgba(244, 162, 97, 0.3);', content)

    # Remove border-left/right/top/bottom colored lines
    content = re.sub(r'border-left:\s*[^;]*(?:red|green|#ff0000|#00ff00|#f00|#0f0)[^;]*;', '', content, flags=re.IGNORECASE)
    content = re.sub(r'border-right:\s*[^;]*(?:red|green|#ff0000|#00ff00|#f00|#0f0)[^;]*;', '', content, flags=re.IGNORECASE)
    content = re.sub(r'border-top:\s*[^;]*(?:red|green|#ff0000|#00ff00|#f00|#0f0)[^;]*;', '', content, flags=re.IGNORECASE)
    content = re.sub(r'border-bottom:\s*[^;]*(?:red|green|#ff0000|#00ff00|#f00|#0f0)[^;]*;', '', content, flags=re.IGNORECASE)

    return content

# Process all HTML files
print("Removing red and green borders from cards...")

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
        content = remove_colored_borders(content)
        with open(page, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {page}")

# Fix property-management index
pm_index = 'property-management/index.html'
if os.path.exists(pm_index):
    with open(pm_index, 'r', encoding='utf-8') as f:
        content = f.read()
    content = remove_colored_borders(content)
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
        content = remove_colored_borders(content)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {directory}")

print("\nRemoved all red and green borders!")