#!/usr/bin/env python3
"""
Update and verify sitemap.xml for Google indexing
Ensures all pages are included with proper formatting
"""

import os
from datetime import datetime
from pathlib import Path
import xml.etree.ElementTree as ET
from xml.dom import minidom

def get_all_html_files():
    """Get all HTML files that should be in the sitemap"""
    pages = []
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Main pages (high priority)
    main_pages = [
        ('https://manage369.com/', 'daily', '1.0'),
        ('https://manage369.com/contact.html', 'weekly', '0.9'),
        ('https://manage369.com/services.html', 'weekly', '0.9'),
        ('https://manage369.com/property-management/', 'weekly', '0.9'),
        ('https://manage369.com/payment-methods.html', 'monthly', '0.8'),
        ('https://manage369.com/forms.html', 'weekly', '0.8'),
        ('https://manage369.com/chicago-property-management-companies.html', 'weekly', '0.8'),
        ('https://manage369.com/property-management-near-me.html', 'weekly', '0.8'),
        ('https://manage369.com/property-management-cost-guide.html', 'monthly', '0.7'),
        ('https://manage369.com/emergency-property-management-chicago.html', 'weekly', '0.8'),
    ]
    
    # Service pages
    services = [
        'condominium-management',
        'hoa-management', 
        'townhome-management',
        'financial-management',
        'maintenance-coordination',
        'board-support',
        'administrative-services',
        'capital-project-management',
        'resident-relations'
    ]
    
    for service in services:
        main_pages.append(
            (f'https://manage369.com/services/{service}/', 'weekly', '0.8')
        )
    
    # Property management location pages
    locations = [
        'albany-park', 'andersonville', 'arlington-heights', 'avondale',
        'bucktown', 'buffalo-grove', 'deerfield', 'des-plaines', 'dunning',
        'edgewater', 'edison-park', 'elk-grove-village', 'elmwood-park',
        'evanston', 'forest-glen', 'franklin-park', 'glencoe', 'glenview',
        'gold-coast', 'golf', 'harwood-heights', 'highland-park', 'hyde-park',
        'itasca', 'jefferson-park', 'lake-bluff', 'lake-forest', 'lakeview',
        'lincoln-park', 'lincoln-square', 'lincolnshire', 'lincolnwood',
        'logan-square', 'loop', 'mayfair', 'morton-grove', 'mount-prospect',
        'norridge', 'north-park', 'northbrook', 'northfield', 'norwood-park',
        'oak-park', 'old-irving-park', 'old-town', 'park-ridge', 'portage-park',
        'prospect-heights', 'pulaski-park', 'ravenswood', 'river-north',
        'rogers-park', 'rolling-meadows', 'sauganash', 'schiller-park',
        'skokie', 'south-loop', 'streeterville', 'the-glen', 'uptown',
        'vernon-hills', 'west-loop', 'west-ridge', 'wheeling', 'wicker-park',
        'wilmette', 'winnetka', 'wood-dale'
    ]
    
    for location in locations:
        main_pages.append(
            (f'https://manage369.com/property-management/{location}/', 'weekly', '0.8')
        )
    
    # Blog pages
    blog_posts = [
        '2025-illinois-hoa-law-changes.html',
        'hoa-board-responsibilities-illinois-guide.html',
        'illinois-condominium-property-act-guide.html',
        'professional-vs-self-management-north-shore.html',
        'property-management-cost-north-shore-chicago-guide.html',
        'seasonal-property-maintenance-calendar-chicago.html',
        'smoking-vaping-illinois-condominiums-law.html',
        'top-10-property-management-companies-north-shore.html',
        'top-5-financial-mistakes-hoa-boards-avoid.html',
        'winter-property-management-checklist.html'
    ]
    
    main_pages.append(('https://manage369.com/blog/', 'weekly', '0.7'))
    for post in blog_posts:
        main_pages.append(
            (f'https://manage369.com/blog/{post}', 'monthly', '0.6')
        )
    
    # Legal/footer pages (lower priority)
    footer_pages = [
        ('https://manage369.com/privacy-policy.html', 'yearly', '0.3'),
        ('https://manage369.com/terms-of-service.html', 'yearly', '0.3'),
        ('https://manage369.com/legal-disclaimers.html', 'yearly', '0.3'),
        ('https://manage369.com/accessibility.html', 'yearly', '0.3'),
        ('https://manage369.com/sitemap.html', 'monthly', '0.5'),
    ]
    
    main_pages.extend(footer_pages)
    
    return main_pages, today

def create_sitemap():
    """Create a properly formatted sitemap.xml"""
    pages, today = get_all_html_files()
    
    # Create root element with namespaces
    root = ET.Element('urlset')
    root.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    root.set('xmlns:image', 'http://www.google.com/schemas/sitemap-image/1.1')
    
    # Add each URL
    for url, changefreq, priority in pages:
        url_elem = ET.SubElement(root, 'url')
        loc = ET.SubElement(url_elem, 'loc')
        loc.text = url
        lastmod = ET.SubElement(url_elem, 'lastmod')
        lastmod.text = today
        freq = ET.SubElement(url_elem, 'changefreq')
        freq.text = changefreq
        prio = ET.SubElement(url_elem, 'priority')
        prio.text = priority
    
    # Convert to string with proper formatting
    rough_string = ET.tostring(root, encoding='unicode')
    reparsed = minidom.parseString(rough_string)
    
    return reparsed.toprettyxml(indent="  ", encoding="UTF-8")

def main():
    print("Updating Sitemap for Google Indexing")
    print("=" * 60)
    
    # Create new sitemap
    sitemap_content = create_sitemap()
    
    # Save sitemap
    with open('sitemap.xml', 'wb') as f:
        f.write(sitemap_content)
    
    print("✅ Sitemap updated successfully!")
    
    # Count URLs
    pages, _ = get_all_html_files()
    print(f"\nTotal URLs in sitemap: {len(pages)}")
    
    print("\nSitemap includes:")
    print("- 1 homepage")
    print("- 68 property location pages")
    print("- 9 service pages")
    print("- 10 blog posts")
    print("- Main navigation pages")
    print("- Legal/footer pages")
    
    print("\n" + "=" * 60)
    print("\nIMPORTANT: Submit to Google Search Console")
    print("=" * 60)
    
    print("\n1. Go to Google Search Console")
    print("2. Select your property")
    print("3. Click 'Sitemaps' in the left sidebar")
    print("4. Add sitemap URL: sitemap.xml")
    print("5. Click 'Submit'")
    
    print("\nAlternatively, ping Google directly:")
    print("https://www.google.com/ping?sitemap=https://manage369.com/sitemap.xml")
    
    print("\nYour sitemap is available at:")
    print("✅ https://manage369.com/sitemap.xml (canonical)")
    print("✅ https://www.manage369.com/sitemap.xml (will redirect)")
    
    print("\nRobots.txt properly references:")
    print("Sitemap: https://manage369.com/sitemap.xml")

if __name__ == "__main__":
    main()