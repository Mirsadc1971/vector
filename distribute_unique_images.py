import os
import random
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
print(f"Available images: {len(property_images)}")

# Distribute images across all directories
image_assignments = {}
for i, directory in enumerate(property_dirs):
    # Cycle through images if we have more directories than images
    image_index = i % len(property_images)
    assigned_image = property_images[image_index]
    image_assignments[directory.name] = assigned_image
    
    # Read the index.html file
    index_file = directory / "index.html"
    if index_file.exists():
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace any existing image references in og:image and twitter:image
        original_content = content
        
        # Replace in og:image meta tag
        import re
        content = re.sub(
            r'(<meta property="og:image" content="https://manage369\.com/images/)[^"]+(")',
            rf'\1{assigned_image}\2',
            content
        )
        
        # Replace in twitter:image meta tag
        content = re.sub(
            r'(<meta name="twitter:image" content="https://manage369\.com/images/)[^"]+(")',
            rf'\1{assigned_image}\2',
            content
        )
        
        # Replace in any img src tags that reference property images
        content = re.sub(
            r'(<img[^>]+src="(?:\.\./)*images/)[^"]+\.(jpg|webp)(")',
            rf'\1{assigned_image}\3',
            content
        )
        
        # Write back if changes were made
        if content != original_content:
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[OK] {directory.name}: assigned {assigned_image}")
        else:
            print(f"     {directory.name}: no changes needed")

# Print summary
print(f"\n[COMPLETE] Image distribution complete!")
print(f"Total directories processed: {len(property_dirs)}")
print(f"Each image used approximately {len(property_dirs) // len(property_images)} times")

# Save the distribution map
with open("image_distribution_map.txt", "w") as f:
    f.write("IMAGE DISTRIBUTION MAP\n")
    f.write("=" * 50 + "\n\n")
    for dir_name, img_name in sorted(image_assignments.items()):
        f.write(f"{dir_name}: {img_name}\n")
    
print("\nImage distribution map saved to image_distribution_map.txt")