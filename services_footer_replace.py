#!/usr/bin/env python3
import os
import glob
import re

# Define the new footer
new_footer = '''<!-- Footer -->
<footer style="background: #2C3E50; color: #e5e7eb; padding: 1.5rem 0; margin-top: 2rem;">
    <div style="max-width: 1200px; margin: 0 auto; padding: 0 2rem;">
        <div style="display: grid; grid-template-columns: 2fr 1fr 1fr 1fr 1.5fr; gap: 2rem; align-items: start;">
            <!-- Company Info -->
            <div>
                <h3 style="font-size: 1.1rem; margin: 0 0 0.3rem 0; color: #F1C40F; font-weight: 600;">MANAGE369</h3>
                <p style="font-size: 0.85rem; margin: 0; line-height: 1.3; color: #e5e7eb;">
                    1400 Patriot Blvd #357, Glenview, IL<br>
                    📱 Text: <a href="sms:8476522338" style="color: #60a5fa; text-decoration: none;">(847) 652-2338</a><br>
                    <a href="mailto:service@manage369.com" style="color: #60a5fa; text-decoration: none;">service@manage369.com</a><br>
                    <span style="font-size: 0.8rem; color: #9ca3af;">License: 291.000211</span>
                </p>
            </div>
            
            <!-- Services -->
            <div>
                <h4 style="font-size: 0.9rem; margin: 0 0 0.3rem 0; color: #F1C40F; font-weight: 600;">Services</h4>
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
                <h4 style="font-size: 0.9rem; margin: 0 0 0.3rem 0; color: #F1C40F; font-weight: 600;">Quick Links</h4>
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
                <h4 style="font-size: 0.9rem; margin: 0 0 0.3rem 0; color: #F1C40F; font-weight: 600;">Resources</h4>
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
                <div style="font-size: 0.75rem; color: #F1C40F; line-height: 1.4; margin-bottom: 0.5rem;">
                    CAI National Member<br>
                    IREM Certified<br>
                    CCIM Designated<br>
                    NAR Member<br>
                    IDFPR Licensed
                </div>
                <div style="font-size: 0.75rem; color: #6b7280; margin-top: 0.5rem; padding-top: 0.5rem; border-top: 1px solid #374151;">
                    © 2025 Manage369<br>
                    All rights reserved
                </div>
            </div>
        </div>
    </div>
</footer>'''

def replace_footer_in_file(filepath):
    """Replace any existing footer with the new footer."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if it already has the new footer
        if 'background: #2C3E50' in content:
            print(f"Skipping {filepath} (already has new footer)")
            return False
        
        # Try multiple footer patterns and replace them
        footer_patterns = [
            # Pattern 1: Simple footer tags
            r'<footer[^>]*>.*?</footer>',
            # Pattern 2: Footer with class
            r'<footer\s+class="[^"]*"[^>]*>.*?</footer>',
        ]
        
        updated = False
        for pattern in footer_patterns:
            if re.search(pattern, content, re.DOTALL | re.MULTILINE):
                new_content = re.sub(pattern, new_footer, content, flags=re.DOTALL | re.MULTILINE)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated {filepath}")
                updated = True
                break
        
        if not updated:
            print(f"No footer pattern found in {filepath}")
        
        return updated
            
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    # Focus on services directory and other important subdirectories
    services_pattern = "services/**/index.html"
    other_patterns = [
        "service-areas/**/index.html",
        "admin/index.html"
    ]
    
    files_to_update = []
    
    # Get services files
    services_files = glob.glob(services_pattern, recursive=True)
    files_to_update.extend(services_files)
    
    # Get other subdirectory files
    for pattern in other_patterns:
        files_to_update.extend(glob.glob(pattern, recursive=True))
    
    # Filter out files that already have the new footer
    final_files = []
    for filepath in files_to_update:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            if 'background: #2C3E50' not in content and '<footer' in content:
                final_files.append(filepath)
        except Exception as e:
            print(f"Error checking {filepath}: {e}")
    
    print(f"Found {len(final_files)} subdirectory HTML files to update")
    for f in final_files:
        print(f"  - {f}")
    
    updated_count = 0
    for filepath in final_files:
        if replace_footer_in_file(filepath):
            updated_count += 1
    
    print(f"Updated {updated_count} files")

if __name__ == "__main__":
    main()