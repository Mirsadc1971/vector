import os
import re

# List of pages missing favicon (from the earlier check)
missing_favicon_pages = [
    'andersonville', 'beverly', 'bridgeport', 'bronzeville', 'bucktown',
    'edgewater', 'gold-coast', 'humboldt-park', 'irving-park', 'jefferson-park',
    'kenwood', 'lakeview', 'lincoln-park', 'lincoln-square', 'little-italy'
]

favicon_link = '    <link rel="icon" type="image/x-icon" href="/favicon.ico">\n'

for page_dir in missing_favicon_pages:
    file_path = f'property-management/{page_dir}/index.html'
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if favicon is really missing
        if 'favicon' not in content.lower():
            # Add favicon after viewport meta tag
            pattern = r'(    <meta name="viewport"[^>]+>\n)'
            replacement = r'\1' + favicon_link
            
            new_content = re.sub(pattern, replacement, content)
            
            if new_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"[OK] Added favicon to {page_dir}")
            else:
                print(f"[WARN] Could not add favicon to {page_dir} - pattern not found")
        else:
            print(f"[INFO] {page_dir} already has favicon")
    else:
        print(f"[ERROR] {page_dir} page not found")

print("\nFavicon references added to all missing pages!")