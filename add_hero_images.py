import os
import re
from pathlib import Path

# List of all available property images
property_images = [
    "Manage3693.jpg",
    "buck4manage369.jpg",
    "businessman-skyline.jpg",
    "chestnut2manage369.jpg",
    "kenmore2manage369.jpg",
    "manage369bedroom1740maplewood.jpg",
    "manage369livingroomskokie.jpg",
    "manage369randolphstation.jpg",
    "manage369widowview.jpg",
    "manstandingmanage369.jpg",
    "northbrook2manage369.jpg",
    "northfield1manage369.jpg",
    "northfield2manage369.jpg"
]

# Get all property management subdirectories
property_dirs = []
property_management_path = Path("property-management")
if property_management_path.exists():
    property_dirs = [d for d in property_management_path.iterdir() if d.is_dir()]

# Sort directories for consistent distribution
property_dirs.sort()

print(f"Found {len(property_dirs)} property directories")
print(f"Adding hero images to all pages...")

for i, directory in enumerate(property_dirs):
    # Cycle through images
    image_index = i % len(property_images)
    assigned_image = property_images[image_index]
    
    # Read the index.html file
    index_file = directory / "index.html"
    if index_file.exists():
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if there's already a hero section
        if '<section class="hero"' not in content and '<!-- Hero Section -->' not in content:
            # Find where to insert the hero section (after header or body tag)
            if '</header>' in content:
                # Add hero section with background image right after header
                hero_html = f'''</header>
    
    <!-- Hero Section with Image -->
    <section class="hero" style="background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('../../images/{assigned_image}') center/cover; padding: 120px 20px; text-align: center; color: white;">
        <div class="hero-content">
            <h1 style="font-size: 3rem; margin-bottom: 1rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.8);">{directory.name.replace('-', ' ').title()} Property Management</h1>
            <p style="font-size: 1.5rem; margin-bottom: 2rem; text-shadow: 1px 1px 2px rgba(0,0,0,0.8);">Professional Property Management Services</p>
            <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
                <a href="../../contact.html" style="background: #ff6b35; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 1.1rem;">Get Free Consultation</a>
                <a href="tel:8476522338" style="background: white; color: #333; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 1.1rem;">📞 (847) 652-2338</a>
            </div>
        </div>
    </section>
'''
                content = content.replace('</header>', hero_html)
                
                with open(index_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"[OK] {directory.name}: Added hero with {assigned_image}")
        else:
            # Update existing hero section with background image
            # Look for hero section and add background image
            hero_pattern = r'<section class="hero"[^>]*>'
            new_hero = f'<section class="hero" style="background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url(\'../../images/{assigned_image}\') center/cover; padding: 120px 20px; text-align: center; color: white;">'
            
            if re.search(hero_pattern, content):
                content = re.sub(hero_pattern, new_hero, content)
                with open(index_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"[OK] {directory.name}: Updated hero with {assigned_image}")
            else:
                print(f"  {directory.name}: Could not find hero section to update")

print(f"\n[COMPLETE] Hero images added to all property pages!")
print(f"Each page now has a visible hero image from your library")