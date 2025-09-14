#!/usr/bin/env python3
"""
Remove colored borders from FAQ sections and other elements
"""

import os
import re
from pathlib import Path

def remove_colored_borders(file_path):
    """Remove colored borders from a single HTML file"""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Remove colored border-left styles
    patterns_to_remove = [
        r'border-left:\s*4px\s+solid\s+#[0-9a-fA-F]{3,6}[^;]*;?',
        r'border-left:\s*\d+px\s+solid\s+#[0-9a-fA-F]{3,6}[^;]*;?',
        r'border-left-color:\s*#[0-9a-fA-F]{3,6}[^;]*;?',
    ]

    for pattern in patterns_to_remove:
        content = re.sub(pattern, '', content, flags=re.IGNORECASE)

    # Remove any empty style attributes that might be left
    content = re.sub(r'style="\s*"', '', content)

    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[CLEANED] {file_path}")
        return True

    return False

def main():
    """Remove colored borders from all HTML files"""

    print("Removing colored borders from all HTML files...")
    print("=" * 60)

    fixed_count = 0
    checked_count = 0

    # Check all HTML files in project
    for file in Path('.').rglob('*.html'):
        if file.is_file() and not str(file).endswith('.backup'):
            checked_count += 1
            if remove_colored_borders(file):
                fixed_count += 1

    print("=" * 60)
    print(f"Process complete!")
    print(f"Files checked: {checked_count}")
    print(f"Files cleaned: {fixed_count}")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)) or '.')
    main()