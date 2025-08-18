import os
import re
from pathlib import Path

def fix_footer_readability(file_path):
    """Fix footer text readability and remove duplicate certifications"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes_made = False
    
    # Remove duplicate certification sections - keep only one
    # First, remove the certification badges section if it exists
    cert_badge_pattern = r'<div class="certifications">.*?<div class="cert-badge">CAI</div>.*?<div class="cert-badge">NAR</div>.*?</div>'
    if re.search(cert_badge_pattern, content, re.DOTALL):
        content = re.sub(cert_badge_pattern, '', content, flags=re.DOTALL)
        changes_made = True
    
    # Keep the text-based certification line in footer-bottom
    # Make sure it's readable (light gray text)
    cert_text_pattern = r'CAI National Member \| IREM Certified \| CCIM Designated \| NAR Member \| IDFPR Licensed'
    if cert_text_pattern in content:
        # Find and fix the certification text styling
        content = re.sub(
            r'<div style="text-align: center; margin-bottom: 10px; color: #[0-9a-f]{6}; font-size: 0.9rem;">\s*' + cert_text_pattern,
            '<div style="text-align: center; margin-bottom: 10px; color: #9ca3af; font-size: 0.9rem;">\n                ' + cert_text_pattern,
            content
        )
        changes_made = True
    
    # Add/update footer CSS to ensure all text is readable
    if '</style>' in content and '.site-footer' not in content[:content.find('</style>')]:
        # Find the last </style> before </head>
        style_close = content.find('</style>')
        if style_close > 0:
            footer_css = """
    /* Footer Readability Fix */
    .site-footer, footer {
        background: #1f2937 !important;
        color: #e5e7eb !important;
    }
    
    .site-footer a, footer a,
    .footer-column a, .footer-content a {
        color: #e5e7eb !important;
        text-decoration: none;
    }
    
    .site-footer a:hover, footer a:hover {
        color: #ffffff !important;
        text-decoration: underline;
    }
    
    .footer-column h3, footer h3 {
        color: #ffffff !important;
        margin-bottom: 1rem;
    }
    
    .footer-column ul, footer ul {
        list-style: none;
        padding: 0;
    }
    
    .footer-column li, footer li {
        margin-bottom: 0.5rem;
    }
    
    .footer-bottom {
        background: #111827 !important;
        color: #9ca3af !important;
        border-top: 1px solid #374151;
        padding: 1.5rem 0;
        margin-top: 2rem;
    }
    
    .footer-license, .footer-copyright {
        color: #9ca3af !important;
    }
    
    /* Remove/hide duplicate cert badges */
    .cert-badge, .certifications {
        display: none !important;
    }
"""
            content = content[:style_close] + footer_css + '\n' + content[style_close:]
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

print(f"Fixing footer readability in {len(html_files)} HTML files")
print("-" * 50)

updated = 0
skipped = 0

for file in html_files:
    try:
        if fix_footer_readability(file):
            print(f"[FIXED] {file}")
            updated += 1
        else:
            skipped += 1
    except Exception as e:
        print(f"[ERROR] {file}: {str(e)}")

print("-" * 50)
print(f"\n[COMPLETE] Footer readability fixes complete!")
print(f"  Files updated: {updated}")
print(f"  Files unchanged: {skipped}")