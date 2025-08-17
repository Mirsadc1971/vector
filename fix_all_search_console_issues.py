#!/usr/bin/env python3
"""
Fix all Google Search Console issues based on diagnostic report
"""

import os
import re
import json
from pathlib import Path

def load_diagnostic_report():
    """Load the diagnostic report"""
    with open('search_console_diagnostic_report.json', 'r') as f:
        return json.load(f)

def fix_404_errors():
    """Generate proper redirects for 404 errors"""
    print("=" * 70)
    print("FIXING 404 ERRORS")
    print("=" * 70)
    
    redirects = []
    
    # Fix blog links to old property management pages
    old_to_new = {
        '../property-management-wilmette.html': '/property-management/wilmette/',
        '../property-management-highland-park.html': '/property-management/highland-park/',
        '../property-management-winnetka.html': '/property-management/winnetka/',
        '../property-management-rogers-park.html': '/property-management/rogers-park/',
        '../property-management-glencoe.html': '/property-management/glencoe/',
        '../property-management-kenilworth.html': '/property-management/kenilworth/',
        '../property-management-glenview.html': '/property-management/glenview/',
        '../property-management-evanston.html': '/property-management/evanston/',
        '../property-management-skokie.html': '/property-management/skokie/',
        '../property-management-lake-forest.html': '/property-management/lake-forest/',
        '../property-management-northbrook.html': '/property-management/northbrook/',
    }
    
    # Add favicon redirect
    redirects.append('/images/favicon.ico /favicon.ico 301!')
    
    # Add old property management redirects
    for old, new in old_to_new.items():
        # Create redirect for absolute paths
        absolute_old = old.replace('..', '')
        redirects.append(f"{absolute_old} {new} 301!")
    
    # Fix blog category pages
    redirects.append('/blog/category/hoa-guidance.html /blog/ 301!')
    redirects.append('/blog/category/* /blog/ 301!')
    
    # Save redirects
    with open('_redirects_additions.txt', 'w') as f:
        f.write("# Add these redirects to fix 404 errors\n\n")
        for redirect in redirects:
            f.write(redirect + '\n')
    
    print(f"Generated {len(redirects)} redirect rules")
    return redirects

