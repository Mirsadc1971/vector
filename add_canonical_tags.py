import os
import re
from pathlib import Path

def add_canonical_tag(file_path, canonical_url):
    """Add or update canonical tag in HTML file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Check if canonical already exists
    if '<link rel="canonical"' in html:
        # Update existing
        html = re.sub(
            r'<link\s+rel=["\']canonical["\'].*?>',
            f'<link rel="canonical" href="{canonical_url}">',
            html,
            flags=re.IGNORECASE
        )
    else:
        # Add new canonical tag before </head>
        canonical_tag = f'    <link rel="canonical" href="{canonical_url}">\n'
        html = html.replace('</head>', canonical_tag + '</head>')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return True

def implement_canonicals():
    """Add canonical tags to all HTML files"""
    base_url = "https://manage369.com"
    updated_count = 0
    
    # Process all HTML files
    for file_path in Path('.').glob('**/*.html'):
        # Skip unwanted directories
        if any(skip in str(file_path) for skip in ['node_modules', '.git', 'stellar-repo', 'tinggi', 'forms-BACKUP']):
            continue
        
        path_str = str(file_path).replace('\\', '/').replace('./', '')
        
        # Determine canonical URL
        if path_str == 'index.html':
            canonical = base_url + '/'
        elif path_str.endswith('/index.html'):
            # Directory index files
            dir_path = path_str.replace('/index.html', '')
            canonical = base_url + '/' + dir_path + '/'
        elif path_str == '404.html' or path_str == '500.html':
            # Error pages don't need canonical
            continue
        elif path_str.endswith('.html'):
            # Regular HTML files
            canonical = base_url + '/' + path_str
        else:
            canonical = base_url + '/' + path_str
        
        # Clean up double slashes (except after https:)
        canonical = re.sub(r'(?<!:)//+', '/', canonical)
        
        try:
            if add_canonical_tag(file_path, canonical):
                updated_count += 1
                print(f"Updated: {path_str} -> {canonical}")
        except Exception as e:
            print(f"Error updating {path_str}: {e}")
    
    print(f"\nTotal files updated: {updated_count}")

if __name__ == "__main__":
    implement_canonicals()
