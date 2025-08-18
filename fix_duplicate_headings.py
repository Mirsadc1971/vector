"""
Fix duplicate "Why [Location] Demands Excellence" headings in all property management pages
"""

import os
import re
import glob

def fix_duplicate_heading(filepath):
    """Remove duplicate heading from a single HTML file"""
    
    # Get location name from filepath
    location_name = os.path.basename(os.path.dirname(filepath))
    location_display = location_name.replace('-', ' ').title()
    
    print(f"Processing: {location_display}")
    
    try:
        # Read the file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # The duplicate heading pattern to find and remove
        # This is the plain h2 that appears after the styled one
        duplicate_pattern = f'<h2>\s*Manage369: Your Trusted {location_display} Property Management Partner\s*</h2>'
        
        # First, let's check if there's a duplicate "Why [Location] Demands Excellence" heading
        # The styled one is inside a div with gradient background
        # The duplicate would be a plain h2
        
        # Count occurrences of the heading text
        heading_text = f"Why {location_display} Demands Excellence"
        occurrences = content.count(heading_text)
        
        if occurrences > 1:
            print(f"  Found {occurrences} occurrences of heading, fixing...")
            
            # Find the plain h2 version (not the styled one in the div)
            # The styled one has style="color: white; font-size: 2.5rem"
            # We want to remove any plain <h2> with this text
            
            # Pattern for plain h2 (without the white color styling)
            plain_h2_pattern = f'<h2>\\s*🏆?\\s*{re.escape(heading_text)}.*?</h2>(?!.*color: white)'
            
            # Remove the plain h2 if it exists
            content_before = content
            content = re.sub(plain_h2_pattern, '', content, flags=re.DOTALL)
            
            if content != content_before:
                print(f"  Removed duplicate plain heading")
        
        # Also check for duplicate "Manage369: Your Trusted" headings
        trusted_heading = f"Manage369: Your Trusted {location_display} Property Management Partner"
        trusted_occurrences = content.count(trusted_heading)
        
        if trusted_occurrences > 1:
            print(f"  Found {trusted_occurrences} occurrences of 'Trusted' heading, fixing...")
            # Keep only the first occurrence
            first_index = content.find(trusted_heading)
            if first_index != -1:
                # Find the second occurrence
                second_index = content.find(trusted_heading, first_index + len(trusted_heading))
                if second_index != -1:
                    # Remove the h2 tag containing the second occurrence
                    h2_start = content.rfind('<h2>', 0, second_index)
                    h2_end = content.find('</h2>', second_index) + 5
                    if h2_start != -1 and h2_end != -1:
                        content = content[:h2_start] + content[h2_end:]
                        print(f"  Removed duplicate 'Trusted' heading")
        
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
    
    for filepath in files:
        if fix_duplicate_heading(filepath):
            success_count += 1
    
    print("=" * 50)
    print(f"Update Complete!")
    print(f"Successfully processed: {success_count}/{len(files)} pages")

if __name__ == "__main__":
    main()