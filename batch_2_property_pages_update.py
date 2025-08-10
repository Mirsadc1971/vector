#!/usr/bin/env python3
"""
Batch 2 Property Management Pages Update Script
Updates property management pages to match Norridge structure
"""

import os
import re
from pathlib import Path

# Batch 2 locations to process
BATCH_2_LOCATIONS = [
    'hyde-park', 'itasca', 'jefferson-park', 'lake-bluff', 'lake-forest',
    'lakeview', 'lincoln-park', 'lincoln-square', 'lincolnshire', 'lincolnwood',
    'logan-square', 'loop', 'mayfair', 'morton-grove', 'mount-prospect',
    'north-park', 'northbrook', 'northfield', 'norwood-park', 'oak-park',
    'old-irving-park', 'old-town', 'park-ridge'
]

BASE_PATH = Path('C:/Users/mirsa/manage369-live/property-management')

# Consultation form HTML template
CONSULTATION_FORM = '''
    <!-- Consultation Form Section -->
    <section class="consultation-section" style="background: #f8f9fa; padding: 4rem 2rem; margin: 4rem 0 0 0;">
        <div class="consultation-content" style="max-width: 1000px; margin: 0 auto;">
            <h2 style="color: #4a90e2; margin-bottom: 2rem; text-align: center; font-size: 2.5rem;">Schedule Your Professional Consultation</h2>
            <p style="text-align: center; color: #666; margin-bottom: 3rem; font-size: 1.1rem; line-height: 1.7;">Connect with our locally-established team to explore how our 18+ years of North Shore expertise can benefit your community.</p>
            
            <div class="consultation-form" style="background: white; padding: 3rem; border-radius: 1rem; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
                <form action="mailto:service@manage369.com" method="post" enctype="text/plain">
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.5rem;">
                        <div style="margin-bottom: 1.5rem;">
                            <label for="first-name" style="display: block; margin-bottom: 0.5rem; font-weight: 600; color: #333;">First Name *</label>
                            <input type="text" id="first-name" name="first-name" required style="width: 100%; padding: 1rem; border: 2px solid #e5e7eb; border-radius: 0.5rem; font-size: 1rem;">
                        </div>
                        
                        <div style="margin-bottom: 1.5rem;">
                            <label for="last-name" style="display: block; margin-bottom: 0.5rem; font-weight: 600; color: #333;">Last Name *</label>
                            <input type="text" id="last-name" name="last-name" required style="width: 100%; padding: 1rem; border: 2px solid #e5e7eb; border-radius: 0.5rem; font-size: 1rem;">
                        </div>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.5rem;">
                        <div style="margin-bottom: 1.5rem;">
                            <label for="email" style="display: block; margin-bottom: 0.5rem; font-weight: 600; color: #333;">Email Address *</label>
                            <input type="email" id="email" name="email" required style="width: 100%; padding: 1rem; border: 2px solid #e5e7eb; border-radius: 0.5rem; font-size: 1rem;">
                        </div>
                        
                        <div style="margin-bottom: 1.5rem;">
                            <label for="phone-consult" style="display: block; margin-bottom: 0.5rem; font-weight: 600; color: #333;">Phone Number *</label>
                            <input type="tel" id="phone-consult" name="phone" required style="width: 100%; padding: 1rem; border: 2px solid #e5e7eb; border-radius: 0.5rem; font-size: 1rem;">
                        </div>
                    </div>
                    
                    <div style="margin-bottom: 1.5rem;">
                        <label for="property-type" style="display: block; margin-bottom: 0.5rem; font-weight: 600; color: #333;">Property Type *</label>
                        <select id="property-type" name="property-type" required style="width: 100%; padding: 1rem; border: 2px solid #e5e7eb; border-radius: 0.5rem; font-size: 1rem;">
                            <option value="">Select Property Type</option>
                            <option value="condominium">Condominium Association</option>
                            <option value="hoa">Homeowners Association (HOA)</option>
                            <option value="townhome">Townhome Community</option>
                            <option value="mixed-use">Mixed-Use Property</option>
                        </select>
                    </div>
                    
                    <div style="margin-bottom: 1.5rem;">
                        <label for="services" style="display: block; margin-bottom: 0.5rem; font-weight: 600; color: #333;">Services Needed</label>
                        <select id="services" name="services" style="width: 100%; padding: 1rem; border: 2px solid #e5e7eb; border-radius: 0.5rem; font-size: 1rem;">
                            <option value="">Select Primary Service</option>
                            <option value="full-management">Full Property Management</option>
                            <option value="financial-only">Financial Management Only</option>
                            <option value="consulting">Consulting Services</option>
                            <option value="maintenance-coordination">Maintenance Coordination</option>
                        </select>
                    </div>
                    
                    <div style="margin-bottom: 1.5rem;">
                        <label for="message" style="display: block; margin-bottom: 0.5rem; font-weight: 600; color: #333;">How Can We Serve Your Community? *</label>
                        <textarea id="message" name="message" rows="5" placeholder="Share your community's goals, current management situation, or specific areas where our expertise could benefit your property..." required style="width: 100%; padding: 1rem; border: 2px solid #e5e7eb; border-radius: 0.5rem; font-size: 1rem; resize: vertical;"></textarea>
                    </div>
                    
                    <button type="submit" style="width: 100%; background: #ff9500; color: white; padding: 1rem; border: none; border-radius: 0.5rem; font-size: 1.1rem; font-weight: 600; cursor: pointer; transition: all 0.3s;">Request Professional Consultation</button>
                </form>
            </div>
        </div>
    </section>
'''

