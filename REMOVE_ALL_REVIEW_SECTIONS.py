import os
import re

base_dir = "property-management"
processed = 0
modified = 0

for location in os.listdir(base_dir):
    location_path = os.path.join(base_dir, location)
    if os.path.isdir(location_path):
        index_file = os.path.join(location_path, "index.html")
        
        if os.path.exists(index_file):
            processed += 1
            with open(index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Pattern to remove entire Review Collection CTA sections
            # This will match from the comment to the closing div
            pattern = r'<!-- Review Collection CTA -->.*?</div>\s*'
            
            # Remove all occurrences (there may be multiple)
            new_content = re.sub(pattern, '', content, flags=re.DOTALL)
            
            # Also remove any standalone review divs with the blue background
            pattern2 = r'<div style="background: #4285f4;[^>]*>.*?(?:Managed a Property|Leave a Review|Share your experience).*?</div>\s*'
            new_content = re.sub(pattern2, '', new_content, flags=re.DOTALL)
            
            if new_content != original_content:
                with open(index_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                modified += 1
                print(f"Removed review sections from {location}")

print(f"\nProcessed {processed} files")
print(f"Modified {modified} files")