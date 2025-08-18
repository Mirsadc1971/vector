import os
import re
from pathlib import Path

def fix_sticky_footer(file_path):
    """Add CSS to make footer stick to bottom of page"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes_made = False
    
    # Check if sticky footer CSS already exists
    if 'min-height: 100vh' in content and 'flex: 1' in content:
        return False, []
    
    # Find the closing </style> tag before </head>
    style_close_pattern = r'</style>\s*(?=</head>|<link|<style)'
    matches = list(re.finditer(style_close_pattern, content))
    
    if matches:
        # Insert sticky footer CSS before the last </style> tag
        last_match = matches[-1]
        
        sticky_footer_css = """
        /* Sticky Footer Solution */
        html, body {
            height: 100%;
            margin: 0;
            padding: 0;
        }
        
        body {
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }
        
        /* Main content wrapper */
        main, #main, .main-content, 
        .hero-section + *, 
        .service-areas-section,
        .services-content,
        .contact-content,
        .payment-content,
        .about-content {
            flex: 1 0 auto;
        }
        
        /* Ensure footer stays at bottom */
        .site-footer, footer {
            flex-shrink: 0;
            margin-top: auto;
            width: 100%;
        }
        
        /* Fix for sections that might break layout */
        section {
            width: 100%;
        }
        
        /* Ensure proper spacing */
        .service-areas-section {
            padding-bottom: 3rem;
        }
        
        /* Mobile adjustments */
        @media (max-width: 768px) {
            body {
                min-height: 100vh;
                min-height: -webkit-fill-available;
            }
        }
    </style>"""
        
        # Insert the CSS
        content = content[:last_match.start()] + sticky_footer_css + '\n    ' + content[last_match.start():]
        changes_made = True
        return True, ["Added sticky footer CSS"]
    
    # If no style tag found, add one before </head>
    head_close_pattern = r'</head>'
    head_match = re.search(head_close_pattern, content)
    
    if head_match:
        sticky_footer_style = """    <style>
        /* Sticky Footer Solution */
        html, body {
            height: 100%;
            margin: 0;
            padding: 0;
        }
        
        body {
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }
        
        /* Main content wrapper */
        main, #main, .main-content, 
        .hero-section + *, 
        .service-areas-section,
        .services-content,
        .contact-content,
        .payment-content,
        .about-content {
            flex: 1 0 auto;
        }
        
        /* Ensure footer stays at bottom */
        .site-footer, footer {
            flex-shrink: 0;
            margin-top: auto;
            width: 100%;
        }
        
        /* Fix for sections that might break layout */
        section {
            width: 100%;
        }
        
        /* Ensure proper spacing */
        .service-areas-section {
            padding-bottom: 3rem;
        }
        
        /* Mobile adjustments */
        @media (max-width: 768px) {
            body {
                min-height: 100vh;
                min-height: -webkit-fill-available;
            }
        }
    </style>
"""
        content = content[:head_match.start()] + sticky_footer_style + '\n' + content[head_match.start():]
        changes_made = True
        return True, ["Added sticky footer style block"]
    
    return False, []

# Process all HTML files
html_files = []

# Add main pages
main_pages = [
    'index.html',
    'services.html',
    'contact.html',
    'payment-methods.html',
    'about.html',
    'forms.html',
    'forms-clean.html',
    'manage369-forms.html'
]

for page in main_pages:
    if os.path.exists(page):
        html_files.append(page)

# Add property management pages
for file in Path('property-management').rglob('index.html'):
    html_files.append(str(file))

# Add service pages
for file in Path('services').rglob('index.html'):
    html_files.append(str(file))

print(f"Fixing sticky footer on {len(html_files)} HTML files")
print("-" * 50)

updated = 0
skipped = 0
errors = 0

for file in html_files:
    try:
        result, changes = fix_sticky_footer(file)
        if result:
            print(f"[FIXED] {file}")
            updated += 1
        else:
            skipped += 1
    except Exception as e:
        errors += 1
        print(f"[ERROR] {file}: {str(e)}")

print("-" * 50)
print(f"\n[COMPLETE] Sticky footer fixes complete!")
print(f"\nResults:")
print(f"  Files updated: {updated}")
print(f"  Files unchanged: {skipped}")
print(f"  Errors: {errors}")