#!/usr/bin/env python3
"""
Fix contact forms on all 68 property pages
Ensures all pages have a properly styled contact form above the footer
"""

import os
import re
from pathlib import Path

# Standard contact form HTML to add to pages
CONTACT_FORM_HTML = """
<!-- Property Management Consultation Form Section -->
<section class="consultation-form-section">
    <div class="consultation-container">
        <div class="consultation-header">
            <h2>Get Your Free Property Management Consultation</h2>
            <p>Ready to experience professional property management excellence? Contact us today for a personalized consultation tailored to your community's unique needs.</p>
        </div>
        
        <form class="consultation-form" action="#" method="POST">
            <div class="form-grid">
                <div class="form-row">
                    <div class="form-group">
                        <label for="name">Full Name *</label>
                        <input type="text" id="name" name="name" required placeholder="Enter your full name">
                    </div>
                    <div class="form-group">
                        <label for="email">Email Address *</label>
                        <input type="email" id="email" name="email" required placeholder="your.email@example.com">
                    </div>
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label for="phone">Phone Number *</label>
                        <input type="tel" id="phone" name="phone" required placeholder="(847) 652-2338">
                    </div>
                    <div class="form-group">
                        <label for="property-address">Property Address</label>
                        <input type="text" id="property-address" name="property-address" placeholder="123 Main Street, Chicago, IL">
                    </div>
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label for="property-type">Property Type *</label>
                        <select id="property-type" name="property-type" required>
                            <option value="">Select Property Type</option>
                            <option value="condominium">Condominium Association</option>
                            <option value="hoa">Homeowners Association</option>
                            <option value="townhome">Townhome Community</option>
                            <option value="coop">Cooperative Building</option>
                            <option value="mixed-use">Mixed-Use Development</option>
                            <option value="commercial">Commercial Property</option>
                            <option value="other">Other</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="units">Number of Units</label>
                        <input type="number" id="units" name="units" min="1" placeholder="e.g., 25">
                    </div>
                </div>
                
                <div class="form-group full-width">
                    <label for="message">Tell Us About Your Property Management Needs</label>
                    <textarea id="message" name="message" rows="4" placeholder="Describe your current challenges, goals, or specific services you're interested in..."></textarea>
                </div>
                
                <div class="form-actions">
                    <button type="submit" class="consultation-submit-btn">
                        <span>Request Free Consultation</span>
                        <span class="btn-icon">→</span>
                    </button>
                </div>
            </div>
        </form>
        
        <div class="consultation-footer">
            <p class="consultation-note">
                <strong>Quick Response Guarantee:</strong> We'll contact you within 24 hours to schedule your free consultation.
            </p>
            <div class="consultation-contact">
                <p>Prefer to speak directly? Call us at <a href="tel:8476522338"><strong>(847) 652-2338</strong></a></p>
            </div>
        </div>
    </div>
</section>
"""

def check_page_for_form(content):
    """Check if page has a consultation form"""
    # Check for various form indicators
    has_form = any([
        'consultation-form-section' in content,
        'consultation-form' in content,
        'Get Your Free Property Management Consultation' in content,
        'Schedule Your Free' in content and 'Consultation' in content
    ])
    return has_form

def fix_page_css_links(content):
    """Ensure page has correct CSS links"""
    # Check if page has the master CSS
    if 'property-pages-master.css' not in content:
        # Add master CSS after styles.css
        if '<link rel="stylesheet" href="../../css/styles.css">' in content:
            content = content.replace(
                '<link rel="stylesheet" href="../../css/styles.css">',
                '<link rel="stylesheet" href="../../css/styles.css">\n    <link rel="stylesheet" href="../../css/property-pages-master.css">'
            )
        elif '</head>' in content:
            # Add before closing head tag
            content = content.replace(
                '</head>',
                '    <link rel="stylesheet" href="../../css/styles.css">\n    <link rel="stylesheet" href="../../css/property-pages-master.css">\n</head>'
            )
    
    return content

def add_contact_form(content, location_name):
    """Add contact form before footer"""
    # Customize the form for the location
    custom_form = CONTACT_FORM_HTML.replace(
        'placeholder="123 Main Street, Chicago, IL"',
        f'placeholder="123 Main Street, {location_name.replace("-", " ").title()}, IL"'
    )
    
    # Find where to insert the form (before footer)
    footer_patterns = [
        r'<footer[^>]*>',
        r'<!-- PERFECT FOOTER',
        r'<!--\s*Footer\s*-->',
        r'<div class="footer'
    ]
    
    inserted = False
    for pattern in footer_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            content = re.sub(
                pattern,
                custom_form + '\n\n' + r'\g<0>',
                content,
                count=1,
                flags=re.IGNORECASE
            )
            inserted = True
            break
    
    if not inserted:
        # If no footer found, add before closing body tag
        content = content.replace('</body>', custom_form + '\n\n</body>')
    
    return content

