"""
Check image distribution across property pages
"""

import os
import re
from collections import Counter

image_counter = Counter()
pages_checked = 0

prop_dir = 'C:\\Users\\mirsa\\manage369-live\\property-management'

for location in os.listdir(prop_dir):
    if location == 'index.html' or location == 'index-old.html':
        continue
        
    filepath = os.path.join(prop_dir, location, 'index.html')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find hero image
        match = re.search(r"url\(['\"].*?/([^/'\"]+\.jpg)", content)
        if match:
            image = match.group(1)
            image_counter[image] += 1
            pages_checked += 1
            
print(f"Total pages checked: {pages_checked}")
print(f"Unique images used: {len(image_counter)}")
print("\nImage distribution:")
for img, count in sorted(image_counter.items(), key=lambda x: x[1], reverse=True):
    print(f"  {img}: {count} pages")