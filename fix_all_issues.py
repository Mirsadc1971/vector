"""
Fix all issues in property management pages:
1. Remove duplicate/nested "Why [Location]" sections
2. Fix H1 to show "[Location] Property Management Services - Manage369"
"""

import os
import re
import glob
from bs4 import BeautifulSoup

def fix_page_issues(filepath):
    """Fix all issues in a single HTML file"""
    
    # Get location name from filepath
    location_name = os.path.basename(os.path.dirname(filepath))
    location_display = location_name.replace('-', ' ').title()
    
    print(f"Processing: {location_display}")
    
    try:
        # Read the file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Fix 1: Update H1 in hero section
        hero_section = soup.find('section', {'class': 'hero'})
        if hero_section:
            h1 = hero_section.find('h1')
            if h1:
                # Correct format: "[Location] Property Management Services - Manage369"
                h1.string = f"{location_display} Property Management Services - Manage369"
                print(f"  Fixed H1 heading")
        
        # Fix 2: Remove duplicate "Why [Location]" sections
        # Find all divs with the purple gradient background
        gradient_divs = soup.find_all('div', style=lambda value: value and 'background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)' in value)
        
        if len(gradient_divs) > 1:
            print(f"  Found {len(gradient_divs)} gradient sections, removing duplicates...")
            # Keep only the first one, remove the rest
            for div in gradient_divs[1:]:
                div.decompose()
        
        # Fix 3: Check for nested "Why" sections
        # Look for comments
        content_str = str(soup)
        why_section_count = content_str.count(f'<!-- Why {location_display} Section -->')
        
        if why_section_count > 1:
            print(f"  Found {why_section_count} 'Why' section comments, cleaning up...")
            
            # Parse again to work with clean structure
            lines = content_str.split('\n')
            new_lines = []
            inside_duplicate = False
            section_depth = 0
            
            for i, line in enumerate(lines):
                # Check if this is the start of a duplicate section
                if f'<!-- Why {location_display} Section -->' in line:
                    if section_depth > 0:
                        # This is a nested duplicate, skip it
                        inside_duplicate = True
                        continue
                    section_depth += 1
                
                # If we're inside a duplicate, check for the end
                if inside_duplicate:
                    # Look for the closing of the duplicate section
                    if '</div>' in line:
                        # Count divs to track nesting
                        # Skip this line and check if we're done with the duplicate
                        if '<!-- Community Features Section -->' in lines[i+1:i+5] if i+5 < len(lines) else []:
                            inside_duplicate = False
                        continue
                    else:
                        continue
                
                new_lines.append(line)
            
            content_str = '\n'.join(new_lines)
            soup = BeautifulSoup(content_str, 'html.parser')
        
        # Fix 4: Clean up any duplicate h2 headings with same text
        headings = soup.find_all('h2')
        seen_texts = set()
        for h2 in headings:
            if h2.text:
                text = h2.text.strip()
                if text in seen_texts and '🏆 Why' in text:
                    # This is a duplicate heading
                    h2.decompose()
                    print(f"  Removed duplicate h2: {text[:50]}...")
                else:
                    seen_texts.add(text)
        
        # Save the updated file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup.prettify()))
        
        print(f"  [SUCCESS] Fixed {location_display}")
        return True
        
    except Exception as e:
        print(f"  [ERROR] Error processing {filepath}: {e}")
        return False

def main():
    """Main function to process all property management pages"""
    
    # Get all property management HTML files
    pattern = r'C:\Users\mirsa\manage369-live\property-management\*\index.html'
    files = glob.glob(pattern)
    
    print(f"Found {len(files)} property management pages to fix")
    print("=" * 50)
    
    success_count = 0
    failed_files = []
    
    for filepath in files:
        if fix_page_issues(filepath):
            success_count += 1
        else:
            failed_files.append(filepath)
    
    print("=" * 50)
    print(f"Update Complete!")
    print(f"Successfully fixed: {success_count}/{len(files)} pages")
    
    if failed_files:
        print(f"\nFailed to fix {len(failed_files)} pages:")
        for f in failed_files:
            location = os.path.basename(os.path.dirname(f))
            print(f"  - {location}")
    
    return success_count == len(files)

if __name__ == "__main__":
    # Run the fixes
    success = main()
    
    if success:
        print("\n[COMPLETE] All pages fixed successfully!")
    else:
        print("\n[WARNING] Some pages had issues. Please review the failed files.")