#!/usr/bin/env python3
"""
Update all property management pages to use the master CSS file
This script will:
1. Add link to property-pages.css
2. Remove inline styles that are now in the master CSS
3. Ensure consistent structure across all pages
"""

import os
import re
from pathlib import Path

def update_property_page(file_path):
    """Update a single property page to use master CSS"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already updated
    if 'property-pages.css' in content:
        print(f"  [OK] Already updated: {file_path}")
        return False
    
    # Add link to property-pages.css after styles.css
    if '<link rel="stylesheet" href="../../css/styles.css">' in content:
        content = content.replace(
            '<link rel="stylesheet" href="../../css/styles.css">',
            '<link rel="stylesheet" href="../../css/styles.css">\n    <link rel="stylesheet" href="../../css/property-pages.css">'
        )
    
    # Remove large inline style blocks for sections that are now in master CSS
    # Pattern to remove style blocks with common section styles
    style_patterns = [
        # Remove style blocks that define service-card, faq-section, etc.
        r'<style>\s*\/\*[^*]*\*\/\s*\.service-card[^<]*</style>',
        r'<style>\s*\.main-content[^<]*</style>',
        r'<style>\s*\.services-section[^<]*</style>',
        r'<style>\s*\.excellence-section[^<]*</style>',
        r'<style>\s*\.stats-section[^<]*</style>',
        r'<style>\s*\.cta-section[^<]*</style>',
        r'<style>\s*\.faq-section[^<]*</style>',
        r'<style>\s*\.why-choose-section[^<]*</style>',
        r'<style>\s*\.contact-section[^<]*</style>',
    ]
    
    for pattern in style_patterns:
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # Fix class names for consistency
    # Change main-content to content if needed
    content = content.replace('class="main-content"', 'class="content"')
    
    # Remove empty style tags
    content = re.sub(r'<style>\s*</style>', '', content)
    
    # Write updated content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  [UPDATED] {file_path}")
    return True

def main():
    """Main function to update all property pages"""
    
    print("Starting property pages CSS update...")
    print("=" * 50)
    
    # Path to property-management directory
    prop_mgmt_dir = Path('property-management')
    
    if not prop_mgmt_dir.exists():
        print("Error: property-management directory not found!")
        return
    
    # Get all subdirectories (each represents a location)
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
            
            if update_property_page(index_file):
                updated_count += 1
        else:
            print(f"  [WARNING] No index.html in: {location_dir.name}")
    
    print("\n" + "=" * 50)
    print(f"Update complete!")
    print(f"  Total pages found: {total_count}")
    print(f"  Pages updated: {updated_count}")
    print(f"  Already up-to-date: {total_count - updated_count}")

if __name__ == "__main__":
    main()