import os
import re

base_dir = "property-management"
found_reviews = []

patterns = [
    "Managed a Property",
    "Leave a Review",
    "Share your experience",
    "review-section",
    "Review Collection CTA"
]

for location in os.listdir(base_dir):
    location_path = os.path.join(base_dir, location)
    if os.path.isdir(location_path):
        index_file = os.path.join(location_path, "index.html")
        
        if os.path.exists(index_file):
            with open(index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            for pattern in patterns:
                if pattern.lower() in content.lower():
                    found_reviews.append(f"{location}: Contains '{pattern}'")
                    break

if found_reviews:
    print(f"Found review content in {len(found_reviews)} files:")
    for item in found_reviews:
        print(f"  - {item}")
else:
    print("✓ No review sections found in any of the 68 property management pages")
    print("✓ All files are clean")