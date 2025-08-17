import os
import re

# Content templates for each location
location_content = {
    "glenview": """
    <section class="content">
        <p>Glenview stands as one of Chicago's most prestigious North Shore suburbs, where tree-lined streets meet exceptional schools and The Glen Town Center creates a perfect blend of suburban tranquility and modern convenience. This distinguished community of 48,000 residents has consistently ranked among the best places to live in Illinois, offering an ideal environment for families and professionals who value quality of life, excellent education, and proximity to both Chicago and O'Hare Airport. At Manage369, we understand what makes Glenview special - from the historic charm of downtown Glenview with its Metra station providing direct access to Chicago, to the modern luxury of The Glen's mixed-use development, this is a community that demands property management excellence to match its exceptional standards.</p>
        
        <p>Our comprehensive property management approach recognizes that Glenview properties serve a sophisticated clientele who have chosen this community for its outstanding schools, beautiful parks, and strong sense of neighborhood. Whether managing luxury <a href="../../services/condominium-management/index.html">condominiums</a> near The Glen Town Center, established <a href="../../services/townhome-management/index.html">townhome communities</a> along Waukegan Road, or prestigious <a href="../../services/hoa-management/index.html">homeowner associations</a> in the Tall Trees neighborhood, we bring the same commitment to excellence that Glenview residents expect in every aspect of their lives.</p>
        
        <p>Glenview's strategic location offers residents the perfect balance of suburban serenity and urban accessibility. The Milwaukee District North Metra line provides convenient transportation to downtown Chicago, while easy access to I-294 and I-94 connects residents to the entire metropolitan area. This accessibility, combined with Glenview's exceptional schools including Glenbrook South High School and numerous Blue Ribbon elementary schools, makes it a highly desirable location for families and professionals alike.</p>
    </section>""",
    
    "northbrook": """
    <section class="content">
        <p>Northbrook exemplifies North Shore excellence with its perfect blend of residential charm, corporate sophistication, and natural beauty that has made it one of Chicago's most sought-after suburbs for over a century. This distinguished community of 33,000 residents enjoys a unique position as both a peaceful suburban retreat and a thriving business hub, home to major corporations like Allstate and UL while maintaining the tree-lined streets and excellent schools that families treasure. At Manage369, we understand that Northbrook property management requires a sophisticated approach that matches the community's high standards - from the luxury developments along Techny Road to the established neighborhoods near Village Green Park, every property deserves management that preserves and enhances its value.</p>
        
        <p>Our property management philosophy in Northbrook recognizes the diverse needs of this exceptional community. Whether we're managing modern <a href="../../services/condominium-management/index.html">luxury condominiums</a> near Northbrook Court, established <a href="../../services/townhome-management/index.html">townhome communities</a> along Sanders Road, or prestigious <a href="../../services/hoa-management/index.html">homeowner associations</a> in the Mission Hills area, we bring deep local knowledge and professional expertise to every property. Our team understands that Northbrook residents have chosen this community for its exceptional quality of life, and our management services reflect that same commitment to excellence.</p>
        
        <p>The Village of Northbrook's commitment to maintaining its "casual elegance" is evident in everything from its award-winning park district to its thriving downtown business district. With convenient access to the Edens Expressway and Metra's Milwaukee District North line, residents enjoy easy connectivity to Chicago while maintaining their suburban lifestyle. This combination of accessibility, excellent schools including Glenbrook North High School, and abundant green space makes Northbrook properties highly desirable investments that require professional management to maintain their premium value.</p>
    </section>"""
}

# Default content for locations not in the dict
default_content = """
    <section class="content">
        <p>{location_title} represents a distinctive community within the Chicago metropolitan area, offering residents a unique blend of suburban comfort and urban accessibility that makes it an attractive location for property investment and residential living. This thriving neighborhood has developed its own character while maintaining strong connections to the broader Chicago region, creating an environment where property values remain stable and community life flourishes. At Manage369, we bring deep understanding of {location_title}'s specific needs and characteristics to every property we manage, ensuring that our services align with the community's expectations and standards.</p>
        
        <p>Our comprehensive property management services in {location_title} are tailored to meet the diverse needs of property owners and residents. Whether managing modern <a href="../../services/condominium-management/index.html">condominium complexes</a>, established <a href="../../services/townhome-management/index.html">townhome communities</a>, or traditional <a href="../../services/hoa-management/index.html">homeowner associations</a>, we provide professional oversight that protects property values while enhancing quality of life for residents. Our 18+ years of experience managing properties throughout Chicago and the suburbs gives us unique insights into what makes each community special.</p>
        
        <p>With convenient transportation options and access to major highways, {location_title} offers residents the perfect balance of community living and metropolitan connectivity. The area's schools, parks, and local amenities create an environment where families thrive and property values appreciate steadily. Our property management approach recognizes these assets and works to maintain the high standards that make {location_title} a desirable place to live and invest.</p>
    </section>"""

base_dir = "property-management"
count = 0

for location in os.listdir(base_dir):
    location_path = os.path.join(base_dir, location)
    if os.path.isdir(location_path):
        index_file = os.path.join(location_path, "index.html")
        
        if os.path.exists(index_file):
            with open(index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if content section already exists
            if '<section class="content">' in content:
                print(f"Skipping {location} - content section already exists")
                continue
            
            # Get the specific content or use default
            if location in location_content:
                new_content_section = location_content[location]
            else:
                location_title = location.replace('-', ' ').title()
                new_content_section = default_content.format(location_title=location_title)
            
            # Find where to insert - after the hero section
            hero_end = content.find('</section>')
            if hero_end != -1:
                # Find the actual end of hero section
                hero_end = content.find('</section>', content.find('<section class="hero">'))
                if hero_end != -1:
                    insert_pos = hero_end + len('</section>')
                    new_content = content[:insert_pos] + '\n' + new_content_section + content[insert_pos:]
                    
                    with open(index_file, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    count += 1
                    print(f"Added content to {location}")

print(f"\nAdded unique content sections to {count} pages")