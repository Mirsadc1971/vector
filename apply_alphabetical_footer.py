"""
Apply reorganized alphabetical footer to all pages
"""

import os
from bs4 import BeautifulSoup
import re

def get_new_footer_html():
    """Return the new alphabetically organized footer HTML"""
    return '''<!-- REORGANIZED FOOTER - 3 COLUMNS ALPHABETICAL -->
<style>
/* PERFECT FOOTER WITH 3 COLUMNS - ALPHABETICAL ORGANIZATION */
footer {
    background: #2c3e50;
    color: white;
    line-height: 1.6;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.footer-main {
    max-width: 1200px;
    margin: 0 auto;
    padding: 40px 20px;
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 40px;
}

.footer-column {
    line-height: 1.6;
}

.footer-logo {
    font-size: 24px;
    color: #ff6b35;
    margin-bottom: 8px;
    font-weight: normal;
}

.footer-description {
    color: white;
    line-height: 1.6;
    margin-bottom: 8px;
}

.footer-stats {
    color: white;
    line-height: 1.6;
    margin-bottom: 8px;
}

.footer-contact-line {
    color: white;
    line-height: 1.6;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
}

.footer-contact-line a {
    color: white;
    text-decoration: none;
}

.footer-contact-line a:hover {
    text-decoration: underline;
}

.footer-license {
    color: #ff6b35;
    font-weight: bold;
    line-height: 1.6;
}

.footer-column h3 {
    color: #ff6b35;
    font-size: 18px;
    margin-bottom: 15px;
    font-weight: normal;
}

.footer-links {
    list-style: none;
    padding: 0;
    margin: 0;
}

.footer-links li {
    margin-bottom: 10px;
}

.footer-links a {
    color: white;
    text-decoration: none;
    line-height: 1.6;
}

.footer-links a:hover {
    color: #ff6b35;
}

.footer-divider {
    border: none;
    border-top: 1px solid rgba(255, 255, 255, 0.2);
    margin: 20px 0;
    max-width: 1200px;
    margin-left: auto;
    margin-right: auto;
}

.footer-bottom {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px 40px;
    text-align: center;
}

.certifications {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 30px;
    margin-bottom: 20px;
    flex-wrap: wrap;
}

.cert-badge {
    height: 60px;
    max-height: 60px;
    background: white;
    border-radius: 8px;
    padding: 10px 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #2c3e50;
    font-weight: bold;
    font-size: 14px;
}

.footer-copyright {
    text-align: center;
    color: white;
    font-size: 14px;
    line-height: 1.6;
}

/* RESPONSIVE DESIGN */
@media (max-width: 768px) {
    .footer-main {
        grid-template-columns: 1fr;
        gap: 30px;
        text-align: center;
        padding: 40px 15px;
    }
    
    .footer-contact-line {
        justify-content: center;
    }
    
    .certifications {
        gap: 15px;
    }
    
    .cert-badge {
        height: 50px;
        max-height: 50px;
        padding: 8px 12px;
        font-size: 12px;
    }
}
</style>

<footer>
    <div class="footer-main">
        <!-- COLUMN 1: MANAGE369 INFO -->
        <div class="footer-column">
            <div class="footer-logo">Manage369</div>
            <div class="footer-description">Premier Chicago & North Shore Property Management</div>
            <div class="footer-stats">18+ Years of Excellence • 50+ Properties • 2,450+ Units</div>
            <div class="footer-contact-line">
                📞 <a href="tel:8476522338">(847) 652-2338</a>
            </div>
            <div class="footer-contact-line">
                ✉️ <a href="mailto:service@manage369.com">service@manage369.com</a>
            </div>
            <div class="footer-contact-line">
                📍 1400 Patriot Boulevard 357, Glenview, IL 60026
            </div>
            <div class="footer-license">IDFPR Management Firm License 291.000211</div>
        </div>
        
        <!-- COLUMN 2: QUICK LINKS (ALPHABETICAL) -->
        <div class="footer-column">
            <h3>Quick Links</h3>
            <ul class="footer-links">
                <li><a href="{base_path}property-management/">Areas We Serve</a></li>
                <li><a href="{base_path}blog/">Blog</a></li>
                <li><a href="{base_path}contact.html">Contact</a></li>
                <li><a href="{base_path}payment-methods.html">Payment Methods</a></li>
                <li><a href="{base_path}services.html">Services</a></li>
            </ul>
        </div>
        
        <!-- COLUMN 3: RESOURCES (ALPHABETICAL) -->
        <div class="footer-column">
            <h3>Resources</h3>
            <ul class="footer-links">
                <li><a href="{base_path}accessibility.html">Accessibility</a></li>
                <li><a href="{base_path}forms.html">Forms & Documents</a></li>
                <li><a href="{base_path}legal-disclaimers.html">Legal Disclaimers</a></li>
                <li><a href="{base_path}privacy-policy.html">Privacy Policy</a></li>
                <li><a href="{base_path}sitemap.html">Sitemap</a></li>
                <li><a href="{base_path}terms-of-service.html">Terms of Service</a></li>
            </ul>
        </div>
    </div>
    
    <hr class="footer-divider">
    
    <div class="footer-bottom">
        <div class="certifications">
            <div class="cert-badge">CAI</div>
            <div class="cert-badge">CCIM</div>
            <div class="cert-badge">IDFPR</div>
            <div class="cert-badge">IREM</div>
            <div class="cert-badge">NAR</div>
        </div>
        <div class="footer-copyright">
            © 2025 Manage369. All Rights Reserved.
        </div>
    </div>
</footer>'''

