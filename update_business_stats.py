import os
import re

def update_stats_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Update unit counts
    content = content.replace("2,400+ units", "2,450+ units")
    content = content.replace("2,400 units", "2,450 units")
    content = content.replace("2400+ units", "2450+ units")
    content = content.replace("2400 units", "2450 units")
    content = content.replace("2,400", "2,450")
    content = content.replace("2400", "2450")
    
    # Update years in business - Since 2007 = 18 years
    content = content.replace("Since 2006", "Since 2007")
    content = content.replace("since 2006", "since 2007")
    content = content.replace("Trusted Since 2006", "Trusted Since 2007")
    
    # Update in H2 if present
    content = content.replace("Serving Since 2007", "Serving Since 2007")  # Already correct
    
    # Update years of experience if showing 17 or other
    content = re.sub(r'\b17\+ Years', '18+ Years', content)
    content = re.sub(r'\b17 Years', '18 Years', content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Update homepage
if update_stats_in_file('index.html'):
    print("Updated: index.html")

# Update all HTML files
updated_count = 0
for root, dirs, files in os.walk('.'):
    if 'node_modules' in root or '.git' in root:
        continue
    
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            if update_stats_in_file(filepath):
                updated_count += 1
                print(f"Updated: {filepath}")

print(f"\nTotal files updated: {updated_count}")
print("\nBusiness stats updated to:")
print("  Units managed: 2,450+")
print("  In business since: 2007")
print("  Years of experience: 18+")