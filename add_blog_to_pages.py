#!/usr/bin/env python3
import os
import re

os.chdir('C:\\Users\\mirsa\\Documents\\manage369-live\\property-management')

# Blog section HTML to add before FAQ
blog_section = '''<!-- Blog Section -->
<section style="background: rgba(44,62,80,0.1);">
<div class="container">
<h2>Latest Property Management Insights</h2>
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 30px; margin: 40px 0;">
<article style="background: rgba(44, 62, 80, 0.3); border: 1px solid rgba(244, 162, 97, 0.3); border-radius: 8px; padding: 25px;">
<h3 style="color: var(--primary-gold); margin-bottom: 15px;">2025 HOA Budget Planning Guide</h3>
<p style="color: var(--text-light); margin-bottom: 15px;">Essential tips for boards preparing next year's budget, including reserve fund strategies and assessment planning.</p>
<a href="/blog/2025-hoa-budget-planning" style="color: var(--primary-gold); font-weight: 600;">Read More</a>
</article>
<article style="background: rgba(44, 62, 80, 0.3); border: 1px solid rgba(244, 162, 97, 0.3); border-radius: 8px; padding: 25px;">
<h3 style="color: var(--primary-gold); margin-bottom: 15px;">Winter Maintenance Checklist</h3>
<p style="color: var(--text-light); margin-bottom: 15px;">Protect your property this winter with our comprehensive maintenance checklist for Chicago's harsh weather.</p>
<a href="/blog/winter-maintenance-checklist" style="color: var(--primary-gold); font-weight: 600;">Read More</a>
</article>
<article style="background: rgba(44, 62, 80, 0.3); border: 1px solid rgba(244, 162, 97, 0.3); border-radius: 8px; padding: 25px;">
<h3 style="color: var(--primary-gold); margin-bottom: 15px;">Board Meeting Best Practices</h3>
<p style="color: var(--text-light); margin-bottom: 15px;">Run more effective board meetings with these proven strategies for organization and resident engagement.</p>
<a href="/blog/board-meeting-best-practices" style="color: var(--primary-gold); font-weight: 600;">Read More</a>
</article>
</div>
<div style="text-align: center;">
<a href="/blog" style="display: inline-block; background: var(--primary-gold); color: var(--background-dark); padding: 12px 30px; border-radius: 25px; font-weight: 600; text-decoration: none;">View All Articles</a>
</div>
</div>
</section>

'''

dirs = [d for d in os.listdir('.') if os.path.isdir(d)]
print(f"Adding blog section and footer link to {len(dirs)} pages...")

for directory in dirs:
    file_path = os.path.join(directory, 'index.html')
    if not os.path.exists(file_path):
        continue

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add blog section before FAQ if not already there
    if 'Blog Section' not in content and '<!-- FAQ Section -->' in content:
        content = content.replace('<!-- FAQ Section -->', blog_section + '<!-- FAQ Section -->')
    elif 'Blog Section' not in content and 'Frequently Asked Questions' in content:
        # Find the FAQ section
        pattern = r'(<section[^>]*>[\s\S]*?<h2[^>]*>Frequently Asked Questions</h2>)'
        content = re.sub(pattern, blog_section + r'\1', content, count=1)

    # Add blog link to footer if not already there
    if '/blog' not in content and '<h4 style="color: var(--primary-gold);">Quick Links</h4>' in content:
        # Add blog link after Areas We Serve
        content = re.sub(
            r'(<a href="/property-management"[^>]*>Areas We Serve</a>)',
            r'\1\n<a href="/blog" style="display: block; margin: 5px 0;">Blog</a>',
            content
        )
    elif '/blog' not in content and 'Quick Links' in content:
        # Try another pattern
        content = re.sub(
            r'(Areas We Serve</a>)',
            r'\1\n<a href="/blog" style="display: block; margin: 5px 0;">Blog</a>',
            content
        )

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Updated {directory}")

print("\nAll pages now have blog section and footer link!")