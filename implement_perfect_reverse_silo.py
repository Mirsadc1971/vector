#!/usr/bin/env python3
"""
Professional Reverse Silo Implementation for Manage369
Pushes link equity from all pages upward to homepage
Created by Claude - August 29, 2025
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
import json

class ReverseSiloImplementation:
    def __init__(self):
        self.base_dir = Path('.')
        self.homepage_url = "https://www.manage369.com/"
        self.changes_made = []
        self.pages_processed = 0
        
        # Define page categories
        self.area_pages = list(self.base_dir.glob('property-management/**/index.html'))
        self.service_pages = list(self.base_dir.glob('services/**/index.html'))
        self.blog_pages = list(self.base_dir.glob('blog/*.html'))
        self.utility_pages = [
            'contact.html', 'forms.html', 'payment-methods.html',
            'privacy-policy.html', 'terms-of-service.html', 'accessibility.html'
        ]
        
    def create_offer_cta_section(self, page_type="area"):
        """Create a professional CTA section that links to homepage offer"""
        
        if page_type == "area":
            return '''
    <!-- Reverse Silo: Special Offer CTA -->
    <section style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 3rem 1.5rem; margin: 3rem 0; border-radius: 12px;">
        <div style="max-width: 800px; margin: 0 auto; text-align: center;">
            <h2 style="color: #1e3a8a; font-size: 2rem; font-weight: 700; margin-bottom: 1rem;">
                Limited Time: Save 75% on Property Management
            </h2>
            <p style="color: #4b5563; font-size: 1.1rem; margin-bottom: 1.5rem; line-height: 1.6;">
                Your community deserves professional management at an exceptional value. 
                Switch to Manage369 before October 31, 2025 and save 75% over two years.
            </p>
            <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; margin-bottom: 1.5rem;">
                <div style="background: white; padding: 1rem 2rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <strong style="color: #1e3a8a;">Year 1:</strong> 50% Off
                </div>
                <div style="background: white; padding: 1rem 2rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <strong style="color: #1e3a8a;">Year 2:</strong> 25% Off
                </div>
                <div style="background: white; padding: 1rem 2rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <strong style="color: #1e3a8a;">$500</strong> Referral Bonus
                </div>
            </div>
            <a href="/" style="display: inline-block; background: #1e3a8a; color: white; padding: 1rem 3rem; font-size: 1.1rem; font-weight: 600; text-decoration: none; border-radius: 8px; transition: all 0.3s ease;" onmouseover="this.style.background='#2a5298'" onmouseout="this.style.background='#1e3a8a'">
                View Full Offer Details →
            </a>
            <p style="color: #6b7280; font-size: 0.9rem; margin-top: 1rem;">
                Licensed & Insured | IDFPR #291.000211 | Serving All Chicago & North Shore
            </p>
        </div>
    </section>
'''
        elif page_type == "service":
            return '''
    <!-- Reverse Silo: Service to Homepage CTA -->
    <section style="background: #f0f4f8; padding: 2.5rem 1.5rem; margin: 3rem 0; border-left: 4px solid #1e3a8a;">
        <div style="max-width: 800px; margin: 0 auto;">
            <h3 style="color: #1e3a8a; font-size: 1.6rem; font-weight: 600; margin-bottom: 1rem;">
                Start Saving on Professional Management Today
            </h3>
            <p style="color: #4b5563; font-size: 1rem; margin-bottom: 1.5rem; line-height: 1.6;">
                Join 50+ properties and 2,450+ units that trust Manage369 for professional property management. 
                Limited-time 75% savings available through October 31, 2025.
            </p>
            <a href="/" style="color: #1e3a8a; font-weight: 600; text-decoration: none; display: inline-flex; align-items: center;" onmouseover="this.style.textDecoration='underline'" onmouseout="this.style.textDecoration='none'">
                Learn About Our Limited-Time Offer <span style="margin-left: 0.5rem;">→</span>
            </a>
        </div>
    </section>
'''
        else:  # blog/utility
            return '''
    <!-- Reverse Silo: Blog/Utility to Homepage Link -->
    <div style="background: #f8f9fa; padding: 1.5rem; margin: 2rem 0; border-radius: 8px; text-align: center;">
        <p style="color: #4b5563; margin-bottom: 1rem;">
            <strong>Special Offer:</strong> Save 75% on property management services
        </p>
        <a href="/" style="color: #1e3a8a; font-weight: 500; text-decoration: none;" onmouseover="this.style.textDecoration='underline'" onmouseout="this.style.textDecoration='none'">
            View Current Promotions →
        </a>
    </div>
'''

    def create_breadcrumb_navigation(self, page_path):
        """Create breadcrumb navigation that always includes homepage"""
        page_name = page_path.stem.replace('-', ' ').title()
        parent_dir = page_path.parent.name
        
        if 'property-management' in str(page_path):
            area_name = page_path.parent.name.replace('-', ' ').title()
            return f'''
    <!-- Breadcrumb Navigation (Reverse Silo) -->
    <nav style="padding: 1rem 2rem; background: #f8f9fa; border-bottom: 1px solid #e5e7eb;">
        <ol style="list-style: none; display: flex; align-items: center; gap: 0.5rem; margin: 0; padding: 0; font-size: 0.9rem;">
            <li><a href="/" style="color: #1e3a8a; text-decoration: none; font-weight: 500;">Home</a></li>
            <li style="color: #6b7280;">›</li>
            <li><a href="/#areas" style="color: #1e3a8a; text-decoration: none;">Service Areas</a></li>
            <li style="color: #6b7280;">›</li>
            <li style="color: #4b5563;">{area_name} Property Management</li>
        </ol>
    </nav>
'''
        elif 'services' in str(page_path):
            service_name = page_path.parent.name.replace('-', ' ').title()
            return f'''
    <!-- Breadcrumb Navigation (Reverse Silo) -->
    <nav style="padding: 1rem 2rem; background: #f8f9fa; border-bottom: 1px solid #e5e7eb;">
        <ol style="list-style: none; display: flex; align-items: center; gap: 0.5rem; margin: 0; padding: 0; font-size: 0.9rem;">
            <li><a href="/" style="color: #1e3a8a; text-decoration: none; font-weight: 500;">Home</a></li>
            <li style="color: #6b7280;">›</li>
            <li><a href="/#services" style="color: #1e3a8a; text-decoration: none;">Services</a></li>
            <li style="color: #6b7280;">›</li>
            <li style="color: #4b5563;">{service_name}</li>
        </ol>
    </nav>
'''
        else:
            return ''

    def add_neighboring_area_links(self, current_area):
        """Add links to 3-4 neighboring areas for cross-linking"""
        all_areas = [
            'glenview', 'northbrook', 'highland-park', 'winnetka', 'wilmette',
            'evanston', 'skokie', 'morton-grove', 'lincolnwood', 'park-ridge',
            'des-plaines', 'mount-prospect', 'arlington-heights', 'buffalo-grove',
            'deerfield', 'northfield', 'glencoe', 'lake-forest', 'lake-bluff'
        ]
        
        # Remove current area
        current_area_name = current_area.replace('-', '').lower()
        nearby_areas = [a for a in all_areas if current_area_name not in a.replace('-', '')][:4]
        
        links_html = '''
    <!-- Neighboring Areas (Cross-Linking for Reverse Silo) -->
    <section style="background: white; padding: 2rem; margin: 2rem 0; border: 1px solid #e5e7eb; border-radius: 8px;">
        <h3 style="color: #1e3a8a; font-size: 1.3rem; margin-bottom: 1rem;">We Also Serve Nearby Communities</h3>
        <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
'''
        
        for area in nearby_areas:
            area_title = area.replace('-', ' ').title()
            links_html += f'''            <a href="/property-management/{area}/" style="padding: 0.5rem 1rem; background: #f8f9fa; border-radius: 6px; color: #1e3a8a; text-decoration: none; transition: all 0.2s;" onmouseover="this.style.background='#e9ecef'" onmouseout="this.style.background='#f8f9fa'">{area_title}</a>
'''
        
        links_html += '''        </div>
        <p style="margin-top: 1.5rem; color: #6b7280; font-size: 0.9rem;">
            <a href="/" style="color: #1e3a8a; font-weight: 500; text-decoration: none;">View all 68 service areas</a> we proudly serve across Chicago & North Shore
        </p>
    </section>
'''
        return links_html

    def update_footer_homepage_link(self, soup):
        """Ensure footer has strong homepage link"""
        footer = soup.find('footer')
        if footer:
            # Check if we already have a homepage CTA in footer
            if not footer.find(string=re.compile('Special Offer')):
                footer_cta = BeautifulSoup('''
    <div style="background: #1e3a8a; padding: 1.5rem; margin-bottom: 2rem; text-align: center; border-radius: 8px;">
        <p style="color: white; margin-bottom: 0.5rem; font-size: 1.1rem;">
            <strong>Limited Time:</strong> Save 75% on Property Management
        </p>
        <a href="/" style="color: #fbbf24; font-weight: 600; text-decoration: none;" onmouseover="this.style.textDecoration='underline'" onmouseout="this.style.textDecoration='none'">
            View Special Offer →
        </a>
    </div>
''', 'html.parser')
                footer.insert(0, footer_cta)
        return soup

    def process_area_page(self, file_path):
        """Process a single area page for reverse silo"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        area_name = file_path.parent.name
        
        # Add breadcrumb after header
        header = soup.find('header')
        if header:
            breadcrumb = BeautifulSoup(self.create_breadcrumb_navigation(file_path), 'html.parser')
            header.insert_after(breadcrumb)
        
        # Find main content area and add CTA
        main_content = soup.find('main') or soup.find('article') or soup.find('section', class_='content')
        if main_content:
            # Add offer CTA after main content
            offer_cta = BeautifulSoup(self.create_offer_cta_section("area"), 'html.parser')
            main_content.append(offer_cta)
            
            # Add neighboring areas section
            neighbors = BeautifulSoup(self.add_neighboring_area_links(area_name), 'html.parser')
            main_content.append(neighbors)
        
        # Update footer
        soup = self.update_footer_homepage_link(soup)
        
        # Save updated file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        self.pages_processed += 1
        self.changes_made.append(f"Area page: {area_name}")

    def process_service_page(self, file_path):
        """Process a service page for reverse silo"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        service_name = file_path.parent.name
        
        # Add breadcrumb
        header = soup.find('header')
        if header:
            breadcrumb = BeautifulSoup(self.create_breadcrumb_navigation(file_path), 'html.parser')
            header.insert_after(breadcrumb)
        
        # Add service CTA
        main_content = soup.find('main') or soup.find('article') or soup.find('section', class_='content')
        if main_content:
            service_cta = BeautifulSoup(self.create_offer_cta_section("service"), 'html.parser')
            main_content.append(service_cta)
        
        # Update footer
        soup = self.update_footer_homepage_link(soup)
        
        # Save updated file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        self.pages_processed += 1
        self.changes_made.append(f"Service page: {service_name}")

    def process_blog_page(self, file_path):
        """Process a blog page for reverse silo"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Add blog CTA
        main_content = soup.find('main') or soup.find('article') or soup.find('section', class_='content')
        if main_content:
            blog_cta = BeautifulSoup(self.create_offer_cta_section("blog"), 'html.parser')
            main_content.append(blog_cta)
        
        # Update footer
        soup = self.update_footer_homepage_link(soup)
        
        # Save updated file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        self.pages_processed += 1
        self.changes_made.append(f"Blog page: {file_path.name}")

    def run(self):
        """Execute the complete reverse silo implementation"""
        print("Starting Professional Reverse Silo Implementation")
        print("=" * 60)
        
        # Process all area pages
        print(f"\nProcessing {len(self.area_pages)} area pages...")
        for page in self.area_pages:
            self.process_area_page(page)
            print(f"  - {page.parent.name}")
        
        # Process all service pages  
        print(f"\nProcessing {len(self.service_pages)} service pages...")
        for page in self.service_pages:
            self.process_service_page(page)
            print(f"  - {page.parent.name}")
        
        # Process all blog pages
        print(f"\nProcessing {len(self.blog_pages)} blog pages...")
        for page in self.blog_pages:
            self.process_blog_page(page)
            print(f"  - {page.name}")
        
        # Create summary report
        self.create_summary_report()
        
        print("\n" + "=" * 60)
        print(f"REVERSE SILO IMPLEMENTATION COMPLETE!")
        print(f"Total pages processed: {self.pages_processed}")
        print(f"All pages now push link equity to homepage")
        print(f"Homepage offer promoted across entire site")
        print(f"Cross-linking implemented between related pages")
        print("\nExpected Results:")
        print("  - Homepage authority significantly increased")
        print("  - Better conversion funnel to special offer")
        print("  - Improved user navigation and experience")
        print("  - Stronger local SEO signals to Google")

    def create_summary_report(self):
        """Create a detailed summary of changes"""
        with open('REVERSE_SILO_IMPLEMENTATION.md', 'w') as f:
            f.write("# Reverse Silo Implementation Report\n\n")
            f.write(f"Date: August 29, 2025\n")
            f.write(f"Total Pages Modified: {self.pages_processed}\n\n")
            f.write("## Changes Made:\n\n")
            f.write("### Key Implementation Points:\n")
            f.write("- All pages now link to homepage with offer CTA\n")
            f.write("- Breadcrumb navigation added pointing to homepage\n")
            f.write("- Cross-linking between related area pages\n")
            f.write("- Footer CTAs added to drive conversions\n")
            f.write("- Strategic internal linking to consolidate authority\n\n")
            f.write("### Pages Modified:\n")
            for change in self.changes_made:
                f.write(f"- {change}\n")
            f.write("\n### SEO Impact:\n")
            f.write("This reverse silo structure will:\n")
            f.write("1. Push link equity from 68 area pages to Homepage\n")
            f.write("2. Strengthen homepage authority for competitive terms\n")
            f.write("3. Create clear conversion path to special offer\n")
            f.write("4. Improve overall site architecture for Google\n")
            f.write("5. Boost local ranking signals through cross-linking\n")

if __name__ == "__main__":
    implementer = ReverseSiloImplementation()
    implementer.run()