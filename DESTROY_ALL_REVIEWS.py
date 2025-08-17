import os
import re

count = 0

# Search EVERYWHERE
for root, dirs, files in os.walk('.'):
    # Skip git and node_modules
    if '.git' in root or 'node_modules' in root:
        continue
    
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            
            # Remove ALL review-related content
            patterns = [
                # Review CTAs
                r'<!-- Review Collection CTA -->.*?</div>\s*',
                # Managed a Property sections
                r'<div[^>]*>.*?Managed a Property.*?</div>\s*',
                # Leave a Review sections
                r'<h3[^>]*>.*?Managed a Property.*?</h3>.*?</div>\s*',
                # Review links
                r'<a[^>]*>.*?Leave a Review.*?</a>',
                r'<a[^>]*>.*?Google Reviews.*?</a>',
                # Share experience text
                r'<p[^>]*>.*?Share your experience.*?</p>',
                # Review sections
                r'<section[^>]*class="[^"]*review[^"]*"[^>]*>.*?</section>',
                # Any div with review content
                r'<div[^>]*style="[^"]*background:\s*#4285f4[^"]*"[^>]*>.*?Leave a Review.*?</div>',
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

print(f"\n✓ DESTROYED review sections in {count} files")