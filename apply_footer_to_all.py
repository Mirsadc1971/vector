"""
Apply alphabetical footer to all pages safely
"""

import os
import re

def update_footer_links(content):
    """Update just the footer links to alphabetical order"""
    
    # Find the Quick Links section
    quick_links_pattern = r'(<h3[^>]*>[\s]*Quick Links[\s]*</h3>[\s]*<ul[^>]*>)(.*?)(</ul>)'
    
    # New alphabetical quick links
    new_quick_links = """
                <li><a href="../">Areas We Serve</a></li>
                <li><a href="../../blog/">Blog</a></li>
                <li><a href="../../contact.html">Contact</a></li>
                <li><a href="../../payment-methods.html">Payment Methods</a></li>
                <li><a href="../../services.html">Services</a></li>"""
    
    # For root level pages
    new_quick_links_root = """
                <li><a href="property-management/">Areas We Serve</a></li>
                <li><a href="blog/">Blog</a></li>
                <li><a href="contact.html">Contact</a></li>
                <li><a href="payment-methods.html">Payment Methods</a></li>
                <li><a href="services.html">Services</a></li>"""
    
    # For service pages
    new_quick_links_service = """
                <li><a href="../property-management/">Areas We Serve</a></li>
                <li><a href="../blog/">Blog</a></li>
                <li><a href="../contact.html">Contact</a></li>
                <li><a href="../payment-methods.html">Payment Methods</a></li>
                <li><a href="../services.html">Services</a></li>"""
    
    # Find Resources section
    resources_pattern = r'(<h3[^>]*>[\s]*Resources[\s]*</h3>[\s]*<ul[^>]*>)(.*?)(</ul>)'
    
    # New alphabetical resources
    new_resources = """
                <li><a href="../../accessibility.html">Accessibility</a></li>
                <li><a href="../../forms.html">Forms & Documents</a></li>
                <li><a href="../../legal-disclaimers.html">Legal Disclaimers</a></li>
                <li><a href="../../privacy-policy.html">Privacy Policy</a></li>
                <li><a href="../../sitemap.html">Sitemap</a></li>
                <li><a href="../../terms-of-service.html">Terms of Service</a></li>"""
    
    new_resources_root = """
                <li><a href="accessibility.html">Accessibility</a></li>
                <li><a href="forms.html">Forms & Documents</a></li>
                <li><a href="legal-disclaimers.html">Legal Disclaimers</a></li>
                <li><a href="privacy-policy.html">Privacy Policy</a></li>
                <li><a href="sitemap.html">Sitemap</a></li>
                <li><a href="terms-of-service.html">Terms of Service</a></li>"""
    
    new_resources_service = """
                <li><a href="../accessibility.html">Accessibility</a></li>
                <li><a href="../forms.html">Forms & Documents</a></li>
                <li><a href="../legal-disclaimers.html">Legal Disclaimers</a></li>
                <li><a href="../privacy-policy.html">Privacy Policy</a></li>
                <li><a href="../sitemap.html">Sitemap</a></li>
                <li><a href="../terms-of-service.html">Terms of Service</a></li>"""
    
    # Find certifications and make alphabetical
    cert_pattern = r'(<div class="certifications">)(.*?)(</div>)'
    
    new_certs = """
            <div class="cert-badge">CAI</div>
            <div class="cert-badge">CCIM</div>
            <div class="cert-badge">IDFPR</div>
            <div class="cert-badge">IREM</div>
            <div class="cert-badge">NAR</div>"""
    
    # Determine page type by path structure
    if '../../' in content:
        # Property management pages (nested)
        content = re.sub(quick_links_pattern, r'\1' + new_quick_links + r'\3', content, flags=re.DOTALL)
        content = re.sub(resources_pattern, r'\1' + new_resources + r'\3', content, flags=re.DOTALL)
    elif '../property-management/' in content or '../blog/' in content:
        # Service pages
        content = re.sub(quick_links_pattern, r'\1' + new_quick_links_service + r'\3', content, flags=re.DOTALL)
        content = re.sub(resources_pattern, r'\1' + new_resources_service + r'\3', content, flags=re.DOTALL)
    else:
        # Root pages
        content = re.sub(quick_links_pattern, r'\1' + new_quick_links_root + r'\3', content, flags=re.DOTALL)
        content = re.sub(resources_pattern, r'\1' + new_resources_root + r'\3', content, flags=re.DOTALL)
    
    # Update certifications
    def replace_certs(match):
        return match.group(1) + new_certs + match.group(3)
    
    content = re.sub(cert_pattern, replace_certs, content, flags=re.DOTALL)
    
    return content

# Process all pages
root_dir = 'C:\\Users\\mirsa\\manage369-live'
pages_updated = 0
pages_skipped = 0

# Root level HTML files
for filename in os.listdir(root_dir):
    if filename.endswith('.html'):
        filepath = os.path.join(root_dir, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = update_footer_links(content)
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            pages_updated += 1
            print(f"Updated: {filename}")
        else:
            pages_skipped += 1

# Property management pages
prop_dir = os.path.join(root_dir, 'property-management')
for location in os.listdir(prop_dir):
    if location == 'index.html' or location == 'index-old.html':
        # Handle property-management index separately
        if location == 'index.html':
            filepath = os.path.join(prop_dir, location)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = update_footer_links(content)
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                pages_updated += 1
                print(f"Updated: property-management/{location}")
            else:
                pages_skipped += 1
        continue
    
    # Location subdirectories
    location_path = os.path.join(prop_dir, location)
    if os.path.isdir(location_path):
        index_file = os.path.join(location_path, 'index.html')
        if os.path.exists(index_file):
            with open(index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = update_footer_links(content)
            
            if new_content != content:
                with open(index_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                pages_updated += 1
                print(f"Updated: property-management/{location}/index.html")
            else:
                pages_skipped += 1

# Service pages
service_dir = os.path.join(root_dir, 'services')
if os.path.exists(service_dir):
    for filename in os.listdir(service_dir):
        if filename.endswith('.html'):
            filepath = os.path.join(service_dir, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = update_footer_links(content)
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                pages_updated += 1
                print(f"Updated: services/{filename}")
            else:
                pages_skipped += 1

# Blog pages
blog_dir = os.path.join(root_dir, 'blog')
if os.path.exists(blog_dir):
    for filename in os.listdir(blog_dir):
        if filename.endswith('.html'):
            filepath = os.path.join(blog_dir, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = update_footer_links(content)
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                pages_updated += 1
                print(f"Updated: blog/{filename}")
            else:
                pages_skipped += 1

print(f"\n[COMPLETE] Updated {pages_updated} pages, skipped {pages_skipped} pages")