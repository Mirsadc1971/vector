#!/usr/bin/env python3
import os

os.chdir('C:\\Users\\mirsa\\Documents\\manage369-live\\property-management')

# Correct blog section with real blog links
blog_section = '''<!-- Blog Section -->
<section style="background: rgba(44,62,80,0.1);">
<div class="container">
<h2>Latest Property Management Insights</h2>
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 30px; margin: 40px 0;">
<article style="background: rgba(44, 62, 80, 0.3); border: 1px solid rgba(244, 162, 97, 0.3); border-radius: 8px; padding: 25px;">
<h3 style="color: var(--primary-gold); margin-bottom: 15px;">2025 Illinois HOA Law Changes</h3>
<p style="color: var(--text-light); margin-bottom: 15px;">Essential updates for boards on new legislation affecting HOAs and condominiums in Illinois.</p>
<a href="/blog/2025-illinois-hoa-law-changes.html" style="color: var(--primary-gold); font-weight: 600;">Read More</a>
</article>
<article style="background: rgba(44, 62, 80, 0.3); border: 1px solid rgba(244, 162, 97, 0.3); border-radius: 8px; padding: 25px;">
<h3 style="color: var(--primary-gold); margin-bottom: 15px;">Winter Property Management Checklist</h3>
<p style="color: var(--text-light); margin-bottom: 15px;">Protect your property this winter with our comprehensive maintenance checklist for Chicago's harsh weather.</p>
<a href="/blog/winter-property-management-checklist.html" style="color: var(--primary-gold); font-weight: 600;">Read More</a>
</article>
<article style="background: rgba(44, 62, 80, 0.3); border: 1px solid rgba(244, 162, 97, 0.3); border-radius: 8px; padding: 25px;">
<h3 style="color: var(--primary-gold); margin-bottom: 15px;">Top 5 Financial Mistakes HOA Boards Avoid</h3>
<p style="color: var(--text-light); margin-bottom: 15px;">Learn the most common financial pitfalls and how to protect your association's financial health.</p>
<a href="/blog/top-5-financial-mistakes-hoa-boards-avoid.html" style="color: var(--primary-gold); font-weight: 600;">Read More</a>
</article>
</div>
<div style="text-align: center;">
<a href="/blog/" style="display: inline-block; background: var(--primary-gold); color: var(--background-dark); padding: 12px 30px; border-radius: 25px; font-weight: 600; text-decoration: none;">View All Articles</a>
</div>
</div>
</section>

'''

dirs = [d for d in os.listdir('.') if os.path.isdir(d)]
print(f"Fixing blog links in {len(dirs)} pages...")

for directory in dirs:
    file_path = os.path.join(directory, 'index.html')
    if not os.path.exists(file_path):
        continue

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace the blog section with correct links
    import re

    # Find and replace the blog section
    pattern = r'<!-- Blog Section -->.*?</section>'
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, blog_section, content, flags=re.DOTALL)
        print(f"Fixed blog section in {directory}")

    # Fix footer blog link
    content = content.replace('href="/blog"', 'href="/blog/"')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("\nAll blog links fixed to point to actual blog pages!")