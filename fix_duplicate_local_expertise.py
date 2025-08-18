"""
Remove duplicate "Local Expertise: Understanding [Location]'s Unique Market" sections
"""

import os
from bs4 import BeautifulSoup

def fix_duplicate_sections(filepath, location_display):
    """Remove duplicate Local Expertise sections"""
    
    print(f"Processing: {location_display}")
    
    try:
        # Read the file
        with open(filepath, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find all divs with the Local Expertise heading
        local_expertise_divs = []
        for div in soup.find_all('div', style=lambda value: value and 'background: #2c3e50' in value):
            h2 = div.find('h2')
            if h2 and 'Local Expertise' in h2.get_text():
                local_expertise_divs.append(div)
        
        # If we have duplicates, remove all but the first one
        if len(local_expertise_divs) > 1:
            print(f"  Found {len(local_expertise_divs)} Local Expertise sections - removing duplicates")
            for div in local_expertise_divs[1:]:
                div.decompose()
            
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
    
    print("Removing duplicate Local Expertise sections")
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
        
        result = fix_duplicate_sections(filepath, location_display)
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