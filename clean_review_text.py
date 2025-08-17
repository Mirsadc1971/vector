import os
import re

count = 0
files_checked = 0

# Check all HTML files
for root, dirs, files in os.walk('.'):
    if '.git' in root or 'node_modules' in root:
        continue
    
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            files_checked += 1
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            
            # Patterns to remove any HTML element containing these phrases
            patterns = [
                # Remove any element containing "Leave a Review"
                r'<[^>]+>(?:[^<]|<(?!/))*?Leave a Review(?:[^<]|<(?!/))*?</[^>]+>',
                # Remove any element containing "Share your experience"  
                r'<[^>]+>(?:[^<]|<(?!/))*?Share your experience(?:[^<]|<(?!/))*?</[^>]+>',
                # Remove h1 with "Share Your Experience"
                r'<h1[^>]*>Share Your Experience</h1>',
                # Remove divs/paragraphs with these texts
                r'<div[^>]*>[^<]*Share your experience[^<]*</div>',
                r'<p[^>]*>[^<]*Share your experience[^<]*</p>',
            ]
            
            for pattern in patterns:
                content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
            
            # Clean up extra whitespace
            content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
            
            if content != original:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                count += 1
                print(f"Cleaned: {os.path.relpath(filepath)}")

print(f"\nChecked {files_checked} HTML files")
print(f"Cleaned {count} files")