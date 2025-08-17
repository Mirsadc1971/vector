import re
from pathlib import Path

def add_canonical(file_path, canonical_url):
    """Add or update canonical tag"""
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    if '<link rel="canonical"' in html:
        html = re.sub(
            r'<link\s+rel=["']canonical["'].*?>',
            f'<link rel="canonical" href="{canonical_url}">',
            html, flags=re.IGNORECASE
        )
    else:
        html = html.replace('</head>', f'    <link rel="canonical" href="{canonical_url}">\n</head>')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Fixed: {file_path}")

# Fix missing canonicals
canonicals_to_fix = [{'page': 'perfect-footer.html', 'canonical': 'https://manage369.com/perfect-footer.html'}]


for fix in canonicals_to_fix:
    if Path(fix['page']).exists():
        add_canonical(fix['page'], fix['canonical'])

# Fix duplicates
duplicates = []


for fix in duplicates:
    if Path(fix['page']).exists():
        add_canonical(fix['page'], fix['canonical_to'])

print("Canonical fixes applied!")
