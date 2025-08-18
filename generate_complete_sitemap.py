"""
Generate comprehensive sitemap with all pages and proper priorities
"""

import os
from datetime import datetime
import re

print("GENERATING COMPREHENSIVE SITEMAP")
print("=" * 60)

# Today's date
today = datetime.now().strftime('%Y-%m-%d')

# Start sitemap
sitemap = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
'''

# Page priorities and frequencies
page_configs = {
    'index.html': (1.0, 'daily'),
    'contact.html': (0.95, 'weekly'),
    'services.html': (0.9, 'weekly'),
    'forms.html': (0.85, 'weekly'),
    'payment-methods.html': (0.8, 'monthly'),
    'property-management/': (0.9, 'weekly'),
    # North Shore Premium Areas - Higher priority
    'property-management/wilmette/': (0.85, 'weekly'),
    'property-management/winnetka/': (0.85, 'weekly'),
    'property-management/glencoe/': (0.85, 'weekly'),
    'property-management/highland-park/': (0.85, 'weekly'),
    'property-management/glenview/': (0.85, 'weekly'),
    'property-management/northbrook/': (0.85, 'weekly'),
    'property-management/lake-forest/': (0.85, 'weekly'),
    'property-management/lake-bluff/': (0.85, 'weekly'),
    'property-management/deerfield/': (0.85, 'weekly'),
    'property-management/evanston/': (0.85, 'weekly'),
    # Chicago Premium Areas - Higher priority
    'property-management/gold-coast/': (0.85, 'weekly'),
    'property-management/lincoln-park/': (0.85, 'weekly'),
    'property-management/river-north/': (0.85, 'weekly'),
    'property-management/loop/': (0.85, 'weekly'),
    'property-management/streeterville/': (0.85, 'weekly'),
    'property-management/lakeview/': (0.85, 'weekly'),
    'property-management/old-town/': (0.85, 'weekly'),
    'property-management/west-loop/': (0.85, 'weekly'),
    # Service pages
    'services/hoa-management/': (0.85, 'weekly'),
    'services/condominium-management/': (0.85, 'weekly'),
    'services/townhome-management/': (0.85, 'weekly'),
    'services/financial-management/': (0.8, 'monthly'),
    'services/maintenance-coordination/': (0.8, 'monthly'),
    'services/board-support/': (0.8, 'monthly'),
    # Blog
    'blog/': (0.7, 'weekly'),
    # Legal/Info pages
    'privacy-policy.html': (0.5, 'yearly'),
    'terms-of-service.html': (0.5, 'yearly'),
    'legal-disclaimers.html': (0.5, 'yearly'),
    'accessibility.html': (0.5, 'yearly'),
    'sitemap.html': (0.4, 'monthly')
}

# Function to add URL to sitemap
def add_url(path, priority=0.7, changefreq='monthly', check_images=False):
    """Add URL with optional image detection"""
    
    url = f"https://manage369.com/{path}"
    if path == 'index.html':
        url = "https://manage369.com/"
    elif path.endswith('/index.html'):
        url = f"https://manage369.com/{path.replace('/index.html', '/')}".replace('//', '/')
    elif path.endswith('.html'):
        url = f"https://manage369.com/{path}"
    else:
        url = f"https://manage369.com/{path}".replace('//', '/')
    
    entry = f'''  <url>
    <loc>{url}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority:.1f}</priority>'''
    
    # Check for images if requested
    if check_images and os.path.exists(f'C:\\Users\\mirsa\\manage369-live\\{path.replace("/", "\\")}'):
        filepath = f'C:\\Users\\mirsa\\manage369-live\\{path.replace("/", "\\")}'
        if os.path.isdir(filepath):
            filepath = os.path.join(filepath, 'index.html')
        
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find hero/main images
                images = re.findall(r'url\([\'"]?(?:\.\.\/)*images/([^\'")]+)', content)
                for img in images[:1]:  # Add first image only
                    img_url = f"https://manage369.com/images/{img}"
                    entry += f'''
    <image:image>
      <image:loc>{img_url}</image:loc>
      <image:title>Property Management {path.replace('property-management/', '').replace('/', ' ').title()}</image:title>
    </image:image>'''
            except:
                pass
    
    entry += '\n  </url>\n'
    return entry

# Add homepage
sitemap += add_url('index.html', 1.0, 'daily', True)

# Add main pages
main_pages = ['contact.html', 'services.html', 'forms.html', 'payment-methods.html']
for page in main_pages:
    priority, freq = page_configs.get(page, (0.8, 'weekly'))
    sitemap += add_url(page, priority, freq)

# Add property management main page
sitemap += add_url('property-management/', 0.9, 'weekly')

# Add all property management area pages
prop_dir = 'C:\\Users\\mirsa\\manage369-live\\property-management'
locations = []
for location in os.listdir(prop_dir):
    if os.path.isdir(os.path.join(prop_dir, location)):
        locations.append(location)

# Sort locations with premium areas first
premium_north = ['wilmette', 'winnetka', 'glencoe', 'highland-park', 'glenview', 
                 'northbrook', 'lake-forest', 'lake-bluff', 'deerfield', 'evanston']
premium_chicago = ['gold-coast', 'lincoln-park', 'river-north', 'loop', 'streeterville',
                   'lakeview', 'old-town', 'west-loop', 'bucktown', 'wicker-park']

# Add premium areas first
for location in premium_north + premium_chicago:
    if location in locations:
        path = f'property-management/{location}/'
        priority, freq = page_configs.get(path, (0.85, 'weekly'))
        sitemap += add_url(path, priority, freq, True)
        locations.remove(location)

# Add remaining areas
for location in sorted(locations):
    path = f'property-management/{location}/'
    sitemap += add_url(path, 0.75, 'monthly', True)

# Add service pages
service_pages = [
    'services/hoa-management/',
    'services/condominium-management/',
    'services/townhome-management/',
    'services/financial-management/',
    'services/maintenance-coordination/',
    'services/board-support/',
    'services/administrative-services/',
    'services/capital-project-management/',
    'services/resident-relations/'
]

for page in service_pages:
    priority, freq = page_configs.get(page, (0.8, 'monthly'))
    sitemap += add_url(page, priority, freq)

# Add blog pages
blog_pages = [
    'blog/',
    'blog/2025-illinois-hoa-law-changes.html',
    'blog/hoa-board-responsibilities-illinois-guide.html',
    'blog/illinois-condominium-property-act-guide.html',
    'blog/professional-vs-self-management-north-shore.html',
    'blog/property-management-cost-north-shore-chicago-guide.html',
    'blog/seasonal-property-maintenance-calendar-chicago.html',
    'blog/smoking-vaping-illinois-condominiums-law.html',
    'blog/top-10-property-management-companies-north-shore.html',
    'blog/top-5-financial-mistakes-hoa-boards-avoid.html',
    'blog/winter-property-management-checklist.html'
]

for page in blog_pages:
    priority, freq = page_configs.get(page, (0.7, 'monthly'))
    sitemap += add_url(page, priority, freq)

# Add utility pages
utility_pages = [
    'privacy-policy.html',
    'terms-of-service.html',
    'legal-disclaimers.html',
    'accessibility.html',
    'sitemap.html'
]

for page in utility_pages:
    priority, freq = page_configs.get(page, (0.5, 'yearly'))
    sitemap += add_url(page, priority, freq)

# Add specialized landing pages if they exist
landing_pages = [
    'property-management-near-me.html',
    'property-management-cost-guide.html',
    'chicago-property-management-companies.html',
    'emergency-property-management-chicago.html'
]

for page in landing_pages:
    if os.path.exists(f'C:\\Users\\mirsa\\manage369-live\\{page}'):
        sitemap += add_url(page, 0.7, 'monthly')

# Close sitemap
sitemap += '</urlset>'

# Write sitemap
with open('sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(sitemap)

# Count URLs
url_count = sitemap.count('<url>')
image_count = sitemap.count('<image:image>')

print(f"Sitemap generated successfully!")
print(f"Total URLs: {url_count}")
print(f"URLs with images: {image_count}")
print(f"\nPriority distribution:")
print("- Homepage: 1.0 (daily updates)")
print("- Contact: 0.95 (weekly)")
print("- Main services: 0.9 (weekly)")
print("- Premium areas: 0.85 (weekly)")
print("- Other areas: 0.75 (monthly)")
print("- Blog: 0.7 (monthly)")
print("- Legal pages: 0.5 (yearly)")
print(f"\nSitemap saved to: sitemap.xml")
print("\nNEXT STEPS:")
print("1. Deploy this sitemap")
print("2. Submit to Google Search Console")
print("3. Test with sitemap validator")
print("4. Monitor indexing in Search Console")