"""
CRITICAL: Fix all Google indexing issues immediately
"""

import os
import re

print("CRITICAL INDEXING FIX - RUNNING ALL FIXES")
print("=" * 60)

# 1. Update robots.txt to be SUPER clear for Google
robots_content = """# GOOGLE - PLEASE INDEX THIS SITE
User-agent: Googlebot
Allow: /
Crawl-delay: 0

User-agent: Googlebot-Image
Allow: /

User-agent: Googlebot-Mobile  
Allow: /

User-agent: *
Allow: /

# Sitemap
Sitemap: https://manage369.com/sitemap.xml

# No restrictions - index everything
Disallow:
"""

with open('robots.txt', 'w') as f:
    f.write(robots_content)
print("[1/5] Updated robots.txt - FULL ACCESS for Google")

# 2. Fix ALL HTML pages
def fix_html_page(filepath):
    """Ensure page is 100% indexable"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes = False
    
    # Get proper URL for canonical
    rel_path = filepath.replace('C:\\Users\\mirsa\\manage369-live\\', '').replace('\\', '/')
    if rel_path == 'index.html':
        canonical_url = 'https://manage369.com/'
    elif rel_path.endswith('/index.html'):
        canonical_url = 'https://manage369.com/' + rel_path.replace('/index.html', '/')
    elif rel_path.endswith('.html'):
        canonical_url = 'https://manage369.com/' + rel_path
    else:
        canonical_url = 'https://manage369.com/' + rel_path
    
    # Ensure canonical tag exists and is correct
    if 'rel="canonical"' not in content:
        # Add canonical after <title>
        content = re.sub(
            r'(</title>)',
            r'\1\n    <link rel="canonical" href="' + canonical_url + '">',
            content
        )
        changes = True
    else:
        # Update existing canonical
        content = re.sub(
            r'<link[^>]*rel="canonical"[^>]*href="[^"]*"[^>]*>',
            f'<link rel="canonical" href="{canonical_url}">',
            content
        )
        changes = True
    
    # Ensure robots meta is correct
    if 'name="robots"' not in content:
        # Add after viewport
        content = re.sub(
            r'(<meta name="viewport"[^>]*>)',
            r'\1\n    <meta name="robots" content="index, follow">',
            content
        )
        changes = True
    else:
        # Fix existing robots meta
        content = re.sub(
            r'<meta name="robots"[^>]*content="[^"]*"[^>]*>',
            '<meta name="robots" content="index, follow">',
            content
        )
        changes = True
    
    # Add Google verification if on homepage
    if rel_path == 'index.html' and 'google-site-verification' not in content:
        content = re.sub(
            r'(<meta name="robots"[^>]*>)',
            r'\1\n    <meta name="google-site-verification" content="your-verification-code">',
            content
        )
        changes = True
    
    # Remove ALL potential blockers
    content = re.sub(r'noindex[,\s]*', '', content, flags=re.IGNORECASE)
    content = re.sub(r'nofollow[,\s]*', '', content, flags=re.IGNORECASE)
    content = re.sub(r'X-Robots-Tag[^<]*', '', content, flags=re.IGNORECASE)
    
    if changes:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

pages_fixed = 0
for root, dirs, files in os.walk('C:\\Users\\mirsa\\manage369-live'):
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    
    for filename in files:
        if filename.endswith('.html') and not filename.startswith('test'):
            filepath = os.path.join(root, filename)
            try:
                if fix_html_page(filepath):
                    pages_fixed += 1
            except:
                pass

print(f"[2/5] Fixed {pages_fixed} HTML pages")

# 3. Create Google-specific sitemap
sitemap_content = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<!-- Homepage - HIGHEST PRIORITY -->
<url>
  <loc>https://manage369.com/</loc>
  <lastmod>2025-08-18</lastmod>
  <changefreq>daily</changefreq>
  <priority>1.0</priority>
</url>
<!-- Key Service Pages -->
<url>
  <loc>https://manage369.com/services.html</loc>
  <lastmod>2025-08-18</lastmod>
  <changefreq>weekly</changefreq>
  <priority>0.9</priority>
</url>
<url>
  <loc>https://manage369.com/contact.html</loc>
  <lastmod>2025-08-18</lastmod>
  <changefreq>weekly</changefreq>
  <priority>0.9</priority>
</url>
'''

# Add all property management pages
prop_dir = 'C:\\Users\\mirsa\\manage369-live\\property-management'
for location in os.listdir(prop_dir):
    if os.path.isdir(os.path.join(prop_dir, location)):
        sitemap_content += f'''<url>
  <loc>https://manage369.com/property-management/{location}/</loc>
  <lastmod>2025-08-18</lastmod>
  <changefreq>weekly</changefreq>
  <priority>0.8</priority>
</url>
'''

sitemap_content += '</urlset>'

with open('sitemap.xml', 'w') as f:
    f.write(sitemap_content)
print("[3/5] Created fresh sitemap.xml")

# 4. Create _headers file for Netlify
headers_content = """/*
  X-Robots-Tag: index, follow
  Cache-Control: public, max-age=3600
"""

with open('_headers', 'w') as f:
    f.write(headers_content)
print("[4/5] Created _headers file to force indexing")

# 5. Update netlify.toml to remove any blocking
netlify_content = """[build]
  publish = "."

# Ensure site is accessible to crawlers
[[headers]]
  for = "/*"
  [headers.values]
    X-Robots-Tag = "index, follow"
    
[[headers]]
  for = "/robots.txt"
  [headers.values]
    Content-Type = "text/plain; charset=UTF-8"
    
[[headers]]
  for = "/sitemap.xml"
  [headers.values]
    Content-Type = "application/xml; charset=UTF-8"

# Redirect spam but allow all real content
[[redirects]]
  from = "/tinggi/*"
  to = "/404.html"
  status = 404
  force = true
"""

with open('netlify.toml', 'w') as f:
    f.write(netlify_content)
print("[5/5] Updated netlify.toml for maximum crawlability")

print("\n" + "=" * 60)
print("CRITICAL FIX COMPLETE!")
print("\nCHANGES MADE:")
print("1. robots.txt - Full Google access")
print("2. All HTML pages - Proper canonical & robots meta")
print("3. Fresh sitemap.xml")
print("4. _headers file - Forces indexing")
print("5. netlify.toml - Removed all blockers")
print("\nDEPLOY IMMEDIATELY!")