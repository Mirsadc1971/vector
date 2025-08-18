"""
Add Vittoria Logli website link to all Northwest Suburbs property management pages
"""

import os
import re
from bs4 import BeautifulSoup

# List of 20 Northwest Suburbs communities
NORTHWEST_SUBURBS = [
    'arlington-heights',
    'buffalo-grove',
    'des-plaines',
    'elk-grove-village',
    'franklin-park',
    'harwood-heights',
    'itasca',
    'lincolnwood',
    'morton-grove',  # Already done as part of North Shore
    'mount-prospect',
    'norridge',
    'northbrook',  # Already done as part of North Shore
    'park-ridge',
    'prospect-heights',
    'rolling-meadows',
    'rosemont',
    'schaumburg',
    'skokie',  # Already done as part of North Shore
    'wheeling',
    'wood-dale'
]

def add_vittoria_link(filepath, location_display):
    """Add or update Vittoria Logli link in the Real Estate Partners section"""
    
    print(f"Processing: {location_display}")
    
    try:
        # Read the file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Check if link already exists
        if 'vittorialogli.com' in str(soup):
            print(f"  Link already exists in {location_display}")
            return True
        
        # Find the Real Estate Network/Partners section
        found_section = False
        
        # Look for the div with "Real Estate" in h3
        for div in soup.find_all('div', style=lambda value: value and 'background: rgba(255,255,255,0.1)' in value):
            h3 = div.find('h3')
            if h3 and ('Real Estate' in h3.text or '🏡' in h3.text):
                # Found the real estate section
                p_tag = div.find('p')
                if p_tag:
                    # Update the paragraph with the link
                    new_content = f'Strong partnerships with {location_display}\'s leading real estate professionals including <a href="https://www.vittorialogli.com/" target="_blank" style="color: #ffd700; text-decoration: underline; font-weight: bold;">Vittoria Logli</a> ensure smooth transitions and maintained property appeal.'
                    
                    # Create new tag with the content
                    new_p = soup.new_tag('p', style='line-height: 1.8;')
                    # Parse the HTML content properly
                    new_p_content = BeautifulSoup(new_content, 'html.parser')
                    for element in new_p_content:
                        new_p.append(element)
                    p_tag.replace_with(new_p)
                    
                    print(f"  Added Vittoria Logli link to {location_display}")
                    found_section = True
                    break
        
        if not found_section:
            # Try to find by searching for the text pattern
            for p in soup.find_all('p'):
                if p.text and 'real estate' in p.text.lower() and ('partnership' in p.text.lower() or 'network' in p.text.lower()):
                    parent = p.parent
                    if parent and 'rgba(255,255,255,0.1)' in str(parent):
                        # Update this paragraph
                        new_content = f'Strong partnerships with {location_display}\'s leading real estate professionals including <a href="https://www.vittorialogli.com/" target="_blank" style="color: #ffd700; text-decoration: underline; font-weight: bold;">Vittoria Logli</a> ensure smooth transitions and maintained property appeal.'
                        
                        new_p = soup.new_tag('p', style='line-height: 1.8;')
                        new_p_content = BeautifulSoup(new_content, 'html.parser')
                        for element in new_p_content:
                            new_p.append(element)
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
    """Main function to process all Northwest Suburbs property management pages"""
    
    print("Adding Vittoria Logli links to Northwest Suburbs property pages")
    print("=" * 50)
    
    success_count = 0
    failed_files = []
    processed_files = []
    skipped_files = []
    
    # Process each Northwest Suburbs community
    for community in NORTHWEST_SUBURBS:
        filepath = f'C:\\Users\\mirsa\\manage369-live\\property-management\\{community}\\index.html'
        
        # Check if file exists
        if not os.path.exists(filepath):
            print(f"  [SKIP] File not found: {community}")
            continue
        
        location_display = community.replace('-', ' ').title()
        
        # Check if already has link
        with open(filepath, 'r', encoding='utf-8') as f:
            if 'vittorialogli.com' in f.read():
                print(f"  [SKIP] {location_display} already has Vittoria link")
                skipped_files.append(community)
                continue
        
        if add_vittoria_link(filepath, location_display):
            success_count += 1
            processed_files.append(community)
        else:
            failed_files.append(community)
    
    print("=" * 50)
    print(f"Update Complete!")
    print(f"Successfully updated: {success_count} pages")
    if processed_files:
        print(f"Processed communities: {', '.join(processed_files)}")
    if skipped_files:
        print(f"Skipped (already had link): {', '.join(skipped_files)}")
    
    if failed_files:
        print(f"\nFailed to update {len(failed_files)} pages:")
        for f in failed_files:
            print(f"  - {f}")
    
    return success_count > 0

if __name__ == "__main__":
    # Run the update
    success = main()
    
    if success:
        print("\n[COMPLETE] Vittoria Logli links added to Northwest Suburbs pages!")
    else:
        print("\n[INFO] No new pages were updated (may already have links).")