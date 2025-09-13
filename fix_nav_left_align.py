#!/usr/bin/env python3
"""
Fix navigation - move it back to proper left/center alignment
"""

import re
from pathlib import Path

def fix_nav_alignment(filepath):
    """Fix navigation to be properly aligned"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove the bad nav centering that pushes it right
    content = content.replace('margin: 0 auto !important;', 'margin: 0 !important;')
    content = content.replace('justify-content: center !important;', 'justify-content: flex-start !important;')

    # Replace the navigation fix with correct alignment
    nav_fix = """
/* Fix Navigation Layout - Proper Alignment */
.header {
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    padding: 1rem 2rem !important;
}

.logo {
    flex: 0 0 auto !important;
    margin-right: 2rem !important;
}

.nav {
    display: flex !important;
    align-items: center !important;
    gap: 0 !important;
    flex: 1 1 auto !important;
    justify-content: flex-start !important;
    margin-left: 0 !important;
}

.header-cta {
    flex: 0 0 auto !important;
    margin-left: 2rem !important;
}

/* Ensure nav links stay together */
.nav-link {
    white-space: nowrap !important;
}

.dropdown {
    position: relative !important;
}

/* Mobile menu stays on right */
.mobile-menu-toggle {
    margin-left: auto !important;
}

/* Remove conflicting styles */
nav {
    position: static !important;
    transform: none !important;
}
"""

    # Replace the old fix with the new one
    if 'Fix Navigation Alignment' in content:
        # Find and replace the entire style block
        pattern = r'/\* Fix Navigation Alignment \*/.*?(?=/\*|</style>)'
        content = re.sub(pattern, nav_fix, content, flags=re.DOTALL)
    elif 'Fix Navigation Layout' not in content:
        # Add it if not present
        content = content.replace('</head>', f'<style>\n{nav_fix}\n</style>\n</head>')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return True

def main():
    # Process all HTML files
    html_files = list(Path('.').glob('**/*.html'))

    # Filter out system directories
    html_files = [f for f in html_files if not any(
        part in str(f) for part in ['.git', 'node_modules', '_site', 'dist', 'backup']
    )]

    print(f"Fixing navigation alignment in {len(html_files)} files...")

    modified = 0
    for filepath in html_files:
        if fix_nav_alignment(filepath):
            modified += 1

    print(f"\nCompleted! Fixed {modified} files")
    print("\nLayout fixed to:")
    print("[LOGO] [NAV ITEMS LEFT-ALIGNED] --------- [PHONE BUTTON]")

if __name__ == "__main__":
    main()