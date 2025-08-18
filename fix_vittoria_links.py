"""
Fix the Vittoria Logli links that were improperly added to Northwest Suburbs pages
"""

import os
import re

# Northwest Suburbs that need fixing
NORTHWEST_SUBURBS_TO_FIX = [
    'arlington-heights',
    'buffalo-grove', 
    'des-plaines',
    'elk-grove-village',
    'franklin-park',
    'harwood-heights',
    'itasca',
    'lincolnwood',
    'mount-prospect',
    'norridge',
    'park-ridge',
    'prospect-heights',
    'rolling-meadows',
    'wheeling',
    'wood-dale'
]

def fix_vittoria_link(filepath, location_display):
    """Fix the Vittoria Logli link in the Real Estate Partners section"""
    
    print(f"Fixing: {location_display}")
    
    try:
        # Read the file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the broken text pattern
        broken_pattern = f"Strong partnerships with {location_display}'s leading real estate professionals including\\s+ensure smooth transitions"
        
        # Replace with correct text including the link
        correct_text = f'Strong partnerships with {location_display}\'s leading real estate professionals including <a href="https://www.vittorialogli.com/" target="_blank" style="color: #ffd700; text-decoration: underline; font-weight: bold;">Vittoria Logli</a> ensure smooth transitions'
        
        # Do the replacement
        content = re.sub(broken_pattern, correct_text, content)
        
        # Also check for a variant pattern
        broken_pattern2 = f"Proud partnership with {location_display}'s top real estate professionals including\\s+for seamless property transitions"
        correct_text2 = f'Proud partnership with {location_display}\'s top real estate professionals including <a href="https://www.vittorialogli.com/" target="_blank" style="color: #ffd700; text-decoration: underline; font-weight: bold;">Vittoria Logli</a> for seamless property transitions'
        
        content = re.sub(broken_pattern2, correct_text2, content)
        
        # Save the fixed file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  Fixed {location_display}")
        return True
        
    except Exception as e:
        print(f"  [ERROR] Error processing {filepath}: {e}")
        return False

def main():
    """Main function to fix all Northwest Suburbs pages"""
    
    print("Fixing Vittoria Logli links in Northwest Suburbs pages")
    print("=" * 50)
    
    success_count = 0
    failed_files = []
    
    for community in NORTHWEST_SUBURBS_TO_FIX:
        filepath = f'C:\\Users\\mirsa\\manage369-live\\property-management\\{community}\\index.html'
        
        if not os.path.exists(filepath):
            print(f"  [SKIP] File not found: {community}")
            continue
        
        location_display = community.replace('-', ' ').title()
        
        if fix_vittoria_link(filepath, location_display):
            success_count += 1
        else:
            failed_files.append(community)
    
    print("=" * 50)
    print(f"Fix Complete!")
    print(f"Successfully fixed: {success_count} pages")
    
    if failed_files:
        print(f"\nFailed to fix {len(failed_files)} pages:")
        for f in failed_files:
            print(f"  - {f}")

if __name__ == "__main__":
    main()