import os
from datetime import datetime
from pathlib import Path

def generate_sitemap():
    """Generate a properly formatted sitemap.xml"""
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Start sitemap
    sitemap = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">'''
    
    # Main pages with priority
    main_pages = [
        ('/', 1.0, 'daily'),
        ('/contact.html', 0.9, 'weekly'),
        ('/services.html', 0.9, 'weekly'),
        ('/payment-methods.html', 0.8, 'monthly'),
        ('/forms.html', 0.8, 'weekly'),
        ('/property-management/', 0.9, 'weekly'),
    ]
    
    for url, priority, freq in main_pages:
        sitemap += f'''
  <url>
    <loc>https://manage369.com{url}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{priority}</priority>
  </url>'''
    
    # Property management pages
    property_dirs = []
    property_path = Path('property-management')
    if property_path.exists():
        for dir_path in property_path.iterdir():
            if dir_path.is_dir() and (dir_path / 'index.html').exists():
                property_dirs.append(dir_path.name)
    
    property_dirs.sort()
    
    for dir_name in property_dirs:
        sitemap += f'''
  <url>
    <loc>https://manage369.com/property-management/{dir_name}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>'''
    
    # Service pages
    service_pages = [
        'administrative-services',
        'board-support',
        'capital-project-management',
        'condominium-management',
        'financial-management',
        'hoa-management',
        'maintenance-coordination',
        'resident-relations',
        'townhome-management'
    ]
    
    for service in service_pages:
        sitemap += f'''
  <url>
    <loc>https://manage369.com/services/{service}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>'''
    
    # Other important pages
    other_pages = [
        ('/sitemap.html', 0.3, 'monthly'),
        ('/construction-request.html', 0.6, 'monthly'),
        ('/ho6-insurance.html', 0.6, 'monthly'),
        ('/move-permit.html', 0.6, 'monthly'),
        ('/repair-request.html', 0.6, 'monthly'),
        ('/violation-report.html', 0.6, 'monthly'),
    ]
    
    for url, priority, freq in other_pages:
        if os.path.exists(url.lstrip('/')):
            sitemap += f'''
  <url>
    <loc>https://manage369.com{url}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{priority}</priority>
  </url>'''
    
    # Close sitemap
    sitemap += '''
</urlset>'''
    
    return sitemap

# Generate and save sitemap
sitemap_content = generate_sitemap()
with open('sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(sitemap_content)

print("Generated updated sitemap.xml")
print(f"Total URLs in sitemap: {sitemap_content.count('<url>')}")