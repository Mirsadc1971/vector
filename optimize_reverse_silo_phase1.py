import os
import re

def optimize_area_page_ctas(filepath, city_name):
    """Phase 1: Optimize CTAs with better copy and enhanced internal linking"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Add breadcrumb navigation after header
    breadcrumb_html = f'''<!-- Breadcrumb Navigation for SEO -->
<nav aria-label="breadcrumb" style="background: #f8f9fa; padding: 1rem 0; margin-bottom: 0;">
    <div style="max-width: 1200px; margin: 0 auto; padding: 0 2rem;">
        <ol style="list-style: none; display: flex; align-items: center; margin: 0; padding: 0; font-size: 0.875rem;">
            <li><a href="../../" style="color: #2563eb; text-decoration: none;">Home</a></li>
            <li style="margin: 0 0.5rem; color: #6b7280;">›</li>
            <li><a href="../" style="color: #2563eb; text-decoration: none;">Service Areas</a></li>
            <li style="margin: 0 0.5rem; color: #6b7280;">›</li>
            <li style="color: #4b5563; font-weight: 500;">{city_name} Property Management</li>
        </ol>
    </div>
</nav>'''
    
    # Insert breadcrumb after header, before hero section
    if '<section class="hero"' in content and '<!-- Breadcrumb Navigation' not in content:
        content = content.replace('<section class="hero"', breadcrumb_html + '\n<section class="hero"')
    
    # 2. Optimize Hero CTA with better action-oriented copy
    hero_cta_old = 'Request a Consultation'
    hero_cta_new = f'Get FREE {city_name} Consultation'
    content = content.replace(f'>{hero_cta_old}<', f'>{hero_cta_new}<')
    
    # 3. Optimize strategic CTA copy - make it more action-oriented
    old_heading = f"Ready to Transform Your {city_name} Property Management?"
    new_heading = f"Get Your FREE {city_name} Property Analysis Today"
    content = content.replace(old_heading, new_heading)
    
    old_subheading = f"Join 50+ communities who've reduced costs by 50% with Manage369"
    new_subheading = f"Join 50+ {city_name} Properties Saving Thousands Every Year"
    content = content.replace(old_subheading, new_subheading)
    
    old_button = "Request Your Free Consultation →"
    new_button = f"Start Saving in {city_name} Today →"
    content = content.replace(old_button, new_button)
    
    # 4. Optimize mid-content CTA
    old_mid_text = "See why your neighbors switched to Manage369 and saved thousands."
    new_mid_text = f"Discover why {city_name} property owners save 50% with Manage369's proven management system."
    content = content.replace(old_mid_text, new_mid_text)
    
    old_mid_button = "Get Your Custom Savings Analysis →"
    new_mid_button = f"Calculate Your {city_name} Savings →"
    content = content.replace(old_mid_button, new_mid_button)
    
    # 5. Optimize bottom mega CTA
    old_bottom_heading = "Start Saving 50% on Property Management"
    new_bottom_heading = f"Transform Your {city_name} Property Management Today"
    content = content.replace(old_bottom_heading, new_bottom_heading)
    
    old_bottom_text = f"Join {city_name}'s most satisfied property communities"
    new_bottom_text = f"Join 2,450+ Units Already Saving with Manage369"
    content = content.replace(old_bottom_text, new_bottom_text)
    
    # 6. Add related areas section for better internal linking
    related_areas_html = f'''
    <!-- Related Service Areas - Enhanced Internal Linking -->
    <div style="background: #f8f9fa; padding: 2rem; margin: 2rem 0; border-radius: 12px;">
        <h3 style="color: #1e3a8a; margin-bottom: 1rem;">Explore Nearby Property Management Services</h3>
        <p style="color: #4b5563; margin-bottom: 1.5rem;">Manage369 proudly serves communities throughout Chicago and the North Shore:</p>
        <div style="display: flex; flex-wrap: wrap; gap: 0.75rem;">'''
    
    # Add contextual nearby area links based on location
    nearby_areas = get_nearby_areas(city_name)
    for area in nearby_areas[:6]:  # Limit to 6 nearby areas
        area_url = area.lower().replace(' ', '-')
        related_areas_html += f'''
            <a href="../{area_url}/" style="background: white; color: #2563eb; padding: 0.5rem 1rem; border-radius: 6px; text-decoration: none; border: 1px solid #e5e7eb; transition: all 0.3s;" onmouseover="this.style.background='#2563eb'; this.style.color='white';" onmouseout="this.style.background='white'; this.style.color='#2563eb';">
                {area}
            </a>'''
    
    related_areas_html += '''
        </div>
        <p style="margin-top: 1.5rem; font-size: 0.875rem; color: #6b7280;">
            <a href="../" style="color: #2563eb; text-decoration: underline;">View all 68 service areas →</a>
        </p>
    </div>'''
    
    # Insert related areas before the consultation form
    if '<section class="consultation-form">' in content and '<!-- Related Service Areas' not in content:
        content = content.replace('<section class="consultation-form">', related_areas_html + '\n<section class="consultation-form">')
    
    # 7. Add mobile-optimized sticky CTA (improved visibility)
    mobile_sticky_cta = '''
    <!-- Mobile Sticky CTA - Enhanced Visibility -->
    <div id="mobileStickyFooter" style="position: fixed; bottom: 0; left: 0; right: 0; background: linear-gradient(135deg, #1e3a8a, #2563eb); padding: 1rem; text-align: center; z-index: 9999; display: none; box-shadow: 0 -4px 6px rgba(0,0,0,0.1);">
        <div style="display: flex; gap: 0.75rem; justify-content: center; align-items: center;">
            <a href="tel:8476522338" style="flex: 1; background: white; color: #1e3a8a; padding: 0.875rem; border-radius: 8px; text-decoration: none; font-weight: bold; font-size: 1rem;">
                📞 Call Now
            </a>
            <a href="../../contact.html" style="flex: 1; background: #F4A261; color: white; padding: 0.875rem; border-radius: 8px; text-decoration: none; font-weight: bold; font-size: 1rem;">
                Get Free Quote
            </a>
        </div>
    </div>
    
    <style>
    @media (max-width: 768px) {
        #mobileStickyFooter {
            display: block !important;
        }
        body {
            padding-bottom: 80px; /* Prevent content from being hidden */
        }
    }
    </style>'''
    
    # Add mobile sticky CTA before closing body tag
    if '</body>' in content and 'mobileStickyFooter' not in content:
        content = content.replace('</body>', mobile_sticky_cta + '\n</body>')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def get_nearby_areas(city_name):
    """Return nearby areas based on geographic proximity"""
    
    north_shore = ['Wilmette', 'Winnetka', 'Evanston', 'Highland Park', 'Lake Forest', 'Glencoe', 'Northbrook', 'Glenview', 'Kenilworth', 'Lake Bluff']
    northwest_suburbs = ['Des Plaines', 'Mount Prospect', 'Arlington Heights', 'Buffalo Grove', 'Wheeling', 'Prospect Heights', 'Rolling Meadows', 'Palatine', 'Elk Grove Village']
    chicago_north = ['Lincoln Park', 'Lakeview', 'Gold Coast', 'River North', 'Old Town', 'Lincoln Square', 'Ravenswood', 'Uptown', 'Edgewater', 'Rogers Park']
    chicago_northwest = ['Edison Park', 'Norwood Park', 'Jefferson Park', 'Portage Park', 'Irving Park', 'Albany Park', 'North Park', 'Sauganash', 'Forest Glen']
    west_suburbs = ['Oak Park', 'Elmwood Park', 'Franklin Park', 'Schiller Park', 'Norridge', 'Harwood Heights', 'River Grove', 'Melrose Park']
    
    all_areas = {
        'north_shore': north_shore,
        'northwest_suburbs': northwest_suburbs,
        'chicago_north': chicago_north,
        'chicago_northwest': chicago_northwest,
        'west_suburbs': west_suburbs
    }
    
    # Find which group the city belongs to
    for group_name, areas in all_areas.items():
        if city_name in areas:
            # Return other areas from the same group, excluding the current city
            nearby = [area for area in areas if area != city_name]
            return nearby[:6]  # Return up to 6 nearby areas
    
    # Default fallback - return popular areas
    return ['Glenview', 'Wilmette', 'Evanston', 'Northbrook', 'Skokie', 'Des Plaines']

# Update all area pages
updated_count = 0
for root, dirs, files in os.walk('property-management'):
    if 'node_modules' in root or '.git' in root:
        continue
    
    for file in files:
        if file == 'index.html' and 'property-management' in root:
            filepath = os.path.join(root, file)
            # Extract city name from path
            city_name = root.split(os.sep)[-1].replace('-', ' ').title()
            
            # Skip the main property management index
            if city_name == 'Property Management':
                continue
                
            if optimize_area_page_ctas(filepath, city_name):
                updated_count += 1
                print(f"Optimized: {city_name}")

print(f"\n✅ Phase 1 Implementation Complete!")
print(f"Total area pages optimized: {updated_count}")
print("\n📋 Optimizations Applied:")
print("  1. Added breadcrumb navigation for better SEO")
print("  2. Optimized CTA copy with action-oriented language")
print("  3. Enhanced internal linking with related areas")
print("  4. Improved mobile CTA visibility with sticky footer")
print("  5. Location-specific CTA personalization")