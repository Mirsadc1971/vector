#!/usr/bin/env python3
"""
Fix all service page links to use directory URLs instead of index.html
This ensures compatibility with web servers that don't automatically serve index.html
"""

import os
import re
import sys
from pathlib import Path

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

def fix_service_links_in_file(filepath):
    """Fix service links in a single file."""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Pattern to find service links with index.html
    service_patterns = [
        # Fix absolute paths
        (r'href="(/services/[^"]+/)index\.html"', r'href="\1"'),
        # Fix relative paths with services/
        (r'href="((?:\.\./)*services/[^"]+/)index\.html"', r'href="\1"'),
        # Fix src attributes for any service references
        (r'src="((?:\.\./)*services/[^"]+/)index\.html"', r'src="\1"'),
    ]
    
    for pattern, replacement in service_patterns:
        content = re.sub(pattern, replacement, content)
    
    # Count changes
    changes = 0
    if content != original_content:
        changes = len(re.findall(r'/index\.html"', original_content)) - len(re.findall(r'/index\.html"', content))
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return changes

def main():
    """Fix service links across the entire site."""
    
    print("🔧 Fixing service page links across the site...")
    print("=" * 60)
    
    total_changes = 0
    files_updated = 0
    
    # Process all HTML files
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories and version control
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
        
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                
                changes = fix_service_links_in_file(filepath)
                
                if changes > 0:
                    total_changes += changes
                    files_updated += 1
                    relative_path = os.path.relpath(filepath, '.')
                    print(f"✅ Updated {relative_path}: {changes} links fixed")
    
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"✅ Files updated: {files_updated}")
    print(f"🔗 Total links fixed: {total_changes}")
    
    if total_changes > 0:
        print("\n✨ Service links have been fixed to use directory URLs!")
        print("🚀 These changes ensure compatibility with web servers.")
    else:
        print("\n✅ No service links needed fixing.")

if __name__ == "__main__":
    main()