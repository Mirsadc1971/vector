"""
Create comprehensive interlinking structure - 400+ internal links
Ensures proper link flow: Home -> Service Pages -> Area Pages -> Related Areas
"""

import os
import re
from collections import defaultdict

print("CREATING COMPREHENSIVE INTERLINKING STRUCTURE")
print("=" * 60)

# Define page hierarchy
HOME = 'index.html'
SERVICE_PAGES = [
    'services.html',
    'contact.html', 
    'forms.html',
    'payment-methods.html',
    'services/hoa-management/',
    'services/condominium-management/',
    'services/townhome-management/',
    'services/financial-management/',
    'services/maintenance-coordination/',
    'services/board-support/',
    'services/administrative-services/',
    'services/resident-relations/',
    'services/capital-project-management/'
]

# Get all property management areas
AREA_PAGES = []
prop_dir = 'C:\\Users\\mirsa\\manage369-live\\property-management'
for location in os.listdir(prop_dir):
    if os.path.isdir(os.path.join(prop_dir, location)):
        AREA_PAGES.append(f'property-management/{location}/')

# Define North Shore premium areas
NORTH_SHORE_PREMIUM = [
    'wilmette', 'winnetka', 'glencoe', 'highland-park', 'lake-forest',
    'kenilworth', 'northbrook', 'glenview', 'deerfield', 'lake-bluff'
]

# Define Chicago premium neighborhoods  
CHICAGO_PREMIUM = [
    'gold-coast', 'lincoln-park', 'river-north', 'loop', 'streeterville',
    'lakeview', 'old-town', 'west-loop', 'bucktown', 'wicker-park'
]

def add_related_areas_section(filepath, content):
    """Add related areas section to property pages"""
    
    # Get location from filepath
    location = filepath.split('\\')[-2] if 'property-management' in filepath else None
    if not location:
        return content
    
    # Determine related areas
    related_areas = []
    
    if location in NORTH_SHORE_PREMIUM:
        # Link to other North Shore areas
        related_areas = [a for a in NORTH_SHORE_PREMIUM if a != location][:5]
        section_title = "Other North Shore Communities We Serve"
    elif location in CHICAGO_PREMIUM:
        # Link to other Chicago neighborhoods
        related_areas = [a for a in CHICAGO_PREMIUM if a != location][:5]
        section_title = "Other Chicago Neighborhoods We Serve"
    else:
        # Mix of both
        related_areas = NORTH_SHORE_PREMIUM[:3] + CHICAGO_PREMIUM[:2]
        section_title = "Popular Areas We Serve"
    
    # Create HTML for related areas
    related_html = f'''
    <!-- Related Areas Section -->
    <section style="background: #f8f9fa; padding: 3rem 2rem; margin-top: 3rem;">
        <div style="max-width: 1200px; margin: 0 auto;">
            <h2 style="text-align: center; color: #1e40af; margin-bottom: 2rem;">{section_title}</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
'''
    
    for area in related_areas:
        area_name = area.replace('-', ' ').title()
        related_html += f'''                <a href="../{area}/" style="background: white; padding: 1.5rem; text-align: center; text-decoration: none; color: #1e40af; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); transition: all 0.3s;">
                    <h3 style="margin: 0; font-size: 1.1rem;">{area_name}</h3>
                    <p style="margin: 0.5rem 0 0 0; color: #666; font-size: 0.9rem;">Property Management</p>
                </a>
'''
    
    related_html += '''            </div>
        </div>
    </section>
'''
    
    # Add before footer
    if '</footer>' in content:
        content = content.replace('</footer>', related_html + '</footer>')
    
    return content

