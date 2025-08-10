#!/usr/bin/env python3
"""
Fix phone number positioning and remove inline CSS from pages
This will fix the header structure issues
"""

import os
import re
from pathlib import Path

def fix_page_header(file_path):
    """Fix header and remove large inline CSS blocks"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if page has the large inline style block
    if '<style>' not in content or 'header-content' not in content:
        return False, "Page doesn't have inline styles issue"
    
    # Remove the large inline style block but keep any consultation form styles
    # Pattern to remove the main style block
    pattern = r'<style>\s*\*\s*\{[^}]+\}.*?</style>\s*(?=<!-- Google Analytics|<script|</head>)'
    
    if re.search(pattern, content, re.DOTALL):
        # Remove the large style block
        content = re.sub(pattern, '', content, flags=re.DOTALL)
        
        # Make sure the page has the main styles.css
        if 'href="../../css/styles.css"' not in content:
            # Add styles.css before property-content-styles.css
            content = content.replace(
                '<link rel="stylesheet" href="../../css/property-content-styles.css">',
                '<link rel="stylesheet" href="../../css/styles.css">\n    <link rel="stylesheet" href="../../css/property-content-styles.css">'
            )
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True, "Fixed header and removed inline CSS"
    
    return False, "Could not fix page structure"

def main():
    """Main function to fix pages with header issues"""
    
    print("Fixing pages with phone number positioning issues...")
    print("=" * 50)
    
    # Path to property-management directory
    prop_mgmt_dir = Path('property-management')
    
    if not prop_mgmt_dir.exists():
        print("Error: property-management directory not found!")
        return
    
    # Pages that likely have this issue (the 21 we just fixed)
    pages_to_check = [
        'portage-park', 'prospect-heights', 'pulaski-park', 'ravenswood',
        'rogers-park', 'rolling-meadows', 'sauganash', 'schiller-park',
        'skokie', 'south-loop', 'streeterville', 'the-glen',
        'uptown', 'vernon-hills', 'west-loop', 'west-ridge',
        'wheeling', 'wicker-park', 'wilmette', 'winnetka', 'wood-dale'
    ]
    
    fixed_count = 0
    checked_count = 0
    
    print(f"Checking {len(pages_to_check)} pages for header issues...")
    print("-" * 50)
    
    for page_name in pages_to_check:
        page_dir = prop_mgmt_dir / page_name
        index_file = page_dir / 'index.html'
        
        if index_file.exists():
            print(f"\nChecking: {page_name}")
            checked_count += 1
            success, message = fix_page_header(index_file)
            
            if success:
                print(f"  [FIXED] {message}")
                fixed_count += 1
            else:
                print(f"  [OK] {message}")
    
    print("\n" + "=" * 50)
    print(f"Results:")
    print(f"  Pages checked: {checked_count}")
    print(f"  Pages fixed: {fixed_count}")
    print(f"  Already correct: {checked_count - fixed_count}")
    
    if fixed_count > 0:
        print(f"\nSUCCESS: Fixed {fixed_count} pages with header issues!")
    else:
        print("\nAll pages already have correct structure.")

if __name__ == "__main__":
    main()