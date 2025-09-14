#!/usr/bin/env python3
import os
import re

# CSS to add for proper service card alignment
service_card_css = '''
/* Fix the service cards grid layout */
.services-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
}

/* Make all cards equal height */
.service-card {
    display: flex;
    flex-direction: column;
    min-height: 300px;
    padding: 2rem;
}

/* Push buttons to bottom of cards */
.service-card .btn {
    margin-top: auto;
    align-self: center;
}

/* Fix the 6-card bottom section */
.complete-services-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
    max-width: 1200px;
    margin: 2rem auto;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
    .services-grid,
    .complete-services-grid {
        grid-template-columns: 1fr;
    }
}
'''

def fix_service_cards(file_path):
    """Fix service card grid in a single file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove old service-grid CSS if exists
    content = re.sub(r'\.services-grid\s*\{[^}]*\}', '', content, flags=re.DOTALL)
    content = re.sub(r'\.service-card\s*\{[^}]*\}', '', content, flags=re.DOTALL)
    content = re.sub(r'\.complete-services-grid\s*\{[^}]*\}', '', content, flags=re.DOTALL)

    # Add new CSS before closing style tag
    if '</style>' in content:
        content = content.replace('</style>', service_card_css + '\n</style>')

    return content

# Process all HTML files
print("Fixing service card grids across entire site...")

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
        content = fix_service_cards(page)
        with open(page, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {page}")

# Fix property-management index
pm_index = 'property-management/index.html'
if os.path.exists(pm_index):
    content = fix_service_cards(pm_index)
    with open(pm_index, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed {pm_index}")

# Fix all area pages
os.chdir('property-management')
dirs = [d for d in os.listdir('.') if os.path.isdir(d)]

for directory in dirs:
    file_path = os.path.join(directory, 'index.html')
    if os.path.exists(file_path):
        content = fix_service_cards(file_path)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {directory}")

print("\nAll service card grids fixed across entire site!")