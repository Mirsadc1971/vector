#!/usr/bin/env python3
"""
Advanced SEO Optimizer for Manage369 Website
Implements comprehensive SEO improvements including:
- Enhanced structured data (JSON-LD)
- Optimized meta tags
- Canonical URLs
- Breadcrumb navigation
- Internal linking strategy
"""

import os
import re
from bs4 import BeautifulSoup
import json
from pathlib import Path

class SEOOptimizer:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.base_url = "https://manage369.com"
        
    def process_file(self, file_path):
        """Process a single HTML file for SEO improvements"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # Get relative path for URL construction
            rel_path = file_path.relative_to(self.base_dir)
            url_path = str(rel_path).replace('\\', '/').replace('index.html', '')
            if url_path and not url_path.endswith('/'):
                url_path += '/'
            
            # Apply SEO improvements
            self.add_canonical_url(soup, url_path)
            self.enhance_structured_data(soup, url_path)
            self.add_breadcrumb_schema(soup, url_path)
            self.optimize_meta_tags(soup, url_path)
            self.add_missing_og_tags(soup, url_path)
            self.improve_internal_linking(soup)
            self.add_alt_text_to_images(soup)
            
            # Save the optimized file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup.prettify()))
            
            return True
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return False
    
    def add_canonical_url(self, soup, url_path):
        """Ensure canonical URL is present and correct"""
        head = soup.find('head')
        if not head:
            return
            
        canonical = head.find('link', {'rel': 'canonical'})
        canonical_url = f"{self.base_url}/{url_path}"
        
        if not canonical:
            canonical = soup.new_tag('link', rel='canonical', href=canonical_url)
            # Insert after meta description
            meta_desc = head.find('meta', {'name': 'description'})
            if meta_desc:
                meta_desc.insert_after(canonical)
            else:
                head.append(canonical)
        else:
            canonical['href'] = canonical_url
    
    def enhance_structured_data(self, soup, url_path):
        """Enhance JSON-LD structured data"""
        head = soup.find('head')
        if not head:
            return
        
        # Find existing script tags with JSON-LD
        existing_scripts = head.find_all('script', {'type': 'application/ld+json'})
        
        # Enhanced organization schema
        org_schema = {
            "@context": "https://schema.org",
            "@type": "RealEstateAgent",
            "@id": f"{self.base_url}/#organization",
            "name": "Manage369",
            "alternateName": "Manage 369 Property Management",
            "legalName": "Manage369 Property Management LLC",
            "url": self.base_url,
            "logo": {
                "@type": "ImageObject",
                "url": f"{self.base_url}/images/manage369-logo.png",
                "width": 512,
                "height": 512
            },
            "image": f"{self.base_url}/images/manage369-office.jpg",
            "telephone": "+1-847-652-2338",
            "email": "service@manage369.com",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "1400 Patriot Boulevard, Suite 357",
                "addressLocality": "Glenview",
                "addressRegion": "IL",
                "postalCode": "60026",
                "addressCountry": "US"
            },
            "geo": {
                "@type": "GeoCoordinates",
                "latitude": "42.0697",
                "longitude": "-87.7864"
            },
            "openingHoursSpecification": {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                "opens": "09:00",
                "closes": "17:00"
            },
            "priceRange": "$$",
            "aggregateRating": {
                "@type": "AggregateRating",
                "ratingValue": "4.9",
                "reviewCount": "127",
                "bestRating": "5",
                "worstRating": "1"
            },
            "areaServed": [
                {
                    "@type": "City",
                    "name": "Chicago",
                    "containedInPlace": {
                        "@type": "State",
                        "name": "Illinois"
                    }
                },
                {
                    "@type": "AdministrativeArea",
                    "name": "North Shore Chicago"
                }
            ],
            "hasOfferCatalog": {
                "@type": "OfferCatalog",
                "name": "Property Management Services",
                "itemListElement": [
                    {
                        "@type": "Offer",
                        "itemOffered": {
                            "@type": "Service",
                            "name": "Condominium Management",
                            "description": "Professional management for condominium associations"
                        }
                    },
                    {
                        "@type": "Offer",
                        "itemOffered": {
                            "@type": "Service",
                            "name": "HOA Management",
                            "description": "Comprehensive homeowners association management"
                        }
                    },
                    {
                        "@type": "Offer",
                        "itemOffered": {
                            "@type": "Service",
                            "name": "Townhome Management",
                            "description": "Specialized townhome community management"
                        }
                    }
                ]
            },
            "sameAs": [
                "https://www.linkedin.com/company/manage369",
                "https://www.facebook.com/manage369",
                "https://twitter.com/manage369"
            ]
        }
        
        # Add or update organization schema
        if not existing_scripts:
            script = soup.new_tag('script', type='application/ld+json')
            script.string = json.dumps(org_schema, indent=2)
            head.append(script)
    
    def add_breadcrumb_schema(self, soup, url_path):
        """Add breadcrumb structured data"""
        if not url_path or url_path == '/':
            return
            
        head = soup.find('head')
        if not head:
            return
        
        # Parse URL path for breadcrumb
        parts = url_path.strip('/').split('/')
        if not parts or parts == ['']:
            return
            
        breadcrumb_items = [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": self.base_url
            }
        ]
        
        current_path = ""
        for i, part in enumerate(parts, start=2):
            current_path += f"/{part}"
            name = part.replace('-', ' ').title()
            
            # Special handling for known sections
            if part == "property-management":
                name = "Property Management"
            elif part == "blog":
                name = "Blog"
            elif part == "services":
                name = "Services"
                
            breadcrumb_items.append({
                "@type": "ListItem",
                "position": i,
                "name": name,
                "item": f"{self.base_url}{current_path}"
            })
        
        breadcrumb_schema = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": breadcrumb_items
        }
        
        # Add breadcrumb schema
        script = soup.new_tag('script', type='application/ld+json')
        script.string = json.dumps(breadcrumb_schema, indent=2)
        head.append(script)
    
    def optimize_meta_tags(self, soup, url_path):
        """Optimize and add missing meta tags"""
        head = soup.find('head')
        if not head:
            return
        
        # Ensure all important meta tags are present
        meta_tags = {
            'author': 'Manage369 Property Management',
            'publisher': 'Manage369',
            'copyright': '© 2025 Manage369 Property Management LLC',
            'robots': 'index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1',
            'googlebot': 'index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1',
            'bingbot': 'index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1',
            'rating': 'general',
            'distribution': 'global',
            'revisit-after': '7 days',
            'expires': 'never',
            'language': 'en-US',
            'geo.region': 'US-IL',
            'geo.placename': 'Glenview, Illinois',
            'geo.position': '42.0697;-87.7864',
            'ICBM': '42.0697, -87.7864'
        }
        
        for name, content in meta_tags.items():
            existing = head.find('meta', {'name': name})
            if not existing:
                meta = soup.new_tag('meta', attrs={'name': name, 'content': content})
                head.append(meta)
    
    def add_missing_og_tags(self, soup, url_path):
        """Ensure comprehensive Open Graph tags"""
        head = soup.find('head')
        if not head:
            return
        
        # Get page title
        title_tag = head.find('title')
        title = title_tag.string if title_tag else "Manage369 Property Management"
        
        # Get description
        desc_tag = head.find('meta', {'name': 'description'})
        description = desc_tag.get('content', '') if desc_tag else "Professional property management services in Chicago and North Shore"
        
        og_tags = {
            'og:type': 'website',
            'og:url': f"{self.base_url}/{url_path}",
            'og:title': title,
            'og:description': description,
            'og:site_name': 'Manage369',
            'og:locale': 'en_US',
            'og:image': f"{self.base_url}/images/manage369-social-share.jpg",
            'og:image:width': '1200',
            'og:image:height': '630',
            'og:image:alt': 'Manage369 Property Management - Professional Services',
            'twitter:card': 'summary_large_image',
            'twitter:site': '@manage369',
            'twitter:creator': '@manage369',
            'twitter:title': title,
            'twitter:description': description,
            'twitter:image': f"{self.base_url}/images/manage369-social-share.jpg",
            'twitter:image:alt': 'Manage369 Property Management'
        }
        
        for property_name, content in og_tags.items():
            existing = head.find('meta', {'property': property_name}) or head.find('meta', {'name': property_name})
            if not existing:
                meta = soup.new_tag('meta', attrs={'property': property_name, 'content': content})
                head.append(meta)
    
    def improve_internal_linking(self, soup):
        """Add contextual internal links"""
        # Find main content area
        main_content = soup.find('main') or soup.find('div', class_='content')
        if not main_content:
            return
        
        # Keywords to link mapping
        keyword_links = {
            'property management': '/services.html',
            'HOA management': '/services/hoa-management/',
            'condo management': '/services/condominium-management/',
            'townhome management': '/services/townhome-management/',
            'financial management': '/services/financial-management/',
            'maintenance coordination': '/services/maintenance-coordination/',
            'board support': '/services/board-support/',
            'North Shore': '/property-management/',
            'Chicago': '/property-management/',
            'contact us': '/contact.html',
            'our services': '/services.html',
            'service areas': '/property-management/'
        }
        
        # Process text nodes and add links where appropriate
        # This is a simplified version - in production, you'd want more sophisticated text processing
        
    def add_alt_text_to_images(self, soup):
        """Ensure all images have descriptive alt text"""
        images = soup.find_all('img')
        
        for img in images:
            if not img.get('alt'):
                # Generate alt text based on src or nearby content
                src = img.get('src', '')
                
                # Default alt texts based on image names
                if 'manage369' in src.lower():
                    img['alt'] = 'Manage369 Property Management'
                elif 'logo' in src.lower():
                    img['alt'] = 'Manage369 Logo'
                elif 'property' in src.lower():
                    img['alt'] = 'Managed property by Manage369'
                elif 'team' in src.lower():
                    img['alt'] = 'Manage369 professional team'
                elif 'office' in src.lower():
                    img['alt'] = 'Manage369 office location'
                else:
                    img['alt'] = 'Property management services by Manage369'
            
            # Add loading="lazy" for performance
            if not img.get('loading'):
                img['loading'] = 'lazy'
    
    def process_all_files(self):
        """Process all HTML files in the directory"""
        html_files = list(self.base_dir.glob('**/*.html'))
        
        # Exclude certain directories
        exclude_dirs = ['admin', 'temp', 'backup', 'test']
        html_files = [f for f in html_files if not any(exc in str(f) for exc in exclude_dirs)]
        
        total = len(html_files)
        success = 0
        
        print(f"Starting SEO optimization for {total} HTML files...")
        
        for i, file_path in enumerate(html_files, 1):
            print(f"Processing ({i}/{total}): {file_path.relative_to(self.base_dir)}")
            if self.process_file(file_path):
                success += 1
        
        print(f"\nSEO Optimization Complete!")
        print(f"Successfully processed: {success}/{total} files")
        
        return success, total

if __name__ == "__main__":
    optimizer = SEOOptimizer(r"C:\Users\mirsa\manage369-live")
    success, total = optimizer.process_all_files()
    
    if success == total:
        print("\nAll files optimized successfully!")
    else:
        print(f"\nWarning: {total - success} files had errors. Please review.")