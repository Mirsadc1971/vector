"""
Apply final improved footer with flexbox to ALL pages
"""

import os
from bs4 import BeautifulSoup

def get_new_footer_html():
    """Return the improved footer HTML with flexbox layout"""
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
    display: flex;
    justify-content: space-between;
    gap: 60px;
}

.footer-column {
    line-height: 1.6;
    flex: 1;
    min-width: 250px;
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
        flex-direction: column;
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
        
        # Find and remove ALL existing footers and footer styles
        # Remove any existing footer style tags
        for style in soup.find_all('style'):
            if style.string and ('footer' in style.string.lower() or 'PERFECT FOOTER' in style.string or 'REORGANIZED FOOTER' in style.string):
                style.decompose()
        
        # Remove existing footer
        old_footer = soup.find('footer')
        if old_footer:
            old_footer.decompose()
        
        # Also look for comments that might indicate footer sections
        for comment in soup.find_all(string=lambda text: isinstance(text, str) and '<!-- REORGANIZED FOOTER' in text):
            comment.extract()
        for comment in soup.find_all(string=lambda text: isinstance(text, str) and '<!-- PERFECT FOOTER' in text):
            comment.extract()
            
        # Get the new footer with proper base path
        new_footer_html = get_new_footer_html().replace('{base_path}', base_path)
        
        # Parse the new footer
        new_footer_soup = BeautifulSoup(new_footer_html, 'html.parser')
        
        # Find the body tag and append the new footer
        body = soup.find('body')
        if body:
            # Add the comment, style tag and footer at the end of body
            for element in new_footer_soup:
                body.append(element)
        
        # Save the updated file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        return True
            
    except Exception as e:
        print(f"  [ERROR] Error processing {filepath}: {e}")
        return False

def main():
    """Main function to update all footers"""
    
    print("Applying improved flexbox footer to ALL pages")
    print("=" * 50)
    
    total_success = 0
    all_failed = []
    
    base_dir = 'C:\\Users\\mirsa\\manage369-live'
    
    # 1. Process ALL property-management pages (68 locations)
    print("\n1. Processing Property Management Pages (68 locations)...")
    prop_dir = os.path.join(base_dir, 'property-management')
    if os.path.exists(prop_dir):
        for location in os.listdir(prop_dir):
            location_path = os.path.join(prop_dir, location)
            if os.path.isdir(location_path):
                index_file = os.path.join(location_path, 'index.html')
                if os.path.exists(index_file):
                    print(f"  Processing: property-management/{location}/index.html")
                    if replace_footer(index_file, '../../'):
                        total_success += 1
                    else:
                        all_failed.append(f"property-management/{location}/index.html")
        
        # Also process the main property management index
        prop_index = os.path.join(prop_dir, 'index.html')
        if os.path.exists(prop_index):
            print(f"  Processing: property-management/index.html")
            if replace_footer(prop_index, '../'):
                total_success += 1
            else:
                all_failed.append("property-management/index.html")
    
    # 2. Process ALL service pages (9 service types)
    print("\n2. Processing Service Pages (9 types)...")
    services_dir = os.path.join(base_dir, 'services')
    service_types = [
        'administrative-services',
        'board-support', 
        'capital-project-management',
        'condominium-management',
        'financial-management',
        'hoa-management',
        'maintenance-coordination',
        'resident-relations',
        'townhome-management'
    ]
    
    for service in service_types:
        service_path = os.path.join(services_dir, service, 'index.html')
        if os.path.exists(service_path):
            print(f"  Processing: services/{service}/index.html")
            if replace_footer(service_path, '../../'):
                total_success += 1
            else:
                all_failed.append(f"services/{service}/index.html")
    
    # 3. Process main pages at root level
    print("\n3. Processing Root Level Pages...")
    root_pages = [
        'index.html',           # Home
        'services.html',        # Services main
        'contact.html',         # Contact
        'pay-dues.html',        # Pay Dues
        'payment-methods.html', # Payment Methods
        'forms.html',           # Forms & Documents
        'privacy-policy.html',  # Privacy Policy
        'terms-of-service.html',# Terms of Service
        'sitemap.html',         # Sitemap
        'accessibility.html',   # Accessibility
        'legal-disclaimers.html'# Legal Disclaimers
    ]
    
    for page in root_pages:
        page_path = os.path.join(base_dir, page)
        if os.path.exists(page_path):
            print(f"  Processing: {page}")
            if replace_footer(page_path, ''):
                total_success += 1
            else:
                all_failed.append(page)
        else:
            print(f"  [SKIP] {page} not found")
    
    # 4. Process ALL blog pages
    print("\n4. Processing Blog Pages...")
    blog_dir = os.path.join(base_dir, 'blog')
    if os.path.exists(blog_dir):
        for blog_file in os.listdir(blog_dir):
            if blog_file.endswith('.html'):
                blog_path = os.path.join(blog_dir, blog_file)
                print(f"  Processing: blog/{blog_file}")
                if replace_footer(blog_path, '../'):
                    total_success += 1
                else:
                    all_failed.append(f"blog/{blog_file}")
    
    # 5. Check for any other HTML files we might have missed
    print("\n5. Checking for additional HTML files...")
    # Check for any other directories with HTML files
    other_dirs = ['about', 'resources', 'testimonials', 'careers']
    for dir_name in other_dirs:
        dir_path = os.path.join(base_dir, dir_name)
        if os.path.exists(dir_path):
            if os.path.isdir(dir_path):
                for file in os.listdir(dir_path):
                    if file.endswith('.html'):
                        file_path = os.path.join(dir_path, file)
                        print(f"  Processing: {dir_name}/{file}")
                        if replace_footer(file_path, '../'):
                            total_success += 1
                        else:
                            all_failed.append(f"{dir_name}/{file}")
    
    print("\n" + "=" * 50)
    print(f"Process Complete!")
    print(f"Successfully updated: {total_success} pages")
    
    if all_failed:
        print(f"\nFailed to update {len(all_failed)} pages:")
        for f in all_failed:
            print(f"  - {f}")
    
    print(f"\nTotal pages processed: {total_success + len(all_failed)}")

if __name__ == "__main__":
    main()