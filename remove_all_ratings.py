import os
import re

def remove_all_rating_fields(filepath):
    """Remove ALL aggregateRating and review-related fields from schemas"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    
    # Pattern to remove entire aggregateRating blocks including the comma before
    # This matches from the comma before "aggregateRating" to the closing brace
    pattern1 = r',\s*"aggregateRating":\s*\{[^}]*?"reviewCount":\s*"[^"]*"\s*\}'
    
    # Also remove any standalone aggregateRating without leading comma
    pattern2 = r'"aggregateRating":\s*\{[^}]*?"reviewCount":\s*"[^"]*"\s*\}\s*,?'
    
    # Remove all aggregateRating blocks
    new_content = re.sub(pattern1, '', content, flags=re.DOTALL)
    new_content = re.sub(pattern2, '', new_content, flags=re.DOTALL)
    
    # Also remove any review arrays that might still exist
    pattern3 = r',\s*"review":\s*\[[^\]]*?\]'
    new_content = re.sub(pattern3, '', new_content, flags=re.DOTALL)
    
    # Remove any reviewCount fields that might be standalone
    pattern4 = r',\s*"reviewCount":\s*"[^"]*"'
    new_content = re.sub(pattern4, '', new_content, flags=re.DOTALL)
    
    # Remove any ratingValue fields
    pattern5 = r',\s*"ratingValue":\s*"[^"]*"'
    new_content = re.sub(pattern5, '', new_content, flags=re.DOTALL)
    
    if new_content != content:
        modified = True
        content = new_content
        
        # Clean up any double commas or formatting issues
        content = re.sub(r',\s*,', ',', content)
        content = re.sub(r'}\s*,\s*,', '},', content)
        content = re.sub(r',\s*}', '}', content)
        content = re.sub(r'{\s*,', '{', content)
        
        print(f"  Removed all rating fields from {filepath}")
    
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False

def main():
    """Remove all rating-related fields from property management pages"""
    
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
    
    # Also check main pages
    other_files = [
        'index.html',
        'chicago-property-management-companies.html',
        'services/condominium-management/index.html'
    ]
    
    for f in other_files:
        if os.path.exists(f):
            files_to_fix.append(f)
    
    fixed_count = 0
    
    print("Removing ALL rating-related schema fields...")
    for filepath in files_to_fix:
        if remove_all_rating_fields(filepath):
            fixed_count += 1
    
    print(f"\n[COMPLETE] Removed rating fields from {fixed_count} files")
    print("Pages now have clean LocalBusiness schema without any rating/review fields.")
    print("This will resolve the 'Invalid object type for field itemReviewed' error.")

if __name__ == "__main__":
    main()