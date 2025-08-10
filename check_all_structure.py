#!/usr/bin/env python3
import os
import glob

def check_html_structure(file_path):
    """Check for common HTML structure issues"""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    issues = []
    
    # Check for required closing tags
    if '</header>' not in content:
        issues.append("Missing </header> tag")
    if '</body>' not in content:
        issues.append("Missing </body> tag")
    if '</html>' not in content:
        issues.append("Missing </html> tag")
    
    # Check for duplicate closing tags
    if content.count('</body>') > 1:
        issues.append(f"Multiple </body> tags ({content.count('</body>')})")
    if content.count('</html>') > 1:
        issues.append(f"Multiple </html> tags ({content.count('</html>')})")
    
    # Check tag balance
    open_divs = content.count('<div')
    close_divs = content.count('</div>')
    if open_divs != close_divs:
        issues.append(f"Unbalanced div tags: {open_divs} open, {close_divs} close")
    
    open_sections = content.count('<section')
    close_sections = content.count('</section>')
    if open_sections != close_sections:
        issues.append(f"Unbalanced section tags: {open_sections} open, {close_sections} close")
    
    # Check for location-content as div (should be section)
    if '<div class="location-content">' in content:
        issues.append("location-content is still a div (should be section)")
    
    # Check for orphaned location-content (outside section)
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'class="location-content"' in line:
            # Check if it's properly a section tag
            if '<section' not in line:
                issues.append(f"location-content not properly tagged as section (line {i+1})")
    
    return issues

# Get all property management HTML files
property_files = glob.glob(r"C:\Users\mirsa\manage369-live\property-management\*\index.html")

print(f"Checking {len(property_files)} property pages for structural issues...\n")

problem_pages = {}
clean_pages = []

for file_path in property_files:
    dir_name = os.path.basename(os.path.dirname(file_path))
    issues = check_html_structure(file_path)
    
    if issues:
        problem_pages[dir_name] = issues
    else:
        clean_pages.append(dir_name)

print("="*60)
print(f"RESULTS:")
print(f"Clean pages: {len(clean_pages)}")
print(f"Pages with issues: {len(problem_pages)}")

if problem_pages:
    print("\n" + "="*60)
    print("PAGES WITH ISSUES:")
    for page, issues in problem_pages.items():
        print(f"\n{page}:")
        for issue in issues:
            print(f"  - {issue}")

print("\n" + "="*60)
if clean_pages:
    print(f"CLEAN PAGES ({len(clean_pages)}):")
    for i in range(0, len(clean_pages), 5):
        print("  " + ", ".join(clean_pages[i:i+5]))