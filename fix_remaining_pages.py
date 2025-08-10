#!/usr/bin/env python3
"""
Fix the remaining 21 pages that need CSS styling
These pages have a different structure and need special handling
"""

import os
import re
from pathlib import Path

def fix_page_css(file_path):
    """Fix CSS link for pages with different structure"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has the CSS
    if 'property-content-styles.css' in content:
        return False, "Already has CSS"
    
    # Try different patterns to find where to add CSS
    patterns = [
        # Pattern 1: After any existing CSS file
        (r'(<link rel="stylesheet" href="[^"]+\.css">)', r'\1\n    <link rel="stylesheet" href="../../css/property-content-styles.css">'),
        # Pattern 2: Before closing head tag if no CSS found
        (r'(</head>)', r'    <link rel="stylesheet" href="../../css/property-content-styles.css">\n\1'),
        # Pattern 3: After meta tags
        (r'(<meta[^>]+>\s*\n)(?=\s*<)', r'\1    <link rel="stylesheet" href="../../css/property-content-styles.css">\n'),
    ]
    
    modified = False
    for pattern, replacement in patterns:
        if re.search(pattern, content):
            new_content = re.sub(pattern, replacement, content, count=1)
            if new_content != content:
                content = new_content
                modified = True
                break
    
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, "CSS added successfully"
    
    return False, "Could not find place to add CSS"

def main():
    """Main function to fix remaining pages"""
    
    print("Fixing remaining pages with CSS styling...")
    print("=" * 50)
    
    # Path to property-management directory
    prop_mgmt_dir = Path('property-management')
    
    if not prop_mgmt_dir.exists():
        print("Error: property-management directory not found!")
        return
    
    # List of pages that need fixing (from previous run)
    pages_to_fix = [
        'portage-park', 'prospect-heights', 'pulaski-park', 'ravenswood',
        'rogers-park', 'rolling-meadows', 'sauganash', 'schiller-park',
        'skokie', 'south-loop', 'streeterville', 'the-glen',
        'uptown', 'vernon-hills', 'west-loop', 'west-ridge',
        'wheeling', 'wicker-park', 'wilmette', 'winnetka', 'wood-dale'
    ]
    
    fixed_count = 0
    error_count = 0
    
    print(f"Processing {len(pages_to_fix)} pages...")
    print("-" * 50)
    
    for page_name in pages_to_fix:
        page_dir = prop_mgmt_dir / page_name
        index_file = page_dir / 'index.html'
        
        if index_file.exists():
            print(f"\nProcessing: {page_name}")
            success, message = fix_page_css(index_file)
            
            if success:
                print(f"  [FIXED] {message}")
                fixed_count += 1
            else:
                print(f"  [INFO] {message}")
                if "Could not" in message:
                    error_count += 1
        else:
            print(f"\n[ERROR] Page not found: {page_name}")
            error_count += 1
    
    # Now check ALL pages to make sure we got everything
    print("\n" + "=" * 50)
    print("Verifying all pages...")
    
    all_locations = [d for d in prop_mgmt_dir.iterdir() if d.is_dir()]
    total_with_css = 0
    total_pages = 0
    
    for location_dir in sorted(all_locations):
        index_file = location_dir / 'index.html'
        if index_file.exists():
            total_pages += 1
            with open(index_file, 'r', encoding='utf-8') as f:
                if 'property-content-styles.css' in f.read():
                    total_with_css += 1
    
    print(f"\nFinal Status:")
    print(f"  Total pages: {total_pages}")
    print(f"  Pages with CSS: {total_with_css}")
    print(f"  Pages without CSS: {total_pages - total_with_css}")
    print(f"\n  Fixed in this run: {fixed_count}")
    print(f"  Errors: {error_count}")
    
    if total_pages - total_with_css == 0:
        print("\n✓ SUCCESS: All pages now have CSS styling!")
    else:
        print(f"\n⚠ WARNING: {total_pages - total_with_css} pages still need CSS")

if __name__ == "__main__":
    main()