def replace_footer(filepath, base_path=''):
    """Replace the footer in an HTML file"""
    
    try:
        # Read the file
        with open(filepath, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find and remove the old footer
        old_footer = soup.find('footer')
        if old_footer:
            # Also remove any style tag that might be right before the footer
            prev_sibling = old_footer.find_previous_sibling()
            if prev_sibling and prev_sibling.name == 'style':
                # Check if this style is footer-related
                style_text = prev_sibling.get_text()
                if 'footer' in style_text.lower() or 'PERFECT FOOTER' in style_text:
                    prev_sibling.decompose()
            
            old_footer.decompose()
        
        # Get the new footer with proper base path
        new_footer_html = get_new_footer_html().replace('{base_path}', base_path)
        
        # Parse the new footer
        new_footer_soup = BeautifulSoup(new_footer_html, 'html.parser')
        
        # Find the body tag and append the new footer
        body = soup.find('body')
        if body:
            # Add the style tag and footer at the end of body
            for element in new_footer_soup:
                body.append(element)
        
        # Save the updated file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        return True
            
    except Exception as e:
        print(f"  [ERROR] Error processing {filepath}: {e}")
        return False

def process_directory(directory, base_path, dir_name):
    """Process all HTML files in a directory"""
    
    success_count = 0
    failed_files = []
    
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        
        # Process subdirectories
        if os.path.isdir(item_path):
            # For property-management pages
            index_file = os.path.join(item_path, 'index.html')
            if os.path.exists(index_file):
                print(f"  Processing: {item}/index.html")
                if replace_footer(index_file, base_path):
                    success_count += 1
                else:
                    failed_files.append(f"{item}/index.html")
        
        # Process HTML files in current directory
        elif item.endswith('.html'):
            print(f"  Processing: {item}")
            if replace_footer(item_path, base_path):
                success_count += 1
            else:
                failed_files.append(item)
    
    return success_count, failed_files

def main():
    """Main function to update all footers"""
    
    print("Applying alphabetically organized footer to all pages")
    print("=" * 50)
    
    total_success = 0
    all_failed = []
    
    # Process property-management pages (68 pages)
    print("\n1. Processing Property Management Pages...")
    prop_dir = 'C:\\Users\\mirsa\\manage369-live\\property-management'
    if os.path.exists(prop_dir):
        success, failed = process_directory(prop_dir, '../../', 'property-management')
        total_success += success
        all_failed.extend([f"property-management/{f}" for f in failed])
    
    # Process services pages
    print("\n2. Processing Services Pages...")
    services_dir = 'C:\\Users\\mirsa\\manage369-live\\services'
    if os.path.exists(services_dir):
        # Service subdirectories
        for service_type in os.listdir(services_dir):
            service_path = os.path.join(services_dir, service_type)
            if os.path.isdir(service_path):
                index_file = os.path.join(service_path, 'index.html')
                if os.path.exists(index_file):
                    print(f"  Processing: services/{service_type}/index.html")
                    if replace_footer(index_file, '../../'):
                        total_success += 1
                    else:
                        all_failed.append(f"services/{service_type}/index.html")
        
        # Main services.html
        services_html = os.path.join(services_dir, '..', 'services.html')
        if os.path.exists(services_html):
            print(f"  Processing: services.html")
            if replace_footer(services_html, ''):
                total_success += 1
            else:
                all_failed.append("services.html")
    
    # Process root level pages
    print("\n3. Processing Root Level Pages...")
    root_dir = 'C:\\Users\\mirsa\\manage369-live'
    root_pages = [
        'index.html', 'contact.html', 'pay-dues.html', 
        'payment-methods.html', 'forms.html', 'privacy-policy.html',
        'terms-of-service.html', 'sitemap.html', 'accessibility.html',
        'legal-disclaimers.html'
    ]
    
    for page in root_pages:
        page_path = os.path.join(root_dir, page)
        if os.path.exists(page_path):
            print(f"  Processing: {page}")
            if replace_footer(page_path, ''):
                total_success += 1
            else:
                all_failed.append(page)
    
    # Process blog pages if they exist
    print("\n4. Processing Blog Pages...")
    blog_dir = os.path.join(root_dir, 'blog')
    if os.path.exists(blog_dir):
        for item in os.listdir(blog_dir):
            if item.endswith('.html'):
                blog_path = os.path.join(blog_dir, item)
                print(f"  Processing: blog/{item}")
                if replace_footer(blog_path, '../'):
                    total_success += 1
                else:
                    all_failed.append(f"blog/{item}")
    
    print("\n" + "=" * 50)
    print(f"Process Complete!")
    print(f"Successfully updated: {total_success} pages")
    
    if all_failed:
        print(f"\nFailed to update {len(all_failed)} pages:")
        for f in all_failed:
            print(f"  - {f}")

if __name__ == "__main__":
    main()