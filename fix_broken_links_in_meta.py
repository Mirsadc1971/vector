"""
Fix broken HTML links that were accidentally added to meta descriptions
"""

import os
import re

def fix_meta_descriptions(filepath):
    """Remove HTML from meta descriptions"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix meta descriptions with HTML
    content = re.sub(
        r'<meta[^>]*name="description"[^>]*content="([^"]*)<a[^>]*>([^<]*)</a>([^"]*)"',
        r'<meta name="description" content="\1\2\3"',
        content
    )
    
    # Fix broken links in navigation
    content = re.sub(
        r'<a href="[^"]*<a href="[^"]*"[^>]*>[^<]*</a>[^"]*">',
        '',
        content
    )
    
    # Fix title tags with HTML
    content = re.sub(
        r'<title>([^<]*)<a[^>]*>([^<]*)</a>([^<]*)</title>',
        r'<title>\1\2\3</title>',
        content
    )
    
    return content

# Fix all affected files
files_fixed = 0

for root, dirs, files in os.walk('C:\\Users\\mirsa\\manage369-live'):
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    
    for filename in files:
        if filename.endswith('.html'):
            filepath = os.path.join(root, filename)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if '<a href=' in content and 'name="description"' in content:
                    fixed_content = fix_meta_descriptions(filepath)
                    
                    if fixed_content != content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(fixed_content)
                        files_fixed += 1
            except:
                pass

print(f"Fixed {files_fixed} files with broken meta descriptions")