def get_norridge_template():
    """Read the Norridge template file"""
    norridge_path = BASE_PATH / 'norridge' / 'index.html'
    if not norridge_path.exists():
        raise FileNotFoundError(f"Norridge template not found at {norridge_path}")
    
    with open(norridge_path, 'r', encoding='utf-8') as f:
        return f.read()

def update_location_page(location, norridge_content):
    """Update a specific location page to match Norridge structure"""
    location_path = BASE_PATH / location / 'index.html'
    
    if not location_path.exists():
        print(f"Warning: {location_path} does not exist")
        return
    
    print(f"Processing {location}...")
    
    # Read existing content
    with open(location_path, 'r', encoding='utf-8') as f:
        current_content = f.read()
    
    # Extract key information from current page
    location_display = location.replace('-', ' ').title()
    
    # Create new content based on Norridge template
    updated_content = norridge_content
    
    # Update location-specific content
    updated_content = updated_content.replace('Norridge', location_display)
    updated_content = updated_content.replace('norridge', location)
    
    # Update meta tags
    updated_content = re.sub(
        r'<title>.*?</title>',
        f'<title>{location_display} Property Management | Chicago Condo & HOA Management | Manage369</title>',
        updated_content
    )
    
    updated_content = re.sub(
        r'<meta name="description" content=".*?">',
        f'<meta name="description" content="Premier {location_display} property management services. 18+ years managing luxury condos, HOAs & townhomes. CAI/IREM certified professionals. Call (847) 652-2338.">',
        updated_content
    )
    
    # Update Open Graph
    updated_content = re.sub(
        r'<meta property="og:title" content=".*?">',
        f'<meta property="og:title" content="{location_display} Property Management | Manage369">',
        updated_content
    )
    
    updated_content = re.sub(
        r'<meta property="og:url" content=".*?">',
        f'<meta property="og:url" content="https://manage369.com/property-management/{location}/">',
        updated_content
    )
    
    updated_content = re.sub(
        r'<meta property="og:description" content=".*?">',
        f'<meta property="og:description" content="Premier {location_display} property management services. 18+ years managing luxury condos, HOAs & townhomes. CAI/IREM certified professionals.">',
        updated_content
    )
    
    # Update Twitter tags
    updated_content = re.sub(
        r'<meta name="twitter:title" content=".*?">',
        f'<meta name="twitter:title" content="{location_display} Property Management | Manage369">',
        updated_content
    )
    
    updated_content = re.sub(
        r'<meta name="twitter:description" content=".*?">',
        f'<meta name="twitter:description" content="Premier {location_display} property management services. 18+ years managing luxury condos, HOAs & townhomes.">',
        updated_content
    )
    
    # Update schema markup
    updated_content = re.sub(
        r'"name": "Manage369"',
        f'"name": "Manage369"',
        updated_content
    )
    
    updated_content = re.sub(
        r'"description": "Premier.*?",',
        f'"description": "Premier {location_display} property management services. 18+ years managing luxury condos, HOAs & townhomes. CAI/IREM certified professionals.",',
        updated_content
    )
    
    updated_content = re.sub(
        r'"url": "https://manage369\.com/property-management/.*?"',
        f'"url": "https://manage369.com/property-management/{location}/"',
        updated_content
    )
    
    updated_content = re.sub(
        r'"name": ".*?, Illinois"',
        f'"name": "{location_display}, Illinois"',
        updated_content
    )
    
    # Update hero section
    updated_content = re.sub(
        r'<h1>Property Management.*?</h1>',
        f'<h1>Property Management {location_display} - Manage369</h1>',
        updated_content
    )
    
    # Fix phone button class (change phone-button to phone)
    updated_content = re.sub(
        r'class="phone-button"',
        'class="phone"',
        updated_content
    )
    
    # Ensure services dropdown is present in navigation
    services_dropdown = '''<div class="services-dropdown">
                <a href="../../services.html">Services <span>▼</span></a>
                <div class="dropdown-content">
                    <div class="dropdown-header">Property Types</div>
                    <a href="../../services/condominium-management/index.html">Condominium Management</a>
                    <a href="../../services/hoa-management/index.html">HOA Management</a>
                    <a href="../../services/townhome-management/index.html">Townhome Management</a>
                    <div class="dropdown-header">Service Offerings</div>
                    <a href="../../services/financial-management/index.html">Financial Management</a>
                    <a href="../../services/maintenance-coordination/index.html">Maintenance Coordination</a>
                    <a href="../../services/board-support/index.html">Board Support</a>
                    <a href="../../services/administrative-services/index.html">Administrative Services</a>
                    <a href="../../services/capital-project-management/index.html">Capital Project Management</a>
                    <a href="../../services/resident-relations/index.html">Resident Relations</a>
                </div>
            </div>'''
    
    # Replace simple services link with dropdown
    updated_content = re.sub(
        r'<a href="../../services\.html">Services</a>',
        services_dropdown,
        updated_content
    )
    
    # Add consultation form before footer if not already present
    if 'consultation-section' not in updated_content:
        # Find footer and insert consultation form before it
        footer_pattern = r'(<footer>|<!-- PERFECT FOOTER HTML)'
        if re.search(footer_pattern, updated_content):
            updated_content = re.sub(
                footer_pattern,
                CONSULTATION_FORM + r'\n    \1',
                updated_content
            )
    
    # Remove any style attributes (inline styles)
    updated_content = re.sub(r'\s*style="[^"]*"', '', updated_content)
    
    # Write updated content
    with open(location_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"Updated {location}")

def main():
    """Main function to process all batch 2 locations"""
    print("Starting Batch 2 Property Management Pages Update")
    print(f"Processing {len(BATCH_2_LOCATIONS)} locations...")
    
    try:
        # Get Norridge template
        print("Reading Norridge template...")
        norridge_content = get_norridge_template()
        
        # Process each location
        success_count = 0
        for location in BATCH_2_LOCATIONS:
            try:
                update_location_page(location, norridge_content)
                success_count += 1
            except Exception as e:
                print(f"Error processing {location}: {str(e)}")
        
        print(f"\nBatch 2 processing complete!")
        print(f"Successfully updated: {success_count}/{len(BATCH_2_LOCATIONS)} pages")
        
        if success_count < len(BATCH_2_LOCATIONS):
            print(f"Some pages had issues - please review the output above")
        
        print("\nUpdates made to each page:")
        print("   - Matched Norridge page structure and word count")
        print("   - Added consultation form before footer")  
        print("   - Fixed service links with dropdown navigation")
        print("   - Fixed phone button positioning (phone class)")
        print("   - Removed inline styles")
        print("   - Updated meta tags and schema markup")
        
    except Exception as e:
        print(f"Fatal error: {str(e)}")

if __name__ == '__main__':
    main()