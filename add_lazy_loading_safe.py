#!/usr/bin/env python3
"""
Safe Lazy Loading Script for Manage369
Only adds loading="lazy" attribute to images without restructuring HTML
"""

import re
from pathlib import Path

def add_lazy_loading_simple(file_path):
    """Add lazy loading to images without changing HTML structure"""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    modified = False

    # Pattern to find img tags without loading attribute
    # This regex preserves the exact structure
    pattern = r'(<img\s+)([^>]*?)(/?>)'

    def replace_img(match):
        nonlocal modified
        start = match.group(1)
        attrs = match.group(2)
        end = match.group(3)

        # Check if loading attribute already exists
        if 'loading=' not in attrs:
            # Add loading="lazy" before the closing bracket
            modified = True
            return f'{start}{attrs} loading="lazy"{end}'
        return match.group(0)

    # Apply replacement
    content = re.sub(pattern, replace_img, content)

    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """Process key HTML files only"""

    # Process only main files to be safe
    key_files = [
        'index.html',
        'services.html',
        'contact.html',
        'property-management-near-me.html',
        'property-management-cost-guide.html',
        'chicago-property-management-companies.html'
    ]

    print("Adding lazy loading to key pages...")
    print("=" * 50)

    modified_count = 0
    for file_name in key_files:
        file_path = Path(file_name)
        if file_path.exists():
            print(f"Processing: {file_name}")
            if add_lazy_loading_simple(file_path):
                modified_count += 1
                print(f"  [ADDED LAZY LOADING] to {file_name}")
            else:
                print(f"  - Already optimized or no images in {file_name}")
        else:
            print(f"  - File not found: {file_name}")

    print(f"\nCompleted! Modified {modified_count} files.")
    print("\nChanges made:")
    print("- Added loading='lazy' attribute to img tags")
    print("- No HTML structure changes")
    print("- No formatting changes")

if __name__ == "__main__":
    main()