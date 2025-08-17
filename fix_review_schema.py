import os
import re
import json

def fix_review_schema_in_file(filepath):
    """Fix Review schema by adding itemReviewed field"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    
    # Pattern to find Review objects without itemReviewed
    # This pattern finds the review array within Organization/LocalBusiness schema
    pattern = r'("review":\s*\[\s*{\s*"@type":\s*"Review")'
    
    matches = list(re.finditer(pattern, content))
    
    if matches:
        print(f"Fixing {filepath}...")
        
        # Work backwards through matches to preserve string positions
        for match in reversed(matches):
            # Check if itemReviewed already exists nearby
            check_area = content[match.start():match.end() + 500]
            if '"itemReviewed"' not in check_area:
                # Insert itemReviewed after @type: Review
                insert_pos = match.end()
                
                # Find the organization/business name from the same schema block
                # Look backwards for the organization name
                before_content = content[:match.start()]
                org_name_match = re.search(r'"name":\s*"([^"]+)"', before_content[::-1])
                if org_name_match:
                    org_name = org_name_match.group(1)[::-1]
                else:
                    org_name = "Manage369 Property Management"
                
                itemReviewed = ''',
          "itemReviewed": {
            "@type": "Organization",
            "name": "''' + org_name + '"' + '''
          }'''
                
                content = content[:insert_pos] + itemReviewed + content[insert_pos:]
                modified = True
    
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  [FIXED] Review schema in {filepath}")
        return True
    
    return False

def main():
    """Fix Review schema in all HTML files"""
    
    # Files to check
    files_to_fix = [
        'index.html',
        'chicago-property-management-companies.html',
        'services/condominium-management/index.html'
    ]
    
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
        if os.path.exists(filepath):
            if fix_review_schema_in_file(filepath):
                fixed_count += 1
    
    print(f"\n[COMPLETE] Fixed Review schema in {fixed_count} files")
    print("\nThe Review schemas now include the required 'itemReviewed' field.")
    print("This should resolve the Google Search Console validation error.")

if __name__ == "__main__":
    main()