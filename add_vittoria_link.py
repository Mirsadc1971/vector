"""
Add Vittoria Logli website link to all North Shore property management pages
"""

import os
import re
from bs4 import BeautifulSoup

# List of 16 North Shore communities
NORTH_SHORE_COMMUNITIES = [
    'deerfield',
    'evanston',
    'glencoe',
    'glenview',  # Already has the link
    'highland-park',
    'lake-bluff',
    'lake-forest',
    'lincolnshire',
    'northbrook',
    'northfield',
    'wilmette',
    'winnetka',
    'golf',
    'morton-grove',
    'skokie',
    'kenilworth'
]

def add_vittoria_link(filepath, location_display):
    """Add or update Vittoria Logli link in the Real Estate Partners section"""
    
    print(f"Processing: {location_display}")
    
    try:
        # Read the file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find the Real Estate Network/Partners section
        # Look for the div with "Real Estate" in h3
        found_section = False
        
        for div in soup.find_all('div', style=lambda value: value and 'background: rgba(255,255,255,0.1)' in value):
            h3 = div.find('h3')
            if h3 and ('Real Estate' in h3.text or '🏡' in h3.text):
                # Found the real estate section
                p_tag = div.find('p')
                if p_tag:
                    # Check if Vittoria link already exists
                    if 'vittorialogli.com' in str(p_tag):
                        print(f"  Link already exists in {location_display}")
                        found_section = True
                    else:
                        # Update the paragraph with the link
                        new_content = f'Proud partnership with {location_display}\'s top real estate professionals including <a href="https://www.vittorialogli.com/" target="_blank" style="color: #ffd700; text-decoration: underline; font-weight: bold;">Vittoria Logli</a> for seamless property transitions and maintained appeal throughout ownership changes.'
                        
                        # Create new tag with the content
                        new_p = soup.new_tag('p', style='line-height: 1.8;')
                        new_p.append(BeautifulSoup(new_content, 'html.parser'))
                        p_tag.replace_with(new_p)
                        
                        print(f"  Added Vittoria Logli link to {location_display}")
                        found_section = True
        
        if not found_section:
            # If we couldn't find the exact section, search more broadly
            # Look for text containing "Real Estate" and "partnership"
            for p in soup.find_all('p'):
                if p.text and 'real estate' in p.text.lower() and 'partnership' in p.text.lower():
                    # Check if it's in the right section (has the gold color nearby)
                    parent = p.parent
                    if parent and 'rgba(255,255,255,0.1)' in str(parent):
                        # Update this paragraph
                        if 'vittorialogli.com' not in str(p):
                            new_content = f'Strong partnerships with {location_display}\'s leading real estate professionals including <a href="https://www.vittorialogli.com/" target="_blank" style="color: #ffd700; text-decoration: underline; font-weight: bold;">Vittoria Logli</a> ensure smooth transitions and maintained property appeal.'
                            
                            new_p = soup.new_tag('p', style='line-height: 1.8;')
                            new_p.append(BeautifulSoup(new_content, 'html.parser'))
                            p.replace_with(new_p)
                            
                            print(f"  Added Vittoria Logli link to {location_display}")
                            found_section = True
                            break
        
        if not found_section:
            print(f"  [WARNING] Could not find Real Estate section in {location_display}")
        
        # Save the updated file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup.prettify()))
        
        return True
        
    except Exception as e:
        print(f"  [ERROR] Error processing {filepath}: {e}")
        return False

def main():
    """Main function to process all North Shore property management pages"""
    
    print("Adding Vittoria Logli links to North Shore property pages")
    print("=" * 50)
    
    success_count = 0
    failed_files = []
    processed_files = []
    
    # Process each North Shore community
    for community in NORTH_SHORE_COMMUNITIES:
        filepath = f'C:\\Users\\mirsa\\manage369-live\\property-management\\{community}\\index.html'
        
        # Check if file exists
        if not os.path.exists(filepath):
            print(f"  [SKIP] File not found: {community}")
            continue
        
        location_display = community.replace('-', ' ').title()
        
        if add_vittoria_link(filepath, location_display):
            success_count += 1
            processed_files.append(community)
        else:
            failed_files.append(community)
    
    print("=" * 50)
    print(f"Update Complete!")
    print(f"Successfully updated: {success_count} pages")
    print(f"Processed communities: {', '.join(processed_files)}")
    
    if failed_files:
        print(f"\nFailed to update {len(failed_files)} pages:")
        for f in failed_files:
            print(f"  - {f}")
    
    return success_count > 0

if __name__ == "__main__":
    # Run the update
    success = main()
    
    if success:
        print("\n[COMPLETE] Vittoria Logli links added to North Shore pages!")
    else:
        print("\n[WARNING] No pages were updated.")