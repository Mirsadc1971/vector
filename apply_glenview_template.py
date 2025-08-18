"""
Apply Glenview Template Design to All 68 Property Management Pages
This script will update all location pages with the beautiful Glenview design
while preserving each location's unique content.
"""

import os
import re
from bs4 import BeautifulSoup
import glob

def extract_location_info(html_content, filepath):
    """Extract location-specific information from existing page"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Get location name from filepath
    location_name = os.path.basename(os.path.dirname(filepath))
    location_display = location_name.replace('-', ' ').title()
    
    # Extract existing content
    info = {
        'location': location_display,
        'location_path': location_name,
        'title': '',
        'meta_description': '',
        'main_content': '',
        'hero_image': '../../images/kenmore2manage369.jpg'  # Default image
    }
    
    # Get title
    title_tag = soup.find('title')
    if title_tag:
        info['title'] = title_tag.text
    
    # Get meta description
    meta_desc = soup.find('meta', {'name': 'description'})
    if meta_desc:
        info['meta_description'] = meta_desc.get('content', '')
    
    # Get hero section image
    hero_section = soup.find('section', {'class': 'hero'})
    if hero_section and hero_section.get('style'):
        style = hero_section.get('style')
        match = re.search(r"url\('([^']+)'\)", style)
        if match:
            info['hero_image'] = match.group(1)
    
    # Get main content paragraph
    content_section = soup.find('section', {'class': 'content'})
    if content_section:
        first_p = content_section.find('p')
        if first_p:
            info['main_content'] = first_p.text.strip()
    
    return info

def create_enhanced_content(info):
    """Create the enhanced content sections with Glenview template"""
    location = info['location']
    
    # Parse some basic info from existing content
    # This is a simplified version - you might want to customize this more
    population = "thriving community"  # Default, can be extracted if available
    
    # Create the enhanced sections
    enhanced_sections = f"""
        <!-- Why {location} Section -->
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 60px 20px; margin: 20px -20px; text-align: center;">
            <h2 style="color: white; font-size: 2.5rem; margin-bottom: 30px;">🏆 Why {location} Demands Excellence in Property Management</h2>
            <div style="max-width: 1200px; margin: 0 auto;">
                <p style="font-size: 1.2rem; line-height: 1.8; margin-bottom: 40px;">{info['main_content'][:500] if info['main_content'] else f"Welcome to {location}, where residents have discovered the perfect blend of suburban comfort and urban convenience."}</p>
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 30px; margin: 40px 0;">
                    <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;">
                        <h3 style="color: #ffd700;">🎓 Education Excellence</h3>
                        <p>Top-Rated Schools<br>Distinguished Districts<br>Academic Achievement</p>
                    </div>
                    <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;">
                        <h3 style="color: #ffd700;">🚆 Prime Location</h3>
                        <p>Easy Chicago Access<br>Major Transportation<br>Convenient Commuting</p>
                    </div>
                    <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;">
                        <h3 style="color: #ffd700;">🛍️ Local Amenities</h3>
                        <p>Shopping & Dining<br>Recreation Options<br>Community Events</p>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Community Features Section -->
        <div style="background: #f8f9fa; padding: 50px 20px; margin: 20px -20px;">
            <div style="max-width: 1200px; margin: 0 auto;">
                <h3 style="color: #2c3e50; font-size: 2rem; text-align: center; margin-bottom: 30px;">🏙️ {location}: A Community of Distinction</h3>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 40px; align-items: center;">
                    <div>
                        <p style="font-size: 1.1rem; line-height: 1.8;">{location} offers residents an exceptional quality of life with:</p>
                        <ul style="list-style: none; padding: 0; margin: 20px 0;">
                            <li style="padding: 10px 0;">✨ Well-maintained neighborhoods</li>
                            <li style="padding: 10px 0;">🏪 Thriving business districts</li>
                            <li style="padding: 10px 0;">🌳 Beautiful parks and recreation</li>
                            <li style="padding: 10px 0;">🏘️ Diverse housing options</li>
                            <li style="padding: 10px 0;">👥 Strong community spirit</li>
                        </ul>
                    </div>
                    <div style="background: linear-gradient(45deg, #4a90e2, #67b3ff); color: white; padding: 30px; border-radius: 15px;">
                        <h4 style="color: white; margin-bottom: 15px;">Professional Management Essential</h4>
                        <p>Properties in {location} deserve management that understands and preserves the unique character of this exceptional community.</p>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Local Character & Values Section -->
        <div style="padding: 50px 20px;">
            <div style="max-width: 1200px; margin: 0 auto;">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-bottom: 40px;">
                    <div style="background: #fff3cd; padding: 30px; border-radius: 10px; border-left: 5px solid #ffc107;">
                        <h3 style="color: #856404;">🏛️ {location} Character</h3>
                        <p>This community combines residential charm with modern amenities, creating a unique environment that requires sophisticated property management to maintain its distinctive appeal.</p>
                    </div>
                    <div style="background: #d4edda; padding: 30px; border-radius: 10px; border-left: 5px solid #28a745;">
                        <h3 style="color: #155724;">📈 Strong Property Values</h3>
                        <p><strong>Growing</strong> real estate market<br>
                        <strong>Professional management</strong> adds value<br>
                        <strong>Protected</strong> investments</p>
                    </div>
                </div>
            </div>
        </div>
        
        <h2>Manage369: Your Trusted {location} Property Management Partner</h2>
        <h3>Our Promise to {location} Communities</h3>
        <p>Since 2006, Manage369 has earned the trust of {location}'s most discerning property owners. We don't just manage buildings—we cultivate communities. Our approach combines institutional-grade financial management with the personal touch that makes residents feel genuinely cared for.</p>
        
        <h3>Why {location}'s Leading Associations Choose Manage369</h3>
        <ul style="line-height: 1.8; margin: 20px 0;">
            <li><strong>Local Expertise:</strong> Deep knowledge of {location}'s unique neighborhoods and requirements</li>
            <li><strong>Proven Track Record:</strong> 18+ years managing 50+ properties and 2,450+ units across the region</li>
            <li><strong>Technology-Forward:</strong> Cloud-based systems for real-time financial tracking and maintenance coordination</li>
            <li><strong>Certified Excellence:</strong> CAI, IREM, CCIM, and IDFPR certified professionals on staff</li>
            <li><strong>24/7 Availability:</strong> Emergency response team ready whenever {location} properties need us</li>
        </ul>
