import os
import re

def remove_duplicate_schemas(filepath):
    """Remove duplicate LocalBusiness schemas, keeping only the first one"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    
    # Find all script tags with LocalBusiness schemas
    pattern = r'<script type="application/ld\+json">\s*{\s*"@context":\s*"https://schema\.org",\s*"@type":\s*"LocalBusiness"[^}]*?}\s*</script>'
    
    matches = list(re.finditer(pattern, content, re.DOTALL))
    
    if len(matches) > 1:
        print(f"Processing {filepath} - Found {len(matches)} LocalBusiness schemas")
        
        # Keep the first one, remove the rest
        for match in reversed(matches[1:]):  # Work backwards, skip the first
            content = content[:match.start()] + content[match.end():]
            modified = True
            print(f"  [REMOVED] Duplicate LocalBusiness schema at position {match.start()}")
    
    # Also fix any double commas that resulted from our previous additions
    content = re.sub(r'},\s*,', '},', content)
    content = re.sub(r'}\s*,\s*,', '},', content)
    
    if '},,' in content or '  },' in content:
        modified = True
        print(f"  [FIXED] Double comma syntax errors")
    
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False

def main():
    """Remove duplicate schemas from all property management pages"""
    
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
        if remove_duplicate_schemas(filepath):
            fixed_count += 1
    
    print(f"\n[COMPLETE] Fixed duplicate schemas in {fixed_count} files")
    print("Removed duplicate LocalBusiness schemas and fixed syntax errors.")

if __name__ == "__main__":
    main()