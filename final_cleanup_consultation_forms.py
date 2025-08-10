#!/usr/bin/env python3
"""
Final cleanup script to properly remove duplicate consultation forms
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

def fix_consultation_forms(location):
    """Fix consultation form duplication"""
    location_path = BASE_PATH / location / 'index.html'
    
    if not location_path.exists():
        return
    
    with open(location_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count occurrences
    consultation_count = content.count('<!-- Consultation Form Section -->')
    
    if consultation_count > 1:
        print(f"Fixing {location} - found {consultation_count} consultation sections")
        
        # Find the first occurrence and extract it
        start_pattern = r'<!-- Consultation Form Section -->'
        end_pattern = r'</section>'
        
        # Find all consultation sections with their positions
        import re
        sections = []
        start = 0
        while True:
            match_start = content.find('<!-- Consultation Form Section -->', start)
            if match_start == -1:
                break
                
            # Find the closing </section> after this start
            section_start = match_start
            section_depth = 0
            pos = match_start
            section_end = -1
            
            while pos < len(content):
                if content[pos:pos+9] == '<section':
                    section_depth += 1
                elif content[pos:pos+10] == '</section>':
                    section_depth -= 1
                    if section_depth == 0:
                        section_end = pos + 10
                        break
                pos += 1
            
            if section_end != -1:
                section_content = content[section_start:section_end]
                sections.append((section_start, section_end, section_content))
            
            start = match_start + 1
        
        if len(sections) > 1:
            # Remove all sections first
            new_content = content
            for start_pos, end_pos, section_content in reversed(sections):
                new_content = new_content[:start_pos] + new_content[end_pos:]
            
            # Add one section before footer
            footer_patterns = [
                '<!-- PERFECT FOOTER HTML',
                '<footer>',
                '</body>'
            ]
            
            insertion_point = -1
            for pattern in footer_patterns:
                pos = new_content.rfind(pattern)
                if pos != -1:
                    insertion_point = pos
                    break
            
            if insertion_point != -1:
                # Insert the first consultation section before footer
                consultation_section = sections[0][2]
                new_content = (new_content[:insertion_point] + 
                              consultation_section + '\n    ' + 
                              new_content[insertion_point:])
                
                with open(location_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Fixed {location} - removed {len(sections)-1} duplicate sections")

def main():
    """Main function"""
    print("Final cleanup of consultation forms...")
    
    for location in BATCH_2_LOCATIONS:
        fix_consultation_forms(location)
    
    print("Final cleanup complete!")

if __name__ == '__main__':
    main()