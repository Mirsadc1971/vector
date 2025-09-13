#!/usr/bin/env python3
"""
Color-only contrast fix - just replace color values, nothing else
"""

import re

# Read index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Color value replacements ONLY - no CSS, no structure changes
# These are direct color replacements for better contrast

# Fix gray text that's too light on dark backgrounds
content = content.replace('color: #475569', 'color: #9ca3af')  # Lighter gray for better contrast
content = content.replace('color: rgb(75, 85, 99)', 'color: rgb(156, 163, 175)')  # Same in RGB

# Fix light gray on light backgrounds (make darker)
content = content.replace('color: rgb(229, 231, 235)', 'color: rgb(71, 85, 105)')  # Much darker

# Fix green that's too light on dark backgrounds
content = content.replace('color: #16a34a', 'color: #22c55e')  # Brighter green

# Fix gray footer text
content = content.replace('color: rgb(107, 114, 128)', 'color: rgb(55, 65, 81)')  # Darker for footer

# Write back
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied color-only fixes:")
print("- #475569 → #9ca3af (gray text)")
print("- rgb(75, 85, 99) → rgb(156, 163, 175)")
print("- rgb(229, 231, 235) → rgb(71, 85, 105)")
print("- #16a34a → #22c55e (green)")
print("- rgb(107, 114, 128) → rgb(55, 65, 81)")
print("No CSS added, no structure changed - just color values")