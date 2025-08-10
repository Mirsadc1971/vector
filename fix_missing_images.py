#!/usr/bin/env python3
import glob

# Pages that need fixing
pages_to_fix = [
    'south-loop', 'west-loop', 'prospect-heights', 'loop', 
    'edgewater', 'logan-square', 'hyde-park', 'dunning', 'bucktown'
]

# Replace with an existing image
old_image = "manage369kitchenevanston.webp"
new_image = "manage369livingroomskokie.jpg"  # Using a nice existing image

fixed = 0
for page in pages_to_fix:
    file_path = rf"C:\Users\mirsa\manage369-live\property-management\{page}\index.html"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if old_image in content:
            content = content.replace(old_image, new_image)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {page}")
            fixed += 1
        else:
            print(f"No change needed: {page}")
    except Exception as e:
        print(f"Error with {page}: {e}")

print(f"\nTotal fixed: {fixed} pages")