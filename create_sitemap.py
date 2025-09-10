#!/usr/bin/env python3

import os
from datetime import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom

def create_sitemap():
    """Create a comprehensive XML sitemap for all pages"""
    
    # Create root element
    urlset = ET.Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    urlset.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    urlset.set('xsi:schemaLocation', 'http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd')
    
    base_url = 'https://www.manage369.com'
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Priority pages (homepage and main sections)
    priority_pages = [
        ('/', '1.0', 'daily'),
        ('/contact.html', '0.9', 'weekly'),
        ('/services.html', '0.9', 'weekly'),
        ('/property-management/', '0.9', 'weekly'),
        ('/pay-dues.html', '0.8', 'monthly'),
        ('/forms.html', '0.8', 'monthly'),
    ]
    
    # Add priority pages
    for path, priority, changefreq in priority_pages:
        url = ET.SubElement(urlset, 'url')
        ET.SubElement(url, 'loc').text = base_url + path
        ET.SubElement(url, 'lastmod').text = today
        ET.SubElement(url, 'changefreq').text = changefreq
        ET.SubElement(url, 'priority').text = priority
    
    # Service pages
    service_pages = [
        '/services/condominium-management/',
        '/services/hoa-management/',
        '/services/townhome-management/',
        '/services/financial-management/',
        '/services/maintenance-coordination/',
        '/services/board-support/',
        '/services/administrative-services/',
        '/services/capital-project-management/',
        '/services/resident-relations/',
    ]
    
    for path in service_pages:
        url = ET.SubElement(urlset, 'url')
        ET.SubElement(url, 'loc').text = base_url + path
        ET.SubElement(url, 'lastmod').text = today
        ET.SubElement(url, 'changefreq').text = 'weekly'
        ET.SubElement(url, 'priority').text = '0.8'
    
    # All 68 area pages (high priority for local SEO)
    area_pages = [
        'albany-park', 'andersonville', 'arlington-heights', 'avondale',
        'bucktown', 'buffalo-grove', 'deerfield', 'des-plaines', 'dunning',
        'edgewater', 'edison-park', 'elk-grove-village', 'elmwood-park',
        'evanston', 'forest-glen', 'franklin-park', 'glencoe', 'glenview',
        'gold-coast', 'golf', 'harwood-heights', 'highland-park', 'hyde-park',
        'itasca', 'jefferson-park', 'lake-bluff', 'lake-forest', 'lakeview',
        'lincoln-park', 'lincolnshire', 'lincoln-square', 'lincolnwood',
        'logan-square', 'loop', 'mayfair', 'morton-grove', 'mount-prospect',
        'norridge', 'northbrook', 'northfield', 'north-park', 'norwood-park',
        'oak-park', 'old-irving-park', 'old-town', 'park-ridge', 'portage-park',
        'prospect-heights', 'pulaski-park', 'ravenswood', 'river-north',
        'rogers-park', 'rolling-meadows', 'sauganash', 'schiller-park',
        'skokie', 'south-loop', 'streeterville', 'the-glen', 'uptown',
        'vernon-hills', 'west-loop', 'west-ridge', 'wheeling', 'wicker-park',
        'wilmette', 'winnetka', 'wood-dale'
    ]
    
    for area in area_pages:
        url = ET.SubElement(urlset, 'url')
        ET.SubElement(url, 'loc').text = f'{base_url}/property-management/{area}/'
        ET.SubElement(url, 'lastmod').text = today
        ET.SubElement(url, 'changefreq').text = 'weekly'
        ET.SubElement(url, 'priority').text = '0.85'  # High priority for local SEO
    
    # Blog posts (if they exist)
    blog_dir = 'blog'
    if os.path.exists(blog_dir):
        for item in os.listdir(blog_dir):
            if item.endswith('.html') and item != 'index.html':
                url = ET.SubElement(urlset, 'url')
                ET.SubElement(url, 'loc').text = f'{base_url}/blog/{item}'
                ET.SubElement(url, 'lastmod').text = today
                ET.SubElement(url, 'changefreq').text = 'monthly'
                ET.SubElement(url, 'priority').text = '0.6'
        
        # Blog index
        if os.path.exists(os.path.join(blog_dir, 'index.html')):
            url = ET.SubElement(urlset, 'url')
            ET.SubElement(url, 'loc').text = f'{base_url}/blog/'
            ET.SubElement(url, 'lastmod').text = today
            ET.SubElement(url, 'changefreq').text = 'weekly'
            ET.SubElement(url, 'priority').text = '0.7'
    
    # Other important pages
    other_pages = [
        ('/sitemap.html', '0.5', 'monthly'),
        ('/property-management-near-me.html', '0.7', 'weekly'),
        ('/property-management-cost-guide.html', '0.7', 'weekly'),
        ('/emergency-property-management-chicago.html', '0.7', 'weekly'),
        ('/chicago-property-management-companies.html', '0.7', 'weekly'),
        ('/repair-request.html', '0.6', 'monthly'),
        ('/move-permit.html', '0.6', 'monthly'),
        ('/construction-request.html', '0.6', 'monthly'),
        ('/violation-report.html', '0.6', 'monthly'),
        ('/refund-request.html', '0.6', 'monthly'),
        ('/resident-info.html', '0.6', 'monthly'),
        ('/payment-methods.html', '0.6', 'monthly'),
        ('/leave-review.html', '0.6', 'monthly'),
        ('/ho6-insurance.html', '0.6', 'monthly'),
        ('/privacy-policy.html', '0.4', 'yearly'),
        ('/terms-of-service.html', '0.4', 'yearly'),
        ('/legal-disclaimers.html', '0.4', 'yearly'),
        ('/accessibility.html', '0.4', 'yearly'),
    ]
    
    for path, priority, changefreq in other_pages:
        # Check if file exists before adding
        file_path = path.replace('/', '').replace('.html', '') + '.html' if path != '/' else 'index.html'
        if os.path.exists(file_path):
            url = ET.SubElement(urlset, 'url')
            ET.SubElement(url, 'loc').text = base_url + path
            ET.SubElement(url, 'lastmod').text = today
            ET.SubElement(url, 'changefreq').text = changefreq
            ET.SubElement(url, 'priority').text = priority
    
    # Convert to pretty XML
    xml_str = ET.tostring(urlset, encoding='unicode')
    dom = minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent='  ', encoding='UTF-8')
    
    # Write sitemap
    with open('sitemap.xml', 'wb') as f:
        f.write(pretty_xml)
    
    # Count URLs
    url_count = len(urlset.findall('url'))
    
    print(f"[OK] Created sitemap.xml with {url_count} URLs")
    print(f"[OK] Included all 68 area pages with high priority (0.85)")
    print(f"[OK] Set homepage as highest priority (1.0)")
    print(f"[OK] Ready for Google Search Console submission")
    
    return url_count

if __name__ == "__main__":
    create_sitemap()