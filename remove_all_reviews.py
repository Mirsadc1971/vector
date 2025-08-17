import os
import re

def remove_all_review_sections(filepath):
    """Remove ALL review arrays from the file, keep only aggregateRating"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    
    # Pattern to match entire review array sections
    # This matches from ,"review": [ to the closing ]
    pattern = r',\s*"review":\s*\[[^\]]*?\{[^\]]*?\}[^\]]*?\]'
    
    # Remove all review sections
    new_content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    if new_content != content:
        modified = True
        content = new_content
        print(f"  Removed review sections from {filepath}")
    
    # Clean up any double commas or formatting issues
    content = re.sub(r',\s*,', ',', content)
    content = re.sub(r'}\s*,\s*,', '},', content)
    content = re.sub(r',\s*}', '}', content)
    
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False

def main():
    """Remove all review sections from property management pages"""
    
    files_to_fix = []
    
    # Add all property management location pages
    property_mgmt_dir = 'property-management'
    if os.path.exists(property_mgmt_dir):
        for location in os.listdir(property_mgmt_dir):
            location_path = os.path.join(property_mgmt_dir, location)
            if os.path.isdir(location_path):
                index_file = os.path.join(location_path, 'index.html')
                if os.path.exists(index_file):
                    files_to_fix.append(index_file)
    
    fixed_count = 0
    
    print("Removing ALL review sections from pages...")
    for filepath in files_to_fix:
        if remove_all_review_sections(filepath):
            fixed_count += 1
    
    print(f"\n[COMPLETE] Removed review sections from {fixed_count} files")
    print("Pages now only have aggregateRating without review arrays.")

if __name__ == "__main__":
    main()