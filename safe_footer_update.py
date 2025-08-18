"""
Safely update footer to alphabetical order without breaking HTML
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
    
    # Find certifications and make alphabetical
    cert_pattern = r'(<div class="certifications">)(.*?)(</div>)'
    
    new_certs = """
            <div class="cert-badge">CAI</div>
            <div class="cert-badge">CCIM</div>
            <div class="cert-badge">IDFPR</div>
            <div class="cert-badge">IREM</div>
            <div class="cert-badge">NAR</div>"""
    
    # Determine if this is a root page or nested
    if '../../' in content:
        # Nested page
        content = re.sub(quick_links_pattern, r'\1' + new_quick_links + r'\3', content, flags=re.DOTALL)
        content = re.sub(resources_pattern, r'\1' + new_resources + r'\3', content, flags=re.DOTALL)
    else:
        # Root page
        content = re.sub(quick_links_pattern, r'\1' + new_quick_links_root + r'\3', content, flags=re.DOTALL)
        content = re.sub(resources_pattern, r'\1' + new_resources_root + r'\3', content, flags=re.DOTALL)
    
    # Update certifications
    def replace_certs(match):
        return match.group(1) + new_certs + match.group(3)
    
    content = re.sub(cert_pattern, replace_certs, content, flags=re.DOTALL)
    
    return content

# Test on one page first
test_file = 'C:\\Users\\mirsa\\manage369-live\\property-management\\glenview\\index.html'

print("Testing on Glenview page first...")
with open(test_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Make backup
with open(test_file + '.backup2', 'w', encoding='utf-8') as f:
    f.write(content)

# Update
new_content = update_footer_links(content)

# Check if changes were made
if new_content != content:
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("[SUCCESS] Updated Glenview page successfully")
    print("Check the page to make sure it's not broken before proceeding")
else:
    print("No changes made to Glenview page")