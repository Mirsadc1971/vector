import os
import re
from pathlib import Path

# The perfect footer HTML structure
PERFECT_FOOTER = '''    <!-- Footer -->
    <footer class="site-footer">
        <div class="footer-content">
            <!-- Company Info Column -->
            <div class="footer-column">
                <h3>Manage369</h3>
                <p>1400 Patriot Boulevard 357<br>Glenview, IL 60026</p>
                <p style="margin-top: 10px; color: #9ca3af; font-weight: 500;">IDFPR Management Firm License 291.000211</p>
                <p style="margin-top: 10px;"><strong>Phone:</strong> <a href="tel:8476522338">(847) 652-2338</a><br>
                <strong>Email:</strong> <a href="mailto:service@manage369.com">service@manage369.com</a></p>
            </div>
            
            <!-- Quick Links Column -->
            <div class="footer-column">
                <h3>Quick Links</h3>
                <ul>
                <li><a href="{PATH_PREFIX}property-management/">Areas We Serve</a></li>
                <li><a href="{PATH_PREFIX}blog/">Blog</a></li>
                <li><a href="{PATH_PREFIX}contact.html">Contact</a></li>
                <li><a href="{PATH_PREFIX}payment-methods.html">Payment Methods</a></li>
                <li><a href="{PATH_PREFIX}services.html">Services</a></li></ul>
            </div>
            
            <!-- Resources Column -->
            <div class="footer-column">
                <h3>Resources</h3>
                <ul>
                <li><a href="{PATH_PREFIX}accessibility.html">Accessibility</a></li>
                <li><a href="{PATH_PREFIX}forms.html">Forms & Documents</a></li>
                <li><a href="{PATH_PREFIX}legal-disclaimers.html">Legal Disclaimers</a></li>
                <li><a href="{PATH_PREFIX}privacy-policy.html">Privacy Policy</a></li>
                <li><a href="{PATH_PREFIX}sitemap.html">Sitemap</a></li>
                <li><a href="{PATH_PREFIX}terms-of-service.html">Terms of Service</a></li></ul>
            </div>
        </div>
        <div class="footer-bottom">
            <div style="text-align: center; margin-bottom: 10px; color: #9ca3af; font-size: 0.9rem;">
                CAI National Member | IREM Certified | CCIM Designated | NAR Member | IDFPR Licensed
            </div>
            <p style="text-align: center; color: #9ca3af;">&copy; 2025 Manage369. All rights reserved.</p>
        </div>
    </footer>'''

def get_path_prefix(file_path):
    """Get the correct path prefix based on file location"""
    # Convert to Path object
    path = Path(file_path)
    
    # Count how many directories deep we are
    depth = len(path.parts) - 1
    
    if depth == 0:
        # Root level
        return ""
    elif depth == 1:
        # One level deep (like blog/index.html)
        return "../"
    elif depth == 2:
        # Two levels deep (like property-management/glenview/index.html)
        return "../../"
    else:
        # Three or more levels deep
        return "../" * depth

def apply_footer(file_path):
    """Apply the perfect footer to an HTML file"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Get the correct path prefix
    path_prefix = get_path_prefix(file_path)
    footer_html = PERFECT_FOOTER.replace('{PATH_PREFIX}', path_prefix)
    
    # Remove everything from existing footer to end of body
    # This includes any misplaced sections after </footer>
    footer_patterns = [
        r'<footer[^>]*>.*?</body>',
        r'<!-- Footer -->.*?</body>',
        r'<!-- Site Footer -->.*?</body>',
    ]
    
    for pattern in footer_patterns:
        if re.search(pattern, content, re.DOTALL | re.IGNORECASE):
            # Replace footer and everything after it until </body>
            content = re.sub(pattern, footer_html + '\n</body>', content, flags=re.DOTALL | re.IGNORECASE)
            break
    else:
        # If no footer found, add before </body>
        if '</body>' in content:
            content = content.replace('</body>', footer_html + '\n</body>')
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

# Process all HTML files
html_files = []

# Root level HTML files
for file in Path('.').glob('*.html'):
    if file.name not in ['404.html', '500.html']:  # Skip error pages
        html_files.append(str(file))

# All index.html files in subdirectories
for file in Path('.').rglob('*/index.html'):
    html_files.append(str(file))

print(f"Applying perfect footer to {len(html_files)} HTML files")
print("-" * 50)

updated = 0
errors = 0

for file in html_files:
    try:
        if apply_footer(file):
            print(f"[UPDATED] {file}")
            updated += 1
    except Exception as e:
        errors += 1
        print(f"[ERROR] {file}: {str(e)}")

print("-" * 50)
print(f"\n[COMPLETE] Footer application complete!")
print(f"  Files updated: {updated}")
print(f"  Errors: {errors}")