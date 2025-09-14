#!/usr/bin/env python3
import os
import re

def apply_homepage_colors(filepath):
    """Apply exact homepage color scheme to HTML file"""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    original_content = content

    # Homepage color scheme
    # Primary: #F4A261 (gold/orange)
    # Secondary: #2C3E50 (dark blue-gray)
    # Background: #1f2937 (dark gray)
    # Text: #e5e7eb (light gray)
    # Accent: #084298 (deep blue)

    # Replace ALL background colors with homepage dark gray
    patterns = [
        # Replace any hex background colors with homepage background
        (r'background:\s*#[0-9a-fA-F]{3,6}(?![\da-fA-F])', 'background: #1f2937'),
        (r'background-color:\s*#[0-9a-fA-F]{3,6}(?![\da-fA-F])', 'background-color: #1f2937'),
        # Keep #2C3E50 for cards/sections that need contrast
        (r'background:\s*#2C3E50', 'background: #2C3E50'),
        (r'background-color:\s*#2C3E50', 'background-color: #2C3E50'),
    ]

    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

    # Fix body background specifically
    content = re.sub(
        r'<body([^>]*?)style="([^"]*?)background:\s*#[0-9a-fA-F]{3,6}([^"]*?)"',
        r'<body\1style="\2background: #1f2937\3"',
        content
    )

    # Ensure body has correct colors if no style exists
    if '<body' in content and 'style=' not in content.split('<body')[1].split('>')[0]:
        content = re.sub(r'<body([^>]*?)>', r'<body\1 style="background: #1f2937; color: #e5e7eb;">', content)

    # Update text colors to homepage light gray
    content = re.sub(r'color:\s*#333(?:333)?(?![\da-fA-F])', 'color: #e5e7eb', content)
    content = re.sub(r'color:\s*#000(?:000)?(?![\da-fA-F])', 'color: #e5e7eb', content)
    content = re.sub(r'color:\s*#666(?:666)?(?![\da-fA-F])', 'color: #e5e7eb', content)
    content = re.sub(r'color:\s*#999(?:999)?(?![\da-fA-F])', 'color: #e5e7eb', content)

    # Ensure all headings use gold color
    for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        # Add color to headings without style
        content = re.sub(
            f'<{tag}([^>]*?)>(?![^<]*style=)',
            f'<{tag}\\1 style="color: #F4A261;">',
            content
        )
        # Update existing heading colors
        content = re.sub(
            f'<{tag}([^>]*?)style="([^"]*?)color:\\s*#[0-9a-fA-F]{{3,6}}([^"]*?)"',
            f'<{tag}\\1style="\\2color: #F4A261\\3"',
            content
        )

    # Add CSS variables to head if not present
    if ':root {' not in content and '</head>' in content:
        css_vars = """
<style>
/* Homepage Color Scheme */
:root {
    --primary-gold: #F4A261;
    --primary-navy: #2C3E50;
    --background-dark: #1f2937;
    --text-light: #e5e7eb;
    --accent-blue: #084298;
}

body {
    background: var(--background-dark) !important;
    color: var(--text-light) !important;
}

h1, h2, h3, h4, h5, h6 {
    color: var(--primary-gold) !important;
}

.service-card, .card {
    background: var(--primary-navy) !important;
    color: var(--text-light) !important;
}

.btn-primary {
    background: var(--primary-gold) !important;
    color: #1f2937 !important;
}

section {
    background: var(--background-dark) !important;
}

a {
    color: var(--primary-gold);
}

a:hover {
    color: #F4A261;
    opacity: 0.8;
}
</style>
"""
        content = content.replace('</head>', css_vars + '</head>')

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8', errors='ignore') as f:
            f.write(content)
        return True
    return False

def main():
    os.chdir('C:\\Users\\mirsa\\Documents\\manage369-live')

    # Focus on property-management directory
    pm_files = []
    pm_dir = 'property-management'

    if os.path.exists(pm_dir):
        for root, dirs, files in os.walk(pm_dir):
            for f in files:
                if f.endswith('.html'):
                    filepath = os.path.join(root, f)
                    pm_files.append(filepath)

    print(f"Found {len(pm_files)} HTML files in property-management directory")

    fixed_count = 0
    for filepath in pm_files:
        try:
            if apply_homepage_colors(filepath):
                fixed_count += 1
                print(f"Fixed: {filepath}")
        except Exception as e:
            print(f"Error processing {filepath}: {e}")

    print(f"\nApplied homepage colors to {fixed_count} files")

if __name__ == "__main__":
    main()