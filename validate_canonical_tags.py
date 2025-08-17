import os
import re
from pathlib import Path
from urllib.parse import urlparse

def validate_canonical_tags():
    """Validate that all pages have proper canonical tags"""
    print("=" * 70)
    print("CANONICAL TAG VALIDATION REPORT")
    print("=" * 70)
    
    base_url = "https://manage369.com"
    issues = []
    valid_count = 0
    missing_count = 0
    invalid_count = 0
    
    # Scan all HTML files
    html_files = list(Path('.').glob('**/*.html'))
    total_files = 0
    
    print(f"\nValidating canonical tags in HTML files...")
    print("-" * 40)
    
    for file_path in html_files:
        # Skip certain directories
        if any(skip in str(file_path) for skip in ['node_modules', '.git', 'stellar-repo', 'tinggi', 'forms-BACKUP']):
            continue
        
        # Skip error pages
        file_name = os.path.basename(str(file_path))
        if file_name in ['404.html', '500.html']:
            continue
        
        total_files += 1
        path_str = str(file_path).replace('\\', '/')
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                html = f.read()
            
            # Check for canonical tag
            canonical_match = re.search(
                r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']',
                html,
                re.IGNORECASE
            )
            
            if not canonical_match:
                missing_count += 1
                issues.append({
                    'file': path_str,
                    'issue': 'Missing canonical tag',
                    'expected': generate_expected_canonical(path_str, base_url)
                })
            else:
                canonical_url = canonical_match.group(1)
                expected_url = generate_expected_canonical(path_str, base_url)
                
                # Validate canonical URL
                validation_issues = validate_canonical_url(canonical_url, expected_url)
                
                if validation_issues:
                    invalid_count += 1
                    issues.append({
                        'file': path_str,
                        'issue': ', '.join(validation_issues),
                        'current': canonical_url,
                        'expected': expected_url
                    })
                else:
                    valid_count += 1
                    
        except Exception as e:
            issues.append({
                'file': path_str,
                'issue': f'Error reading file: {e}',
                'expected': ''
            })
    
    # Report results
    print(f"\n[VALIDATION SUMMARY]")
    print("-" * 40)
    print(f"Total HTML files checked: {total_files}")
    print(f"Valid canonical tags: {valid_count}")
    print(f"Missing canonical tags: {missing_count}")
    print(f"Invalid canonical tags: {invalid_count}")
    
    if issues:
        print(f"\n[ISSUES FOUND]")
        print("-" * 40)
        for i, issue in enumerate(issues[:20], 1):  # Show first 20 issues
            print(f"\n{i}. {issue['file']}")
            print(f"   Issue: {issue['issue']}")
            if 'current' in issue:
                print(f"   Current: {issue['current']}")
            print(f"   Expected: {issue['expected']}")
    else:
        print("\n[SUCCESS] All canonical tags are valid!")
    
    # Check for duplicate canonicals
    print(f"\n[DUPLICATE CANONICAL CHECK]")
    print("-" * 40)
    
    canonical_urls = {}
    for file_path in html_files:
        if any(skip in str(file_path) for skip in ['node_modules', '.git', 'stellar-repo', 'tinggi']):
            continue
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                html = f.read()
            
            canonical_match = re.search(
                r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']',
                html,
                re.IGNORECASE
            )
            
            if canonical_match:
                url = canonical_match.group(1)
                if url not in canonical_urls:
                    canonical_urls[url] = []
                canonical_urls[url].append(str(file_path).replace('\\', '/'))
        except:
            pass
    
    duplicates = {url: files for url, files in canonical_urls.items() if len(files) > 1}
    
    if duplicates:
        print(f"Found {len(duplicates)} duplicate canonical URLs:")
        for url, files in list(duplicates.items())[:5]:
            print(f"\n  {url}")
            print(f"  Used by: {', '.join(files[:3])}")
    else:
        print("No duplicate canonical URLs found [OK]")
    
    return issues, valid_count, missing_count, invalid_count

def generate_expected_canonical(file_path, base_url):
    """Generate the expected canonical URL for a file"""
    # Clean up path
    path_str = file_path.replace('./', '').replace('\\', '/')
    
    # Special cases
    if path_str == 'index.html':
        return base_url + '/'
    elif path_str.endswith('/index.html'):
        dir_path = path_str.replace('/index.html', '')
        return base_url + '/' + dir_path + '/'
    elif path_str.endswith('.html'):
        return base_url + '/' + path_str
    else:
        return base_url + '/' + path_str

def validate_canonical_url(canonical_url, expected_url):
    """Validate a canonical URL"""
    issues = []
    
    # Check if URL is absolute
    if not canonical_url.startswith('http'):
        issues.append('Canonical URL must be absolute')
    
    # Check for trailing slash consistency
    if expected_url.endswith('/') and not canonical_url.endswith('/'):
        issues.append('Missing trailing slash for directory')
    elif not expected_url.endswith('/') and canonical_url.endswith('/'):
        issues.append('Unexpected trailing slash')
    
    # Check for protocol
    if canonical_url.startswith('http://'):
        issues.append('Should use HTTPS protocol')
    
    # Check for www subdomain
    if 'www.manage369.com' in canonical_url:
        issues.append('Should not use www subdomain')
    
    # Check if URLs match (normalize first)
    normalized_canonical = canonical_url.rstrip('/').lower()
    normalized_expected = expected_url.rstrip('/').lower()
    
    if normalized_canonical != normalized_expected:
        # Only report if not already covered by other issues
        if not any(issue in issues for issue in ['Missing trailing slash', 'Unexpected trailing slash']):
            issues.append('URL does not match expected pattern')
    
    return issues

def generate_recommendations():
    """Generate SEO recommendations"""
    print("\n" + "=" * 70)
    print("SEO RECOMMENDATIONS")
    print("=" * 70)
    
    recommendations = [
        "1. Ensure all canonical URLs use HTTPS protocol",
        "2. Use trailing slashes consistently for directories (/property-management/)",
        "3. Don't use trailing slashes for files (/contact.html)",
        "4. Avoid duplicate canonical URLs across different pages",
        "5. Update _redirects file to enforce canonical URL structure",
        "6. Submit updated sitemap to Google Search Console",
        "7. Monitor for crawl errors after implementation",
        "8. Consider implementing hreflang tags for multi-language support",
        "9. Add self-referencing canonicals to all pages",
        "10. Use absolute URLs, not relative paths"
    ]
    
    for rec in recommendations:
        print(f"  {rec}")
    
    print("\n[NEXT STEPS]")
    print("-" * 40)
    print("1. Fix any missing or invalid canonical tags identified")
    print("2. Update robots.txt to use the optimized version")
    print("3. Implement 301 redirects for duplicate content")
    print("4. Request re-crawling in Google Search Console")
    print("5. Monitor indexing status over next 2-4 weeks")

# Run validation
if __name__ == "__main__":
    issues, valid, missing, invalid = validate_canonical_tags()
    generate_recommendations()
    
    print("\n" + "=" * 70)
    print("VALIDATION COMPLETE")
    print("=" * 70)
    print(f"Success rate: {valid}/{valid+missing+invalid} ({100*valid/(valid+missing+invalid):.1f}%)")