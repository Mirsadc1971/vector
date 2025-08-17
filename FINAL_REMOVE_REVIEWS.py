import os
import re

base_dir = "property-management"
count = 0
processed = 0

for location in os.listdir(base_dir):
    location_path = os.path.join(base_dir, location)
    if os.path.isdir(location_path):
        index_file = os.path.join(location_path, "index.html")
        
        if os.path.exists(index_file):
            processed += 1
            with open(index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Remove all review sections with multiple patterns
            patterns = [
                # Pattern 1: Review Collection CTA blocks
                r'<!-- Review Collection CTA -->.*?</div>\s*(?=\n|<footer|$)',
                # Pattern 2: Any div with "Managed a Property" text
                r'<div[^>]*>(?:[^<]|<(?!/div>))*?Managed a Property.*?</div>\s*',
                # Pattern 3: Review sections with styling
                r'<div style="background: #4285f4;[^"]*">.*?Leave a Review.*?</div>\s*',
                # Pattern 4: Any remaining review CTAs
                r'<div[^>]*>.*?(?:Leave a Review|Share your experience).*?</div>\s*'
            ]
            
            for pattern in patterns:
                content = re.sub(pattern, '', content, flags=re.DOTALL)
            
            if content != original_content:
                with open(index_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                count += 1
                print(f"Cleaned {location}")

print(f"\nProcessed {processed} files, cleaned {count} files")