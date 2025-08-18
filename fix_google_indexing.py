"""
Emergency Google Indexing Fix
This script ensures all pages are properly configured for Google indexing
"""

import os
import re
from datetime import datetime

def update_sitemap():
    """Generate fresh sitemap with all pages"""
    
    # Get all HTML files
    all_pages = []
    root_dir = 'C:\\Users\\mirsa\\manage369-live'
    
    # Root pages
    for filename in os.listdir(root_dir):
        if filename.endswith('.html') and not filename.startswith('test'):
            if filename in ['index.html', 'contact.html', 'services.html', 'payment-methods.html', 
                          'forms.html', 'accessibility.html', 'privacy-policy.html', 
                          'terms-of-service.html', 'sitemap.html', 'legal-disclaimers.html']:
                priority = '1.0' if filename == 'index.html' else '0.8'
                all_pages.append((f"https://manage369.com/{filename}", priority))
    
    # Property management pages - HIGH PRIORITY
    prop_dir = os.path.join(root_dir, 'property-management')
    for location in os.listdir(prop_dir):
        if os.path.isdir(os.path.join(prop_dir, location)):
            all_pages.append((f"https://manage369.com/property-management/{location}/", '0.9'))
    
    # Service pages
    service_dir = os.path.join(root_dir, 'services')
    if os.path.exists(service_dir):
        for filename in os.listdir(service_dir):
            if os.path.isdir(os.path.join(service_dir, filename)):
                all_pages.append((f"https://manage369.com/services/{filename}/", '0.8'))
    
    # Blog pages
    blog_dir = os.path.join(root_dir, 'blog')
    if os.path.exists(blog_dir):
        for filename in os.listdir(blog_dir):
            if filename.endswith('.html'):
                name = filename.replace('.html', '')
                if name == 'index':
                    all_pages.append((f"https://manage369.com/blog/", '0.7'))
                else:
                    all_pages.append((f"https://manage369.com/blog/{filename}", '0.7'))
    
    # Generate sitemap
    today = datetime.now().strftime('%Y-%m-%d')
    
    sitemap_content = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" 
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 
        http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
'''
    
    for url, priority in all_pages:
        freq = 'weekly' if priority == '1.0' else 'monthly'
        sitemap_content += f'''  <url>
    <loc>{url}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{priority}</priority>
  </url>
'''
    
    sitemap_content += '</urlset>'
    
    # Write sitemap
    with open(os.path.join(root_dir, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    
    print(f"[SUCCESS] Sitemap updated with {len(all_pages)} pages")
    return len(all_pages)

def fix_meta_tags():
    """Ensure all pages have proper meta tags for indexing"""
    
    root_dir = 'C:\\Users\\mirsa\\manage369-live'
    pages_fixed = 0
    
    # Process all HTML files
    for root, dirs, files in os.walk(root_dir):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for filename in files:
            if filename.endswith('.html') and not filename.startswith('test'):
                filepath = os.path.join(root, filename)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check if robots meta tag exists
                if 'name="robots"' not in content:
                    # Add robots meta tag after viewport
                    viewport_match = re.search(r'(<meta name="viewport"[^>]*>)', content)
                    if viewport_match:
                        robots_tag = '\n    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">'
                        content = content.replace(viewport_match.group(0), 
                                                viewport_match.group(0) + robots_tag)
                        
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)
                        pages_fixed += 1
                
                # Ensure no noindex
                if 'noindex' in content.lower():
                    content = re.sub(r'noindex[,\s]*', '', content, flags=re.IGNORECASE)
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    pages_fixed += 1
    
    print(f"[SUCCESS] Fixed meta tags on {pages_fixed} pages")
    return pages_fixed

def create_indexing_api_script():
    """Create script for Google Indexing API submission"""
    
    script = '''"""
Google Search Console Indexing API Script
Run this after deployment to request indexing of key pages
"""

# IMPORTANT: This requires Google Search Console API setup
# 1. Go to Google Cloud Console
# 2. Enable Indexing API
# 3. Create service account
# 4. Add service account email to Search Console as owner
# 5. Download credentials JSON

import json
import requests
from oauth2client.service_account import ServiceAccountCredentials
import httplib2

SCOPES = ["https://www.googleapis.com/auth/indexing"]

# Key pages to submit for indexing
URLS = [
    "https://manage369.com/",
    "https://manage369.com/contact.html",
    "https://manage369.com/services.html",
    "https://manage369.com/property-management/glenview/",
    "https://manage369.com/property-management/wilmette/",
    "https://manage369.com/property-management/winnetka/",
    "https://manage369.com/property-management/highland-park/",
    "https://manage369.com/property-management/northbrook/",
    "https://manage369.com/property-management/evanston/",
    "https://manage369.com/property-management/skokie/"
]

