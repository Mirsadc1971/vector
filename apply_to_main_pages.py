#!/usr/bin/env python3
import os
import re

# Read the homepage to get header and footer
with open('index.html', 'r', encoding='utf-8') as f:
    homepage = f.read()

# Extract header section from homepage
header_match = re.search(r'(<header class="header".*?</header>)', homepage, re.DOTALL)
if header_match:
    header_html = header_match.group(1)
else:
    print("Could not find header in homepage")
    exit()

# Extract footer section from homepage
footer_match = re.search(r'(<footer.*?</footer>)', homepage, re.DOTALL)
if footer_match:
    footer_html = footer_match.group(1)
else:
    print("Could not find footer in homepage")
    exit()

# Mobile menu script
mobile_script = '''
<script>
function toggleMobileMenu() {
    const menu = document.getElementById("mobileMenu");
    menu.style.display = menu.style.display === "block" ? "none" : "block";
}
</script>
'''

# List of main pages to update
main_pages = [
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

print(f"Updating header and footer in main pages...")

for page in main_pages:
    if not os.path.exists(page):
        print(f"Skipping {page} - not found")
        continue

    with open(page, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add universal sticky header CSS if not present
    if 'universal-sticky-header.css' not in content:
        content = content.replace('</head>', '<link rel="stylesheet" href="/assets/css/universal-sticky-header.css">\n</head>')

    # Replace existing header
    content = re.sub(r'<header.*?</header>', header_html, content, flags=re.DOTALL)

    # Replace existing footer
    content = re.sub(r'<footer.*?</footer>', footer_html, content, flags=re.DOTALL)

    # Add mobile menu script if not present
    if 'toggleMobileMenu' not in content:
        content = content.replace('</body>', mobile_script + '\n</body>')

    # Update active nav link based on page
    if page == 'services.html':
        content = content.replace('class="nav-link">Home', 'class="nav-link">Home')
        content = content.replace('class="nav-link dropdown-trigger">Services', 'class="nav-link active dropdown-trigger">Services')
    elif page == 'contact.html':
        content = content.replace('class="nav-link">Contact', 'class="nav-link active">Contact')
    elif page in ['pay-dues.html', 'payment-methods.html']:
        content = content.replace('class="nav-link">Pay Dues', 'class="nav-link active">Pay Dues')

    with open(page, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Updated {page}")

print("\nAll main pages updated with universal header and footer!")