"""
    return enhanced_sections

def create_value_section(location):
    """Create the value proposition section"""
    return f"""
    <section style="padding: 60px 20px; background: linear-gradient(to bottom, #ffffff, #f0f4f8);">
        <div class="container">
            <h2 style="text-align: center; font-size: 2.5rem; color: #2c3e50; margin-bottom: 50px;">💎 How Manage369 Adds Extraordinary Value to {location} Properties</h2>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 30px; margin-bottom: 50px;">
                <!-- Value Card 1 -->
                <div style="background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); border-top: 4px solid #4a90e2;">
                    <h3 style="color: #4a90e2; margin-bottom: 20px;">📊 Property Value Enhancement</h3>
                    <div style="background: #e3f2fd; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; text-align: center;">
                            <div>
                                <div style="font-size: 2rem; color: #1976d2; font-weight: bold;">15%</div>
                                <div style="font-size: 0.9rem;">Higher Occupancy</div>
                            </div>
                            <div>
                                <div style="font-size: 2rem; color: #1976d2; font-weight: bold;">40%</div>
                                <div style="font-size: 0.9rem;">Fewer Delinquencies</div>
                            </div>
                        </div>
                    </div>
                    <p>Professional management translates directly to stronger financial positions and higher property values for every {location} owner.</p>
                </div>
                
                <!-- Value Card 2 -->
                <div style="background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); border-top: 4px solid #28a745;">
                    <h3 style="color: #28a745; margin-bottom: 20px;">💬 Proactive Communication</h3>
                    <ul style="list-style: none; padding: 0;">
                        <li style="padding: 10px 0; border-bottom: 1px solid #eee;">📱 Mobile apps for instant updates</li>
                        <li style="padding: 10px 0; border-bottom: 1px solid #eee;">💻 Resident portals for 24/7 access</li>
                        <li style="padding: 10px 0; border-bottom: 1px solid #eee;">📧 Traditional communication methods</li>
                        <li style="padding: 10px 0;">🏘️ Community event coordination</li>
                    </ul>
                    <p style="margin-top: 20px; color: #666;">Residents always know what's happening in their {location} community.</p>
                </div>
                
                <!-- Value Card 3 -->
                <div style="background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); border-top: 4px solid #ffc107;">
                    <h3 style="color: #f39c12; margin-bottom: 20px;">💰 Cost-Efficiency Excellence</h3>
                    <div style="background: #fff8e1; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
                        <div style="font-size: 2.5rem; color: #f39c12; font-weight: bold;">12-18%</div>
                        <div>Operating Cost Reduction</div>
                        <div style="font-size: 0.9rem; color: #666; margin-top: 10px;">First Year Average</div>
                    </div>
                    <p>Strategic vendor partnerships and bulk purchasing power deliver premium services at competitive rates.</p>
                </div>
            </div>
            
            <div style="background: #2c3e50; color: white; padding: 60px 20px; margin: 40px -20px; border-radius: 20px;">
                <h2 style="text-align: center; color: white; font-size: 2.5rem; margin-bottom: 50px;">🗺️ Local Expertise: Understanding {location}'s Unique Market</h2>
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; max-width: 1200px; margin: 0 auto;">
                    <div style="background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px;">
                        <h3 style="color: #ffd700; margin-bottom: 20px;">🏘️ Neighborhood Knowledge</h3>
                        <p style="line-height: 1.8;">Deep understanding of {location}'s diverse neighborhoods, from established residential areas to new developments, ensuring tailored management approaches.</p>
                    </div>
                    
                    <div style="background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px;">
                        <h3 style="color: #ffd700; margin-bottom: 20px;">🤝 Local Connections</h3>
                        <ul style="list-style: none; padding: 0;">
                            <li style="padding: 8px 0;">✓ Municipal relationships</li>
                            <li style="padding: 8px 0;">✓ Trusted vendor network</li>
                            <li style="padding: 8px 0;">✓ Emergency services</li>
                            <li style="padding: 8px 0;">✓ Community partnerships</li>
                        </ul>
                    </div>
                    
                    <div style="background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px;">
                        <h3 style="color: #ffd700; margin-bottom: 20px;">🏡 Real Estate Network</h3>
                        <p style="line-height: 1.8;">Strong partnerships with {location}'s leading real estate professionals ensure smooth transitions and maintained property appeal.</p>
                    </div>
                </div>
            </div>
