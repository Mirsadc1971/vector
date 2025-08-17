import os
import re

base_dir = "property-management"
count = 0

for location in os.listdir(base_dir):
    location_path = os.path.join(base_dir, location) 
    if os.path.isdir(location_path):
        index_file = os.path.join(location_path, "index.html")
        
        if os.path.exists(index_file):
            with open(index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_len = len(content)
            
            # Remove all review CTAs - they appear between footer comment and footer tag
            content = re.sub(
                r'<!-- Review Collection CTA -->.*?(?=<footer>)',
                '',
                content,
                flags=re.DOTALL
            )
            
            # Also remove any standalone review divs
            content = re.sub(
                r'<div[^>]*style="[^"]*background:\s*#4285f4[^"]*"[^>]*>(?:[^<]|<(?!/div))*?Managed a Property(?:[^<]|<(?!/div))*?</div>',
                '',
                content,
                flags=re.DOTALL | re.IGNORECASE
            )
            
            # Remove duplicate Google Maps sections
            map_pattern = r'<!-- Google Maps Integration.*?</section>'
            matches = list(re.finditer(map_pattern, content, re.DOTALL))
            if len(matches) > 1:
                for match in reversed(matches[1:]):
                    content = content[:match.start()] + content[match.end():]
            
            # Remove Google Reviews links
            content = re.sub(
                r'<a[^>]*>.*?Google Reviews.*?</a>',
                '',
                content,
                flags=re.DOTALL | re.IGNORECASE
            )
            
            if len(content) != original_len:
                with open(index_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                count += 1
                print(f"Fixed {location}")

print(f"\nCleaned {count} files")