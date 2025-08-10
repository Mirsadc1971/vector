#!/usr/bin/env python3
"""
Simple script to remove duplicate consultation forms
"""

import re
from pathlib import Path

# Batch 2 locations to process
BATCH_2_LOCATIONS = [
    'hyde-park', 'itasca', 'jefferson-park', 'lake-bluff', 'lake-forest',
    'lakeview', 'lincoln-park', 'lincoln-square', 'lincolnshire', 'lincolnwood',
    'logan-square', 'loop', 'mayfair', 'morton-grove', 'mount-prospect',
    'north-park', 'northbrook', 'northfield', 'norwood-park', 'oak-park',
    'old-irving-park', 'old-town', 'park-ridge'
]

BASE_PATH = Path('C:/Users/mirsa/manage369-live/property-management')

def simple_fix(location):
    """Simple fix for duplicate consultation forms"""
    location_path = BASE_PATH / location / 'index.html'
    
    if not location_path.exists():
        return
    
    with open(location_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count consultation sections
    count = content.count('<!-- Consultation Form Section -->')
    if count > 1:
        print(f"Fixing {location} - found {count} sections")
        
        # Simple approach: find the last occurrence and remove everything before it
        # that contains consultation sections, keeping only the last one
        parts = content.split('<!-- Consultation Form Section -->')
        
        if len(parts) > 2:
            # Keep the first part (before any consultation sections) 
            # and the last consultation section
            new_content = parts[0] + '<!-- Consultation Form Section -->' + parts[-1]
            
            with open(location_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Fixed {location}")

def main():
    """Main function"""
    print("Simple duplicate fix...")
    
    for location in BATCH_2_LOCATIONS:
        simple_fix(location)
    
    print("Simple fix complete!")

if __name__ == '__main__':
    main()