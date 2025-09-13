#!/usr/bin/env python3
"""
Safe contrast fixes - minimal changes to preserve design
"""

import re

# Read index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# MINIMAL, SAFE replacements - only fixing the worst contrast issues
replacements = [
    # Only darken the very light gray text that's unreadable
    (r'color:\s*#475569(?=[^"]*background:\s*rgb\(44,\s*62,\s*80\))', 'color: #94a3b8'),  # Only when on dark blue background
    (r'color:\s*#475569(?=[^"]*background:\s*rgb\(31,\s*41,\s*55\))', 'color: #94a3b8'),  # Only when on darker background

    # Fix the $500 BONUS text to be more visible
    (r'background:\s*rgb\(244,\s*162,\s*97\)([^}]*\$500 BONUS)', r'background: rgb(244, 162, 97); color: #1e293b\1'),

    # Make the green text slightly darker for better contrast
    (r'color:\s*#16a34a;', 'color: #059669;'),  # Slightly darker green
]

# Apply minimal replacements
for old, new in replacements:
    content = re.sub(old, new, content, flags=re.IGNORECASE)

# Add very targeted CSS fixes that won't break the design
targeted_fixes = """
<style>
/* Minimal Contrast Fixes - Preserving Original Design */

/* Fix only the specific problem areas identified by Lighthouse */

/* Fix gray text specifically in offer cards on dark backgrounds */
div[style*="background: rgb(44, 62, 80)"] span[style*="color: #475569"] {
    color: #cbd5e1 !important; /* Light gray for dark backgrounds only */
}

div[style*="background: rgb(31, 41, 55)"] span {
    color: #e2e8f0 !important; /* Ensure readability on very dark backgrounds */
}

/* Fix the referral section text */
div[style*="background: rgb(44, 62, 80)"] div[style*="color: #475569"] {
    color: #94a3b8 !important;
}

/* Ensure the green checkmarks are visible */
div[style*="background: rgb(44, 62, 80)"] div[style*="color: #16a34a"] {
    color: #10b981 !important; /* Brighter green for dark background */
}

/* Fix footer location links - make them more visible */
a[href*="property-management/"][style*="background: rgb(240, 244, 248)"] {
    color: #1e293b !important; /* Dark text on light background */
}

/* Keep focus indicators for accessibility */
a:focus, button:focus {
    outline: 2px solid #F4A261 !important;
    outline-offset: 2px !important;
}

/* Don't change the main design colors - keep brand identity */
/* Only fix the specific contrast failures */
</style>
"""

# Add targeted fixes right before </head>
content = content.replace('</head>', targeted_fixes + '\n</head>')

# Write back
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied SAFE contrast fixes:")
print("- Only fixed specific failing elements")
print("- Preserved original design and brand colors")
print("- Maintained visual hierarchy")
print("- Fixed readability issues without breaking layout")