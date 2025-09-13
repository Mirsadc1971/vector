#!/usr/bin/env python3
"""
Fix Areas We Serve page - change white backgrounds to dark blue
"""

# Read the property-management index.html
with open('property-management/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace white backgrounds with dark blue
content = content.replace('background: white;', 'background: #2C3E50;')
content = content.replace('background: #fff;', 'background: #2C3E50;')
content = content.replace('background: #ffffff;', 'background: #2C3E50;')
content = content.replace('background-color: white;', 'background-color: #2C3E50;')
content = content.replace('background-color: #fff;', 'background-color: #2C3E50;')
content = content.replace('background-color: #ffffff;', 'background-color: #2C3E50;')

# Fix text that might be dark on dark background - make it gold or light
content = content.replace('color: #333;', 'color: #F4A261;')
content = content.replace('color: #000;', 'color: #e5e7eb;')
content = content.replace('color: black;', 'color: #e5e7eb;')

# Fix the gradient overlays to use gold instead of white
content = content.replace('rgba(255,255,255,0.3)', 'rgba(244,162,97,0.3)')
content = content.replace('rgba(255, 255, 255, 0.3)', 'rgba(244, 162, 97, 0.3)')

# Write back
with open('property-management/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed Areas We Serve page colors:")
print("- Changed all white backgrounds to dark blue (#2C3E50)")
print("- Updated text colors for contrast (gold #F4A261 and light gray #e5e7eb)")
print("- Fixed gradient overlays to use gold instead of white")