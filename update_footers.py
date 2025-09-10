#!/usr/bin/env python3
"""
Script to update footers in all property management area files.
"""

import os
import re

# Define the old footer pattern (from the start comment to the end of footer tag)
OLD_FOOTER_PATTERN = r'<!-- PERFECT FOOTER HTML - EXACT SPECIFICATIONS -->.*?</footer>'

# Define the new footer HTML
NEW_FOOTER = '''    <!-- Footer -->
    <footer style="background: #1f2937; color: #e5e7eb; padding: 1.5rem 0; margin-top: 2rem;">
        <div style="max-width: 1200px; margin: 0 auto; padding: 0 2rem;">
            <div style="display: grid; grid-template-columns: 2fr 1fr 1fr 1fr 1.5fr; gap: 2rem; align-items: start;">
                <!-- Company Info -->
                <div>
                    <h3 style="font-size: 1.1rem; margin: 0 0 0.3rem 0; color: #ffffff; font-weight: 600;">MANAGE369</h3>
                    <p style="font-size: 0.85rem; margin: 0; line-height: 1.3; color: #e5e7eb;">
                        1400 Patriot Blvd #357, Glenview, IL<br>
                        📱 Text: <a href="sms:8476522338" style="color: #60a5fa; text-decoration: none;">(847) 652-2338</a><br>
                        <a href="mailto:service@manage369.com" style="color: #60a5fa; text-decoration: none;">service@manage369.com</a><br>
                        <span style="font-size: 0.8rem; color: #9ca3af;">License: 291.000211</span>
                    </p>
                </div>
                
                <!-- Services -->
                <div>
                    <h4 style="font-size: 0.9rem; margin: 0 0 0.3rem 0; color: #fbbf24; font-weight: 600;">Services</h4>
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
                    <h4 style="font-size: 0.9rem; margin: 0 0 0.3rem 0; color: #fbbf24; font-weight: 600;">Quick Links</h4>
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
                    <h4 style="font-size: 0.9rem; margin: 0 0 0.3rem 0; color: #fbbf24; font-weight: 600;">Resources</h4>
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
                    <div style="font-size: 0.75rem; color: #9ca3af; line-height: 1.3; margin-bottom: 0.5rem;">
                        CAI National Member<br>
                        IREM Certified<br>
                        CCIM Designated<br>
                        NAR Member
                    </div>
                    <div style="font-size: 0.8rem; color: #6b7280; margin-top: 0.5rem;">
                        © 2025 Manage369
                    </div>
                </div>
            </div>
        </div>
    </footer>'''

def update_footer_in_file(file_path):
    """Update the footer in a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the footer using regex with DOTALL flag to match across newlines
        updated_content = re.sub(OLD_FOOTER_PATTERN, NEW_FOOTER, content, flags=re.DOTALL)
        
        if updated_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"✓ Updated: {file_path}")
            return True
        else:
            print(f"⚠ No changes needed: {file_path}")
            return False
    except Exception as e:
        print(f"✗ Error updating {file_path}: {e}")
        return False

def main():
    """Main function to update all property management area files."""
    property_mgmt_dir = "property-management"
    
    # Get all area directories (exclude main index.html)
    area_dirs = [d for d in os.listdir(property_mgmt_dir) 
                 if os.path.isdir(os.path.join(property_mgmt_dir, d))]
    
    updated_count = 0
    total_files = 0
    
    for area_dir in sorted(area_dirs):
        index_file = os.path.join(property_mgmt_dir, area_dir, "index.html")
        if os.path.exists(index_file):
            total_files += 1
            if update_footer_in_file(index_file):
                updated_count += 1
    
    print(f"\nSummary:")
    print(f"Total files processed: {total_files}")
    print(f"Files updated: {updated_count}")
    print(f"Files skipped: {total_files - updated_count}")

if __name__ == "__main__":
    main()