"""

def create_faq_section(location):
    """Create the FAQ section"""
    return f"""
            <div style="margin-top: 60px;">
                <h2 style="text-align: center; font-size: 2.5rem; color: #2c3e50; margin-bottom: 50px;">❓ Frequently Asked Questions About Property Management in {location}</h2>
                
                <div style="max-width: 900px; margin: 0 auto;">
                    <div style="background: white; border-left: 4px solid #4a90e2; padding: 25px; margin-bottom: 20px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.08);">
                        <h4 style="color: #4a90e2; margin-bottom: 15px;">🏡 What makes {location} unique for property ownership?</h4>
                        <p style="color: #666; line-height: 1.8;">{location} offers an exceptional blend of community character, convenient location, quality schools, and diverse housing options that create consistent demand and strong property values.</p>
                    </div>
                    
                    <div style="background: white; border-left: 4px solid #28a745; padding: 25px; margin-bottom: 20px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.08);">
                        <h4 style="color: #28a745; margin-bottom: 15px;">👥 How does Manage369 support HOAs and condo boards?</h4>
                        <p style="color: #666; line-height: 1.8;">We provide comprehensive support including meeting facilitation, financial management, vendor coordination, legal compliance guidance, and strategic planning. Our goal is to make board service rewarding rather than burdensome.</p>
                    </div>
                    
                    <div style="background: white; border-left: 4px solid #ffc107; padding: 25px; margin-bottom: 20px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.08);">
                        <h4 style="color: #f39c12; margin-bottom: 15px;">🏘️ What's included in townhome management?</h4>
                        <p style="color: #666; line-height: 1.8;">Our townhome management encompasses financial administration, exterior maintenance coordination, common area upkeep, insurance management, resident communications, and board support—all tailored to townhome communities.</p>
                    </div>
                    
                    <div style="background: white; border-left: 4px solid #dc3545; padding: 25px; margin-bottom: 20px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.08);">
                        <h4 style="color: #dc3545; margin-bottom: 15px;">📊 Can you handle our financial reporting?</h4>
                        <p style="color: #666; line-height: 1.8;">Absolutely. We provide detailed monthly financial statements, annual budgets, reserve studies, tax preparation, and audit support. Our transparent reporting gives complete visibility into your association's financial health.</p>
                    </div>
                    
                    <div style="background: white; border-left: 4px solid #6f42c1; padding: 25px; margin-bottom: 20px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.08);">
                        <h4 style="color: #6f42c1; margin-bottom: 15px;">🔧 Do you coordinate local maintenance?</h4>
                        <p style="color: #666; line-height: 1.8;">Yes, we maintain a network of licensed, insured contractors throughout {location} and offer 24/7 emergency response. Our local presence ensures rapid response times and competitive pricing.</p>
                    </div>
                    
                    <div style="background: white; border-left: 4px solid #17a2b8; padding: 25px; margin-bottom: 20px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.08);">
                        <h4 style="color: #17a2b8; margin-bottom: 15px;">✨ How do owners benefit from full-service management?</h4>
                        <p style="color: #666; line-height: 1.8;">Owners gain peace of mind knowing their investment is professionally protected, property values are maximized, and their community operates smoothly—enjoying ownership without administrative burden.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>
