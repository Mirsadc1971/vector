"""
Fix duplicate certifications in footer
"""

import os
import re

def fix_duplicate_certs(content):
    """Remove duplicate certification badges"""
    
    # Pattern to find the certifications div
    cert_pattern = r'(<div class="certifications">)(.*?)(</div>\s*</div>)'
    
    # Clean certification badges
    clean_certs = """
            <div class="cert-badge">CAI</div>
            <div class="cert-badge">CCIM</div>
            <div class="cert-badge">IDFPR</div>
            <div class="cert-badge">IREM</div>
            <div class="cert-badge">NAR</div>"""
    
    def replace_certs(match):
        return match.group(1) + clean_certs + '</div>'
    
    # Replace duplicated certifications
    content = re.sub(cert_pattern, replace_certs, content, flags=re.DOTALL)
    
    return content

# Process all pages
root_dir = 'C:\\Users\\mirsa\\manage369-live'
pages_fixed = 0

# Check all HTML files
for root, dirs, files in os.walk(root_dir):
    # Skip .git and other hidden directories
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    
    for filename in files:
        if filename.endswith('.html'):
            filepath = os.path.join(root, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if page has duplicate cert badges
            if content.count('cert-badge') > 10:  # More than 2 sets of 5 badges
                new_content = fix_duplicate_certs(content)
                
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    pages_fixed += 1
                    relative_path = os.path.relpath(filepath, root_dir)
                    print(f"Fixed: {relative_path}")

print(f"\n[COMPLETE] Fixed {pages_fixed} pages with duplicate certifications")