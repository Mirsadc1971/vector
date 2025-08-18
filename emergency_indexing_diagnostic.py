"""
EMERGENCY: Diagnose why Google won't index ANY pages
"""

import os
import re

def check_critical_issues():
    """Check for critical indexing blockers"""
    
    print("EMERGENCY INDEXING DIAGNOSTIC")
    print("=" * 50)
    
    issues_found = []
    
    # 1. Check a sample page for common blockers
    sample_file = 'C:\\Users\\mirsa\\manage369-live\\index.html'
    
    with open(sample_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for noindex
    if 'noindex' in content.lower():
        issues_found.append("CRITICAL: noindex found in content")
    
    # Check for X-Robots-Tag
    if 'x-robots-tag' in content.lower():
        issues_found.append("CRITICAL: X-Robots-Tag found")
    
    # Check canonical tag
    canonical_match = re.search(r'<link[^>]*rel="canonical"[^>]*>', content)
    if canonical_match:
        print(f"Canonical found: {canonical_match.group(0)[:100]}")
    else:
        issues_found.append("WARNING: No canonical tag found")
    
    # Check if page is mostly JavaScript
    script_count = content.count('<script')
    noscript_count = content.count('<noscript')
    
    if script_count > 20:
        issues_found.append(f"WARNING: High script count ({script_count})")
    
    if noscript_count == 0:
        issues_found.append("WARNING: No <noscript> tags for fallback content")
    
    # Check meta robots
    robots_meta = re.search(r'<meta[^>]*name="robots"[^>]*content="([^"]*)"', content)
    if robots_meta:
        robots_content = robots_meta.group(1)
        print(f"Meta robots: {robots_content}")
        if 'noindex' in robots_content or 'none' in robots_content:
            issues_found.append(f"CRITICAL: Bad robots meta: {robots_content}")
    
    # Check for blocking JavaScript
    if 'window.location' in content:
        redirect_count = content.count('window.location')
        if redirect_count > 0:
            issues_found.append(f"WARNING: JavaScript redirects found ({redirect_count})")
    
    # Check for forms that might trigger soft 404
    form_count = content.count('<form')
    if form_count > 3:
        issues_found.append(f"WARNING: Many forms on page ({form_count})")
    
    # Check title and description
    title_match = re.search(r'<title>([^<]*)</title>', content)
    if not title_match:
        issues_found.append("CRITICAL: No title tag")
    elif len(title_match.group(1)) < 10:
        issues_found.append("WARNING: Title too short")
    
    desc_match = re.search(r'<meta[^>]*name="description"[^>]*content="([^"]*)"', content)
    if not desc_match:
        issues_found.append("WARNING: No meta description")
    elif len(desc_match.group(1)) < 50:
        issues_found.append("WARNING: Description too short")
    
    # Check for HTTP vs HTTPS issues
    http_links = content.count('http://')
    if http_links > 0:
        issues_found.append(f"WARNING: Non-HTTPS links found ({http_links})")
    
    # Check viewport
    if 'viewport' not in content:
        issues_found.append("CRITICAL: No viewport meta tag")
    
    # Check for structured data errors
    ld_json_count = content.count('application/ld+json')
    if ld_json_count > 5:
        issues_found.append(f"WARNING: Too many structured data blocks ({ld_json_count})")
    
    # Report findings
    print("\nISSUES FOUND:")
    if issues_found:
        for issue in issues_found:
            print(f"  - {issue}")
    else:
        print("  No obvious blockers found")
    
    print("\n" + "=" * 50)
    return issues_found

def check_all_pages_for_pattern():
    """Check all pages for common patterns"""
    
    print("\nCHECKING ALL PAGES FOR PATTERNS...")
    
    root_dir = 'C:\\Users\\mirsa\\manage369-live'
    
    noindex_pages = []
    no_canonical_pages = []
    redirect_pages = []
    
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for filename in files:
            if filename.endswith('.html'):
                filepath = os.path.join(root, filename)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check for noindex
                    if 'noindex' in content.lower():
                        noindex_pages.append(filepath)
                    
                    # Check for canonical
                    if 'rel="canonical"' not in content:
                        no_canonical_pages.append(filepath)
                    
                    # Check for JS redirects
                    if 'window.location.replace' in content or 'window.location.href' in content:
                        redirect_pages.append(filepath)
                
                except:
                    pass
    
    print(f"\nPages with noindex: {len(noindex_pages)}")
    if noindex_pages:
        for p in noindex_pages[:5]:
            print(f"  - {p}")
    
    print(f"\nPages without canonical: {len(no_canonical_pages)}")
    if no_canonical_pages:
        for p in no_canonical_pages[:5]:
            print(f"  - {p}")
    
    print(f"\nPages with JS redirects: {len(redirect_pages)}")
    if redirect_pages:
        for p in redirect_pages[:5]:
            print(f"  - {p}")

def check_netlify_settings():
    """Check for Netlify configuration issues"""
    
    print("\n" + "=" * 50)
    print("CHECKING DEPLOYMENT CONFIGURATION...")
    
    # Check for _redirects file
    if os.path.exists('_redirects'):
        with open('_redirects', 'r') as f:
            redirects = f.read()
        
        print("\n_redirects file found:")
        print(redirects[:500])
        
        if '/*' in redirects:
            print("WARNING: Wildcard redirects found - may cause issues")
    
    # Check for netlify.toml
    if os.path.exists('netlify.toml'):
        with open('netlify.toml', 'r') as f:
            config = f.read()
        
        print("\nnetlify.toml found:")
        print(config[:500])
        
        if 'X-Robots-Tag' in config:
            print("CRITICAL: X-Robots-Tag found in Netlify config!")

def create_emergency_fix():
    """Create emergency fix for all indexing issues"""
    
    print("\n" + "=" * 50)
    print("CREATING EMERGENCY FIX...")
    
    fix_script = '''"""
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
    content = re.sub(r'noindex[,\\s]*', '', content, flags=re.IGNORECASE)
    
    # Fix robots meta tag
    content = re.sub(
        r'<meta name="robots" content="[^"]*">', 
        '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">', 
        content
    )
    
    # Add canonical if missing
    if 'rel="canonical"' not in content:
        # Get the URL from the file path
        rel_path = filepath.replace('C:\\\\Users\\\\mirsa\\\\manage369-live\\\\', '').replace('\\\\', '/')
        if rel_path == 'index.html':
            url = 'https://manage369.com/'
        elif rel_path.endswith('index.html'):
            url = 'https://manage369.com/' + rel_path.replace('index.html', '')
        else:
            url = 'https://manage369.com/' + rel_path
        
        canonical = f'    <link rel="canonical" href="{url}">\\n'
        
        # Add after title
        content = re.sub(r'(</title>)', r'\\1\\n' + canonical, content)
    
    # Remove any JavaScript redirects
    content = re.sub(r'window\\.location\\.[^;]+;', '', content)
    
    # Ensure viewport exists
    if 'viewport' not in content:
        viewport = '    <meta name="viewport" content="width=device-width, initial-scale=1.0">\\n'
        content = re.sub(r'(<head[^>]*>)', r'\\1\\n' + viewport, content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Fix all HTML files
fixed = 0
for root, dirs, files in os.walk('C:\\\\Users\\\\mirsa\\\\manage369-live'):
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    
    for filename in files:
        if filename.endswith('.html'):
            filepath = os.path.join(root, filename)
            if fix_page(filepath):
                fixed += 1

print(f"Fixed {fixed} pages")
'''
    
    with open('emergency_fix_indexing.py', 'w') as f:
        f.write(fix_script)
    
    print("Created emergency_fix_indexing.py")

# Run diagnostics
issues = check_critical_issues()
check_all_pages_for_pattern()
check_netlify_settings()
create_emergency_fix()

print("\n" + "=" * 50)
print("DIAGNOSTIC COMPLETE")
print("\nMOST LIKELY CAUSES:")
print("1. Netlify configuration blocking crawlers")
print("2. JavaScript rendering issues")
print("3. Soft 404 errors")
print("4. Canonical tag issues")
print("\nNEXT STEPS:")
print("1. Run emergency_fix_indexing.py")
print("2. Check Netlify dashboard for headers/redirects")
print("3. Test with Google's URL Inspection tool")
print("4. Check for manual actions in Search Console")