def add_service_links_section(filepath, content):
    """Add service links section to all pages"""
    
    # Determine path prefix based on file location
    if 'property-management' in filepath and 'index.html' in filepath:
        prefix = '../../services/'
    elif 'blog' in filepath:
        prefix = '../services/'
    elif 'services' in filepath and 'index.html' in filepath:
        prefix = '../'
    else:
        prefix = 'services/'
    
    services_html = '''
    <!-- Our Services Section -->
    <section style="background: white; padding: 3rem 2rem;">
        <div style="max-width: 1200px; margin: 0 auto;">
            <h2 style="text-align: center; color: #1e40af; margin-bottom: 2rem;">Our Property Management Services</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem;">
                <a href="''' + prefix + '''hoa-management/" style="background: #f8f9fa; padding: 1.5rem; text-decoration: none; color: #333; border-radius: 8px; border-left: 4px solid #ff9500;">
                    <h3 style="color: #1e40af; margin: 0 0 0.5rem 0;">HOA Management</h3>
                    <p style="margin: 0; font-size: 0.9rem;">Complete homeowners association management services</p>
                </a>
                <a href="''' + prefix + '''condominium-management/" style="background: #f8f9fa; padding: 1.5rem; text-decoration: none; color: #333; border-radius: 8px; border-left: 4px solid #ff9500;">
                    <h3 style="color: #1e40af; margin: 0 0 0.5rem 0;">Condo Management</h3>
                    <p style="margin: 0; font-size: 0.9rem;">High-rise and mid-rise condominium expertise</p>
                </a>
                <a href="''' + prefix + '''financial-management/" style="background: #f8f9fa; padding: 1.5rem; text-decoration: none; color: #333; border-radius: 8px; border-left: 4px solid #ff9500;">
                    <h3 style="color: #1e40af; margin: 0 0 0.5rem 0;">Financial Management</h3>
                    <p style="margin: 0; font-size: 0.9rem;">Budget planning and financial reporting</p>
                </a>
            </div>
        </div>
    </section>
'''
    
    # Add before related areas or footer
    if '<!-- Related Areas Section -->' in content:
        content = content.replace('<!-- Related Areas Section -->', services_html + '<!-- Related Areas Section -->')
    elif '</footer>' in content:
        content = content.replace('</footer>', services_html + '</footer>')
    
    return content

def add_breadcrumb_navigation(filepath, content):
    """Add breadcrumb navigation to all pages"""
    
    # Skip if breadcrumbs already exist
    if 'breadcrumb' in content.lower():
        return content
    
    # Determine breadcrumb based on path
    if 'property-management' in filepath and 'index.html' in filepath:
        location = filepath.split('\\')[-2]
        location_name = location.replace('-', ' ').title()
        breadcrumb = f'''
    <nav style="padding: 1rem 2rem; background: #f8f9fa;">
        <div style="max-width: 1200px; margin: 0 auto;">
            <a href="../../" style="color: #666; text-decoration: none;">Home</a>
            <span style="color: #999; margin: 0 0.5rem;">›</span>
            <a href="../" style="color: #666; text-decoration: none;">Areas We Serve</a>
            <span style="color: #999; margin: 0 0.5rem;">›</span>
            <span style="color: #1e40af;">{location_name}</span>
        </div>
    </nav>
'''
    elif 'services' in filepath and 'index.html' in filepath:
        service = filepath.split('\\')[-2]
        service_name = service.replace('-', ' ').title()
        breadcrumb = f'''
    <nav style="padding: 1rem 2rem; background: #f8f9fa;">
        <div style="max-width: 1200px; margin: 0 auto;">
            <a href="../../" style="color: #666; text-decoration: none;">Home</a>
            <span style="color: #999; margin: 0 0.5rem;">›</span>
            <a href="../../services.html" style="color: #666; text-decoration: none;">Services</a>
            <span style="color: #999; margin: 0 0.5rem;">›</span>
            <span style="color: #1e40af;">{service_name}</span>
        </div>
    </nav>
'''
    else:
        return content
    
    # Add after header
    if '</header>' in content:
        content = content.replace('</header>', '</header>' + breadcrumb)
    
    return content

