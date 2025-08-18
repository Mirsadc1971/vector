"""
Fix duplicate/nested "Why [Location] Demands Excellence" sections in all property management pages
The purple gradient section got duplicated/nested during the template application
"""

import os
import re
import glob

def fix_nested_sections(filepath):
    """Fix nested/duplicate sections in HTML file"""
    
    # Get location name from filepath
    location_name = os.path.basename(os.path.dirname(filepath))
    location_display = location_name.replace('-', ' ').title()
    
    print(f"Processing: {location_display}")
    
    try:
        # Read the file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern to find the nested duplicate section
        # Look for the "Why Location Section" comment followed by another identical comment
        pattern = r'(<!-- Why .+? Section -->.*?<h2 style="color: white.*?>.*?🏆 Why .+? Demands Excellence.*?</h2>.*?<div style="max-width: 1200px.*?>)\s*<!-- Why .+? Section -->.*?</div>\s*</div>\s*</div>'
        
        # Check if we have the nested duplication
        if '<!-- Why ' + location_display + ' Section -->' in content:
            count = content.count('<!-- Why ' + location_display + ' Section -->')
            if count > 1:
                print(f"  Found {count} 'Why {location_display}' sections, fixing...")
                
                # Find the first section start
                first_section_start = content.find('<!-- Why ' + location_display + ' Section -->')
                
                # Find where the first div with gradient background ends
                # We need to find the matching closing divs
                gradient_div_start = content.find('<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)', first_section_start)
                
                if gradient_div_start != -1:
                    # Find the nested duplicate section
                    second_section_start = content.find('<!-- Why ' + location_display + ' Section -->', gradient_div_start + 1)
                    
                    if second_section_start != -1:
                        # Find the end of the proper content (before the duplicate)
                        # Look for the closing divs of the grid
                        grid_end = content.find('</div>\n        </div>\n    </div>', gradient_div_start)
                        
                        # Remove everything from the second section comment to the end of the outer section
                        # Find the closing divs for the outer section
                        outer_end = content.find('</div>\n     </div>\n    </div>', second_section_start)
                        if outer_end == -1:
                            outer_end = content.find('</div>\n      </div>\n     </div>', second_section_start)
                        if outer_end == -1:
                            outer_end = content.find('</div></div></div>', second_section_start)
                        
                        if outer_end != -1:
                            # Remove the duplicate nested section
                            # Keep everything before the second section and after the outer end
                            content = content[:second_section_start] + content[outer_end + 18:]  # 18 for the closing tags
                            print(f"  Removed nested duplicate section")
                
                # Clean up any remaining duplicate headings
                heading_pattern = f'🏆 Why {location_display} Demands Excellence in Property Management'
                heading_count = content.count(heading_pattern)
                if heading_count > 1:
                    print(f"  Found {heading_count} heading occurrences, keeping only first...")
                    # Keep only the first occurrence
                    first_idx = content.find(heading_pattern)
                    if first_idx != -1:
                        # Find and remove subsequent occurrences
                        remaining = content[first_idx + len(heading_pattern):]
                        remaining = remaining.replace(heading_pattern, '')
                        content = content[:first_idx + len(heading_pattern)] + remaining
        
        # Save the updated file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"  [ERROR] Error processing {filepath}: {e}")
        return False

def main():
    """Main function to process all property management pages"""
    
    # Get all property management HTML files
    pattern = r'C:\Users\mirsa\manage369-live\property-management\*\index.html'
    files = glob.glob(pattern)
    
    print(f"Found {len(files)} property management pages to check")
    print("=" * 50)
    
    success_count = 0
    fixed_count = 0
    
    for filepath in files:
        if fix_nested_sections(filepath):
            success_count += 1
    
    print("=" * 50)
    print(f"Update Complete!")
    print(f"Successfully processed: {success_count}/{len(files)} pages")

if __name__ == "__main__":
    main()