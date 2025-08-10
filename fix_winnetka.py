#!/usr/bin/env python3
import os

file_path = r"C:\Users\mirsa\manage369-live\property-management\winnetka\index.html"

# Read the file
with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Fix the header closing tag issue
# Find the mobile menu closing div and add </header> after it
if '</header>' not in content:
    # Find where to insert </header>
    hero_pos = content.find('<section class="hero">')
    if hero_pos > 0:
        # Insert </header> before the hero section
        content = content[:hero_pos] + '    </header>\n    \n    ' + content[hero_pos:]
        print("Added missing </header> tag")

# Fix missing closing tags at the end
if not content.rstrip().endswith('</html>'):
    if not content.rstrip().endswith('</body>'):
        # Find the last </script> tag
        last_script_pos = content.rfind('</script>')
        if last_script_pos > 0:
            # Add closing tags after the last script
            content = content[:last_script_pos + 9] + '\n</body>\n</html>' + content[last_script_pos + 9:]
            print("Added missing </body> and </html> tags")
    else:
        content = content.rstrip() + '\n</html>'
        print("Added missing </html> tag")

# Write the fixed content back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Fixed: {file_path}")