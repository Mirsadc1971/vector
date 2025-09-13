#!/usr/bin/env python3
"""
Apply consistent color scheme from homepage to ALL pages
Dark blue (#2C3E50, #1f2937, #1a252f) and Gold (#F4A261)
"""

import os
from pathlib import Path

# Consistent color scheme based on homepage
COLOR_RULES = """
/* MANAGE369 CONSISTENT COLOR SCHEME */
body {
    background: #1a252f !important;
    color: #e5e7eb !important;
}

section {
    background: #1f2937 !important;
    color: #e5e7eb !important;
}

.header, header, nav {
    background: #2C3E50 !important;
}

h1, h2, h3, h4, h5, h6 {
    color: #F4A261 !important;
}

.card, .area-card, .service-card {
    background: #2C3E50 !important;
    color: #e5e7eb !important;
    border: 1px solid #374151 !important;
}

.card:hover, .area-card:hover, .service-card:hover {
    border-color: #F4A261 !important;
}

a {
    color: #F4A261 !important;
}

.btn, button {
    background: linear-gradient(135deg, #084298 0%, #F4A261 100%) !important;
    color: white !important;
}

footer {
    background: #2C3E50 !important;
    color: #e5e7eb !important;
}

/* Remove any white backgrounds */
[style*="background: white"],
[style*="background: #fff"],
[style*="background: #ffffff"],
[style*="background-color: white"],
[style*="background-color: #fff"],
[style*="background-color: #ffffff"] {
    background: #2C3E50 !important;
}
"""

def fix_html_file(filepath):
    """Apply consistent colors to HTML file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace white backgrounds
    replacements = [
        ('background: white', 'background: #2C3E50'),
        ('background: #fff', 'background: #2C3E50'),
        ('background: #ffffff', 'background: #2C3E50'),
        ('background-color: white', 'background-color: #2C3E50'),
        ('background-color: #fff', 'background-color: #2C3E50'),
        ('background-color: #ffffff', 'background-color: #2C3E50'),
        ('background: rgb(255, 255, 255)', 'background: #2C3E50'),
        ('background: rgb(248, 249, 250)', 'background: #1f2937'),
        ('background: rgb(243, 244, 246)', 'background: #1f2937'),

        # Fix text colors for dark backgrounds
        ('color: #333', 'color: #e5e7eb'),
        ('color: #000', 'color: #e5e7eb'),
        ('color: black', 'color: #e5e7eb'),
        ('color: rgb(0, 0, 0)', 'color: #e5e7eb'),

        # Ensure headers are gold
        ('color: #ff6b35', 'color: #F4A261'),
        ('color: orange', 'color: #F4A261'),
    ]

    for old, new in replacements:
        content = content.replace(old, new)

    # Add consistent color scheme if not present
    if 'MANAGE369 CONSISTENT COLOR SCHEME' not in content:
        # Add before </head>
        content = content.replace('</head>', f'<style>\n{COLOR_RULES}\n</style>\n</head>')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return True

def main():
    # Process all HTML files
    html_files = list(Path('.').glob('**/*.html'))

    # Filter out system directories
    html_files = [f for f in html_files if not any(
        part in str(f) for part in ['.git', 'node_modules', '_site', 'dist']
    )]

    print(f"Applying consistent color scheme to {len(html_files)} HTML files...")

    modified = 0
    for filepath in html_files:
        if fix_html_file(filepath):
            modified += 1
            print(f"  [DONE] {filepath}")

    print(f"\nCompleted! Modified {modified} files")
    print("\nConsistent color scheme applied:")
    print("- Background: Dark blue gradient (#1a252f → #1f2937 → #2C3E50)")
    print("- Headers: Gold (#F4A261)")
    print("- Text: Light gray (#e5e7eb)")
    print("- Links: Gold (#F4A261)")
    print("- Buttons: Blue to gold gradient")
    print("- NO white backgrounds")

if __name__ == "__main__":
    main()