import os
import re

def update_footer_in_file(filepath):
    """Update the footer in a single HTML file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file has a footer
        if '<footer' not in content.lower():
            return False
            
        # New footer HTML with updated certifications and colors
        new_footer = '''    <!-- Footer -->
    <footer style="background: #2C3E50; color: #e5e7eb; padding: 1.5rem 0; margin-top: 2rem;">
        <div style="max-width: 1200px; margin: 0 auto; padding: 0 2rem;">
            <div style="display: grid; grid-template-columns: 2fr 1fr 1fr 1fr 1.5fr; gap: 2rem; align-items: start;">
                <!-- Company Info -->
                <div>
                    <h3 style="font-size: 1.1rem; margin: 0 0 0.3rem 0; color: #F4A261; font-weight: 600;">MANAGE369</h3>
                    <p style="font-size: 0.85rem; margin: 0; line-height: 1.3; color: #e5e7eb;">
                        1400 Patriot Blvd #357, Glenview, IL<br>
                        📱 Text: <a href="sms:8476522338" style="color: #60a5fa; text-decoration: none;">(847) 652-2338</a><br>
                        <a href="mailto:service@manage369.com" style="color: #60a5fa; text-decoration: none;">service@manage369.com</a>
                    </p>
                </div>
                
                <!-- Services -->
                <div>
                    <h4 style="font-size: 0.9rem; margin: 0 0 0.3rem 0; color: #F4A261; font-weight: 600;">Services</h4>
                    <div style="font-size: 0.8rem; line-height: 1.3;">
                        <a href="/services/condominium-management/" style="color: #e5e7eb; text-decoration: none; display: block; padding: 2px 0;">Condominium</a>
                        <a href="/services/hoa-management/" style="color: #e5e7eb; text-decoration: none; display: block; padding: 2px 0;">HOA</a>
                        <a href="/services/townhome-management/" style="color: #e5e7eb; text-decoration: none; display: block; padding: 2px 0;">Townhome</a>
                        <a href="/services/financial-management/" style="color: #e5e7eb; text-decoration: none; display: block; padding: 2px 0;">Financial</a>
                        <a href="/services/maintenance-coordination/" style="color: #e5e7eb; text-decoration: none; display: block; padding: 2px 0;">Maintenance</a>
                        <a href="/services/board-support/" style="color: #e5e7eb; text-decoration: none; display: block; padding: 2px 0;">Board Support</a>
                    </div>
                </div>
                
                <!-- Quick Links -->
                <div>
                    <h4 style="font-size: 0.9rem; margin: 0 0 0.3rem 0; color: #F4A261; font-weight: 600;">Quick Links</h4>
                    <div style="font-size: 0.8rem; line-height: 1.3;">
                        <a href="/property-management/" style="color: #e5e7eb; text-decoration: none; display: block; padding: 2px 0;">Areas We Serve</a>
                        <a href="/contact.html" style="color: #e5e7eb; text-decoration: none; display: block; padding: 2px 0;">Contact</a>
                        <a href="/forms.html" style="color: #e5e7eb; text-decoration: none; display: block; padding: 2px 0;">Forms</a>
                        <a href="/payment-methods.html" style="color: #e5e7eb; text-decoration: none; display: block; padding: 2px 0;">Pay Dues</a>
                        <a href="/blog/" style="color: #e5e7eb; text-decoration: none; display: block; padding: 2px 0;">Blog</a>
                        <a href="/sitemap.html" style="color: #e5e7eb; text-decoration: none; display: block; padding: 2px 0;">Sitemap</a>
                    </div>
                </div>
                
                <!-- Resources -->
                <div>
                    <h4 style="font-size: 0.9rem; margin: 0 0 0.3rem 0; color: #F4A261; font-weight: 600;">Resources</h4>
                    <div style="font-size: 0.8rem; line-height: 1.3;">
                        <a href="/legal-disclaimers.html" style="color: #e5e7eb; text-decoration: none; display: block; padding: 2px 0;">Legal</a>
                        <a href="/privacy-policy.html" style="color: #e5e7eb; text-decoration: none; display: block; padding: 2px 0;">Privacy</a>
                        <a href="/terms-of-service.html" style="color: #e5e7eb; text-decoration: none; display: block; padding: 2px 0;">Terms</a>
                        <a href="/accessibility.html" style="color: #e5e7eb; text-decoration: none; display: block; padding: 2px 0;">Accessibility</a>
                        <a href="/leave-review.html" style="color: #e5e7eb; text-decoration: none; display: block; padding: 2px 0;">Leave Review</a>
                    </div>
                </div>
                
                <!-- Certifications & Copyright -->
                <div style="text-align: right;">
                    <div style="font-size: 0.75rem; color: #F4A261; line-height: 1.4; margin-bottom: 0.5rem;">
                        CAI National Member<br>
                        AMS<br>
                        CMCA<br>
                        IDFPR Licensed<br>
                        License: 291.000211
                    </div>
                    <div style="font-size: 0.75rem; color: #6b7280; margin-top: 0.5rem; padding-top: 0.5rem; border-top: 1px solid #374151;">
                        © 2025 Manage369<br>
                        All rights reserved
                    </div>
                </div>
            </div>
        </div>
    </footer>'''
        
        # For files in subdirectories, adjust the paths
        if '/property-management/' in filepath or '/services/' in filepath or '/blog/' in filepath:
            # These are already in subdirectories, paths are correct
            pass
        else:
            # Root level files need relative paths
            new_footer = new_footer.replace('href="/', 'href="')
        
        # Replace the existing footer
        # Match from <footer to </footer> including all content between
        footer_pattern = r'<footer[^>]*>.*?</footer>'
        
        if re.search(footer_pattern, content, re.DOTALL | re.IGNORECASE):
            new_content = re.sub(footer_pattern, new_footer, content, flags=re.DOTALL | re.IGNORECASE)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    """Update all HTML files with the new footer"""
    root_dir = r'C:\Users\mirsa\manage369-live'
    updated_files = []
    skipped_files = []
    error_files = []
    
    # Files to skip (templates, tests, etc.)
    skip_files = [
        'compact-footer-template.html',
        'google496518917.html',
        'manage369-crossref-snippet.html',
        'manage369-menu.html',
        'offline.html',
        'test-image.html'
    ]
    
    # Walk through all directories
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip .git and other hidden directories
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        
        for filename in filenames:
            if filename.endswith('.html'):
                if filename in skip_files:
                    skipped_files.append(filename)
                    continue
                    
                filepath = os.path.join(dirpath, filename)
                
                if update_footer_in_file(filepath):
                    updated_files.append(filepath)
                    print(f"[OK] Updated: {filepath}")
                else:
                    error_files.append(filepath)
    
    # Summary
    print("\n" + "="*60)
    print(f"FOOTER UPDATE COMPLETE")
    print(f"Updated: {len(updated_files)} files")
    print(f"Skipped: {len(skipped_files)} utility files")
    if error_files:
        print(f"Errors: {len(error_files)} files")
        for f in error_files:
            print(f"  - {f}")
    print("="*60)

if __name__ == "__main__":
    main()