#!/usr/bin/env python3
import os
import glob
import re

def fix_unbalanced_tags(file_path):
    """Fix unbalanced div/section tags and duplicate closing tags"""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original = content
    fixed = False
    
    # Fix duplicate </body> and </html> tags
    if content.count('</body>') > 1:
        # Keep only the last occurrence
        parts = content.rsplit('</body>', 1)
        if len(parts) == 2:
            # Remove all earlier occurrences
            parts[0] = parts[0].replace('</body>', '')
            content = '</body>'.join(parts)
            fixed = True
            print(f"  - Removed duplicate </body> tags")
    
    if content.count('</html>') > 1:
        # Keep only the last occurrence
        parts = content.rsplit('</html>', 1)
        if len(parts) == 2:
            # Remove all earlier occurrences
            parts[0] = parts[0].replace('</html>', '')
            content = '</html>'.join(parts)
            fixed = True
            print(f"  - Removed duplicate </html> tags")
    
    # Fix unbalanced section tags where location-content doesn't close properly
    if '<section class="location-content">' in content:
        # Check if there's a closing </section> before why-choose
        loc_pos = content.find('<section class="location-content">')
        why_pos = content.find('<section class="why-choose">', loc_pos)
        
        if loc_pos > 0 and why_pos > 0:
            between = content[loc_pos:why_pos]
            
            # Count divs and sections in between
            open_divs = between.count('<div')
            close_divs = between.count('</div>')
            open_sections = between.count('<section')
            close_sections = between.count('</section>')
            
            # If location-content section is not closed
            if open_sections > close_sections:
                # Find the last </div> before why-choose and check if it should be </section>
                last_div_close = content.rfind('</div>', loc_pos, why_pos)
                if last_div_close > 0:
                    # Check if this is the wrapper closing
                    wrapper_close_pattern = r'(\s*</div>\s*</div>\s*)(<section class="why-choose">)'
                    match = re.search(wrapper_close_pattern, content[last_div_close-100:why_pos+50])
                    if match:
                        # The second </div> should be </section>
                        before_why = content[:why_pos]
                        after_why = content[why_pos:]
                        
                        # Find and replace the pattern
                        before_why = re.sub(r'(</div>\s*)(</div>)(\s*$)', r'\1</section>\3', before_why.rsplit('</div>\n', 2)[0] + '</div>\n')
                        content = before_why + after_why
                        fixed = True
                        print(f"  - Fixed unclosed location-content section")
    
    # Fix cases where there's one extra </div> (common pattern)
    open_divs = content.count('<div')
    close_divs = content.count('</div>')
    
    if close_divs == open_divs + 1:
        # Find location-content area and check if an extra </div> should be </section>
        if '<section class="location-content">' in content:
            # Find the problematic area
            lines = content.split('\n')
            for i in range(len(lines)-1, 0, -1):
                if '</div>' in lines[i] and i > 0:
                    # Check if previous line also has </div>
                    if '</div>' in lines[i-1]:
                        # Check if next significant line is why-choose
                        for j in range(i+1, min(i+5, len(lines))):
                            if '<section class="why-choose">' in lines[j]:
                                # This </div> should be </section>
                                lines[i] = lines[i].replace('</div>', '</section>')
                                content = '\n'.join(lines)
                                fixed = True
                                print(f"  - Fixed extra </div> -> </section>")
                                break
                        if fixed:
                            break
    
    # Fix cases where there's one less </div> (also common)
    open_divs = content.count('<div')
    close_divs = content.count('</div>')
    
    if open_divs == close_divs + 1:
        # Usually missing a </div> before </section>
        # Find sections that might be missing closing divs
        pattern = r'(\s*)(<section class="why-choose">)'
        match = re.search(pattern, content)
        if match:
            indent = match.group(1)
            # Add missing </div> before the section
            content = re.sub(pattern, r'\1</div>\n\1\2', content, count=1)
            fixed = True
            print(f"  - Added missing </div> before why-choose section")
    
    if fixed:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# List of pages with issues from the check
problem_pages = [
    'elk-grove-village', 'elmwood-park', 'forest-glen', 'franklin-park',
    'harwood-heights', 'jefferson-park', 'loop', 'mayfair', 'norridge',
    'north-park', 'norwood-park', 'oak-park', 'old-irving-park',
    'portage-park', 'prospect-heights', 'sauganash', 'schiller-park',
    'south-loop', 'the-glen', 'vernon-hills', 'west-loop', 'winnetka',
    'wood-dale'
]

print(f"Fixing {len(problem_pages)} pages with structural issues...\n")

fixed = []
not_fixed = []

for page_name in problem_pages:
    file_path = rf"C:\Users\mirsa\manage369-live\property-management\{page_name}\index.html"
    print(f"Fixing {page_name}...")
    
    if os.path.exists(file_path):
        if fix_unbalanced_tags(file_path):
            fixed.append(page_name)
        else:
            not_fixed.append(page_name)
            print(f"  - No automatic fix applied")
    else:
        print(f"  - File not found!")

print(f"\n" + "="*50)
print(f"Fixed: {len(fixed)} pages")
print(f"Not fixed: {len(not_fixed)} pages")

if not_fixed:
    print(f"\nPages that need manual review:")
    for page in not_fixed:
        print(f"  - {page}")