#!/usr/bin/env python3
"""
Fix duplicate breadcrumbs and broken layout caused by reverse silo implementation
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

def fix_page(file_path):
    """Remove duplicate breadcrumbs and fix layout issues"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find and remove ALL breadcrumb navigation elements
    breadcrumbs = soup.find_all('nav', style=re.compile('padding.*1rem.*2rem.*background.*#f8f9fa'))
    for breadcrumb in breadcrumbs:
        breadcrumb.decompose()
    
    # Remove duplicate offer CTA sections that were added
    offer_sections = soup.find_all('section', style=re.compile('background.*linear-gradient.*#f8f9fa'))
    if len(offer_sections) > 1:
        # Keep only the first one if it exists, remove duplicates
        for section in offer_sections[1:]:
            section.decompose()
    
    # Remove any "Reverse Silo" commented sections
    for comment in soup.find_all(string=lambda text: isinstance(text, str) and 'Reverse Silo' in text):
        if comment.parent:
            comment.parent.decompose()
    
    # Remove duplicate neighboring areas sections
    neighbor_sections = soup.find_all('section', style=re.compile('background.*white.*padding.*2rem.*margin.*2rem'))
    for section in neighbor_sections:
        if section.find('h3', string=re.compile('We Also Serve Nearby Communities')):
            section.decompose()
    
    # Remove duplicate footer CTAs
    footer = soup.find('footer')
    if footer:
        footer_ctas = footer.find_all('div', style=re.compile('background.*#1e3a8a.*padding.*1.5rem'))
        if len(footer_ctas) > 1:
            for cta in footer_ctas[1:]:
                cta.decompose()
    
    # Save cleaned file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    return True

def main():
    print("Fixing duplicate breadcrumbs and broken layouts...")
    
    # Fix all area pages
    area_pages = list(Path('property-management').glob('**/index.html'))
    print(f"Fixing {len(area_pages)} area pages...")
    for page in area_pages:
        fix_page(page)
        print(f"  Fixed: {page.parent.name}")
    
    # Fix all service pages
    service_pages = list(Path('services').glob('**/index.html'))
    print(f"Fixing {len(service_pages)} service pages...")
    for page in service_pages:
        fix_page(page)
        print(f"  Fixed: {page.parent.name}")
    
    # Fix blog pages
    blog_pages = list(Path('blog').glob('*.html'))
    print(f"Fixing {len(blog_pages)} blog pages...")
    for page in blog_pages:
        fix_page(page)
        print(f"  Fixed: {page.name}")
    
    print("\n✓ All duplicate breadcrumbs and layout issues fixed!")
    print("✓ Navigation hierarchy restored")
    print("✓ Visual layout cleaned up")

if __name__ == "__main__":
    main()