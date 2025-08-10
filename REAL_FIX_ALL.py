#!/usr/bin/env python3
import os
import glob
import re

def real_fix_header_structure(content):
    """Fix the actual header structure issues"""
    fixed = False
    
    # Find header section
    header_start = content.find('<header class="header">')
    if header_start == -1:
        return content, False
    
    header_end = content.find('</header>', header_start)
    if header_end == -1:
        return content, False
        
    # Extract header section
    header_section = content[header_start:header_end + 9]
    original_header = header_section
    
    # Check if header-content div is properly closed
    if '<div class="header-content">' in header_section:
        # Count divs in header
        header_divs_open = header_section.count('<div')
        header_divs_close = header_section.count('</div>')
        
        # If header-content is not closed properly
        if header_divs_open > header_divs_close:
            # Find where mobile menu starts
            mobile_menu_pos = header_section.find('<div class="mobile-menu"')
            if mobile_menu_pos > 0:
                # Insert </div> before mobile menu to close header-content
                header_section = header_section[:mobile_menu_pos] + '        </div>\n        \n        ' + header_section[mobile_menu_pos:]
                fixed = True
            else:
                # No mobile menu, close header-content before </header>
                header_section = header_section.replace('</header>', '        </div>\n    </header>')
                fixed = True
    
    # Fix any misplaced comments or elements
    header_section = header_section.replace('<!-- Hero Section -->\n    </header>', '</header>')
    header_section = header_section.replace('    <!-- Hero Section -->\n    </header>', '</header>')
    
    if header_section != original_header:
        fixed = True
        content = content[:header_start] + header_section + content[header_end + 9:]
    
    return content, fixed

def fix_location_content_structure(content):
    """Fix location-content div that should be section"""
    fixed = False
    
    # Pattern: <div class="location-content"> after </section>
    pattern = re.compile(r'(</section>\s*\n\s*)<div class="location-content">')
    if pattern.search(content):
        content = pattern.sub(r'\1<section class="location-content">', content)
        fixed = True
        
        # Find and fix the closing tag
        # Look for pattern like </div>\n    </div>\n\n    <section class="why-choose">
        pattern2 = re.compile(r'(</div>\s*\n\s*</div>)(\s*\n\s*<section class="why-choose">)')
        if pattern2.search(content):
            content = pattern2.sub(r'</div>\n    </section>\2', content)
        else:
            # Alternative pattern
            pattern3 = re.compile(r'(</div>\s*\n\s*</div>)(\s*\n\s*<section class="faq-section">)')
            if pattern3.search(content):
                content = pattern3.sub(r'</div>\n    </section>\2', content)
    
    return content, fixed

def fix_all_issues(file_path):
    """Apply all fixes to a file"""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original = content
    any_fixed = False
    
    # Fix header structure
    content, fixed1 = real_fix_header_structure(content)
    if fixed1:
        print(f"  - Fixed header structure")
        any_fixed = True
    
    # Fix location-content structure
    content, fixed2 = fix_location_content_structure(content)
    if fixed2:
        print(f"  - Fixed location-content structure")
        any_fixed = True
    
    # Remove duplicate closing tags
    if content.count('</body>') > 1:
        parts = content.rsplit('</body>', 1)
        parts[0] = parts[0].replace('</body>', '')
        content = '</body>'.join(parts)
        print(f"  - Removed duplicate </body> tags")
        any_fixed = True
    
    if content.count('</html>') > 1:
        parts = content.rsplit('</html>', 1)
        parts[0] = parts[0].replace('</html>', '')
        content = '</html>'.join(parts)
        print(f"  - Removed duplicate </html> tags")
        any_fixed = True
    
    # Ensure closing tags exist
    if '</body>' not in content:
        script_pos = content.rfind('</script>')
        if script_pos > 0:
            content = content[:script_pos+9] + '\n</body>\n</html>'
            print(f"  - Added missing </body> and </html>")
            any_fixed = True
    
    if any_fixed:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Process ALL property management pages
property_files = glob.glob(r"C:\Users\mirsa\manage369-live\property-management\*\index.html")

print(f"Applying REAL fixes to {len(property_files)} property pages...\n")

fixed_pages = []
for file_path in property_files:
    dir_name = os.path.basename(os.path.dirname(file_path))
    print(f"Processing {dir_name}...")
    
    if fix_all_issues(file_path):
        fixed_pages.append(dir_name)

print(f"\n" + "="*60)
print(f"Fixed {len(fixed_pages)} pages")
if fixed_pages:
    print("\nPages fixed:")
    for page in fixed_pages:
        print(f"  - {page}")