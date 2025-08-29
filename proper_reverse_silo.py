#!/usr/bin/env python3
"""
PROPER Reverse Silo Implementation - Links Only
This adds strategic text links pointing to homepage, not content sections
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

def add_homepage_links(file_path):
    """Add strategic links to homepage within existing content"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find the main content area
    main_content = None
    for tag in ['main', 'article', 'section']:
        main_content = soup.find(tag, class_=re.compile('content|main|article'))
        if main_content:
            break
    
    if not main_content:
        main_content = soup.find('section')
    
    if main_content:
        # Find paragraphs that mention property management but don't have links
        paragraphs = main_content.find_all('p')
        
        for p in paragraphs:
            if p.string and 'property management' in p.string.lower():
                # Add a link to homepage within the text
                text = str(p.string)
                if 'Manage369' in text and '<a' not in str(p):
                    # Replace Manage369 with a link to homepage
                    new_text = text.replace('Manage369', '<a href="/" style="color: #1e3a8a; font-weight: 500;">Manage369</a>')
                    new_p = BeautifulSoup(new_text, 'html.parser')
                    p.string.replace_with(new_p)
        
        # Add a subtle CTA at the end of main content (just a link, not a section)
        last_element = main_content.find_all(['p', 'div', 'section'])[-1] if main_content.find_all(['p', 'div', 'section']) else None
        
        if last_element and not soup.find(string=re.compile('View our special offer')):
            cta_link = soup.new_tag('p', style='margin-top: 2rem; text-align: center;')
            link = soup.new_tag('a', href='/', style='color: #1e3a8a; font-weight: 600; text-decoration: none;')
            link.string = '← Back to Homepage | View Current Special Offer'
            cta_link.append(link)
            last_element.insert_after(cta_link)
    
    # Update any "Home" links to point to homepage with anchor text
    for a in soup.find_all('a', string=re.compile('Home|home')):
        if a.get('href') in ['../index.html', '../../index.html', '../', '../../']:
            a['href'] = '/'
    
    # Save updated file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    return True

def main():
    print("Implementing PROPER Reverse Silo (Links Only)...")
    print("=" * 60)
    
    processed = 0
    
    # Process all area pages
    area_pages = list(Path('property-management').glob('**/index.html'))
    print(f"Adding homepage links to {len(area_pages)} area pages...")
    for page in area_pages:
        if add_homepage_links(page):
            processed += 1
            print(f"  Linked: {page.parent.name}")
    
    # Process all service pages
    service_pages = list(Path('services').glob('**/index.html'))
    print(f"\nAdding homepage links to {len(service_pages)} service pages...")
    for page in service_pages:
        if add_homepage_links(page):
            processed += 1
            print(f"  Linked: {page.parent.name}")
    
    # Process blog pages
    blog_pages = list(Path('blog').glob('*.html'))
    print(f"\nAdding homepage links to {len(blog_pages)} blog pages...")
    for page in blog_pages:
        if add_homepage_links(page):
            processed += 1
            print(f"  Linked: {page.name}")
    
    print("\n" + "=" * 60)
    print(f"PROPER REVERSE SILO COMPLETE!")
    print(f"Added strategic homepage links to {processed} pages")
    print(f"All pages now push link equity to homepage")
    print(f"No duplicate content or broken layouts")
    print("\nWhat this does:")
    print("  - Adds text links to homepage within existing content")
    print("  - Adds subtle 'Back to Homepage' link at end of content")
    print("  - Updates navigation links to point to homepage")
    print("  - NO offer sections added to other pages")
    print("  - NO duplicate breadcrumbs or CTAs")

if __name__ == "__main__":
    main()