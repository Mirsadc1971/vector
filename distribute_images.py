import os
import re

# List of available images to distribute
images = [
    "manage369bedroom1740maplewood.jpg",
    "manage369livingroomskokie.jpg", 
    "northbrook2manage369.jpg",
    "buck4manage369.jpg",
    "chestnut2manage369.jpg",
    "kenmore2manage369.jpg",
    "northfield1manage369.jpg",
    "northfield2manage369.jpg",
    "Manage3693.jpg",
    "manage369randolphstation.jpg",
    "manage369widowview.jpg",
    "manstandingmanage369.jpg",
    "businessman-skyline.jpg"
]

base_dir = "property-management"
locations = []

# Get all location directories
for location in os.listdir(base_dir):
    location_path = os.path.join(base_dir, location)
    if os.path.isdir(location_path):
        locations.append(location)

# Sort locations for consistent distribution
locations.sort()

print(f"Found {len(locations)} locations")
print(f"Using {len(images)} different images")

# Distribute images across locations
for i, location in enumerate(locations):
    # Cycle through images
    image_index = i % len(images)
    image_name = images[image_index]
    
    index_file = os.path.join(base_dir, location, "index.html")
    
    if os.path.exists(index_file):
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update Open Graph image meta tag
        pattern = r'(<meta property="og:image" content="https://manage369\.com/images/)[^"]+(")'
        replacement = r'\g<1>' + image_name + r'\g<2>'
        new_content = re.sub(pattern, replacement, content)
        
        # Update Twitter Card image meta tag
        pattern2 = r'(<meta name="twitter:image" content="https://manage369\.com/images/)[^"]+(")'
        new_content = re.sub(pattern2, r'\g<1>' + image_name + r'\g<2>', new_content)
        
        if new_content != content:
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"{location}: {image_name}")

print(f"\nImage distribution complete!")
print(f"Each image is used approximately {len(locations) // len(images)} times")