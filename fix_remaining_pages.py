#!/usr/bin/env python3
import os
import glob

def fix_html_file(file_path):
    """Fix HTML structure issues in a single file"""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original_content = content
    fixed = False
    
    # Check if </header> is missing
    if '<header class="header">' in content and '</header>' not in content:
        # Find <section class="hero"> and add </header> before it
        hero_pos = content.find('<section class="hero">')
        if hero_pos > 0:
            # Work backwards to find the proper indentation
            indent_pos = content.rfind('\n', 0, hero_pos)
            if indent_pos > 0:
                content = content[:hero_pos] + '    </header>\n    \n    ' + content[hero_pos:]
                fixed = True
                print(f"  - Added missing </header> tag")
    
    # Check if </body> and </html> are missing at the end
    if not content.rstrip().endswith('</html>'):
        if not content.rstrip().endswith('</body>'):
            # Find the last </script> tag
            last_script_pos = content.rfind('</script>')
            if last_script_pos > 0:
                # Add closing tags after the last script
                end_pos = last_script_pos + 9
                # Check if there's already content after </script>
                remaining = content[end_pos:].strip()
                if not remaining:
                    content = content[:end_pos] + '\n</body>\n</html>'
                else:
                    content = content.rstrip() + '\n</body>\n</html>'
                fixed = True
                print(f"  - Added missing </body> and </html> tags")
        else:
            content = content.rstrip() + '\n</html>'
            fixed = True
            print(f"  - Added missing </html> tag")
    
    if fixed:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Get all property management HTML files
property_dirs = glob.glob(r"C:\Users\mirsa\manage369-live\property-management\*\index.html")

print(f"Checking {len(property_dirs)} property management pages...\n")

fixed_files = []
already_ok = []

for file_path in property_dirs:
    dir_name = os.path.basename(os.path.dirname(file_path))
    print(f"Checking {dir_name}...")
    
    if fix_html_file(file_path):
        fixed_files.append(dir_name)
        print(f"  FIXED\n")
    else:
        already_ok.append(dir_name)
        print(f"  Already OK\n")

print("\n" + "="*50)
print(f"SUMMARY:")
print(f"Fixed: {len(fixed_files)} pages")
print(f"Already OK: {len(already_ok)} pages")

if fixed_files:
    print(f"\nFixed pages:")
    for page in fixed_files:
        print(f"  - {page}")