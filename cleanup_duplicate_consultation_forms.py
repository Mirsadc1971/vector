#!/usr/bin/env python3
"""
Cleanup script to remove duplicate consultation forms from batch 2 property pages
"""

import os
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

def cleanup_duplicates(location):
    """Remove duplicate consultation forms from a location"""
    location_path = BASE_PATH / location / 'index.html'
    
    if not location_path.exists():
        return
    
    with open(location_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all consultation sections
    consultation_pattern = r'<!-- Consultation Form Section -->.*?</section>'
    matches = re.findall(consultation_pattern, content, re.DOTALL)
    
    if len(matches) > 1:
        print(f"Fixing {location} - found {len(matches)} consultation sections")
        
        # Remove all but keep one before footer
        # First remove all occurrences
        content_cleaned = re.sub(consultation_pattern, '', content, flags=re.DOTALL)
        
        # Add one back before footer
        consultation_form = matches[0]  # Use the first one found
        
        footer_pattern = r'(<footer>|<!-- PERFECT FOOTER HTML)'
        if re.search(footer_pattern, content_cleaned):
            content_cleaned = re.sub(
                footer_pattern,
                consultation_form + r'\n    \1',
                content_cleaned
            )
        
        with open(location_path, 'w', encoding='utf-8') as f:
            f.write(content_cleaned)
        
        print(f"Cleaned up {location}")

def main():
    """Main function to cleanup duplicates"""
    print("Cleaning up duplicate consultation forms...")
    
    for location in BATCH_2_LOCATIONS:
        cleanup_duplicates(location)
    
    print("Cleanup complete!")

if __name__ == '__main__':
    main()