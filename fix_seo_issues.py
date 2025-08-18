import os
import re
from pathlib import Path

def fix_seo_issues(file_path):
    """Fix critical SEO issues in HTML files"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes_made = False
    changes = []
    
    # 1. Fix title tags with embedded HTML (remove anchor tags)
    title_pattern = r'<title>.*?</title>'
    title_matches = re.findall(title_pattern, content, re.DOTALL)
    
    for match in title_matches:
        if '<a href=' in match:
            # Extract text without HTML tags
            clean_title = re.sub(r'<a[^>]*?>', '', match)
            clean_title = re.sub(r'</a>', '', clean_title)
            content = content.replace(match, clean_title)
            changes_made = True
            changes.append("Fixed title tag with embedded HTML")
    
    # 2. Fix unclosed meta description tags
    meta_desc_pattern = r'<meta property="og:description" content="([^"]*)"(?![^>]*>)'
    meta_desc_matches = re.findall(meta_desc_pattern, content)
    
    if meta_desc_matches:
        for match in meta_desc_matches:
            old_meta = f'<meta property="og:description" content="{match}"'
            new_meta = f'<meta property="og:description" content="{match}">'
            content = content.replace(old_meta, new_meta)
            changes_made = True
            changes.append("Fixed unclosed og:description meta tag")
    
    # Also check twitter description
    twitter_desc_pattern = r'<meta property="twitter:description" content="([^"]*)"(?![^>]*>)'
    twitter_matches = re.findall(twitter_desc_pattern, content)
    
    if twitter_matches:
        for match in twitter_matches:
            old_meta = f'<meta property="twitter:description" content="{match}"'
            new_meta = f'<meta property="twitter:description" content="{match}">'
            content = content.replace(old_meta, new_meta)
            changes_made = True
            changes.append("Fixed unclosed twitter:description meta tag")
    
    # 3. Fix Google Analytics ID (should be G-XXXXXXXXX format)
    ga_pattern = r'G-496518917'
    if ga_pattern in content:
        # This ID format is incorrect - should be G- followed by alphanumeric
        content = content.replace('G-496518917', 'G-YOUR-ID-HERE')
        changes_made = True
        changes.append("Fixed invalid Google Analytics ID format")
    
    # 4. Remove google-site-verification placeholder
    if 'content="your-verification-code"' in content:
        # Remove the entire meta tag if it's just a placeholder
        content = re.sub(r'<meta name="google-site-verification" content="your-verification-code">\n?\s*', '', content)
        changes_made = True
        changes.append("Removed placeholder google-site-verification tag")
    
    # 5. Fix duplicate manifest links
    manifest_count = content.count('<link rel="manifest"')
    if manifest_count > 1:
        # Keep only the first manifest link
        lines = content.split('\n')
        new_lines = []
        manifest_seen = False
        for line in lines:
            if '<link rel="manifest"' in line:
                if not manifest_seen:
                    new_lines.append(line)
                    manifest_seen = True
            else:
                new_lines.append(line)
        content = '\n'.join(new_lines)
        changes_made = True
        changes.append("Removed duplicate manifest links")
    
    # 6. Add missing alt text to social share image
    if 'og:image' in content and 'og:image:alt' not in content:
        # Find og:image tag and add alt text after it
        og_image_pattern = r'(<meta property="og:image"[^>]*>)'
        og_image_match = re.search(og_image_pattern, content)
        if og_image_match:
            insert_pos = og_image_match.end()
            alt_tag = '\n    <meta property="og:image:alt" content="Manage369 Property Management - Professional HOA and Condo Management Services">'
            content = content[:insert_pos] + alt_tag + content[insert_pos:]
            changes_made = True
            changes.append("Added og:image:alt tag")
    
    # 7. Ensure proper closing of all meta tags
    # Find all meta tags without closing >
    unclosed_meta_pattern = r'<meta[^>]*[^/>]$'
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if '<meta' in line and not line.strip().endswith('>'):
            lines[i] = line.rstrip() + '>'
            changes_made = True
            changes.append(f"Fixed unclosed meta tag on line {i+1}")
    
    if changes_made and len(lines) > 0:
        content = '\n'.join(lines)
    
    # Write back if changes were made
    if changes_made:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, changes
    return False, []

# Process main pages and property management pages
html_files = []

# Main pages
main_pages = [
    'index.html',
    'services.html',
    'contact.html',
    'payment-methods.html',
    'forms.html'
]

for page in main_pages:
    if os.path.exists(page):
        html_files.append(page)

# Property management pages
for file in Path('property-management').rglob('index.html'):
    html_files.append(str(file))

# Service pages
for file in Path('services').rglob('index.html'):
    html_files.append(str(file))

print(f"Fixing SEO issues in {len(html_files)} HTML files")
print("-" * 50)

updated = 0
skipped = 0
errors = 0

for file in html_files:
    try:
        result, changes = fix_seo_issues(file)
        if result:
            print(f"[FIXED] {file}")
            for change in changes[:3]:  # Show first 3 changes
                print(f"  - {change}")
            if len(changes) > 3:
                print(f"  ... and {len(changes) - 3} more changes")
            updated += 1
        else:
            skipped += 1
    except Exception as e:
        errors += 1
        print(f"[ERROR] {file}: {str(e)}")

print("-" * 50)
print(f"\n[COMPLETE] SEO fixes complete!")
print(f"\nResults:")
print(f"  Files updated: {updated}")
print(f"  Files unchanged: {skipped}")
print(f"  Errors: {errors}")

# Also create a proper Google verification file
verification_html = """google-site-verification: google-site-verification.html"""

with open('google496518917.html', 'w') as f:
    f.write(verification_html)
    print("\nCreated Google verification file: google496518917.html")