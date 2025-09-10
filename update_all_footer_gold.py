#!/usr/bin/env python3
"""
Update ALL footer headers and sections to gold color across all HTML pages
"""

import os
import re
from pathlib import Path

def update_footer_to_gold(file_path):
    """Update all footer headers and sections to use gold color"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Update MANAGE369 header
    content = re.sub(
        r'<h3 style="[^"]*color:\s*#[A-Fa-f0-9]+[^"]*">(MANAGE369|Manage369)</h3>',
        r'<h3 style="font-size: 1.1rem; margin: 0 0 0.3rem 0; color: #F4A261; font-weight: 600;">\1</h3>',
        content
    )
    
    # Update Services header
    content = re.sub(
        r'<h4 style="[^"]*color:\s*#[A-Fa-f0-9]+[^"]*">(Services)</h4>',
        r'<h4 style="font-size: 0.9rem; margin: 0 0 0.3rem 0; color: #F4A261; font-weight: 600;">Services</h4>',
        content
    )
    
    # Update Quick Links header
    content = re.sub(
        r'<h4 style="[^"]*color:\s*#[A-Fa-f0-9]+[^"]*">(Quick Links)</h4>',
        r'<h4 style="font-size: 0.9rem; margin: 0 0 0.3rem 0; color: #F4A261; font-weight: 600;">Quick Links</h4>',
        content
    )
    
    # Update Resources header
    content = re.sub(
        r'<h4 style="[^"]*color:\s*#[A-Fa-f0-9]+[^"]*">(Resources)</h4>',
        r'<h4 style="font-size: 0.9rem; margin: 0 0 0.3rem 0; color: #F4A261; font-weight: 600;">Resources</h4>',
        content
    )
    
    # Update Areas We Serve header (if exists)
    content = re.sub(
        r'<h4 style="[^"]*color:\s*#[A-Fa-f0-9]+[^"]*">(Areas We Serve|Service Areas)</h4>',
        r'<h4 style="font-size: 0.9rem; margin: 0 0 0.3rem 0; color: #F4A261; font-weight: 600;">\1</h4>',
        content
    )
    
    # Update Certifications header (if exists)
    content = re.sub(
        r'<h4 style="[^"]*color:\s*#[A-Fa-f0-9]+[^"]*">(Certifications|Credentials)</h4>',
        r'<h4 style="font-size: 0.9rem; margin: 0 0 0.3rem 0; color: #F4A261; font-weight: 600;">\1</h4>',
        content
    )
    
    # Already handled certifications text in previous script, but ensure it's gold
    # Pattern for certifications div
    pattern = r'<div style="[^"]*font-size:\s*0\.75rem[^"]*color:\s*#[A-Fa-f0-9]+[^"]*">\s*(CAI National Member<br>)'
    if re.search(pattern, content):
        content = re.sub(
            pattern,
            r'<div style="font-size: 0.75rem; color: #F4A261; line-height: 1.4; margin-bottom: 0.5rem; font-weight: 600;">\1',
            content
        )
    
    # Check if any changes were made
    was_updated = content != original_content
    
    return content, was_updated

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
            content, was_updated = update_footer_to_gold(file_path)
            
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
    print(f"Files skipped (no changes needed): {len(skipped_files)}")
    
    if updated_files:
        print("\nUpdated files:")
        for f in updated_files[:10]:  # Show first 10
            print(f"  - {f}")
        if len(updated_files) > 10:
            print(f"  ... and {len(updated_files) - 10} more")
    
    return len(updated_files)

if __name__ == "__main__":
    print("Starting footer update to gold color...")
    print("Changing ALL footer headers to gold (#F4A261)")
    print("-" * 60)
    
    updated_count = process_all_html_files()
    
    if updated_count > 0:
        print(f"\n[SUCCESS] Updated {updated_count} files!")
        print("All footer headers are now in gold color across all pages.")
    else:
        print("\n[WARNING] No files were updated. Headers may already be gold or pattern didn't match.")