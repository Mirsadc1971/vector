import os
import re

def remove_duplicate_review_arrays(filepath):
    """Remove duplicate review arrays, keeping only one per schema block"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    
    # Pattern to find complete review arrays
    review_pattern = r',\s*"review":\s*\[[^\]]*?\](?:\s*\])?'
    
    # Split content by schema blocks (each LocalBusiness schema)
    schema_blocks = content.split('"@type": "LocalBusiness"')
    
    for i in range(1, len(schema_blocks)):  # Skip first split (before first schema)
        block = schema_blocks[i]
        
        # Find all review arrays in this block
        review_matches = list(re.finditer(review_pattern, block, re.DOTALL))
        
        if len(review_matches) > 1:
            print(f"  Found {len(review_matches)} review arrays in block {i}")
            # Keep only the first review array, remove the rest
            for match in reversed(review_matches[1:]):
                block = block[:match.start()] + block[match.end():]
                modified = True
            
            schema_blocks[i] = block
    
    if modified:
        # Reconstruct the content
        content = ('"@type": "LocalBusiness"').join(schema_blocks)
        
        # Clean up any double commas or formatting issues
        content = re.sub(r',\s*,', ',', content)
        content = re.sub(r'}\s*,\s*,', '},', content)
        content = re.sub(r',\s*}', '}', content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"[FIXED] {filepath}")
        return True
    
    return False

def main():
    """Remove duplicate review arrays from all property management pages"""
    
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
    
    print("Removing duplicate review arrays...")
    for filepath in files_to_fix:
        if remove_duplicate_review_arrays(filepath):
            fixed_count += 1
    
    print(f"\n[COMPLETE] Fixed {fixed_count} files")
    print("Each LocalBusiness schema now has only one review array.")

if __name__ == "__main__":
    main()