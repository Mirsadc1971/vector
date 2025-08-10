#!/usr/bin/env python3
"""
Add content styling CSS to all property pages
This script ONLY adds CSS link - does NOT modify hero or footer
"""

import os
from pathlib import Path

def add_css_to_page(file_path):
    """Add content styles CSS link to a property page"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has the CSS
    if 'property-content-styles.css' in content:
        print(f"  [SKIP] Already has CSS: {file_path}")
        return False
    
    # Add the CSS link after styles.css
    # This ONLY adds a CSS link, doesn't modify any content
    if '<link rel="stylesheet" href="../../css/styles.css">' in content:
        content = content.replace(
            '<link rel="stylesheet" href="../../css/styles.css">',
            '<link rel="stylesheet" href="../../css/styles.css">\n    <link rel="stylesheet" href="../../css/property-content-styles.css">'
        )
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  [DONE] Added CSS: {file_path}")
        return True
    else:
        print(f"  [ERROR] Could not find styles.css link: {file_path}")
        return False

def main():
    """Main function to add CSS to all property pages"""
    
    print("Adding content styles CSS to property pages...")
    print("This will NOT modify hero or footer sections")
    print("=" * 50)
    
    # Path to property-management directory
    prop_mgmt_dir = Path('property-management')
    
    if not prop_mgmt_dir.exists():
        print("Error: property-management directory not found!")
        return
    
    # Get all subdirectories
    locations = [d for d in prop_mgmt_dir.iterdir() if d.is_dir()]
    
    updated_count = 0
    total_count = 0
    
    print(f"Found {len(locations)} location directories")
    print("-" * 50)
    
    for location_dir in sorted(locations):
        index_file = location_dir / 'index.html'
        
        if index_file.exists():
            total_count += 1
            print(f"\nProcessing: {location_dir.name}")
            
            if add_css_to_page(index_file):
                updated_count += 1
    
    print("\n" + "=" * 50)
    print(f"Complete!")
    print(f"  Total pages: {total_count}")
    print(f"  Updated: {updated_count}")
    print(f"  Skipped: {total_count - updated_count}")
    print("\nHero and footer sections remain untouched.")

if __name__ == "__main__":
    main()