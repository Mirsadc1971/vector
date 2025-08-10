#!/usr/bin/env python3
import glob
import re

# Google Analytics code to add
ga_code = """    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-496518917"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-496518917');
    </script>
</head>"""

property_files = glob.glob(r"C:\Users\mirsa\manage369-live\property-management\*\index.html")

fixed = 0
already_has = 0

for file_path in property_files:
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Check if already has analytics
    if 'G-496518917' in content or 'gtag' in content:
        already_has += 1
        continue
    
    # Add GA code before </head>
    if '</head>' in content:
        content = content.replace('</head>', ga_code)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed += 1
        print(f"Added GA to: {file_path.split('\\')[-2]}")

print(f"\n{'='*50}")
print(f"Added Google Analytics to: {fixed} pages")
print(f"Already had Analytics: {already_has} pages")
print(f"Total pages processed: {len(property_files)}")