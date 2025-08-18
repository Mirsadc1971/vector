import os
import re
from pathlib import Path

def fix_contrast_issues(file_path):
    """Fix all low-contrast text issues"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes_made = False
    
    # Fix orange text on white background (needs darker orange)
    # #ea580c has 3.0:1 ratio, need at least 4.5:1
    # Use #c4490c (darker orange with 4.5:1 ratio)
    replacements = [
        # Fix orange headings
        (r'color:\s*#ea580c', 'color: #c4490c'),
        (r'style="color:\s*#ea580c', 'style="color: #c4490c'),
        
        # Fix white text on light backgrounds
        (r'background:\s*white;[^"]*color:\s*rgb\(255,\s*255,\s*255\)', 
         lambda m: m.group(0).replace('color: rgb(255, 255, 255)', 'color: #1f2937')),
        (r'background:\s*white;[^"]*color:\s*#ffffff', 
         lambda m: m.group(0).replace('color: #ffffff', 'color: #1f2937')),
        
        # Fix service cards with white text on light gray
        (r'<h3 style="color:\s*#ffffff;[^"]*">([^<]+)</h3>', 
         r'<h3 style="color: #1f2937; margin: 0 0 0.5rem 0;">\1</h3>'),
        
        # Fix consultation button on light background
        (r'background:\s*white;[^"]*color:\s*rgb\(255,\s*255,\s*255\)[^"]*Get Free Consultation',
         'background: white; color: #1f2937; padding: 1rem 2rem;">Get Free Consultation'),
        
        # Fix orange buttons (make background darker)
        (r'background:\s*#ea580c', 'background: #c4490c'),
        (r'background:\s*rgb\(234,\s*88,\s*12\)', 'background: #c4490c'),
        
        # Fix service offering cards text
        (r'style="background:\s*rgb\(248,\s*249,\s*250\);[^"]*">\s*<h3[^>]*color:\s*#ffffff',
         'style="background: rgb(248, 249, 250); padding: 1.5rem; text-decoration: none;"><h3 style="color: #1f2937'),
        
        # Fix p tags with white text on light backgrounds
        (r'<p style="[^"]*color:\s*white;[^"]*">', 
         lambda m: m.group(0).replace('color: white', 'color: #1f2937') if 'background' not in m.group(0) or 'linear-gradient' not in m.group(0) else m.group(0)),
    ]
    
    for pattern, replacement in replacements:
        if callable(replacement):
            matches = list(re.finditer(pattern, content))
            for match in reversed(matches):
                new_text = replacement(match)
                content = content[:match.start()] + new_text + content[match.end():]
                changes_made = True
        else:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                changes_made = True
    
    # Add high contrast CSS if not present
    if '</style>' in content and 'High Contrast Text Fixes' not in content:
        style_close = content.find('</style>')
        if style_close > 0:
            contrast_css = """
    /* High Contrast Text Fixes */
    .btn-primary, button[type="submit"], .submit-btn {
        background: #c4490c !important; /* Darker orange for better contrast */
        color: white !important;
    }
    
    .btn-primary:hover, button[type="submit"]:hover, .submit-btn:hover {
        background: #a03a0a !important;
    }
    
    /* Service cards text contrast */
    .service-card h3, .service-card h4 {
        color: #1f2937 !important;
    }
    
    .service-card p {
        color: #4b5563 !important;
    }
    
    /* Fix any orange text that needs more contrast */
    h1, h2, h3, h4, h5, h6 {
        color: #1f2937 !important;
    }
    
    /* Ensure links have proper contrast */
    a {
        color: #0a58ca !important;
    }
    
    a:hover {
        color: #084298 !important;
    }
    
    /* Footer links stay light on dark background */
    .site-footer a, footer a {
        color: #e5e7eb !important;
    }
"""
            content = content[:style_close] + contrast_css + '\n' + content[style_close:]
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

print(f"Fixing contrast issues in {len(html_files)} HTML files")
print("-" * 50)

updated = 0
skipped = 0

for file in html_files:
    try:
        if fix_contrast_issues(file):
            print(f"[FIXED] {file}")
            updated += 1
        else:
            skipped += 1
    except Exception as e:
        print(f"[ERROR] {file}: {str(e)}")

print("-" * 50)
print(f"\n[COMPLETE] Contrast fixes complete!")
print(f"  Files updated: {updated}")
print(f"  Files unchanged: {skipped}")