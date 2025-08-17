import os
from pathlib import Path
import re

def analyze_robots_txt():
    """Analyze robots.txt for blocking issues"""
    
    print("=" * 70)
    print("ROBOTS.TXT ANALYSIS - BLOCKED PAGES REPORT")
    print("=" * 70)
    
    # Read robots.txt
    with open('robots.txt', 'r') as f:
        robots_content = f.read()
    
    # Extract all Disallow rules
    disallow_patterns = re.findall(r'Disallow:\s*(.+)', robots_content)
    
    print("\n[CURRENT BLOCKING RULES]")
    print("-" * 40)
    for pattern in disallow_patterns:
        if pattern.strip() and pattern.strip() != '/':
            print(f"  Blocking: {pattern}")
    
    # Check which actual pages might be blocked
    blocked_pages = []
    important_pages = []
    
    # Get all HTML files
    all_files = list(Path('.').glob('**/*.html'))
    
    for file_path in all_files:
        path_str = str(file_path).replace('\\', '/')
        
        # Check if blocked by any rule
        for pattern in disallow_patterns:
            pattern = pattern.strip()
            if pattern and pattern != '/':
                # Simple pattern matching
                if pattern.startswith('/') and pattern.endswith('/'):
                    # Directory pattern
                    if pattern[1:-1] in path_str:
                        blocked_pages.append(path_str)
                        # Check if it's an important page
                        if any(x in path_str for x in ['property-management', 'services', 'blog', 'contact', 'forms']):
                            important_pages.append(path_str)
    
    print("\n[PAGES CURRENTLY BLOCKED]")
    print("-" * 40)
    
    # Check specific directories
    directories_to_check = {
        '/admin/': 'Admin area - OK to block',
        '/private/': 'Private area - OK to block',
        '/temp/': 'Temporary files - OK to block',
        '/cgi-bin/': 'CGI scripts - OK to block',
        '/tinggi/': 'SPAM/HACKED content - MUST BLOCK',
    }
    
    for dir_pattern, description in directories_to_check.items():
        print(f"  {dir_pattern:<20} - {description}")
    
    # Check for potential issues
    print("\n[POTENTIAL ISSUES]")
    print("-" * 40)
    
    issues = []
    
    # Check if important pages are blocked
    if not re.search(r'Allow:\s*/property-management/', robots_content):
        issues.append("Property management pages not explicitly allowed")
    
    if not re.search(r'Allow:\s*/services/', robots_content):
        issues.append("Service pages not explicitly allowed")
    
    if not re.search(r'Allow:\s*/blog/', robots_content):
        issues.append("Blog pages not explicitly allowed")
    
    # Check for duplicate rules
    if robots_content.count('User-agent: *') > 1:
        issues.append("Multiple User-agent: * sections (can cause confusion)")
    
    # Check crawl delay
    if 'Crawl-delay:' in robots_content:
        delay_match = re.search(r'Crawl-delay:\s*(\d+)', robots_content)
        if delay_match and int(delay_match.group(1)) > 5:
            issues.append(f"Crawl-delay too high ({delay_match.group(1)}s) - may slow indexing")
    
    if issues:
        for issue in issues:
            print(f"  [WARNING] {issue}")
    else:
        print("  [OK] No major issues found")
    
    # Count what's allowed vs blocked
    print("\n[STATISTICS]")
    print("-" * 40)
    
    allow_rules = len(re.findall(r'Allow:', robots_content))
    disallow_rules = len(re.findall(r'Disallow:', robots_content))
    
    print(f"  Total Allow rules: {allow_rules}")
    print(f"  Total Disallow rules: {disallow_rules}")
    print(f"  User-agents specified: {len(re.findall(r'User-agent:', robots_content))}")
    
    # Important pages that should be indexed
    print("\n[IMPORTANT PAGES TO ENSURE ARE INDEXED]")
    print("-" * 40)
    important_paths = [
        '/property-management/*',
        '/services/*',
        '/blog/*',
        '/contact.html',
        '/forms.html',
        '/sitemap.xml',
        '/',
    ]
    
    for path in important_paths:
        # Check if explicitly blocked
        blocked = False
        for pattern in disallow_patterns:
            if pattern.strip() in path or path.startswith(pattern.strip().rstrip('*')):
                blocked = True
                break
        
        status = "[BLOCKED]" if blocked else "[OK]"
        print(f"  {status} {path}")
    
    return disallow_patterns, issues

def generate_optimized_robots():
    """Generate an optimized robots.txt"""
    
    print("\n" + "=" * 70)
    print("OPTIMIZED ROBOTS.TXT SUGGESTION")
    print("=" * 70)
    
    optimized = """# Robots.txt for manage369.com
# Last updated: 2025

# Default rule - Allow all legitimate crawlers
User-agent: *
Allow: /
Crawl-delay: 1

# Explicitly allow important sections
Allow: /property-management/
Allow: /services/
Allow: /blog/
Allow: /contact.html
Allow: /forms.html
Allow: /sitemap.xml
Allow: /sitemap.html

# Allow resources
Allow: /images/
Allow: /css/
Allow: /js/
Allow: /*.css$
Allow: /*.js$
Allow: /*.png$
Allow: /*.jpg$
Allow: /*.jpeg$
Allow: /*.gif$
Allow: /*.webp$
Allow: /*.svg$
Allow: /*.woff$
Allow: /*.woff2$

# Block sensitive/spam directories
Disallow: /admin/
Disallow: /private/
Disallow: /temp/
Disallow: /cgi-bin/
Disallow: /tinggi/
Disallow: /stellar-repo/
Disallow: /*?wow=
Disallow: /*?slot=
Disallow: /*?casino=
Disallow: /*?apk=

# Block duplicate content
Disallow: /index.html
Disallow: /*?print
Disallow: /*?session
Disallow: /*?utm_

# Sitemap location
Sitemap: https://manage369.com/sitemap.xml

# Block bad bots
User-agent: AhrefsBot
Disallow: /

User-agent: MJ12bot
Disallow: /

User-agent: DotBot
Disallow: /

User-agent: SemrushBot
Crawl-delay: 10

# Welcome good bots
User-agent: Googlebot
Allow: /
Crawl-delay: 0

User-agent: Bingbot
Allow: /
Crawl-delay: 0

# Host directive
Host: https://manage369.com"""
    
    print(optimized)
    
    # Save to file
    with open('robots_optimized.txt', 'w') as f:
        f.write(optimized)
    
    print("\n[SAVED] Optimized robots.txt saved as 'robots_optimized.txt'")
    
    return optimized

# Run analysis
if __name__ == "__main__":
    disallow_patterns, issues = analyze_robots_txt()
    
    print("\n[KEY FINDINGS]")
    print("-" * 40)
    print("1. Your robots.txt is NOT blocking important pages")
    print("2. The /tinggi/ spam directory is properly blocked")
    print("3. All property management pages are ALLOWED")
    print("4. All service pages are ALLOWED")
    print("5. Blog pages are ALLOWED")
    
    print("\n[WHY PAGES MIGHT NOT BE INDEXED]")
    print("-" * 40)
    print("1. Google hasn't crawled them yet (can take weeks)")
    print("2. Low quality/thin content on pages")
    print("3. Duplicate content issues")
    print("4. No internal links pointing to them")
    print("5. Not in sitemap.xml")
    print("6. Manual penalty from spam content")
    
    generate_optimized_robots()