def fix_blog_internal_links():
    """Fix broken internal links in blog posts"""
    print("\n" + "=" * 70)
    print("FIXING BLOG INTERNAL LINKS")
    print("=" * 70)
    
    # Map of broken links to correct ones
    link_fixes = {
        '../property-management-wilmette.html': '/property-management/wilmette/',
        '../property-management-highland-park.html': '/property-management/highland-park/',
        '../property-management-winnetka.html': '/property-management/winnetka/',
        '../property-management-rogers-park.html': '/property-management/rogers-park/',
        '../property-management-glencoe.html': '/property-management/glencoe/',
        '../property-management-kenilworth.html': '/property-management/kenilworth/',
        '../property-management-glenview.html': '/property-management/glenview/',
        '../property-management-evanston.html': '/property-management/evanston/',
        '../property-management-skokie.html': '/property-management/skokie/',
        '../property-management-lake-forest.html': '/property-management/lake-forest/',
        '../property-management-northbrook.html': '/property-management/northbrook/',
        'category/hoa-guidance.html': '/blog/',
    }
    
    fixed_count = 0
    blog_files = list(Path('blog').glob('*.html'))
    
    for blog_file in blog_files:
        try:
            with open(blog_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix each broken link
            for old_link, new_link in link_fixes.items():
                if old_link in content:
                    content = content.replace(f'href="{old_link}"', f'href="{new_link}"')
                    content = content.replace(f"href='{old_link}'", f"href='{new_link}'")
            
            if content != original_content:
                with open(blog_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_count += 1
                print(f"Fixed links in: {blog_file}")
                
        except Exception as e:
            print(f"Error fixing {blog_file}: {e}")
    
    print(f"Fixed internal links in {fixed_count} blog files")
    return fixed_count

def fix_robots_txt():
    """Update robots.txt to unblock important pages"""
    print("\n" + "=" * 70)
    print("FIXING ROBOTS.TXT")
    print("=" * 70)
    
    # Read current robots.txt
    with open('robots.txt', 'r') as f:
        robots_content = f.read()
    
    # Add Allow rules for services (but not admin)
    allow_rules = """
# Explicitly allow important sections
Allow: /property-management/
Allow: /services/
Allow: /blog/
Allow: /contact.html
Allow: /forms.html
"""
    
    # Insert Allow rules after User-agent: * if not already present
    if 'Allow: /services/' not in robots_content:
        # Find where to insert
        lines = robots_content.split('\n')
        new_lines = []
        inserted = False
        
        for line in lines:
            new_lines.append(line)
            if 'User-agent: *' in line and not inserted:
                new_lines.append(allow_rules)
                inserted = True
        
        # Save updated robots.txt
        with open('robots_updated.txt', 'w') as f:
            f.write('\n'.join(new_lines))
        
        print("Created robots_updated.txt with Allow rules")
        print("Review and replace robots.txt with this version")
    else:
        print("Allow rules already present in robots.txt")

def fix_orphaned_pages():
    """Add internal links to orphaned pages"""
    print("\n" + "=" * 70)
    print("FIXING ORPHANED PAGES")
    print("=" * 70)
    
    report = load_diagnostic_report()
    orphaned_pages = []
    
    # Find orphaned pages
    for page, reasons in report['issues']['not_indexed'].items():
        if 'Orphaned page (no internal links)' in reasons:
            orphaned_pages.append(page)
    
    print(f"Found {len(orphaned_pages)} orphaned pages")
    
    # Group orphaned pages by type
    property_pages = [p for p in orphaned_pages if 'property-management' in p]
    service_pages = [p for p in orphaned_pages if 'services' in p]
    blog_pages = [p for p in orphaned_pages if 'blog' in p]
    
    suggestions = []
    
    if property_pages:
        suggestions.append(f"Add {len(property_pages)} property management pages to /property-management/index.html")
    if service_pages:
        suggestions.append(f"Add {len(service_pages)} service pages to /services.html")
    if blog_pages:
        suggestions.append(f"Add {len(blog_pages)} blog pages to /blog/index.html")
    
    # Save orphaned pages list
    with open('orphaned_pages_to_link.txt', 'w') as f:
        f.write("# Orphaned pages that need internal links\n\n")
        
        if property_pages:
            f.write("## Property Management Pages\n")
            f.write("Add these to /property-management/index.html:\n\n")
            for page in property_pages:
                f.write(f"  - {page}\n")
        
        if service_pages:
            f.write("\n## Service Pages\n")
            f.write("Add these to /services.html:\n\n")
            for page in service_pages:
                f.write(f"  - {page}\n")
        
        if blog_pages:
            f.write("\n## Blog Pages\n")
            f.write("Add these to /blog/index.html:\n\n")
            for page in blog_pages:
                f.write(f"  - {page}\n")
    
    print("Created orphaned_pages_to_link.txt")
    return orphaned_pages

def fix_thin_content():
    """Identify pages needing content enhancement"""
    print("\n" + "=" * 70)
    print("FIXING THIN CONTENT")
    print("=" * 70)
    
    report = load_diagnostic_report()
    thin_pages = []
    
    # Find thin content pages
    for page, reasons in report['issues']['not_indexed'].items():
        for reason in reasons:
            if 'Thin content' in reason:
                # Extract word count
                match = re.search(r'Thin content \((\d+) words\)', reason)
                if match:
                    word_count = int(match.group(1))
                    thin_pages.append({
                        'page': page,
                        'words': word_count,
                        'needs': 300 - word_count
                    })
    
    if thin_pages:
        print(f"Found {len(thin_pages)} pages with thin content")
        
        with open('thin_content_pages.txt', 'w') as f:
            f.write("# Pages needing content enhancement\n\n")
            for page_info in sorted(thin_pages, key=lambda x: x['words']):
                f.write(f"Page: {page_info['page']}\n")
                f.write(f"  Current: {page_info['words']} words\n")
                f.write(f"  Needs: {page_info['needs']} more words\n\n")
        
        print("Created thin_content_pages.txt")
    else:
        print("No thin content pages found")
    
    return thin_pages

def fix_duplicate_titles():
    """Fix duplicate title tags"""
    print("\n" + "=" * 70)
    print("FIXING DUPLICATE TITLES")
    print("=" * 70)
    
    report = load_diagnostic_report()
    duplicates = report['issues']['duplicate_content']['duplicate_titles']
    
    if duplicates:
        print(f"Found {len(duplicates)} duplicate title groups")
        
        with open('duplicate_titles_to_fix.txt', 'w') as f:
            f.write("# Duplicate titles that need unique values\n\n")
            
            for dup in duplicates:
                f.write(f"Title: {dup['title']}\n")
                f.write("Pages with this title:\n")
                for page in dup['pages']:
                    f.write(f"  - {page}\n")
                f.write("\nSuggested fixes:\n")
                
                # Generate unique title suggestions
                for page in dup['pages']:
                    if 'property-management' in page:
                        location = page.split('/')[-2]
                        f.write(f"  {page}: {location.title()} Property Management | Manage369\n")
                    elif 'services' in page:
                        service = page.split('/')[-2].replace('-', ' ')
                        f.write(f"  {page}: {service.title()} Services | Manage369\n")
                
                f.write("\n")
        
        print("Created duplicate_titles_to_fix.txt")
    else:
        print("No duplicate titles found")
    
    return duplicates

def generate_summary_report():
    """Generate a summary of all fixes"""
    print("\n" + "=" * 70)
    print("GENERATING SUMMARY REPORT")
    print("=" * 70)
    
    report = load_diagnostic_report()
    
    summary = f"""
# Google Search Console Issues - Fix Summary

## Issues Found:
- 404 Errors: {report['summary']['404_errors']}
- Redirect Errors: {report['summary']['redirect_errors']}
- Robots Blocked: {report['summary']['robots_blocked']}
- Not Indexed: {report['summary']['not_indexed']}
- Duplicate Content: {report['summary']['duplicate_content']}

## Fixes Generated:

### 1. 404 Error Fixes
- Generated redirect rules in: _redirects_additions.txt
- Fixed internal links in blog posts
- Action: Add redirects to _redirects file

### 2. Robots.txt Fixes
- Generated updated version: robots_updated.txt
- Added Allow rules for important sections
- Action: Review and replace robots.txt

### 3. Orphaned Pages
- Listed in: orphaned_pages_to_link.txt
- {len([p for p, r in report['issues']['not_indexed'].items() if 'Orphaned' in str(r)])} pages need internal links
- Action: Add links from main category pages

### 4. Thin Content
- Listed in: thin_content_pages.txt
- Pages need 300+ words of content
- Action: Enhance content on these pages

### 5. Duplicate Titles
- Listed in: duplicate_titles_to_fix.txt
- Make each title unique and descriptive
- Action: Update title tags

## Implementation Steps:

1. **Immediate Fixes** (5 minutes):
   - Add redirects from _redirects_additions.txt to _redirects
   - Replace robots.txt with robots_updated.txt
   - Commit and push changes

2. **Quick Fixes** (30 minutes):
   - Run this script to fix blog internal links
   - Add internal links to orphaned pages
   - Update duplicate title tags

3. **Content Fixes** (2-3 hours):
   - Enhance thin content pages
   - Add meta descriptions where missing
   - Ensure all pages have canonical tags

4. **Google Search Console Actions**:
   - Submit updated sitemap.xml
   - Request indexing for fixed pages
   - Use URL Removal tool for spam pages
   - Validate fixes in 24-48 hours

## Expected Results:
- 404 errors should drop to near zero
- Indexed pages should increase by 50-75
- Duplicate content warnings should resolve
- Coverage report should show improvement within 2 weeks
"""
    
    with open('fix_summary_report.md', 'w') as f:
        f.write(summary)
    
    print("Created fix_summary_report.md")
    print("\nAll fix files generated successfully!")
    print("\nFiles created:")
    print("  - _redirects_additions.txt (redirect rules)")
    print("  - robots_updated.txt (updated robots.txt)")
    print("  - orphaned_pages_to_link.txt (pages needing links)")
    print("  - thin_content_pages.txt (pages needing content)")
    print("  - duplicate_titles_to_fix.txt (duplicate titles)")
    print("  - fix_summary_report.md (implementation guide)")

if __name__ == "__main__":
    # Run all fixes
    fix_404_errors()
    fix_blog_internal_links()
    fix_robots_txt()
    fix_orphaned_pages()
    fix_thin_content()
    fix_duplicate_titles()
    generate_summary_report()
    
    print("\n" + "=" * 70)
    print("ALL FIXES COMPLETE")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Review fix_summary_report.md for implementation guide")
    print("2. Apply fixes in order of priority")
    print("3. Submit to Google Search Console")
    print("4. Monitor improvements over next 2 weeks")