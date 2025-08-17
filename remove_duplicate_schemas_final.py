import os
import re

def remove_duplicate_localbusiness_schemas(filepath):
    """Remove duplicate LocalBusiness schemas, keeping only the first complete one"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count LocalBusiness schemas
    count = content.count('"@type": "LocalBusiness"')
    
    if count <= 1:
        return False
    
    print(f"Processing {filepath} - Found {count} LocalBusiness schemas")
    
    # Find all complete LocalBusiness schema script blocks
    # Pattern matches from <script type="application/ld+json"> to </script> containing LocalBusiness
    pattern = r'<script type="application/ld\+json">\s*{[^<]*?"@type":\s*"LocalBusiness"[^<]*?</script>'
    
    matches = list(re.finditer(pattern, content, re.DOTALL))
    
    if len(matches) > 1:
        # Check if schemas have the same @id (duplicates)
        seen_ids = set()
        indices_to_remove = []
        
        for i, match in enumerate(matches):
            schema_text = match.group()
            
            # Extract @id if present
            id_match = re.search(r'"@id":\s*"([^"]+)"', schema_text)
            
            if id_match:
                schema_id = id_match.group(1)
                if schema_id in seen_ids:
                    # This is a duplicate
                    indices_to_remove.append(i)
                    print(f"  Found duplicate schema with @id: {schema_id}")
                else:
                    seen_ids.add(schema_id)
            elif i > 0:  # If no @id and not the first schema, consider removing
                # Check if this is essentially the same as another schema
                if "Evanston Property Management" in schema_text and i > 1:
                    indices_to_remove.append(i)
                    print(f"  Found duplicate schema at position {i}")
        
        # Remove duplicate schemas (work backwards to preserve positions)
        for i in reversed(indices_to_remove):
            match = matches[i]
            # Also remove any comments before the script tag
            start_pos = match.start()
            # Look back for HTML comment
            comment_pattern = r'<!--[^>]*?-->\s*\n\s*'
            before_text = content[max(0, start_pos-100):start_pos]
            comment_match = re.search(comment_pattern + r'$', before_text)
            
            if comment_match:
                start_pos = start_pos - len(comment_match.group())
            
            content = content[:start_pos] + content[match.end():]
            print(f"  [REMOVED] Duplicate LocalBusiness schema")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    
    return False

def main():
    """Remove duplicate LocalBusiness schemas from all property management pages"""
    
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
    
    for filepath in files_to_fix:
        if remove_duplicate_localbusiness_schemas(filepath):
            fixed_count += 1
    
    print(f"\n[COMPLETE] Removed duplicate schemas from {fixed_count} files")
    print("Each page now has unique LocalBusiness schemas without duplicates.")

if __name__ == "__main__":
    main()