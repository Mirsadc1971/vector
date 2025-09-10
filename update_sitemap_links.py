#!/usr/bin/env python3

import os
import re

def update_sitemap_links():
    """Update all sitemap.html links to sitemap.xml"""
    
    updated_files = []
    
    # Find all HTML files
    for root, dirs, files in os.walk('.'):
        # Skip certain directories
        if any(skip in root for skip in ['.git', 'node_modules', '.claude']):
            continue
            
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check if file contains sitemap.html
                    if 'sitemap.html' in content:
                        # Replace sitemap.html with sitemap.xml
                        new_content = content.replace('sitemap.html', 'sitemap.xml')
                        
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        
                        updated_files.append(filepath)
                        print(f"[OK] Updated {filepath}")
                        
                except Exception as e:
                    print(f"[SKIP] Error processing {filepath}: {e}")
    
    print(f"\n[COMPLETE] Updated {len(updated_files)} files")
    print("\nUpdated files:")
    for file in updated_files[:10]:  # Show first 10
        print(f"  - {file}")
    if len(updated_files) > 10:
        print(f"  ... and {len(updated_files) - 10} more")

if __name__ == "__main__":
    update_sitemap_links()