import os
import re

def remove_fake_property_listings(filepath):
    """Remove fake property names and replace with generic descriptions"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    
    # Pattern to find the Properties We Manage section
    # This matches from the h3 tag to the closing </ul>
    pattern = r'(<h3[^>]*>[^<]*Properties We Manage[^<]*</h3>\s*<ul[^>]*>)(.*?)(</ul>)'
    
    def replace_properties(match):
        # Replace with generic descriptions
        generic_properties = """<li style="padding: 8px 0; color: #555;"><i class="fas fa-building" style="color: #4285f4; margin-right: 10px;"></i>Multiple condominium associations</li>
<li style="padding: 8px 0; color: #555;"><i class="fas fa-building" style="color: #4285f4; margin-right: 10px;"></i>Townhome communities</li>
<li style="padding: 8px 0; color: #555;"><i class="fas fa-building" style="color: #4285f4; margin-right: 10px;"></i>HOA-managed properties</li>
<li style="padding: 8px 0; color: #555;"><i class="fas fa-building" style="color: #4285f4; margin-right: 10px;"></i>Residential complexes</li>
"""
        return match.group(1) + generic_properties + match.group(3)
    
    # Replace the properties section
    new_content = re.sub(pattern, replace_properties, content, flags=re.DOTALL)
    
    if new_content != content:
        modified = True
        content = new_content
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  Removed fake properties from {filepath}")
        return True
    
    return False

def main():
    """Remove fake property listings from all location pages"""
    
    property_mgmt_dir = 'property-management'
    processed = 0
    
    if os.path.exists(property_mgmt_dir):
        locations = os.listdir(property_mgmt_dir)
        print(f"Processing {len(locations)} location directories...")
        
        for location in locations:
            location_path = os.path.join(property_mgmt_dir, location)
            if os.path.isdir(location_path):
                index_file = os.path.join(location_path, 'index.html')
                if os.path.exists(index_file):
                    if remove_fake_property_listings(index_file):
                        processed += 1
    
    print(f"\n[COMPLETE] Removed fake property listings from {processed} pages")
    print("All pages now have generic property descriptions instead of fake names")

if __name__ == "__main__":
    main()