def add_contextual_links(content, filepath):
    """Add contextual links within content"""
    
    # Define keyword to link mappings
    keyword_links = {
        'HOA management': 'services/hoa-management/',
        'condominium management': 'services/condominium-management/',
        'property management services': 'services.html',
        'contact us': 'contact.html',
        'North Shore': 'property-management/wilmette/',
        'Chicago': 'property-management/gold-coast/',
        'financial management': 'services/financial-management/',
        'maintenance': 'services/maintenance-coordination/',
        'board support': 'services/board-support/'
    }
    
    # Add links for first occurrence of keywords
    for keyword, link in keyword_links.items():
        # Determine correct path based on current file location
        if 'property-management' in filepath:
            full_link = '../../' + link
        elif 'services' in filepath:
            full_link = '../../' + link
        else:
            full_link = link
        
        # Only link if not already linked
        if keyword in content and f'href="{full_link}"' not in content:
            # Replace first occurrence
            pattern = rf'\b{re.escape(keyword)}\b'
            replacement = f'<a href="{full_link}" style="color: #1e40af; text-decoration: underline;">{keyword}</a>'
            content = re.sub(pattern, replacement, content, count=1, flags=re.IGNORECASE)
    
    return content

def add_call_to_action_links(content, filepath):
    """Add call-to-action sections with links"""
    
    cta_html = '''
    <!-- Call to Action Section -->
    <section style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 3rem 2rem; margin-top: 3rem;">
        <div style="max-width: 800px; margin: 0 auto; text-align: center;">
            <h2 style="color: white; margin-bottom: 1rem;">Ready to Get Started?</h2>
            <p style="color: rgba(255,255,255,0.9); margin-bottom: 2rem;">Join 50+ properties that trust Manage369 for professional management</p>
            <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
                <a href="../../contact.html" style="background: white; color: #667eea; padding: 1rem 2rem; text-decoration: none; border-radius: 5px; font-weight: bold;">Get Free Consultation</a>
                <a href="../../services.html" style="background: transparent; color: white; padding: 1rem 2rem; text-decoration: none; border-radius: 5px; font-weight: bold; border: 2px solid white;">View All Services</a>
                <a href="tel:8476522338" style="background: #ff9500; color: white; padding: 1rem 2rem; text-decoration: none; border-radius: 5px; font-weight: bold;">Call (847) 652-2338</a>
            </div>
        </div>
    </section>
'''
    
    # Adjust paths based on location
    if 'property-management' in filepath:
        cta_html = cta_html.replace('../../', '../../')
    elif 'services' in filepath:
        cta_html = cta_html.replace('../../', '../../')
    else:
        cta_html = cta_html.replace('../../', '')
    
    # Add before footer
    if '</footer>' in content and '<!-- Call to Action Section -->' not in content:
        content = content.replace('</footer>', cta_html + '</footer>')
    
    return content

# Process all HTML files
total_links_added = 0
files_processed = 0

for root, dirs, files in os.walk('C:\\Users\\mirsa\\manage369-live'):
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    
    for filename in files:
        if filename.endswith('.html') and not filename.startswith('test'):
            filepath = os.path.join(root, filename)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_link_count = content.count('href=')
                
                # Add various linking sections
                content = add_breadcrumb_navigation(filepath, content)
                content = add_related_areas_section(filepath, content)
                content = add_service_links_section(filepath, content)
                content = add_contextual_links(content, filepath)
                content = add_call_to_action_links(content, filepath)
                
                new_link_count = content.count('href=')
                links_added = new_link_count - original_link_count
                
                if links_added > 0:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    total_links_added += links_added
                    files_processed += 1
                    
                    if files_processed % 10 == 0:
                        print(f"Processed {files_processed} files, added {total_links_added} links so far...")
            
            except Exception as e:
                print(f"Error processing {filepath}: {str(e)}")

print("\n" + "=" * 60)
print(f"INTERLINKING COMPLETE!")
print(f"Files processed: {files_processed}")
print(f"Total internal links added: {total_links_added}")
print("\nLink distribution:")
print("- Breadcrumb navigation on all inner pages")
print("- Related areas sections on property pages")
print("- Service links on all pages")
print("- Contextual links in content")
print("- Call-to-action links with contact/services")
print("\nThis creates a strong internal linking structure for SEO!")