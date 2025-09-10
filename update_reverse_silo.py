import os
import re

def update_area_page_links(filepath, city_name):
    """Update area pages with strategic internal links pointing to contact page"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the hero CTA button and update it
    hero_cta_pattern = r'<a class="btn btn-secondary" href="[^"]*contact\.html"[^>]*>.*?</a>'
    hero_cta_replacement = f'''<a class="btn btn-secondary" href="../../contact.html" style="background: rgba(255,255,255,0.95); color: #111827; border: 2px solid white; padding: 18px 36px; font-size: 1.2rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; box-shadow: 0 4px 20px rgba(0,0,0,0.3);">
      Request a Consultation
     </a>'''
    
    content = re.sub(hero_cta_pattern, hero_cta_replacement, content, flags=re.DOTALL)
    
    # Add strategic CTA after the opening paragraph (after first </p> in main content)
    # Find the section with "Why Choose Manage369"
    pattern = r'(<h2[^>]*>Why Choose Manage369 for [^<]+</h2>\s*<p[^>]*>.*?</p>)'
    
    strategic_cta = f'''
    <!-- Strategic Internal Link - Part of Reverse Silo Structure -->
    <div style="background: linear-gradient(135deg, #1e3a8a, #2563eb); color: white; padding: 2rem; border-radius: 12px; margin: 2rem 0; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
        <h3 style="font-size: 1.5rem; margin-bottom: 1rem;">Ready to Transform Your {city_name} Property Management?</h3>
        <p style="font-size: 1.1rem; margin-bottom: 1.5rem;">Join 50+ communities who've reduced costs by 75% with Manage369</p>
        <a href="../../contact.html" style="background: #F4A261; color: #1e3a8a; padding: 15px 40px; border-radius: 50px; text-decoration: none; display: inline-block; font-weight: bold; font-size: 1.1rem; transition: all 0.3s;" onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 6px 20px rgba(0,0,0,0.3)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 15px rgba(0,0,0,0.2)'">
            Request Your Free Consultation →
        </a>
    </div>'''
    
    if re.search(pattern, content):
        content = re.sub(pattern, r'\1' + strategic_cta, content, count=1)
    
    # Add another CTA in the middle of local info section
    local_pattern = r'(<h2[^>]*>Living in ' + re.escape(city_name) + r'[^<]*</h2>.*?</p>.*?</p>)'
    
    mid_cta = f'''
    <!-- Mid-Content Strategic Link -->
    <div style="background: #f7f9fc; border-left: 5px solid #F4A261; padding: 1.5rem; margin: 2rem 0;">
        <strong style="color: #1e3a8a; font-size: 1.2rem;">🏆 {city_name} Property Owners:</strong>
        <p style="margin: 0.5rem 0; color: #4b5563;">See why your neighbors switched to Manage369 and saved thousands.</p>
        <a href="../../contact.html" style="color: #2563eb; font-weight: bold; text-decoration: underline;">
            Get Your Custom Savings Analysis →
        </a>
    </div>'''
    
    if re.search(local_pattern, content, re.DOTALL):
        content = re.sub(local_pattern, r'\1' + mid_cta, content, count=1, flags=re.DOTALL)
    
    # Add bottom CTA before footer
    footer_pattern = r'(</section>\s*<!-- Footer -->)'
    
    bottom_cta = f'''
    <!-- Bottom Strategic CTA - Complete the Reverse Silo -->
    <div style="background: linear-gradient(135deg, #F4A261, #e67e22); padding: 3rem 2rem; text-align: center; margin-top: 3rem;">
        <h2 style="color: white; font-size: 2rem; margin-bottom: 1rem;">Start Saving 75% on Property Management Today</h2>
        <p style="color: white; font-size: 1.2rem; margin-bottom: 2rem;">Join {city_name}'s most satisfied property communities</p>
        <div style="display: flex; gap: 1.5rem; justify-content: center; flex-wrap: wrap;">
            <a href="../../contact.html" style="background: white; color: #e67e22; padding: 18px 40px; border-radius: 50px; text-decoration: none; font-weight: bold; font-size: 1.1rem; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                📞 Request Consultation
            </a>
            <a href="sms:8476522338" style="background: transparent; color: white; border: 2px solid white; padding: 18px 40px; border-radius: 50px; text-decoration: none; font-weight: bold; font-size: 1.1rem;">
                📱 Text Us Now
            </a>
        </div>
    </div>
    
    \1'''
    
    if re.search(footer_pattern, content):
        content = re.sub(footer_pattern, bottom_cta, content, count=1)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

# Get all area pages
area_pages = []
for root, dirs, files in os.walk('property-management'):
    for file in files:
        if file == 'index.html' and 'property-management' in root:
            filepath = os.path.join(root, file)
            # Extract city name from path
            city_name = root.split(os.sep)[-1].replace('-', ' ').title()
            area_pages.append((filepath, city_name))

# Update all area pages
updated = 0
for filepath, city_name in area_pages:
    if update_area_page_links(filepath, city_name):
        print(f"Updated: {filepath} for {city_name}")
        updated += 1

print(f"\nTotal area pages updated: {updated}")
print("\n✅ Reverse Silo Structure Implemented:")
print("   All area pages → Contact page (master conversion)")
print("   Multiple strategic CTAs per page")
print("   Consistent user journey")