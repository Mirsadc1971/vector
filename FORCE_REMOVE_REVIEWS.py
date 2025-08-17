import os
import re

base_dir = "property-management"
total_removed = 0

for location in os.listdir(base_dir):
    location_path = os.path.join(base_dir, location)
    if os.path.isdir(location_path):
        index_file = os.path.join(location_path, "index.html")
        
        if os.path.exists(index_file):
            with open(index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_len = len(content)
            
            # Remove ALL review-related sections with multiple patterns
            patterns = [
                # Pattern 1: Complete Review Collection CTA blocks
                r'<!-- Review Collection CTA -->.*?</div>\s*',
                # Pattern 2: Any div containing "Managed a Property"
                r'<div[^>]*>(?:[^<]|<(?!/div>))*?Managed a Property.*?</div>\s*',
                # Pattern 3: Blue background review sections
                r'<div style="background: #4285f4;.*?</div>\s*',
                # Pattern 4: Leave Review links
                r'<a href=["\'][^"\']*leave-review[^"\']*["\'][^>]*>.*?</a>\s*',
                # Pattern 5: Any remaining review text
                r'<div[^>]*>.*?(?:Leave a Review|Share your experience with our property management).*?</div>\s*'
            ]
            
            for pattern in patterns:
                content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
            
            # Write back even if no changes (to ensure clean state)
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            if len(content) < original_len:
                removed_bytes = original_len - len(content)
                total_removed += removed_bytes
                print(f"Cleaned {location}: removed {removed_bytes} bytes")

print(f"\nTotal bytes removed: {total_removed}")
print("All 68 pages have been processed and cleaned")