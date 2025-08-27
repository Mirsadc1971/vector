#!/usr/bin/env python3
"""
Fix all URLs to use www.manage369.com consistently
This fixes the critical SEO issue of mixed URL versions
"""

import os
import re
from pathlib import Path

def fix_urls_in_file(filepath):
    """Replace all non-www URLs with www URLs"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Count replacements for reporting
        count = 0
        
        # Replace all variations of manage369.com with www.manage369.com
        patterns = [
            (r'https://manage369\.com', 'https://www.manage369.com'),
            (r'http://manage369\.com', 'https://www.manage369.com'),
            (r'"manage369\.com', '"www.manage369.com'),
            (r'>manage369\.com', '>www.manage369.com'),
        ]
        
        for pattern, replacement in patterns:
            new_content, n = re.subn(pattern, replacement, content)
            count += n
            content = new_content
        
        if count > 0:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return count
        return 0
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return 0

def main():
    """Fix all HTML files in the project"""
    root = Path('.')
    total_files = 0
    total_replacements = 0
    
    # Find all HTML files
    html_files = list(root.glob('**/*.html'))
    
    print(f"Found {len(html_files)} HTML files to process...")
    print("-" * 50)
    
    for filepath in html_files:
        # Skip node_modules and other build directories
        if 'node_modules' in str(filepath) or '.git' in str(filepath):
            continue
        
        replacements = fix_urls_in_file(filepath)
        if replacements > 0:
            print(f"Fixed {replacements} URLs in: {filepath}")
            total_files += 1
            total_replacements += replacements
    
    print("-" * 50)
    print(f"COMPLETE: Fixed {total_replacements} URLs across {total_files} files")
    print("\nNOTE: Remember to also update:")
    print("1. Google Search Console - verify www version")
    print("2. Google Business Profile - update website URL")
    print("3. Any backlinks you control")
    print("4. Social media profiles")

if __name__ == "__main__":
    main()