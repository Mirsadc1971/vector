"""
Remove ALL duplicate sections from property management pages
"""

import os
from bs4 import BeautifulSoup

def fix_all_duplicates(filepath, location_display):
    """Remove all types of duplicate sections"""
    
    print(f"Processing: {location_display}")
    
    try:
        # Read the file
        with open(filepath, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        changes_made = False
        
        # 1. Fix duplicate "How Manage369 Adds Extraordinary Value" sections
        value_sections = []
        for section in soup.find_all('section'):
            h2 = section.find('h2')
            if h2 and 'How Manage369 Adds Extraordinary Value' in h2.get_text():
                value_sections.append(section)
        
        if len(value_sections) > 1:
            print(f"  Found {len(value_sections)} 'Extraordinary Value' sections - removing duplicates")
            for section in value_sections[1:]:
                section.decompose()
            changes_made = True
        
        # 2. Fix duplicate "Your [Location] Property Deserves Excellence" sections
        excellence_sections = []
        for section in soup.find_all('section'):
            h2 = section.find('h2')
            if h2 and 'Property Deserves Excellence' in h2.get_text():
                excellence_sections.append(section)
        
        if len(excellence_sections) > 1:
            print(f"  Found {len(excellence_sections)} 'Deserves Excellence' sections - removing duplicates")
            for section in excellence_sections[1:]:
                section.decompose()
            changes_made = True
            
        # 3. Fix duplicate FAQ sections within the main value section
        faq_divs = []
        for div in soup.find_all('div'):
            h2 = div.find('h2')
            if h2 and 'Frequently Asked Questions About Property Management' in h2.get_text():
                faq_divs.append(div)
        
        if len(faq_divs) > 1:
            print(f"  Found {len(faq_divs)} FAQ divs - removing duplicates")
            for div in faq_divs[1:]:
                div.decompose()
            changes_made = True
        
        if changes_made:
            # Save the fixed file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            
            print(f"  [SUCCESS] Fixed {location_display}")
            return True
        else:
            print(f"  [SKIP] No duplicates found")
            return False
            
    except Exception as e:
        print(f"  [ERROR] Error processing {filepath}: {e}")
        return False

def main():
    """Main function to fix all pages"""
    
    print("Removing ALL duplicate sections from property pages")
    print("=" * 50)
    
    success_count = 0
    skipped_count = 0
    failed_files = []
    
    # Get all property management directories
    base_dir = 'C:\\Users\\mirsa\\manage369-live\\property-management'
    
    for community_dir in os.listdir(base_dir):
        filepath = os.path.join(base_dir, community_dir, 'index.html')
        
        if not os.path.exists(filepath):
            continue
        
        location_display = community_dir.replace('-', ' ').title()
        
        result = fix_all_duplicates(filepath, location_display)
        if result is True:
            success_count += 1
        elif result is False:
            skipped_count += 1
        else:
            failed_files.append(community_dir)
    
    print("=" * 50)
    print(f"Process Complete!")
    print(f"Successfully fixed: {success_count} pages")
    print(f"Skipped (no duplicates): {skipped_count} pages")
    
    if failed_files:
        print(f"\nFailed to process {len(failed_files)} pages:")
        for f in failed_files:
            print(f"  - {f}")

if __name__ == "__main__":
    main()