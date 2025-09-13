#!/usr/bin/env python3
"""
Fix navigation menu alignment - ensure it's properly positioned
"""

import re
from pathlib import Path

def fix_nav_in_file(filepath):
    """Fix navigation alignment in HTML file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix navigation CSS
    nav_fix = """
/* Fix Navigation Alignment */
.header {
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    padding: 1rem 2rem !important;
}

.logo {
    flex-shrink: 0 !important;
}

.nav {
    display: flex !important;
    align-items: center !important;
    gap: 0 !important;
    margin: 0 auto !important;
    justify-content: center !important;
}

.header-cta {
    flex-shrink: 0 !important;
    margin-left: auto !important;
}

/* Mobile menu fix */
.mobile-menu-toggle {
    margin-left: auto !important;
}

/* Remove any conflicting styles */
nav {
    position: static !important;
    transform: none !important;
    margin: 0 !important;
}
"""

    # Add nav fix CSS if not present
    if 'Fix Navigation Alignment' not in content:
        content = content.replace('</head>', f'<style>\n{nav_fix}\n</style>\n</head>')

    # Fix any shifted nav elements
    content = re.sub(r'margin-left:\s*auto\s*!important;\s*margin-left:\s*auto\s*!important;',
                     'margin-left: auto !important;', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return True

def main():
    # Process all HTML files
    html_files = list(Path('.').glob('**/*.html'))

    # Filter out system directories
    html_files = [f for f in html_files if not any(
        part in str(f) for part in ['.git', 'node_modules', '_site', 'dist', 'index.html.backup']
    )]

    print(f"Fixing navigation alignment in {len(html_files)} files...")

    modified = 0
    for filepath in html_files:
        if fix_nav_in_file(filepath):
            modified += 1
            print(f"  Fixed: {filepath}")

    print(f"\nCompleted! Fixed {modified} files")
    print("Navigation should now be properly centered")

if __name__ == "__main__":
    main()