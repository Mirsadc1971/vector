#!/usr/bin/env python3
import os
import glob

def fix_final_issues(file_path):
    """Final comprehensive fix for remaining issues"""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original = content
    fixed = False
    
    # Count tags
    open_divs = content.count('<div')
    close_divs = content.count('</div>')
    
    # If one more open div than close div
    if open_divs == close_divs + 1:
        # Add missing </div> before </body>
        body_pos = content.rfind('</body>')
        if body_pos > 0:
            # Add a </div> before the last script/body tags
            script_pos = content.rfind('</script>', 0, body_pos)
            if script_pos > 0:
                content = content[:script_pos+9] + '\n    </div>' + content[script_pos+9:]
                fixed = True
                print(f"  - Added missing </div> before </body>")
    
    # If one more close div than open div
    elif close_divs == open_divs + 1:
        # This might be a </div> that should be </section>
        # Check for location-content pattern
        if '<section class="location-content">' in content:
            # Find if there's a </div> right before why-choose that should be </section>
            import re
            pattern = r'(</div>)(\s*\n\s*<section class="why-choose">)'
            if re.search(pattern, content):
                content = re.sub(pattern, r'</section>\2', content, count=1)
                fixed = True
                print(f"  - Changed </div> to </section> before why-choose")
    
    # Remove any remaining duplicate </body> or </html> tags
    if content.count('</body>') > 1:
        parts = content.rsplit('</body>', 1)
        if len(parts) == 2:
            parts[0] = parts[0].replace('</body>', '')
            content = '</body>'.join(parts)
            fixed = True
            print(f"  - Removed duplicate </body> tags")
    
    if content.count('</html>') > 1:
        parts = content.rsplit('</html>', 1)
        if len(parts) == 2:
            parts[0] = parts[0].replace('</html>', '')
            content = '</html>'.join(parts)
            fixed = True
            print(f"  - Removed duplicate </html> tags")
    
    if fixed:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# List of remaining problem pages
problem_pages = [
    'loop', 'old-irving-park', 'portage-park', 'prospect-heights',
    'sauganash', 'south-loop', 'vernon-hills', 'west-loop', 'wood-dale'
]

print(f"Applying final fixes to {len(problem_pages)} remaining pages...\n")

fixed = []
still_broken = []

for page_name in problem_pages:
    file_path = rf"C:\Users\mirsa\manage369-live\property-management\{page_name}\index.html"
    print(f"Fixing {page_name}...")
    
    if os.path.exists(file_path):
        if fix_final_issues(file_path):
            fixed.append(page_name)
        else:
            still_broken.append(page_name)
            print(f"  - No issues detected")
    else:
        print(f"  - File not found!")

print(f"\n" + "="*50)
print(f"Fixed: {len(fixed)} pages")
print(f"Still need review: {len(still_broken)} pages")

if still_broken:
    print(f"\nPages that may still need review:")
    for page in still_broken:
        print(f"  - {page}")