def index_url(url, credentials_file="credentials.json"):
    """Submit URL to Google for indexing"""
    
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        credentials_file, scopes=SCOPES
    )
    http = credentials.authorize(httplib2.Http())
    
    content = {
        "url": url,
        "type": "URL_UPDATED"
    }
    
    response, content = http.request(
        "https://indexing.googleapis.com/v3/urlNotifications:publish",
        method="POST",
        body=json.dumps(content),
        headers={"Content-Type": "application/json"}
    )
    
    return response, content

if __name__ == "__main__":
    print("Submitting URLs to Google Indexing API...")
    for url in URLS:
        try:
            response, content = index_url(url)
            print(f"✓ Submitted: {url}")
        except Exception as e:
            print(f"✗ Failed: {url} - {str(e)}")
'''
    
    with open('submit_to_google.py', 'w', encoding='utf-8') as f:
        f.write(script)
    
    print("[SUCCESS] Created Google Indexing API script")

def create_manual_submission_urls():
    """Create list of URLs for manual submission to Search Console"""
    
    urls_content = """URGENT: Submit these URLs manually to Google Search Console

1. Go to: https://search.google.com/search-console
2. Select your property (manage369.com)
3. Go to "URL Inspection" tool
4. Paste each URL and click "Request Indexing"

PRIORITY 1 - Submit immediately:
https://manage369.com/
https://manage369.com/contact.html
https://manage369.com/services.html
https://manage369.com/property-management/glenview/
https://manage369.com/property-management/wilmette/
https://manage369.com/property-management/winnetka/
https://manage369.com/property-management/highland-park/
https://manage369.com/property-management/northbrook/

PRIORITY 2 - Submit after Priority 1:
https://manage369.com/property-management/evanston/
https://manage369.com/property-management/skokie/
https://manage369.com/property-management/glencoe/
https://manage369.com/property-management/deerfield/
https://manage369.com/property-management/morton-grove/
https://manage369.com/property-management/lincolnwood/
https://manage369.com/property-management/golf/
https://manage369.com/property-management/des-plaines/

PRIORITY 3 - Chicago neighborhoods:
https://manage369.com/property-management/lincoln-park/
https://manage369.com/property-management/lakeview/
https://manage369.com/property-management/gold-coast/
https://manage369.com/property-management/river-north/
https://manage369.com/property-management/loop/

Also submit the sitemap:
https://manage369.com/sitemap.xml
"""
    
    with open('GOOGLE_SUBMISSION_URLS.txt', 'w', encoding='utf-8') as f:
        f.write(urls_content)
    
    print("[SUCCESS] Created manual submission URLs list")

def verify_robots_txt():
    """Ensure robots.txt is properly configured"""
    
    robots_content = """User-agent: *
Allow: /
Sitemap: https://manage369.com/sitemap.xml

# Specifically allow Googlebot
User-agent: Googlebot
Allow: /
Crawl-delay: 0

User-agent: Googlebot-Image
Allow: /

User-agent: Googlebot-Mobile
Allow: /

# Allow all assets
Allow: /images/
Allow: /css/
Allow: /js/
Allow: /*.css$
Allow: /*.js$
Allow: /*.jpg$
Allow: /*.jpeg$
Allow: /*.png$
Allow: /*.gif$
Allow: /*.svg$
Allow: /*.webp$

# No restrictions on crawling
"""
    
    with open('robots.txt', 'w', encoding='utf-8') as f:
        f.write(robots_content)
    
    print("[SUCCESS] Updated robots.txt for maximum crawlability")

# Run all fixes
print("EMERGENCY GOOGLE INDEXING FIX")
print("=" * 40)

total_pages = update_sitemap()
pages_fixed = fix_meta_tags()
verify_robots_txt()
create_indexing_api_script()
create_manual_submission_urls()

print("\n" + "=" * 40)
print("INDEXING FIX COMPLETE!")
print(f"- Sitemap: {total_pages} pages")
print(f"- Meta tags fixed: {pages_fixed} pages")
print("- robots.txt: Optimized for Google")
print("- Created submission scripts")
print("\nNEXT STEPS:")
print("1. Deploy these changes immediately")
print("2. Submit URLs using GOOGLE_SUBMISSION_URLS.txt")
print("3. Submit sitemap in Search Console")
print("4. Use Fetch as Google to test pages")
print("5. Monitor Search Console for indexing status")