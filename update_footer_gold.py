#!/usr/bin/env python3
"""
Update footer certifications section to gold color across all HTML pages
"""

import os
import re
from pathlib import Path

def update_footer_certifications(file_path):
    """Update the certifications section in footer to use gold color"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to find the certifications div
    # Looking for the div containing "CAI National Member"
    pattern = r'(<div style="[^"]*font-size:\s*0\.75rem[^"]*color:\s*#e5e7eb[^"]*">\s*CAI National Member<br>\s*AMS<br>\s*CMCA<br>\s*IDFPR Licensed<br>\s*License:\s*291\.000211\s*</div>)'
    
    # Replacement with gold color
    replacement = r'<div style="font-size: 0.75rem; color: #F4A261; line-height: 1.4; margin-bottom: 0.5rem; font-weight: 600;">\n                        CAI National Member<br>\n                        AMS<br>\n                        CMCA<br>\n                        IDFPR Licensed<br>\n                        License: 291.000211\n                    </div>'
    
    # Check if pattern exists
    if re.search(pattern, content):
        updated_content = re.sub(pattern, replacement, content)
        return updated_content, True
    
    # Alternative pattern (with different formatting)
    pattern2 = r'<div style="[^"]*">\s*CAI National Member<br>\s*AMS<br>\s*CMCA<br>\s*IDFPR Licensed<br>\s*License:\s*291\.000211\s*</div>'
    
    if re.search(pattern2, content):
        updated_content = re.sub(pattern2, replacement, content)
        return updated_content, True
    
    # More flexible pattern to catch variations
    pattern3 = r'(CAI National Member<br>\s*AMS<br>\s*CMCA<br>\s*IDFPR Licensed<br>\s*License:\s*291\.000211)'
    
    if re.search(pattern3, content):
        # Find the div containing this text and update its style
        div_pattern = r'(<div style="[^"]*">)(\s*CAI National Member<br>\s*AMS<br>\s*CMCA<br>\s*IDFPR Licensed<br>\s*License:\s*291\.000211\s*</div>)'
        
        def replace_div(match):
            return '<div style="font-size: 0.75rem; color: #F4A261; line-height: 1.4; margin-bottom: 0.5rem; font-weight: 600;">' + match.group(2)
        
        updated_content = re.sub(div_pattern, replace_div, content)
        return updated_content, True
    
    return content, False

def process_all_html_files():
    """Process all HTML files in the project"""
    
    root_dir = Path('C:/Users/mirsa/manage369-live')
    html_files = []
    updated_files = []
    skipped_files = []
    
    # Find all HTML files
    for path in root_dir.rglob('*.html'):
        # Skip node_modules, .git, and other build directories
        if any(skip in str(path) for skip in ['.git', 'node_modules', 'dist', 'build']):
            continue
        html_files.append(path)
    
    print(f"Found {len(html_files)} HTML files to process")
    
    # Process each file
    for file_path in html_files:
        try:
            content, was_updated = update_footer_certifications(file_path)
            
            if was_updated:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                updated_files.append(str(file_path.relative_to(root_dir)))
                print(f"[UPDATED] {file_path.relative_to(root_dir)}")
            else:
                skipped_files.append(str(file_path.relative_to(root_dir)))
                
        except Exception as e:
            print(f"[ERROR] Processing {file_path}: {e}")
    
    # Print summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Total files processed: {len(html_files)}")
    print(f"Files updated: {len(updated_files)}")
    print(f"Files skipped (no matching pattern): {len(skipped_files)}")
    
    if updated_files:
        print("\nUpdated files:")
        for f in updated_files[:10]:  # Show first 10
            print(f"  - {f}")
        if len(updated_files) > 10:
            print(f"  ... and {len(updated_files) - 10} more")
    
    return len(updated_files)

if __name__ == "__main__":
    print("Starting footer certification update...")
    print("Changing certification text to gold color (#F4A261)")
    print("-" * 60)
    
    updated_count = process_all_html_files()
    
    if updated_count > 0:
        print(f"\n[SUCCESS] Updated {updated_count} files!")
        print("The CAI National Member section is now in gold color across all pages.")
    else:
        print("\n[WARNING] No files were updated. The pattern might not match or files may already be updated.")