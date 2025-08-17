import os
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse

def extract_links(file_path):
    """Extract all links from an HTML file"""
    links = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find href links
        href_pattern = r'href=["\'](.*?)["\']'
        hrefs = re.findall(href_pattern, content, re.IGNORECASE)
        
        # Find src links (images, scripts)
        src_pattern = r'src=["\'](.*?)["\']'
        srcs = re.findall(src_pattern, content, re.IGNORECASE)
        
        links.extend(hrefs)
        links.extend(srcs)
        
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return links

def check_internal_link(link, base_path):
    """Check if an internal link exists"""
    if link.startswith('http'):
        return True  # Skip external links for now
    
    if link.startswith('mailto:') or link.startswith('tel:'):
        return True  # Skip email and phone links
    
    if link.startswith('#'):
        return True  # Skip anchor links
    
    # Remove query parameters and anchors
    link = link.split('?')[0].split('#')[0]
    
    if not link:
        return True
    
    # Handle absolute paths
    if link.startswith('/'):
        link = link[1:]
    
    # Check if file exists
    file_path = Path(base_path) / link
    
    # If it's a directory, check for index.html
    if file_path.is_dir():
        index_file = file_path / 'index.html'
        return index_file.exists()
    
    # Check if file exists
    if file_path.exists():
        return True
    
    # Check if it's an HTML file without extension
    if not file_path.suffix:
        html_file = Path(str(file_path) + '.html')
        if html_file.exists():
            return True
    
    return False

def scan_website():
    """Scan all HTML files for broken links"""
    broken_links = {}
    all_links = {}
    redirect_suggestions = []
    
    # Get all HTML files
    html_files = list(Path('.').glob('**/*.html'))
    
    print(f"Scanning {len(html_files)} HTML files for broken links...")
    print("=" * 60)
    
    for html_file in html_files:
        if 'node_modules' in str(html_file) or '.git' in str(html_file):
            continue
            
        file_links = extract_links(html_file)
        relative_path = str(html_file).replace('\\', '/')
        
        for link in file_links:
            if link not in all_links:
                all_links[link] = []
            all_links[link].append(relative_path)
            
            # Check if internal link exists
            if not link.startswith('http') and not check_internal_link(link, '.'):
                if link not in broken_links:
                    broken_links[link] = []
                broken_links[link].append(relative_path)
    
    # Report broken links
    if broken_links:
        print("\n[ERROR] BROKEN INTERNAL LINKS FOUND:")
        print("-" * 60)
        for link, pages in sorted(broken_links.items())[:20]:  # Show first 20
            print(f"\n'{link}' is broken")
            print(f"  Found in: {', '.join(pages[:3])}")
            
            # Suggest redirects
            if link.endswith('/'):
                suggestion = link.rstrip('/') + '.html'
                if Path(suggestion).exists():
                    redirect_suggestions.append(f"/{link} -> /{suggestion}")
    else:
        print("\n[OK] No broken internal links found!")
    
    # Check for common redirect patterns
    print("\n" + "=" * 60)
    print("COMMON REDIRECT PATTERNS TO IMPLEMENT:")
    print("-" * 60)
    
    common_redirects = [
        ('/*.php', '/'),  # Old PHP pages to home
        ('/index.html', '/'),  # Index.html to root
        ('/home.html', '/'),  # Common variations
        ('/property-management.html', '/property-management/'),
        ('/services.html', '/services/'),
        ('/about.html', '/about.html'),
        ('/contact-us.html', '/contact.html'),
    ]
    
    for old, new in common_redirects:
        print(f"{old} -> {new}")
    
    return broken_links, redirect_suggestions

