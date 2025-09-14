#!/usr/bin/env python3
import os
import re

# Process all area pages
os.chdir('property-management')
dirs = [d for d in os.listdir('.') if os.path.isdir(d)]
print(f"Fixing hero images in {len(dirs)} area pages...")

for directory in dirs:
    file_path = os.path.join(directory, 'index.html')
    if not os.path.exists(file_path):
        continue

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix the hero image paths - use absolute paths to the main images folder
    content = re.sub(
        r"url\('images/manage369.*?'\)",
        "url('/images/buck4manage369_optimized.jpg')",
        content
    )

    # Also fix webp version
    content = re.sub(
        r"url\('images/manage369.*?\.webp'\)",
        "url('/images/buck4manage369_compressed.webp')",
        content
    )

    # Remove the dark overlay by making gradient much more transparent
    # Change from rgba(8,66,152,0.25) to rgba(8,66,152,0.05) for much lighter overlay
    content = re.sub(
        r'linear-gradient\(135deg, rgba\(8,66,152,0\.25\) 0%, rgba\(244,162,97,0\.25\) 100%\)',
        'linear-gradient(135deg, rgba(8,66,152,0.05) 0%, rgba(244,162,97,0.05) 100%)',
        content
    )

    # Add the hero section HTML if it's missing
    if 'class="hero-optimized"' not in content:
        # Find where to insert hero section (after header, before main content)
        header_end = content.find('</header>')
        if header_end != -1:
            hero_html = '''
<section class="hero-optimized">
    <div class="hero-content">
        <h1>''' + directory.replace('-', ' ').title() + ''' Property Management</h1>
        <p>Professional HOA, Condominium & Townhome Management Services</p>
    </div>
</section>
'''
            content = content[:header_end + 9] + hero_html + content[header_end + 9:]

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Fixed {directory}")

print("\nAll hero images fixed with correct paths and lighter overlay!")