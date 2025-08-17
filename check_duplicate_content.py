import os
import re
from pathlib import Path
import hashlib

def extract_content_signature(file_path):
    """Extract content signature from HTML file using regex"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # Extract title
        title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
        title_text = title_match.group(1).strip() if title_match else ''
        
        # Get meta description
        desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html, re.IGNORECASE)
        desc_text = desc_match.group(1) if desc_match else ''
        
        # Check for existing canonical
        canonical_match = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']', html, re.IGNORECASE)
        canonical_url = canonical_match.group(1) if canonical_match else None
        
        # Get body content for hash (remove scripts and styles)
        body_text = html
        body_text = re.sub(r'<script.*?</script>', '', body_text, flags=re.IGNORECASE | re.DOTALL)
        body_text = re.sub(r'<style.*?</style>', '', body_text, flags=re.IGNORECASE | re.DOTALL)
        body_text = re.sub(r'<[^>]+>', '', body_text)  # Remove HTML tags
        body_text = ' '.join(body_text.split())[:500]  # First 500 chars
        
        return {
            'title': title_text,
            'description': desc_text,
            'content_hash': hashlib.md5(body_text.encode()).hexdigest(),
            'canonical': canonical_url,
            'file': str(file_path).replace('\\', '/')
        }
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def find_duplicates():
    """Find duplicate content across the site"""
    print("=" * 70)
    print("DUPLICATE CONTENT ANALYSIS")
    print("=" * 70)
    
    # Scan all HTML files
    html_files = list(Path('.').glob('**/*.html'))
    content_signatures = {}
    canonical_issues = []
    
    print(f"\nScanning {len(html_files)} HTML files...")
    
    for file_path in html_files:
        # Skip certain directories
        if any(skip in str(file_path) for skip in ['node_modules', '.git', 'stellar-repo', 'tinggi']):
            continue
        
        signature = extract_content_signature(file_path)
        if not signature:
            continue
        
        # Check for duplicate content
        content_key = f"{signature['title']}|{signature['content_hash']}"
        
        if content_key not in content_signatures:
            content_signatures[content_key] = []
        content_signatures[content_key].append(signature)
    
    # Find duplicates
    print("\n[DUPLICATE CONTENT FOUND]")
    print("-" * 40)
    
    duplicate_count = 0
    duplicate_groups = []
    
    for key, pages in content_signatures.items():
        if len(pages) > 1:
            duplicate_count += 1
            duplicate_groups.append(pages)
            print(f"\nDuplicate Set #{duplicate_count}:")
            print(f"  Title: {pages[0]['title'][:60]}...")
            print(f"  Files:")
            for page in pages:
                canonical_status = " [HAS CANONICAL]" if page['canonical'] else " [NO CANONICAL]"
                print(f"    - {page['file']}{canonical_status}")
    
    # Check for common duplicate patterns
    print("\n[COMMON DUPLICATE PATTERNS]")
    print("-" * 40)
    
    patterns = {
        'index_duplicates': [],
        'trailing_slash': [],
        'html_extension': []
    }
    
    # Check for index.html duplicates
    for file_path in html_files:
        path_str = str(file_path).replace('\\', '/')
        
        # Check for index.html that could be /
        if path_str.endswith('/index.html'):
            dir_path = path_str.replace('/index.html', '')
            patterns['index_duplicates'].append((path_str, dir_path))
        
        # Check for .html pages that match directory names
        if path_str.endswith('.html') and not path_str.endswith('/index.html'):
            name_without_html = path_str.replace('.html', '')
            # Check if a directory with same name exists
            potential_dir = Path(name_without_html)
            if potential_dir.exists() and potential_dir.is_dir():
                patterns['html_extension'].append((path_str, name_without_html + '/'))
    
    # Report patterns
    if patterns['index_duplicates']:
        print("\n1. Index.html duplicates (should use directory URL):")
        for orig, canonical in patterns['index_duplicates'][:5]:
            print(f"   {orig} -> {canonical}/")
    
    if patterns['html_extension']:
        print("\n2. HTML files with matching directories:")
        for orig, canonical in patterns['html_extension'][:5]:
            print(f"   {orig} -> {canonical}")
    
    # Check for missing canonicals
    print("\n[MISSING CANONICAL TAGS]")
    print("-" * 40)
    
    missing_canonical = []
    for key, pages in content_signatures.items():
        for page in pages:
            if not page['canonical']:
                missing_canonical.append(page['file'])
    
    print(f"Found {len(missing_canonical)} pages without canonical tags")
    if missing_canonical[:10]:
        print("First 10 pages missing canonical:")
        for path in missing_canonical[:10]:
            print(f"  - {path}")
    
    return duplicate_groups, patterns, missing_canonical

def generate_canonical_implementation():
    """Generate script to add canonical tags"""
    print("\n" + "=" * 70)
    print("GENERATING CANONICAL TAG IMPLEMENTATION")
    print("=" * 70)
    
    implementation = '''import os
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
            r'<link\s+rel=["\\']canonical["\\'].*?>',
            f'<link rel="canonical" href="{canonical_url}">',
            html,
            flags=re.IGNORECASE
        )
    else:
        # Add new canonical tag before </head>
        canonical_tag = f'    <link rel="canonical" href="{canonical_url}">\\n'
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
        
        path_str = str(file_path).replace('\\\\', '/').replace('./', '')
        
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
    
    print(f"\\nTotal files updated: {updated_count}")

if __name__ == "__main__":
    implement_canonicals()
'''
    
    # Save implementation script
    with open('add_canonical_tags.py', 'w') as f:
        f.write(implementation)
    
    print("Implementation script saved as: add_canonical_tags.py")
    
    return implementation

# Run analysis
if __name__ == "__main__":
    duplicates, patterns, missing = find_duplicates()
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total duplicate content groups: {len(duplicates)}")
    print(f"Pages missing canonical tags: {len(missing)}")
    print(f"Index.html duplicates: {len(patterns['index_duplicates'])}")
    
    print("\n[RECOMMENDED ACTIONS]")
    print("1. Add canonical tags to all pages")
    print("2. Use consistent URL structure (with trailing slashes for directories)")
    print("3. Redirect index.html to directory URLs")
    print("4. Implement 301 redirects for duplicate URLs")
    
    generate_canonical_implementation()