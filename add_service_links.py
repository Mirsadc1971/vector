import os
import re

def add_service_links(directory):
    """Add internal links to main services within the content text of property pages"""
    
    updated_files = []
    total_links_added = 0
    
    for filename in os.listdir(directory):
        if filename == 'index.html':
            continue
            
        filepath = os.path.join(directory, filename, 'index.html')
        
        if not os.path.exists(filepath):
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        links_added = 0
        location_name = filename.replace('-', ' ').title()
        
        # Check if we already have these links in the content to avoid duplicates
        existing_condo_links = content.count('href="../../services/condominium-management/index.html"')
        existing_hoa_links = content.count('href="../../services/hoa-management/index.html"') 
        existing_town_links = content.count('href="../../services/townhome-management/index.html"')
        
        print(f"Checking {filename}: Found {existing_condo_links} condo, {existing_hoa_links} HOA, {existing_town_links} townhome links")
        
        # Find the main content paragraphs after the hero section
        # Look for the first mentions of each service type to link
        
        # Find content between hero and services-grid
        hero_end = content.find('</section>', content.find('class="hero"'))
        services_start = content.find('<div class="services-grid">')
        
        if hero_end > 0 and services_start > hero_end:
            # Get the content section
            content_section = content[hero_end:services_start]
            
            # Check if we need to add links (only if we don't have many already)
            if existing_condo_links < 5:  # Add link if we have fewer than 5
                # Find a good place to add condominium link
                if 'condominium' in content_section.lower() and not '<a href="../../services/condominium-management' in content_section:
                    # Simple replacement of first occurrence
                    content_section = content_section.replace(
                        'condominium complexes',
                        '<a href="../../services/condominium-management/index.html">condominium complexes</a>',
                        1
                    )
                    links_added += 1
                    print(f"  Added condominium link in {filename}")
            
            if existing_hoa_links < 5:
                if 'homeowner associations' in content_section.lower() and not '<a href="../../services/hoa-management' in content_section:
                    content_section = content_section.replace(
                        'homeowner associations',
                        '<a href="../../services/hoa-management/index.html">homeowner associations</a>',
                        1
                    )
                    links_added += 1
                    print(f"  Added HOA link in {filename}")
            
            if existing_town_links < 5:
                if 'townhome communit' in content_section.lower() and not '<a href="../../services/townhome-management' in content_section:
                    content_section = content_section.replace(
                        'townhome communities',
                        '<a href="../../services/townhome-management/index.html">townhome communities</a>',
                        1
                    )
                    links_added += 1
                    print(f"  Added townhome link in {filename}")
            
            # Rebuild content if we added links
            if links_added > 0:
                content = content[:hero_end] + content_section + content[services_start:]
                total_links_added += links_added
                
                # Save the updated file
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                updated_files.append(filename)
    
    return updated_files, total_links_added

# Run the update
directory = r'C:\Users\mirsa\manage369-live\property-management'
updated, total_links = add_service_links(directory)

print(f"\n=== SUMMARY ===")
print(f"Updated {len(updated)} pages")
print(f"Added {total_links} internal service links total")
print(f"Goal: Add strategic links to main services (3 per page where possible)")

if len(updated) > 0:
    print(f"\nPages updated:")
    for page in updated[:10]:  # Show first 10
        print(f"  - {page}")
    if len(updated) > 10:
        print(f"  ... and {len(updated)-10} more")

print("\nInternal linking to main services has been strengthened!")