def remove_duplicate_forms(content):
    """Remove duplicate consultation forms if they exist"""
    # Count occurrences
    form_count = content.count('consultation-form-section')
    
    if form_count > 1:
        # Keep only the last one (closest to footer)
        parts = content.split('<!-- Property Management Consultation Form Section -->')
        if len(parts) > 2:
            # Reconstruct with only the last form
            content = parts[0] + '<!-- Property Management Consultation Form Section -->' + parts[-1]
    
    return content

def fix_malformed_forms(content):
    """Fix forms that display as text instead of HTML"""
    # Fix common issues with forms displaying as text
    patterns_to_fix = [
        # Fix escaped HTML
        (r'&lt;form', '<form'),
        (r'&lt;/form&gt;', '</form>'),
        (r'&lt;input', '<input'),
        (r'&lt;select', '<select'),
        (r'&lt;/select&gt;', '</select>'),
        (r'&lt;option', '<option'),
        (r'&lt;/option&gt;', '</option>'),
        (r'&lt;textarea', '<textarea'),
        (r'&lt;/textarea&gt;', '</textarea>'),
        (r'&lt;button', '<button'),
        (r'&lt;/button&gt;', '</button>'),
        (r'&lt;label', '<label'),
        (r'&lt;/label&gt;', '</label>'),
        (r'&lt;div', '<div'),
        (r'&lt;/div&gt;', '</div>'),
        (r'&gt;', '>'),
        (r'&quot;', '"'),
    ]
    
    for pattern, replacement in patterns_to_fix:
        content = content.replace(pattern, replacement)
    
    return content

def process_page(file_path, location_name):
    """Process a single property page"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes_made = []
    
    # 1. Fix CSS links
    new_content = fix_page_css_links(content)
    if new_content != content:
        changes_made.append("Added master CSS")
        content = new_content
    
    # 2. Fix malformed forms
    new_content = fix_malformed_forms(content)
    if new_content != content:
        changes_made.append("Fixed malformed HTML")
        content = new_content
    
    # 3. Check for form
    has_form = check_page_for_form(content)
    
    if not has_form:
        # Add the form
        content = add_contact_form(content, location_name)
        changes_made.append("Added contact form")
    else:
        # Remove duplicates if any
        new_content = remove_duplicate_forms(content)
        if new_content != content:
            changes_made.append("Removed duplicate forms")
            content = new_content
    
    # Save if changes were made
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, changes_made
    
    return False, []

def main():
    """Main function to fix all property pages"""
    print("Fixing contact forms on all property pages...")
    print("=" * 50)
    
    # Path to property-management directory
    prop_mgmt_dir = Path('property-management')
    
    if not prop_mgmt_dir.exists():
        print("Error: property-management directory not found!")
        return
    
    # Get all location directories
    locations = [d for d in prop_mgmt_dir.iterdir() if d.is_dir()]
    
    fixed_count = 0
    total_count = 0
    issues = []
    
    print(f"Processing {len(locations)} locations...")
    print("-" * 50)
    
    for location_dir in sorted(locations):
        index_file = location_dir / 'index.html'
        
        if index_file.exists():
            total_count += 1
            location_name = location_dir.name
            
            print(f"\nProcessing: {location_name}")
            success, changes = process_page(index_file, location_name)
            
            if success:
                fixed_count += 1
                print(f"  [FIXED] Changes: {', '.join(changes)}")
            else:
                print(f"  [OK] No changes needed")
        else:
            issues.append(f"No index.html in {location_dir.name}")
    
    print("\n" + "=" * 50)
    print(f"Results:")
    print(f"  Total pages processed: {total_count}")
    print(f"  Pages fixed: {fixed_count}")
    print(f"  Pages already correct: {total_count - fixed_count}")
    
    if issues:
        print(f"\nIssues found:")
        for issue in issues:
            print(f"  - {issue}")
    
    print(f"\nAll {total_count} pages now have properly styled contact forms!")

if __name__ == "__main__":
    main()