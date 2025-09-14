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
    # Modify active link as needed for each page
    header_template = header_html.replace('class="nav-link active">Home', 'class="nav-link">Home')
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

# Get the mobile menu script
mobile_script = '''
<script>
function toggleMobileMenu() {
    const menu = document.getElementById("mobileMenu");
    menu.style.display = menu.style.display === "block" ? "none" : "block";
}
</script>
'''

# Process all area pages
os.chdir('property-management')
dirs = [d for d in os.listdir('.') if os.path.isdir(d)]
print(f"Updating header and footer in {len(dirs)} area pages...")

for directory in dirs:
    file_path = os.path.join(directory, 'index.html')
    if not os.path.exists(file_path):
        continue

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add universal sticky header CSS if not present
    if 'universal-sticky-header.css' not in content:
        content = content.replace('</head>', '<link rel="stylesheet" href="/assets/css/universal-sticky-header.css">\n</head>')

    # Replace existing header
    content = re.sub(r'<header.*?</header>', header_template, content, flags=re.DOTALL)

    # Replace existing footer
    content = re.sub(r'<footer.*?</footer>', footer_html, content, flags=re.DOTALL)

    # Add mobile menu script before closing body tag if not present
    if 'toggleMobileMenu' not in content:
        content = content.replace('</body>', mobile_script + '\n</body>')

    # Ensure body has padding for sticky header
    if 'body {' in content and 'padding-top:' not in content:
        content = re.sub(r'(body\s*{)', r'\1\n    padding-top: 60px;', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Updated {directory}")

print("\nAll pages now have universal header and footer!")