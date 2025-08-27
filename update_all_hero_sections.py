#!/usr/bin/env python3
"""
Update all property management pages with consistent hero section styling
"""

import os
import re
from pathlib import Path
import random

# Available images to rotate through
IMAGES = [
    'manage369widowview.jpg',
    'manstandingmanage369.jpg',
    'northbrook2manage369.jpg',
    'chestnutmanage369.jpg',
    'buck4manage369.jpg',
    'kenmore2manage369.jpg',
    'northfield1manage369.jpg',
    'northfield2manage369.jpg',
    'manage369bedroom1740maplewood.jpg',
    'manage369livingroomskokie.jpg',
    'manage369randolphstation.jpg',
    'chestnut2manage369.jpg',
    'Manage3693.jpg'
]

def update_hero_section(filepath, image_name):
    """Update hero section with consistent styling"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern to find hero section
        hero_pattern = r'<section class="hero"[^>]*>.*?</section>'
        hero_match = re.search(hero_pattern, content, re.DOTALL)
        
        if not hero_match:
            print(f"No hero section found in {filepath}")
            return False
        
        old_hero = hero_match.group(0)
        
        # Extract the H1 content
        h1_pattern = r'<h1[^>]*>(.*?)</h1>'
        h1_match = re.search(h1_pattern, old_hero, re.DOTALL)
        
        if not h1_match:
            print(f"No H1 found in {filepath}")
            return False
        
        h1_content = h1_match.group(1).strip()
        
        # Extract subtitle if exists
        p_pattern = r'<p[^>]*style[^>]*>(.*?)</p>'
        p_match = re.search(p_pattern, old_hero, re.DOTALL)
        
        subtitle = ""
        if p_match:
            subtitle = p_match.group(1).strip()
        
        # Build new hero section with consistent styling
        new_hero = f'''<section class="hero" style="background: url('../../images/{image_name}') center/cover; padding: 40px 20px 20px; text-align: center; color: white; min-height: 600px; display: flex; align-items: flex-start; justify-content: center;" id="main" role="main">
<div class="hero-content" style="max-width: 1200px; margin: 0 auto; margin-top: 80px;">
<h1 style="font-size: 2.5rem; font-weight: 700; margin-bottom: 1.5rem; color: #ffffff !important; text-shadow: none; line-height: 1.2;">
     {h1_content}
    </h1>
<p style="font-size: 1.8rem; margin-bottom: 2rem; color: #ffffff !important; text-shadow: none; font-weight: 700; max-width: 900px; margin-left: auto; margin-right: auto; line-height: 1.4;">
     {subtitle if subtitle else 'Professional Property Management Services for Your Community'}
    </p>
<div class="hero-stats" style="font-size: 1.6rem; color: #ffffff !important; margin-bottom: 2.5rem; font-weight: 800; text-shadow: none; letter-spacing: 1px;">
     Trusted Since 2006 • Licensed & Insured • 24/7 Emergency Support
    </div>
<div class="cta-buttons" style="display: flex; gap: 2rem; justify-content: center; flex-wrap: wrap;">
<a href="tel:8476522338" class="btn btn-primary" style="background: #ea580c; border-color: #ea580c; color: white; padding: 18px 36px; font-size: 1.2rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; box-shadow: 0 4px 20px rgba(0,0,0,0.3);">
      Schedule Consultation
     </a>
<a href="../../contact.html" class="btn btn-secondary" style="background: rgba(255,255,255,0.95); color: #111827; border: 2px solid white; padding: 18px 36px; font-size: 1.2rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; box-shadow: 0 4px 20px rgba(0,0,0,0.3);">
      Get Free Quote
     </a>
</div>
</div>
</section>'''
        
        # Replace old hero with new
        new_content = content.replace(old_hero, new_hero)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    """Update all property management pages"""
    property_dir = Path('property-management')
    
    # Get all index.html files in subdirectories
    html_files = list(property_dir.glob('*/index.html'))
    
    print(f"Found {len(html_files)} property management pages to update")
    
    updated = 0
    for i, filepath in enumerate(html_files):
        # Rotate through images for variety
        image = IMAGES[i % len(IMAGES)]
        
        if update_hero_section(filepath, image):
            print(f"[OK] Updated {filepath.parent.name} with {image}")
            updated += 1
        else:
            print(f"[FAIL] Failed to update {filepath.parent.name}")
    
    print(f"\nComplete: Updated {updated}/{len(html_files)} pages")

if __name__ == "__main__":
    main()