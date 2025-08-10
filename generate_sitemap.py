#!/usr/bin/env python3
"""
Generate comprehensive XML sitemap for Manage369 website
Includes priority and change frequency optimization
"""

import os
from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom

class SitemapGenerator:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.base_url = "https://manage369.com"
        self.urls = []
        
    def scan_directory(self):
        """Scan directory for all HTML files"""
        html_files = list(self.base_dir.glob('**/*.html'))
        
        # Exclude certain directories and files
        exclude_dirs = ['admin', 'temp', 'backup', 'test', 'private']
        exclude_files = ['404.html', 'error.html', 'index-old.html']
        
        for file_path in html_files:
            # Skip excluded directories
            if any(exc in str(file_path) for exc in exclude_dirs):
                continue
            
            # Skip excluded files
            if file_path.name in exclude_files:
                continue
                
            # Get relative path and convert to URL
            rel_path = file_path.relative_to(self.base_dir)
            url_path = str(rel_path).replace('\\', '/')
            
            # Handle index.html files
            if url_path.endswith('index.html'):
                url_path = url_path.replace('index.html', '')
            
            # Skip non-index HTML files in subdirectories (they're likely templates)
            if '/' in url_path and not url_path.endswith('/') and url_path.endswith('.html'):
                # Only include root-level HTML files and index files
                if url_path.count('/') > 0 and not url_path.startswith('blog/'):
                    continue
            
            # Create full URL
            if url_path:
                full_url = f"{self.base_url}/{url_path}"
            else:
                full_url = self.base_url
                
            # Determine priority and change frequency
            priority, changefreq = self.determine_priority(url_path)
            
            # Get last modified date
            lastmod = datetime.fromtimestamp(file_path.stat().st_mtime).strftime('%Y-%m-%d')
            
            self.urls.append({
                'loc': full_url,
                'lastmod': lastmod,
                'changefreq': changefreq,
                'priority': priority
            })
    
    def determine_priority(self, url_path):
        """Determine URL priority and change frequency based on path"""
        
        # Homepage
        if not url_path or url_path == '/':
            return '1.0', 'daily'
        
        # Main service pages
        if url_path.startswith('services'):
            return '0.9', 'weekly'
        
        # Property management location pages
        if url_path.startswith('property-management/'):
            # Main property management page
            if url_path == 'property-management/':
                return '0.9', 'weekly'
            # Individual location pages
            return '0.8', 'monthly'
        
        # Blog posts
        if url_path.startswith('blog/'):
            # Blog index
            if url_path == 'blog/':
                return '0.8', 'weekly'
            # Individual blog posts
            return '0.7', 'monthly'
        
        # Contact and important pages
        if url_path in ['contact.html', 'forms.html', 'pay-dues.html']:
            return '0.9', 'monthly'
        
        # Legal and policy pages
        if any(term in url_path for term in ['privacy', 'terms', 'legal', 'disclaimer']):
            return '0.3', 'yearly'
        
        # Default for other pages
        return '0.5', 'monthly'
    
    def generate_xml(self):
        """Generate XML sitemap"""
        # Create root element with namespace
        root = ET.Element('urlset')
        root.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
        root.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        root.set('xsi:schemaLocation', 
                'http://www.sitemaps.org/schemas/sitemap/0.9 '
                'http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd')
        
        # Sort URLs by priority (highest first) then alphabetically
        self.urls.sort(key=lambda x: (-float(x['priority']), x['loc']))
        
        # Add each URL to sitemap
        for url_data in self.urls:
            url_elem = ET.SubElement(root, 'url')
            
            loc = ET.SubElement(url_elem, 'loc')
            loc.text = url_data['loc']
            
            lastmod = ET.SubElement(url_elem, 'lastmod')
            lastmod.text = url_data['lastmod']
            
            changefreq = ET.SubElement(url_elem, 'changefreq')
            changefreq.text = url_data['changefreq']
            
            priority = ET.SubElement(url_elem, 'priority')
            priority.text = url_data['priority']
        
        # Convert to string with pretty formatting
        xml_str = ET.tostring(root, encoding='unicode')
        dom = minidom.parseString(xml_str)
        pretty_xml = dom.toprettyxml(indent='  ', encoding='UTF-8')
        
        # Remove extra blank lines
        lines = pretty_xml.decode('utf-8').split('\n')
        lines = [line for line in lines if line.strip()]
        
        return '\n'.join(lines)
    
    def generate_sitemap_index(self):
        """Generate sitemap index if we have multiple sitemaps"""
        # For now, we'll just have one sitemap
        # This method is here for future expansion
        pass
    
    def save_sitemap(self, output_path=None):
        """Save sitemap to file"""
        if output_path is None:
            output_path = self.base_dir / 'sitemap.xml'
        
        # Scan directory and generate XML
        self.scan_directory()
        xml_content = self.generate_xml()
        
        # Save to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        print(f"Sitemap generated with {len(self.urls)} URLs")
        print(f"Saved to: {output_path}")
        
        # Show statistics
        self.show_statistics()
        
        return output_path
    
    def show_statistics(self):
        """Show sitemap statistics"""
        print("\nSitemap Statistics:")
        print("-" * 40)
        
        # Count by change frequency
        freq_count = {}
        for url in self.urls:
            freq = url['changefreq']
            freq_count[freq] = freq_count.get(freq, 0) + 1
        
        print("Change Frequency Distribution:")
        for freq, count in sorted(freq_count.items()):
            print(f"  {freq}: {count} URLs")
        
        # Count by priority
        priority_count = {}
        for url in self.urls:
            priority = url['priority']
            priority_count[priority] = priority_count.get(priority, 0) + 1
        
        print("\nPriority Distribution:")
        for priority, count in sorted(priority_count.items(), reverse=True):
            print(f"  {priority}: {count} URLs")
        
        # Show top priority URLs
        print("\nTop Priority URLs:")
        for url in self.urls[:10]:
            print(f"  [{url['priority']}] {url['loc']}")

if __name__ == "__main__":
    generator = SitemapGenerator(r"C:\Users\mirsa\manage369-live")
    generator.save_sitemap()
    
    print("\nSitemap generation complete!")
    print("Don't forget to:")
    print("1. Submit the sitemap to Google Search Console")
    print("2. Submit the sitemap to Bing Webmaster Tools")
    print("3. Verify the sitemap URL in robots.txt is correct")