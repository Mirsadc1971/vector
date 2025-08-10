#!/usr/bin/env python3
import os
import glob
import re

def check_page_issues(file_path):
    """Check for various issues in a page"""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    issues = []
    
    # Check for mobile menu function
    if 'function toggleMobileMenu()' not in content:
        issues.append("Missing toggleMobileMenu function")
    
    # Check for favicon references
    if 'favicon' not in content.lower():
        issues.append("Missing favicon reference")
    
    # Check for Google Analytics (if not a test page)
    if 'gtag' not in content and 'Google Analytics' not in content:
        issues.append("Missing Google Analytics")
    
    # Check for broken image references
    images = re.findall(r'url\([\'"]?([^\'")]+\.(?:jpg|png|webp|jpeg))[\'"]?\)', content)
    for img in images:
        if 'manage369kitchenevanston' in img:
            issues.append(f"References non-existent image: {img}")
    
    # Check for proper viewport meta tag
    if 'viewport' not in content:
        issues.append("Missing viewport meta tag")
    
    # Check for phone number consistency
    phones = re.findall(r'847[-.\s]?652[-.\s]?2338', content)
    if len(phones) == 0:
        issues.append("Missing phone number")
    
    # Check for proper doctype
    if '<!DOCTYPE html>' not in content:
        issues.append("Missing DOCTYPE")
    
    # Check for duplicate IDs (basic check)
    mobile_menu_count = content.count('id="mobileMenu"')
    if mobile_menu_count > 1:
        issues.append(f"Duplicate mobileMenu ID ({mobile_menu_count} times)")
    
    return issues

# Check all property pages
property_files = glob.glob(r"C:\Users\mirsa\manage369-live\property-management\*\index.html")

print(f"Checking {len(property_files)} property pages for issues...\n")

pages_with_issues = {}
clean_pages = []

for file_path in property_files:
    dir_name = os.path.basename(os.path.dirname(file_path))
    issues = check_page_issues(file_path)
    
    if issues:
        pages_with_issues[dir_name] = issues
    else:
        clean_pages.append(dir_name)

# Report results
print("="*60)
print(f"RESULTS:")
print(f"Pages with issues: {len(pages_with_issues)}")
print(f"Clean pages: {len(clean_pages)}")

if pages_with_issues:
    print("\n" + "="*60)
    print("PAGES WITH ISSUES:\n")
    
    # Group by issue type
    issue_summary = {}
    for page, issues in pages_with_issues.items():
        for issue in issues:
            if issue not in issue_summary:
                issue_summary[issue] = []
            issue_summary[issue].append(page)
    
    # Print summary by issue type
    for issue, pages in issue_summary.items():
        print(f"\n{issue}: ({len(pages)} pages)")
        if len(pages) <= 10:
            for page in pages:
                print(f"  - {page}")
        else:
            print(f"  - {', '.join(pages[:5])}...")
            print(f"    and {len(pages)-5} more")

print("\n" + "="*60)
if len(clean_pages) > 0:
    print(f"\nCOMPLETELY CLEAN PAGES: {len(clean_pages)}")
    if len(clean_pages) <= 20:
        for page in clean_pages:
            print(f"  - {page}")