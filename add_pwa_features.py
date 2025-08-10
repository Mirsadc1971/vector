import os
import re

# Add theme color and service worker to all property pages
property_dirs = os.listdir('property-management')
property_dirs = [d for d in property_dirs if os.path.isdir(f'property-management/{d}')]

theme_color_meta = '    <meta name="theme-color" content="#1e40af">\n'
service_worker_script = """
        // Register Service Worker for PWA
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('/sw.js')
                    .then(registration => console.log('ServiceWorker registered:', registration))
                    .catch(error => console.log('ServiceWorker registration failed:', error));
            });
        }"""

fixed_count = 0

for dir_name in property_dirs:
    file_path = f'property-management/{dir_name}/index.html'
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        modified = False
        
        # Add theme color if missing
        if 'theme-color' not in content:
            # Add after viewport meta tag
            pattern = r'(    <meta name="viewport"[^>]+>\n)'
            replacement = r'\1' + theme_color_meta
            new_content = re.sub(pattern, replacement, content)
            if new_content != content:
                content = new_content
                modified = True
        
        # Add service worker if missing
        if 'serviceWorker' not in content:
            # Add before closing script tag and body
            pattern = r'(    </script>\n)(</body>)'
            replacement = r'\1' + service_worker_script + r'\n    </script>\n\2'
            
            # First, fix the pattern to match actual structure
            if '    </script>\n</body>' in content:
                content = content.replace('    </script>\n</body>', 
                                         '    </script>' + service_worker_script + '\n    </script>\n</body>')
                modified = True
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            fixed_count += 1
            print(f"[OK] Updated {dir_name}")
        else:
            print(f"[SKIP] {dir_name} already has PWA features")

print(f"\nAdded PWA features to {fixed_count} property pages!")