"""

def create_conclusion_section(location):
    """Create the conclusion section"""
    return f"""
    <section style="padding: 60px 20px; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); text-align: center;">
        <div class="container">
            <h2 style="font-size: 2.5rem; margin-bottom: 30px;">Your {location} Property Deserves Excellence</h2>
            <p style="font-size: 1.2rem; line-height: 1.8; max-width: 900px; margin: 0 auto 30px;">{location} represents a unique blend of community spirit, strategic location, and quality living that deserves exceptional property management. This isn't just another neighborhood—it's a place where residents have chosen to build their lives and invest in their futures.</p>
            
            <p style="font-size: 1.1rem; line-height: 1.8; max-width: 900px; margin: 0 auto 30px;">At Manage369, we understand what makes {location} special. We bring 18+ years of experience, certified expertise, and genuine care to every property we manage. Our commitment to excellence ensures your community thrives while your investment grows.</p>
            
            <p style="font-size: 1.3rem; font-weight: bold; margin: 30px auto;">Whether you're a board member, property owner, or resident in {location}, you deserve property management that exceeds expectations.</p>
            
            <div style="margin-top: 40px;">
                <p style="font-size: 1.2rem; font-weight: bold; margin-bottom: 20px;">Welcome to Manage369. Welcome to property management reimagined.</p>
                <a href="tel:8476522338" style="display: inline-block; padding: 15px 40px; background: #4a90e2; color: white; text-decoration: none; border-radius: 5px; font-size: 1.1rem; margin: 10px;">Call (847) 652-2338 Today</a>
            </div>
        </div>
    </section>