def check_htaccess():
    """Analyze .htaccess file for redirect issues"""
    htaccess_path = Path('.htaccess')
    
    print("\n" + "=" * 60)
    print("ANALYZING .HTACCESS REDIRECTS:")
    print("-" * 60)
    
    if htaccess_path.exists():
        with open(htaccess_path, 'r') as f:
            content = f.read()
        
        # Count redirect rules
        redirect_rules = re.findall(r'Redirect(Match|Permanent|Temp)?.*', content, re.IGNORECASE)
        rewrite_rules = re.findall(r'RewriteRule.*', content)
        
        print(f"Found {len(redirect_rules)} Redirect rules")
        print(f"Found {len(rewrite_rules)} RewriteRule rules")
        
        # Check for common issues
        issues = []
        
        if 'RewriteEngine On' not in content:
            issues.append("[WARNING]  RewriteEngine is not enabled")
        
        if content.count('RewriteRule') > 50:
            issues.append("[WARNING]  Too many RewriteRules (>50) - consider consolidating")
        
        if '[R=302]' in content:
            issues.append("[WARNING]  Using 302 (temporary) redirects - consider 301 for SEO")
        
        if issues:
            print("\nPotential Issues:")
            for issue in issues:
                print(f"  {issue}")
        else:
            print("[OK] No obvious redirect issues found")
    else:
        print("No .htaccess file found (using Netlify redirects instead)")

def create_redirect_map():
    """Create a comprehensive redirect map"""
    
    print("\n" + "=" * 60)
    print("CREATING 301 REDIRECT MAP:")
    print("-" * 60)
    
    redirect_map = []
    
    # Add security redirects (blocking spam)
    redirect_map.append(('/tinggi/*', '/404.html', '404'))
    redirect_map.append(('/*?wow=*', '/404.html', '404'))
    
    # Add common SEO redirects
    redirect_map.append(('/index.html', '/', '301'))
    redirect_map.append(('/home', '/', '301'))
    redirect_map.append(('/home.html', '/', '301'))
    
    # Add property management redirects (if old URLs exist)
    locations = [
        'glenview', 'winnetka', 'wilmette', 'evanston', 'highland-park',
        'northbrook', 'lake-forest', 'glencoe', 'deerfield', 'skokie'
    ]
    
    for location in locations:
        # Old URL patterns to new
        redirect_map.append(
            (f'/property-management-{location}.html', 
             f'/property-management/{location}/', '301')
        )
        redirect_map.append(
            (f'/{location}-property-management.html', 
             f'/property-management/{location}/', '301')
        )
    
    # Service page redirects
    services = [
        'condominium-management', 'hoa-management', 'townhome-management',
        'financial-management', 'maintenance-coordination'
    ]
    
    for service in services:
        redirect_map.append(
            (f'/{service}.html', f'/services/{service}/', '301')
        )
    
    return redirect_map

def generate_netlify_redirects(redirect_map):
    """Generate Netlify _redirects file content"""
    
    print("\n" + "=" * 60)
    print("NETLIFY _REDIRECTS FILE:")
    print("-" * 60)
    
    redirects_content = """# Netlify Redirects File
# Generated redirect map for manage369.com

# Security: Block spam/hacked content
/tinggi/*              /404.html              404!
/*wow=*                /404.html              404!
/*slot=*               /404.html              404!
/*casino=*             /404.html              404!
/*apk=*                /404.html              404!

# SEO: Common redirects
/index.html            /                      301!
/home                  /                      301!
/home.html             /                      301!

# Old property management URLs to new structure
"""
    
    for old, new, code in redirect_map[5:15]:  # Skip security ones, show property ones
        redirects_content += f"{old:<40} {new:<40} {code}!\n"
    
    print(redirects_content)
    
    # Save to file
    with open('_redirects_suggested.txt', 'w') as f:
        f.write(redirects_content)
    
    print("\nSaved suggested redirects to: _redirects_suggested.txt")

# Run the scan
if __name__ == "__main__":
    broken_links, suggestions = scan_website()
    check_htaccess()
    redirect_map = create_redirect_map()
    generate_netlify_redirects(redirect_map)
    
    print("\n" + "=" * 60)
    print("SCAN COMPLETE!")
    print(f"Found {len(broken_links)} broken links")
    print(f"Generated {len(redirect_map)} redirect rules")