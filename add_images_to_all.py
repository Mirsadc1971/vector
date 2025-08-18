"""
Add hero images to all pages missing them
"""

import os
import re

# Pages and their assigned images
pages_to_update = {
    'legal-disclaimers.html': 'kenmore2manage369.jpg',
    'privacy-policy.html': 'chestnutmanage369.jpg', 
    'terms-of-service.html': 'buck4manage369.jpg',
    'sitemap.html': 'manage369widowview.jpg',
    'accessibility.html': 'northfield1manage369.jpg',
    'payment-methods.html': 'manage369randolphstation.jpg',
    'emergency-property-management-chicago.html': 'Manage3693.jpg',
    'property-management-near-me.html': 'chestnut2manage369.jpg',
    'property-management-cost-guide.html': 'manage369bedroom1740maplewood.jpg',
    'chicago-property-management-companies.html': 'chestnutmanage3692.jpg'
}

for filename, image in pages_to_update.items():
    filepath = f'C:\\Users\\mirsa\\manage369-live\\{filename}'
    
    if not os.path.exists(filepath):
        print(f"SKIP: {filename} not found")
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find hero section with just gradient and add image
    pattern = r'(\.hero\s*\{[^}]*background:\s*linear-gradient[^;]+);'
    replacement = rf'\1, url("images/{image}"); background-size: cover; background-position: center;'
    
    if re.search(pattern, content):
        content = re.sub(pattern, replacement, content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {filename} with {image}")
    else:
        print(f"No hero gradient found in {filename}")

print("Done!")