"""

def update_service_cards(soup, location):
    """Update the service cards with location-specific content"""
    service_cards = soup.find_all('div', {'class': 'service-card'})
    
    if len(service_cards) >= 3:
        # Update Condominium card
        if service_cards[0]:
            p_tag = service_cards[0].find('p')
            if p_tag:
                p_tag.string = f"From {location}'s high-rise buildings to boutique condominiums, we provide comprehensive condo management that preserves property values and enhances resident satisfaction. Our services include financial planning, maintenance coordination, and board governance support tailored to each building's unique character."
        
        # Update HOA card
        if service_cards[1]:
            p_tag = service_cards[1].find('p')
            if p_tag:
                p_tag.string = f"{location}'s neighborhoods deserve management that upholds their standards. We partner with HOAs throughout {location} to ensure smooth operations, supporting associations of all sizes with equal dedication and expertise."
        
        # Update Townhome card
        if service_cards[2]:
            p_tag = service_cards[2].find('p')
            if p_tag:
                p_tag.string = f"Townhome communities throughout {location} require specialized management that balances individual ownership with shared responsibilities. We excel at managing these hybrid communities with precision and care."

def process_html_file(filepath):
    """Process a single HTML file"""
    print(f"Processing: {filepath}")
    
    try:
        # Read the file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Extract location info
        info = extract_location_info(content, filepath)
        location = info['location']
        
        # Find the content section
        content_section = soup.find('section', {'class': 'content'})
        if not content_section:
            print(f"  Warning: No content section found in {filepath}")
            return False
        
        # Get the first paragraph (we'll replace this)
        first_p = content_section.find('p')
        if first_p:
            # Create new enhanced content
            enhanced_html = create_enhanced_content(info)
            
            # Replace the paragraph with our enhanced content
            new_soup = BeautifulSoup(enhanced_html, 'html.parser')
            first_p.replace_with(new_soup)
        
        # Update the service cards
        update_service_cards(soup, location)
        
        # Find where to insert the value section
        # Look for the "Our Service Offerings" section
        service_offerings_section = None
        for section in soup.find_all('section'):
            h2 = section.find('h2')
            if h2 and 'Our Service Offerings' in h2.text:
                service_offerings_section = section
                break
        
        if service_offerings_section:
            # Insert the value section after service offerings
            value_html = create_value_section(location) + create_faq_section(location)
            value_soup = BeautifulSoup(value_html, 'html.parser')
            service_offerings_section.insert_after(value_soup)
        
        # Find the contact section and add conclusion before it
        contact_section = soup.find('section', {'class': 'contact-section'})
        if contact_section:
            conclusion_html = create_conclusion_section(location)
            conclusion_soup = BeautifulSoup(conclusion_html, 'html.parser')
            contact_section.insert_before(conclusion_soup)
            
            # Update contact section heading
            h2 = contact_section.find('h2')
            if h2:
                h2.string = f"Transform Your {location} Property Management Experience"
        
        # Update hero section
        hero_section = soup.find('section', {'class': 'hero'})
        if hero_section:
            h1 = hero_section.find('h1')
            if h1:
                h1.string = f"Property Management {location}: Excellence in Every Detail"
            p = hero_section.find('p')
            if p:
                p.string = f"Premier HOA & Condo Management for {location} Communities | Trusted Since 2006"
        
        # Save the updated file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup.prettify()))
        
        print(f"  [SUCCESS] Successfully updated {location}")
        return True
        
    except Exception as e:
        print(f"  [ERROR] Error processing {filepath}: {e}")
        return False

def main():
    """Main function to process all property management pages"""
    
    # Get all property management HTML files
    pattern = r'C:\Users\mirsa\manage369-live\property-management\*\index.html'
    files = glob.glob(pattern)
    
    # Skip Glenview since it's already done
    files = [f for f in files if 'glenview' not in f.lower()]
    
    print(f"Found {len(files)} property management pages to update")
    print("=" * 50)
    
    success_count = 0
    failed_files = []
    
    for filepath in files:
        if process_html_file(filepath):
            success_count += 1
        else:
            failed_files.append(filepath)
    
    print("=" * 50)
    print(f"Update Complete!")
    print(f"[SUCCESS] Successfully updated: {success_count}/{len(files)} pages")
    
    if failed_files:
        print(f"[FAILED] Failed to update {len(failed_files)} pages:")
        for f in failed_files:
            print(f"  - {f}")
    
    return success_count == len(files)

if __name__ == "__main__":
    # Run the update
    success = main()
    
    if success:
        print("\n[COMPLETE] All pages updated successfully with Glenview template!")
    else:
        print("\n[WARNING] Some pages had issues. Please review the failed files.")