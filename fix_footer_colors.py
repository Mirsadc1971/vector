import os
import re
from pathlib import Path

def fix_footer_colors(file_path):
    """Fix footer color contrast issues"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes_made = False
    changes = []
    
    # Fix footer background and text colors
    replacements = [
        # Dark purple background to dark gray/black
        (r'background:\s*#4a148c', 'background: #1f2937'),
        (r'background-color:\s*#4a148c', 'background-color: #1f2937'),
        (r'background:\s*#6a1b9a', 'background: #1f2937'),
        (r'background-color:\s*#6a1b9a', 'background-color: #1f2937'),
        
        # Any purple variations to dark gray
        (r'background:\s*#7b1fa2', 'background: #1f2937'),
        (r'background:\s*#8e24aa', 'background: #1f2937'),
        (r'background:\s*#9c27b0', 'background: #1f2937'),
        (r'background:\s*purple', 'background: #1f2937'),
        
        # Footer specific purple backgrounds
        (r'\.site-footer\s*\{[^}]*background:\s*#[46789abcdef]{6}', lambda m: m.group(0).replace(re.search(r'#[46789abcdef]{6}', m.group(0)).group(0), '#1f2937')),
        (r'footer\s*\{[^}]*background:\s*#[46789abcdef]{6}', lambda m: m.group(0).replace(re.search(r'#[46789abcdef]{6}', m.group(0)).group(0), '#1f2937')),
        
        # Ensure text is white/light
        (r'\.site-footer[^}]*color:\s*#[0-9a-f]{3,6}', lambda m: re.sub(r'color:\s*#[0-9a-f]{3,6}', 'color: #ffffff', m.group(0))),
        (r'footer[^}]*color:\s*#[0-9a-f]{3,6}', lambda m: re.sub(r'color:\s*#[0-9a-f]{3,6}', 'color: #ffffff', m.group(0))),
        
        # Footer links should be light/white
        (r'\.footer-column a\s*\{[^}]*color:\s*#[0-9a-f]{3,6}', lambda m: re.sub(r'color:\s*#[0-9a-f]{3,6}', 'color: #e5e7eb', m.group(0))),
        (r'footer a\s*\{[^}]*color:\s*#[0-9a-f]{3,6}', lambda m: re.sub(r'color:\s*#[0-9a-f]{3,6}', 'color: #e5e7eb', m.group(0))),
    ]
    
    for pattern, replacement in replacements:
        if callable(replacement):
            matches = list(re.finditer(pattern, content))
            for match in reversed(matches):
                new_text = replacement(match)
                if new_text != match.group(0):
                    content = content[:match.start()] + new_text + content[match.end():]
                    changes_made = True
                    changes.append(f"Fixed footer color pattern: {pattern[:30]}...")
        else:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                changes_made = True
                changes.append(f"Replaced {pattern[:30]}... with better contrast")
    
    # Add specific footer styles if not present
    if '.site-footer' in content or 'footer' in content:
        # Check if we need to add footer styles
        if not re.search(r'\.site-footer\s*\{[^}]*background:\s*#1f2937', content):
            # Find the last </style> tag
            style_close = content.rfind('</style>')
            if style_close > 0:
                footer_styles = """
    /* Footer Color Fix - High Contrast */
    .site-footer, footer {
        background: #1f2937 !important; /* Dark gray instead of purple */
        color: #ffffff !important;
    }
    
    .site-footer a, footer a,
    .footer-column a, .footer-content a {
        color: #e5e7eb !important; /* Light gray for links */
        text-decoration: none;
    }
    
    .site-footer a:hover, footer a:hover,
    .footer-column a:hover, .footer-content a:hover {
        color: #ffffff !important;
        text-decoration: underline;
    }
    
    .footer-column h3, .footer-column h4,
    footer h3, footer h4 {
        color: #ffffff !important;
    }
    
    .footer-bottom, footer .footer-bottom {
        background: #111827 !important; /* Even darker for bottom */
        color: #9ca3af !important;
        border-top: 1px solid #374151;
    }
    """
                content = content[:style_close] + footer_styles + '\n' + content[style_close:]
                changes_made = True
                changes.append("Added high-contrast footer styles")
    
    # Write back if changes were made
    if changes_made:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, changes
    return False, []

# Process all HTML files
html_files = []

# Get all HTML files
for file in Path('.').glob('*.html'):
    html_files.append(str(file))

for file in Path('.').rglob('*/index.html'):
    html_files.append(str(file))

print(f"Fixing footer colors in {len(html_files)} HTML files")
print("-" * 50)

updated = 0
skipped = 0
errors = 0

for file in html_files:
    try:
        result, changes = fix_footer_colors(file)
        if result:
            print(f"[FIXED] {file}")
            for change in changes[:2]:
                print(f"  - {change}")
            if len(changes) > 2:
                print(f"  ... and {len(changes) - 2} more changes")
            updated += 1
        else:
            skipped += 1
    except Exception as e:
        errors += 1
        print(f"[ERROR] {file}: {str(e)}")

print("-" * 50)
print(f"\n[COMPLETE] Footer color fixes complete!")
print(f"\nResults:")
print(f"  Files updated: {updated}")
print(f"  Files unchanged: {skipped}")
print(f"  Errors: {errors}")