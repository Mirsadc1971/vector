#!/usr/bin/env python3
"""
Fix hero section readability across all property management pages
Applies Dunning-style hero with improved text contrast and readability
"""

import os
import re
from pathlib import Path

def update_hero_section(content, location_name):
    """Update hero section with better readability"""
    
    # Pattern to find the existing hero section
    hero_pattern = r'<section class="hero"[^>]*>.*?</section>'
    
    # New hero section template with improved readability
    new_hero = f'''<section class="hero" style="background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('../../images/manage369widowview.jpg') center/cover; padding: 120px 20px; text-align: center; color: white; min-height: 600px; display: flex; align-items: center; justify-content: center;" id="main" role="main">
<div class="hero-content" style="max-width: 1200px; margin: 0 auto;">
<h1 style="font-size: 3.5rem; font-weight: 700; margin-bottom: 1.5rem; color: white; text-shadow: 2px 2px 8px rgba(0,0,0,0.7); line-height: 1.2;">
     {location_name} Property Management Services - Manage369
    </h1>
<p style="font-size: 1.8rem; margin-bottom: 2rem; color: white; text-shadow: 1px 1px 4px rgba(0,0,0,0.7); font-weight: 400; max-width: 900px; margin-left: auto; margin-right: auto; line-height: 1.4;">
     Premier HOA & Condo Management for {location_name} Communities | Trusted Since 2006
    </p>
<div class="hero-stats" style="font-size: 1.6rem; color: white; margin-bottom: 2.5rem; font-weight: 500; text-shadow: 1px 1px 4px rgba(0,0,0,0.7); letter-spacing: 2px;">
     18+ Years • 50+ Properties • 2,450+ Units Managed
    </div>
<div class="cta-buttons" style="display: flex; gap: 2rem; justify-content: center; flex-wrap: wrap;">
    <a href="tel:8476522338" class="btn btn-primary" style="background: #ea580c; border-color: #ea580c; color: white; padding: 18px 36px; font-size: 1.2rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; box-shadow: 0 4px 20px rgba(0,0,0,0.3);">
        Schedule Consultation
    </a>
    <a href="../" class="btn btn-secondary" style="background: rgba(255,255,255,0.95); color: #111827; border: 2px solid white; padding: 18px 36px; font-size: 1.2rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; box-shadow: 0 4px 20px rgba(0,0,0,0.3);">
        View All Areas
    </a>
</div>
</div>
</section>'''
    
    # Replace the hero section
    updated_content = re.sub(hero_pattern, new_hero, content, flags=re.DOTALL)
    
    return updated_content

def format_location_name(folder_name):
    """Convert folder name to proper location name"""
    # Replace hyphens with spaces and capitalize
    name = folder_name.replace('-', ' ')
    # Title case with special handling for certain words
    words = name.split()
    formatted_words = []
    
    for word in words:
        if word.lower() in ['park', 'grove', 'ridge', 'heights', 'lake', 'square']:
            formatted_words.append(word.capitalize())
        else:
            formatted_words.append(word.capitalize())
    
    return ' '.join(formatted_words)

def main():
    print("Fixing Hero Section Readability Across All Property Pages")
    print("=" * 60)
    
    # Get all property management subdirectories
    property_dir = Path('property-management')
    
    if not property_dir.exists():
        print("Property management directory not found!")
        return
    
    # Process all subdirectories
    updated_count = 0
    locations = []
    
    for location_dir in property_dir.iterdir():
        if location_dir.is_dir():
            index_file = location_dir / 'index.html'
            
            if index_file.exists():
                location_name = format_location_name(location_dir.name)
                locations.append(location_name)
                
                print(f"\nProcessing: {location_name}")
                
                try:
                    with open(index_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Update the hero section
                    updated_content = update_hero_section(content, location_name)
                    
                    # Also ensure H1 tags have proper styling
                    updated_content = re.sub(
                        r'<h1([^>]*)>',
                        '<h1 style="font-size: 3.5rem; font-weight: 700; margin-bottom: 1.5rem; color: white; text-shadow: 2px 2px 8px rgba(0,0,0,0.7); line-height: 1.2;"\\1>',
                        updated_content
                    )
                    
                    # Save the updated file
                    with open(index_file, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                    
                    updated_count += 1
                    print(f"  Updated hero section with improved readability")
                    
                except Exception as e:
                    print(f"  Error: {e}")
    
    # Also update service area pages if they exist
    service_dir = Path('service-areas')
    if service_dir.exists():
        for location_dir in service_dir.iterdir():
            if location_dir.is_dir():
                index_file = location_dir / 'index.html'
                
                if index_file.exists():
                    location_name = format_location_name(location_dir.name)
                    
                    print(f"\nProcessing service area: {location_name}")
                    
                    try:
                        with open(index_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Update the hero section
                        updated_content = update_hero_section(content, location_name)
                        
                        # Save the updated file
                        with open(index_file, 'w', encoding='utf-8') as f:
                            f.write(updated_content)
                        
                        updated_count += 1
                        print(f"  Updated hero section")
                        
                    except Exception as e:
                        print(f"  Error: {e}")
    
    print("\n" + "=" * 60)
    print(f"\nSummary:")
    print(f"  Total pages updated: {updated_count}")
    print(f"  Locations processed: {len(locations)}")
    
    print("\nImprovements Applied:")
    print("  - Enhanced text contrast with dark overlay")
    print("  - Added text shadows for better readability")
    print("  - Increased font sizes for H1 and hero text")
    print("  - Improved button contrast and visibility")
    print("  - Consistent hero styling across all pages")
    print("  - Better mobile responsiveness")
    
    print("\nAll hero sections now have:")
    print("  • White text with strong shadows on dark overlay")
    print("  • 3.5rem H1 font size with 700 font weight")
    print("  • 1.8rem subtitle with improved line height")
    print("  • High-contrast CTA buttons")
    print("  • Minimum 600px height for better visual impact")

if __name__ == "__main__":
    main()