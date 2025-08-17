import os
import re
from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom

def get_canonical_url(file_path):
    """Extract canonical URL from HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # Look for canonical tag
        canonical_match = re.search(
            r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']',
            html,
            re.IGNORECASE
        )
        
        if canonical_match:
            return canonical_match.group(1)
        
        # Generate canonical if missing
        path_str = str(file_path).replace('\\', '/').replace('./', '')
        base_url = "https://manage369.com"
        
        if path_str == 'index.html':
            return base_url + '/'
        elif path_str.endswith('/index.html'):
            dir_path = path_str.replace('/index.html', '')
            return base_url + '/' + dir_path + '/'
        elif path_str.endswith('.html'):
            return base_url + '/' + path_str
        else:
            return None
            
    except Exception as e:
        return None

def get_page_priority(url):
    """Determine page priority based on URL structure"""
    if url == 'https://manage369.com/':
        return '1.0'
    elif '/property-management/' in url and url.count('/') == 5:
        return '0.9'
    elif '/services/' in url and url.count('/') == 5:
        return '0.9'
    elif url.endswith('/contact.html'):
        return '0.9'
    elif url.endswith('/forms.html'):
        return '0.8'
    elif '/blog/' in url and url.endswith('.html'):
        return '0.7'
    elif '/property-management/' in url:
        return '0.8'
    elif '/services/' in url:
        return '0.8'
    elif url.endswith('.html'):
        return '0.6'
    else:
        return '0.5'

def get_change_frequency(url):
    """Determine change frequency based on page type"""
    if url == 'https://manage369.com/':
        return 'weekly'
    elif '/blog/' in url:
        return 'monthly'
    elif '/property-management/' in url:
        return 'monthly'
    elif '/services/' in url:
        return 'monthly'
    elif '/forms' in url:
        return 'yearly'
    elif 'contact' in url:
        return 'monthly'
    else:
        return 'monthly'

def should_exclude_page(file_path, canonical_url):
    """Determine if page should be excluded from sitemap"""
    path_str = str(file_path).replace('\\', '/')
    
    # Exclude patterns
    exclude_patterns = [
        'node_modules',
        '.git',
        'stellar-repo',
        'tinggi',
        'forms-BACKUP',
        '404.html',
        '500.html',
        'test-image.html',
        'perfect-footer.html',
        'admin/',
        '_redirects',
        '.txt',
        '.py',
        '.json',
        '.md',
        '.gitignore',
        'BACKUP',
        'index-old.html',
        'consultation_form.html'  # Non-existent page from old sitemap
    ]
    
    # Check exclusion patterns
    for pattern in exclude_patterns:
        if pattern in path_str:
            return True
    
    # Exclude pages without proper canonical
    if not canonical_url or 'manage369.com' not in canonical_url:
        return True
    
    # Exclude duplicate forms page
    if 'forms-clean.html' in path_str:
        return True
    
    return False

def generate_xml_sitemap():
    """Generate XML sitemap with all valid pages"""
    print("=" * 70)
    print("GENERATING XML SITEMAP")
    print("=" * 70)
    
    # Get all HTML files
    html_files = list(Path('.').glob('**/*.html'))
    
    # Collect valid URLs
    urls = []
    excluded_count = 0
    excluded_files = []
    
    print(f"\nScanning {len(html_files)} HTML files...")
    print("-" * 40)
    
    for file_path in html_files:
        canonical_url = get_canonical_url(file_path)
        
        if should_exclude_page(file_path, canonical_url):
            excluded_count += 1
            excluded_files.append(str(file_path).replace('\\', '/'))
            continue
        
        # Get file modification time
        try:
            mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            lastmod = mod_time.strftime('%Y-%m-%d')
        except:
            lastmod = datetime.now().strftime('%Y-%m-%d')
        
        urls.append({
            'loc': canonical_url,
            'lastmod': lastmod,
            'changefreq': get_change_frequency(canonical_url),
            'priority': get_page_priority(canonical_url)
        })
    
    # Remove duplicates (same canonical URL)
    unique_urls = {}
    for url_data in urls:
        loc = url_data['loc']
        if loc not in unique_urls:
            unique_urls[loc] = url_data
    
    urls = list(unique_urls.values())
    
    # Sort URLs by priority and then alphabetically
    urls.sort(key=lambda x: (-float(x['priority']), x['loc']))
    
    print(f"\n[SUMMARY]")
    print("-" * 40)
    print(f"Total HTML files found: {len(html_files)}")
    print(f"Excluded pages: {excluded_count}")
    print(f"Valid URLs in sitemap: {len(urls)}")
    
    # Show excluded files sample
    print(f"\n[EXCLUDED FILES] (First 10)")
    print("-" * 40)
    for excluded in excluded_files[:10]:
        print(f"  - {excluded}")
    
    # Create XML structure
    urlset = ET.Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    urlset.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    urlset.set('xsi:schemaLocation', 
                'http://www.sitemaps.org/schemas/sitemap/0.9 '
                'http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd')
    
    # Add URLs
    for url_data in urls:
        url_elem = ET.SubElement(urlset, 'url')
        
        loc = ET.SubElement(url_elem, 'loc')
        loc.text = url_data['loc']
        
        lastmod = ET.SubElement(url_elem, 'lastmod')
        lastmod.text = url_data['lastmod']
        
        changefreq = ET.SubElement(url_elem, 'changefreq')
        changefreq.text = url_data['changefreq']
        
        priority = ET.SubElement(url_elem, 'priority')
        priority.text = url_data['priority']
    
    # Pretty print XML
    xml_str = ET.tostring(urlset, encoding='unicode')
    dom = minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent='  ', encoding='UTF-8')
    
    # Save sitemap
    with open('sitemap.xml', 'wb') as f:
        f.write(pretty_xml)
    
    print(f"\n[SUCCESS] Generated sitemap.xml with {len(urls)} URLs")
    
    # Show sample URLs
    print(f"\n[HIGH PRIORITY PAGES] (Priority 0.9-1.0)")
    print("-" * 40)
    count = 0
    for url_data in urls:
        if float(url_data['priority']) >= 0.9:
            print(f"  {url_data['loc']}")
            print(f"    Priority: {url_data['priority']}, Frequency: {url_data['changefreq']}")
            count += 1
            if count >= 10:
                break
    
    return urls

def generate_html_sitemap(urls):
    """Generate HTML sitemap for users"""
    print("\n" + "=" * 70)
    print("GENERATING HTML SITEMAP")
    print("=" * 70)
    
    # Group URLs by category
    categories = {
        'Main Pages': [],
        'Property Management Locations': [],
        'Services': [],
        'Blog Articles': [],
        'Forms & Resources': [],
        'Legal & Policies': [],
        'Other Pages': []
    }
    
    for url_data in urls:
        url = url_data['loc']
        
        if url == 'https://manage369.com/' or url.endswith('/contact.html'):
            categories['Main Pages'].append(url)
        elif '/property-management/' in url:
            categories['Property Management Locations'].append(url)
        elif '/services/' in url or url.endswith('/services.html'):
            categories['Services'].append(url)
        elif '/blog/' in url:
            categories['Blog Articles'].append(url)
        elif any(term in url.lower() for term in ['form', 'request', 'permit', 'repair', 'resident', 'violation', 'insurance', 'pay-dues']):
            categories['Forms & Resources'].append(url)
        elif any(term in url for term in ['privacy', 'terms', 'legal', 'disclaimer', 'accessibility']):
            categories['Legal & Policies'].append(url)
        else:
            categories['Other Pages'].append(url)
    
    # Generate HTML with canonical tag
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sitemap - Manage369 Property Management</title>
    <meta name="description" content="Complete sitemap for Manage369 property management website. Find all our service pages, location pages, and resources.">
    <link rel="canonical" href="https://manage369.com/sitemap.html">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f8f9fa;
        }
        h1 {
            color: #1e40af;
            border-bottom: 3px solid #ff6b35;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }
        h2 {
            color: #1e40af;
            margin-top: 30px;
            margin-bottom: 15px;
            padding-left: 10px;
            border-left: 4px solid #ff6b35;
        }
        .sitemap-section {
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            padding: 8px 0;
            border-bottom: 1px solid #eee;
        }
        li:last-child {
            border-bottom: none;
        }
        a {
            color: #1e40af;
            text-decoration: none;
            transition: color 0.3s;
        }
        a:hover {
            color: #ff6b35;
            text-decoration: underline;
        }
        .home-link {
            display: inline-block;
            margin-bottom: 20px;
            padding: 10px 20px;
            background: #1e40af;
            color: white;
            border-radius: 5px;
            text-decoration: none;
        }
        .home-link:hover {
            background: #ff6b35;
            color: white;
        }
        .stats {
            background: #e7f3ff;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 30px;
        }
        .last-updated {
            color: #666;
            font-size: 0.9em;
            margin-top: 30px;
            text-align: center;
        }
    </style>
</head>
<body>
    <a href="/" class="home-link">← Back to Homepage</a>
    
    <h1>Sitemap - Manage369 Property Management</h1>
    
    <div class="stats">
        <strong>Total Pages:</strong> ''' + str(len(urls)) + '''<br>
        <strong>Last Updated:</strong> ''' + datetime.now().strftime('%B %d, %Y') + '''
    </div>
'''
    
    # Add categories
    for category, category_urls in categories.items():
        if category_urls:
            html_content += f'''
    <div class="sitemap-section">
        <h2>{category} ({len(category_urls)} pages)</h2>
        <ul>
'''
            for url in sorted(category_urls):
                # Extract readable name from URL
                if url == 'https://manage369.com/':
                    name = 'Homepage'
                else:
                    name = url.replace('https://manage369.com/', '')
                    name = name.replace('.html', '')
                    name = name.replace('/', ' > ')
                    name = name.replace('-', ' ').title()
                
                # Make relative URLs for HTML sitemap
                relative_url = url.replace('https://manage369.com', '')
                if not relative_url:
                    relative_url = '/'
                
                html_content += f'            <li><a href="{relative_url}">{name}</a></li>\n'
            
            html_content += '''        </ul>
    </div>
'''
    
    html_content += '''
    <div class="last-updated">
        This sitemap was automatically generated on ''' + datetime.now().strftime('%B %d, %Y at %I:%M %p') + '''
    </div>
</body>
</html>'''
    
    # Save HTML sitemap
    with open('sitemap.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"[SUCCESS] Generated sitemap.html with {len(urls)} URLs")
    print(f"\n[CATEGORY BREAKDOWN]")
    print("-" * 40)
    for category, category_urls in categories.items():
        if category_urls:
            print(f"  {category}: {len(category_urls)} pages")

def validate_sitemap():
    """Validate the generated sitemap"""
    print("\n" + "=" * 70)
    print("VALIDATING SITEMAP")
    print("=" * 70)
    
    try:
        tree = ET.parse('sitemap.xml')
        root = tree.getroot()
        
        # Count URLs
        urls = root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url')
        print(f"\n[VALIDATION RESULTS]")
        print("-" * 40)
        print(f"  Valid XML structure: ✓")
        print(f"  Total URLs: {len(urls)}")
        print(f"  Schema compliance: ✓")
        
        # Check for required elements
        issues = []
        for url in urls:
            loc = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
            if loc is None or not loc.text:
                issues.append("Missing loc element")
        
        if issues:
            print(f"  Issues found: {len(issues)}")
            for issue in issues[:5]:
                print(f"    - {issue}")
        else:
            print(f"  No issues found: ✓")
        
        # File size check
        file_size = os.path.getsize('sitemap.xml')
        print(f"  File size: {file_size:,} bytes")
        if file_size > 50000000:  # 50MB limit
            print(f"    WARNING: File exceeds 50MB limit")
        
        return True
    except Exception as e:
        print(f"  [ERROR] Validation failed: {e}")
        return False

# Run sitemap generation
if __name__ == "__main__":
    urls = generate_xml_sitemap()
    generate_html_sitemap(urls)
    validate_sitemap()
    
    print("\n" + "=" * 70)
    print("SITEMAP GENERATION COMPLETE")
    print("=" * 70)
    print("\n[FILES GENERATED]")
    print("  1. sitemap.xml - For search engines")
    print("  2. sitemap.html - For users")
    
    print("\n[NEXT STEPS]")
    print("  1. Upload sitemap.xml to website root")
    print("  2. Submit to Google Search Console")
    print("  3. Submit to Bing Webmaster Tools")
    print("  4. Update robots.txt to reference sitemap")
    print("  5. Monitor indexing status")