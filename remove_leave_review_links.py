import os
import re

# Remove from homepage
print("Removing Leave Review link from homepage...")
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the Leave Review link
pattern = r'<a href=["\']leave-review\.html["\'][^>]*>.*?Leave Review.*?</a>'
new_content = re.sub(pattern, '', content, flags=re.DOTALL)

if new_content != content:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Removed from homepage")

# Remove from all property management pages
base_dir = "property-management"
count = 0

for location in os.listdir(base_dir):
    location_path = os.path.join(base_dir, location)
    if os.path.isdir(location_path):
        index_file = os.path.join(location_path, "index.html")
        
        if os.path.exists(index_file):
            with open(index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            
            # Remove any Leave Review links
            patterns = [
                r'<a href=["\'][^"\']*leave-review[^"\']*["\'][^>]*>.*?Leave Review.*?</a>',
                r'<a[^>]*style=["\'][^"\']*background:\s*#ff9500[^"\']*["\'][^>]*>.*?Leave Review.*?</a>'
            ]
            
            for pattern in patterns:
                content = re.sub(pattern, '', content, flags=re.DOTALL)
            
            if content != original:
                with open(index_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                count += 1
                print(f"Removed from {location}")

print(f"\nTotal files cleaned: {count}")