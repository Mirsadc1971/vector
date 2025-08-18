"""
EMERGENCY FIX: Force pages to be indexable
"""

import os
import re

def fix_page(filepath):
    """Fix all indexing issues in a page"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Remove any noindex
    content = re.sub(r'noindex[,\s]*', '', content, flags=re.IGNORECASE)
    
    # Fix robots meta tag
    content = re.sub(
        r'<meta name="robots" content="[^"]*">', 
        '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">', 
        content
    )
    
    # Add canonical if missing
    if 'rel="canonical"' not in content:
        # Get the URL from the file path
        rel_path = filepath.replace('C:\\Users\\mirsa\\manage369-live\\', '').replace('\\', '/')
        if rel_path == 'index.html':
            url = 'https://manage369.com/'
        elif rel_path.endswith('index.html'):
            url = 'https://manage369.com/' + rel_path.replace('index.html', '')
        else:
            url = 'https://manage369.com/' + rel_path
        
        canonical = f'    <link rel="canonical" href="{url}">\n'
        
        # Add after title
        content = re.sub(r'(</title>)', r'\1\n' + canonical, content)
    
    # Remove any JavaScript redirects
    content = re.sub(r'window\.location\.[^;]+;', '', content)
    
    # Ensure viewport exists
    if 'viewport' not in content:
        viewport = '    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        content = re.sub(r'(<head[^>]*>)', r'\1\n' + viewport, content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Fix all HTML files
fixed = 0
for root, dirs, files in os.walk('C:\\Users\\mirsa\\manage369-live'):
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    
    for filename in files:
        if filename.endswith('.html'):
            filepath = os.path.join(root, filename)
            if fix_page(filepath):
                fixed += 1

print(f"Fixed {fixed} pages")
