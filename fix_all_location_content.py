#!/usr/bin/env python3
import os
import glob
import re

def fix_location_content(file_path):
    """Fix the location-content div/section issue"""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original = content
    fixed = False
    
    # Find and fix the pattern where location-content is a div outside of sections
    # Pattern 1: </section>\n\n        <div class="location-content">
    pattern1 = re.compile(r'(</section>\s*\n\s*)<div class="location-content">')
    if pattern1.search(content):
        content = pattern1.sub(r'\1<section class="location-content">', content)
        fixed = True
        print(f"  - Fixed opening location-content div -> section")
    
    # Pattern 2: Find the closing of location-content and fix it
    # Look for </div>\n        </div>\n\n    <section class="why-choose">
    pattern2 = re.compile(r'(</div>\s*\n\s*</div>)(\s*\n\s*<section class="why-choose">)')
    if 'class="location-content">' in content and pattern2.search(content):
        # Need to find the right closing divs for location-content
        # Count from location-content to why-choose section
        loc_start = content.find('class="location-content">')
        if loc_start > 0:
            why_start = content.find('<section class="why-choose">', loc_start)
            if why_start > 0:
                # Find the last </div></div> pattern before why-choose
                section_between = content[loc_start:why_start]
                last_double_div = content.rfind('</div>\n        </div>', loc_start, why_start)
                if last_double_div > 0:
                    # Replace with </div></section>
                    before = content[:last_double_div]
                    after = content[last_double_div:]
                    after = after.replace('</div>\n        </div>', '</div>\n    </section>', 1)
                    content = before + after
                    fixed = True
                    print(f"  - Fixed closing location-content div -> section")
    
    # Alternative pattern where it might be differently formatted
    if not fixed and '<div class="location-content">' in content:
        # Check if this div is outside a section
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if '<div class="location-content">' in line:
                # Check previous lines for </section>
                found_section_close = False
                for j in range(max(0, i-5), i):
                    if '</section>' in lines[j]:
                        found_section_close = True
                        break
                
                if found_section_close:
                    # This div should be a section
                    lines[i] = line.replace('<div class="location-content">', '<section class="location-content">')
                    
                    # Find the corresponding closing div
                    depth = 1
                    for j in range(i+1, len(lines)):
                        if '<div' in lines[j]:
                            depth += lines[j].count('<div')
                        if '</div>' in lines[j]:
                            depth -= lines[j].count('</div>')
                        if depth == 0:
                            # This is the closing div for location-content
                            # Check if next non-empty line is why-choose section
                            for k in range(j+1, min(j+5, len(lines))):
                                if '<section class="why-choose">' in lines[k]:
                                    lines[j] = lines[j].replace('</div>', '</section>')
                                    fixed = True
                                    print(f"  - Fixed location-content structure")
                                    break
                            break
                    
                    if fixed:
                        content = '\n'.join(lines)
                    break
    
    if fixed:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Get all property management HTML files
property_files = glob.glob(r"C:\Users\mirsa\manage369-live\property-management\*\index.html")

print(f"Checking {len(property_files)} property pages for location-content issues...\n")

fixed = []
already_ok = []

for file_path in property_files:
    dir_name = os.path.basename(os.path.dirname(file_path))
    print(f"Checking {dir_name}...")
    
    if fix_location_content(file_path):
        fixed.append(dir_name)
    else:
        already_ok.append(dir_name)

print(f"\n" + "="*50)
print(f"Total fixed: {len(fixed)} pages")
print(f"Already OK: {len(already_ok)} pages")

if fixed:
    print("\nFixed pages:")
    for page in fixed:
        print(f"  - {page}")