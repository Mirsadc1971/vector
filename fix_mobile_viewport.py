"""
Fix mobile viewport issues across all pages
"""

import os
import re

def add_mobile_fixes(content):
    """Add CSS to prevent horizontal overflow on mobile"""
    
    # Check if we already have the mobile overflow fix
    if 'overflow-x: hidden' in content and 'body {' in content:
        return content
    
    # Find the closing </head> tag
    head_close = content.find('</head>')
    
    if head_close == -1:
        return content
    
    # Mobile overflow prevention CSS
    mobile_fix = """
    <style>
        /* Prevent horizontal overflow on mobile */
        html, body {
            overflow-x: hidden;
            width: 100%;
        }
        
        * {
            box-sizing: border-box;
        }
        
        /* Ensure all containers respect viewport width */
        section, div, article, aside, header, footer, main {
            max-width: 100vw;
        }
        
        /* Fix for tables on mobile */
        @media (max-width: 768px) {
            table {
                display: block;
                overflow-x: auto;
                white-space: nowrap;
            }
        }
        
        /* Ensure images don't cause overflow */
        img {
            max-width: 100%;
            height: auto;
        }
    </style>
"""
    
    # Insert before </head>
    content = content[:head_close] + mobile_fix + content[head_close:]
    
    return content

# Process all HTML files
root_dir = 'C:\\Users\\mirsa\\manage369-live'
files_updated = 0

# Process root HTML files
for filename in os.listdir(root_dir):
    if filename.endswith('.html'):
        filepath = os.path.join(root_dir, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = add_mobile_fixes(content)
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            files_updated += 1
            print(f"Updated: {filename}")

# Process property management pages
prop_dir = os.path.join(root_dir, 'property-management')
for location in os.listdir(prop_dir):
    if location.endswith('.html'):
        filepath = os.path.join(prop_dir, location)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = add_mobile_fixes(content)
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            files_updated += 1
            print(f"Updated: property-management/{location}")
    elif os.path.isdir(os.path.join(prop_dir, location)):
        index_file = os.path.join(prop_dir, location, 'index.html')
        if os.path.exists(index_file):
            with open(index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = add_mobile_fixes(content)
            
            if new_content != content:
                with open(index_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                files_updated += 1
                print(f"Updated: property-management/{location}/index.html")

# Process service pages
service_dir = os.path.join(root_dir, 'services')
if os.path.exists(service_dir):
    for filename in os.listdir(service_dir):
        if filename.endswith('.html'):
            filepath = os.path.join(service_dir, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = add_mobile_fixes(content)
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                files_updated += 1
                print(f"Updated: services/{filename}")

# Process blog pages  
blog_dir = os.path.join(root_dir, 'blog')
if os.path.exists(blog_dir):
    for filename in os.listdir(blog_dir):
        if filename.endswith('.html'):
            filepath = os.path.join(blog_dir, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = add_mobile_fixes(content)
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                files_updated += 1
                print(f"Updated: blog/{filename}")

print(f"\n[COMPLETE] Added mobile viewport fixes to {files_updated} pages")