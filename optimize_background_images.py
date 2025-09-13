#!/usr/bin/env python3
"""
Background Image Optimization Script
Updates index.html to use optimized WebP images with JPG fallback
"""

import re
import os

def detect_webp_support_script():
    """Generate WebP detection script"""
    return '''
<script>
(function() {
    'use strict';

    // WebP detection function
    function supportsWebP(callback) {
        var webP = new Image();
        webP.onload = webP.onerror = function () {
            callback(webP.height == 2);
        };
        webP.src = 'data:image/webp;base64,UklGRjoAAABXRUJQVlA4IC4AAACyAgCdASoCAAIALmk0mk0iIiIiIgBoSygABc6WWgAA/veff/0PP8bA//LwYAAA';
    }

    // Add WebP support class to HTML element
    supportsWebP(function(supported) {
        var htmlElement = document.documentElement;
        if (supported) {
            htmlElement.classList.add('webp');
        } else {
            htmlElement.classList.add('no-webp');
        }
    });

    // Preload critical background images
    function preloadCriticalImages() {
        var link1 = document.createElement('link');
        link1.rel = 'preload';
        link1.as = 'image';

        var link2 = document.createElement('link');
        link2.rel = 'preload';
        link2.as = 'image';

        // Check WebP support and preload appropriate format
        supportsWebP(function(supported) {
            if (supported) {
                link1.href = 'images/manage369randolphstation.webp';
                link1.type = 'image/webp';
            } else {
                link2.href = 'images/manage369randolphstation.jpg';
                link2.type = 'image/jpeg';
            }

            document.head.appendChild(link1);
            document.head.appendChild(link2);
        });
    }

    // Run preload on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', preloadCriticalImages);
    } else {
        preloadCriticalImages();
    }

})();
</script>'''

def get_critical_css():
    """Generate critical CSS for above-the-fold content"""
    return '''
<style>
/* Critical CSS for above-the-fold content */
.hero-optimized {
    padding: 40px 20px 20px;
    text-align: center;
    color: white;
    min-height: 600px;
    display: flex;
    align-items: flex-start;
    justify-content: center;
    position: relative;
    overflow: hidden;
    will-change: transform;
    transform: translateZ(0);
    background-attachment: scroll;
    background-repeat: no-repeat;
    background-size: cover;
    background-position: center;
}

.webp .hero-optimized {
    background: linear-gradient(135deg, rgba(8,66,152,0.25) 0%, rgba(244,162,97,0.25) 100%),
                url('images/manage369randolphstation.webp') center/cover !important;
}

.no-webp .hero-optimized {
    background: linear-gradient(135deg, rgba(8,66,152,0.25) 0%, rgba(244,162,97,0.25) 100%),
                url('images/manage369randolphstation.jpg') center/cover !important;
}

.hero-optimized .hero-content {
    max-width: 1200px;
    margin: 0 auto;
    margin-top: 80px;
    position: relative;
    z-index: 2;
}

.hero-optimized h1 {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    color: #ffffff !important;
    text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.4), 0 0 20px rgba(0,0,0,0.5);
    line-height: 1.2;
}

@media (max-width: 768px) {
    .hero-optimized {
        min-height: 400px;
        padding: 20px 15px 15px;
    }
    .hero-optimized .hero-content {
        margin-top: 40px;
    }
    .hero-optimized h1 {
        font-size: 2rem;
        margin-top: 1rem;
    }
}
</style>'''

def update_index_html():
    """Update index.html with optimized background image implementation"""

    index_path = 'index.html'

    if not os.path.exists(index_path):
        print(f"Error: {index_path} not found")
        return False

    # Read the current index.html
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Backup original file
    with open('index_original_backup.html', 'w', encoding='utf-8') as f:
        f.write(content)

    # Add WebP detection script before closing head tag
    webp_script = detect_webp_support_script()

    if '</head>' in content:
        content = content.replace('</head>', f'{webp_script}\n</head>')
        print("+ Added WebP detection script to head")

    # Add critical CSS right after head tag
    critical_css = get_critical_css()

    head_pattern = r'(<head[^>]*>)'
    if re.search(head_pattern, content):
        content = re.sub(head_pattern, f'\\1\n{critical_css}', content)
        print("+ Added critical CSS for above-the-fold content")

    # Add image optimization CSS link
    css_link = '<link rel="stylesheet" href="css/image-optimization.css">'

    if '</head>' in content:
        content = content.replace('</head>', f'{css_link}\n</head>')
        print("+ Added image optimization CSS link")

    # Update the main hero section to use optimized classes
    hero_pattern = r'<section class="hero"([^>]*style="[^"]*manage369randolphstation\.jpg[^"]*"[^>]*)>'

    if re.search(hero_pattern, content):
        # Replace the inline style with optimized class
        replacement = '<section class="hero hero-optimized">'
        content = re.sub(hero_pattern, replacement, content)
        print("+ Updated main hero section with optimized class")

    # Update other sections that use the background image
    # Find all style attributes that reference the image
    bg_pattern = r'(style="[^"]*url\([\'"]?images/manage369randolphstation\.jpg[\'"]?\)[^"]*")'

    def replace_bg_style(match):
        style_attr = match.group(1)
        # Add optimized class and keep simplified style
        return 'class="section-with-bg" style="padding: 40px 20px 20px; text-align: center; color: white; min-height: 600px; display: flex; align-items: flex-start; justify-content: center; position: relative; overflow: hidden;"'

    updated_content = re.sub(bg_pattern, replace_bg_style, content)

    if updated_content != content:
        content = updated_content
        print("+ Updated background image references in other sections")

    # Write the updated content
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"+ Successfully updated {index_path}")
    print(f"+ Original file backed up as index_original_backup.html")

    return True

def main():
    """Main function to run the optimization"""
    print("Starting background image optimization...")
    print("=" * 50)

    # Check if WebP file exists
    if not os.path.exists('images/manage369randolphstation.webp'):
        print("Warning: WebP version of image not found")
        print("   Please ensure images/manage369randolphstation.webp exists")
    else:
        print("+ WebP image file found")

    # Check if JPG file exists
    if not os.path.exists('images/manage369randolphstation.jpg'):
        print("Error: JPG version of image not found")
        return False
    else:
        print("+ JPG image file found")

    # Update index.html
    if update_index_html():
        print("\n" + "=" * 50)
        print("Background image optimization completed successfully!")
        print("\nNext steps:")
        print("1. Test the website to ensure images load properly")
        print("2. Check WebP format is used in supported browsers")
        print("3. Verify performance improvements with browser dev tools")
        print("4. Consider implementing similar optimizations for other pages")

        return True
    else:
        print("Failed to update index.html")
        return False

if __name__ == "__main__":
    main()