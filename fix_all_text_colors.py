import os
import re
from pathlib import Path

def fix_text_colors(file_path):
    """Fix all text color issues - make everything readable"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes_made = False
    
    # Fix white text on white/light backgrounds
    replacements = [
        # Service cards with white text on light backgrounds
        (r'color:\s*#ffffff;[^"]*margin-bottom:\s*2rem;">Our', 'color: #1f2937; margin-bottom: 2rem;">Our'),
        (r'color:\s*#ffffff;[^"]*0;">([^<]+)</h3>', r'color: #1f2937; margin: 0 0 0.5rem 0;">\1</h3>'),
        (r'color:\s*#ffffff;[^"]*0;">([^<]+)</h2>', r'color: #1f2937; margin-bottom: 2rem;">\1</h2>'),
        (r'text-decoration:\s*none;\s*color:\s*#ffffff;', 'text-decoration: none; color: #333;'),
        
        # Related areas section with white text
        (r'<h2 style="text-align: center; color: #ffffff;', '<h2 style="text-align: center; color: #1f2937;'),
        (r'<h3 style="margin: 0; font-size: 1.1rem;">([^<]+)</h3>', r'<h3 style="margin: 0; font-size: 1.1rem; color: #1f2937;">\1</h3>'),
        (r'<p style="margin: 0.5rem 0 0 0; color: #ffffff;', '<p style="margin: 0.5rem 0 0 0; color: #666;'),
        
        # Service section cards
        (r'background: #f8f9fa;[^"]*color: #ffffff;', 'background: #f8f9fa; padding: 1.5rem; text-decoration: none; color: #333;'),
        
        # Call to action buttons on light backgrounds
        (r'background: white; color: #ffffff;', 'background: white; color: #1f2937;'),
        
        # Fix sections that have white background with white text
        (r'style="background: white;[^"]*<h2[^>]*color: #ffffff', 'style="background: white; padding: 3rem 2rem;"><div style="max-width: 1200px; margin: 0 auto;"><h2 style="text-align: center; color: #1f2937'),
        
        # Fix any remaining white text on non-dark backgrounds
        (r'background: (?:white|#f8f9fa|#f3f4f6)[^"]*color: #ffffff', lambda m: m.group(0).replace('color: #ffffff', 'color: #333')),
    ]
    
    for pattern, replacement in replacements:
        if callable(replacement):
            matches = list(re.finditer(pattern, content))
            for match in reversed(matches):
                new_text = replacement(match)
                if new_text != match.group(0):
                    content = content[:match.start()] + new_text + content[match.end():]
                    changes_made = True
        else:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                changes_made = True
    
    # Fix professional associations text (CAI, IREM, etc)
    if 'CAI National Member | IREM Certified' in content:
        # Make sure it's visible
        content = re.sub(
            r'<div style="text-align: center; margin-bottom: 10px; color: #[0-9a-f]{6}; font-size: 0.9rem;">',
            '<div style="text-align: center; margin-bottom: 10px; color: #9ca3af; font-size: 0.9rem;">',
            content
        )
        changes_made = True
    
    # Write back if changes were made
    if changes_made:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Process all HTML files
html_files = []

for file in Path('.').glob('*.html'):
    html_files.append(str(file))

for file in Path('.').rglob('*/index.html'):
    html_files.append(str(file))

print(f"Fixing text colors in {len(html_files)} HTML files")
print("-" * 50)

updated = 0
skipped = 0

for file in html_files:
    try:
        if fix_text_colors(file):
            print(f"[FIXED] {file}")
            updated += 1
        else:
            skipped += 1
    except Exception as e:
        print(f"[ERROR] {file}: {str(e)}")

print("-" * 50)
print(f"\n[COMPLETE] Text color fixes complete!")
print(f"  Files updated: {updated}")
print(f"  Files unchanged: {skipped}")