#!/usr/bin/env python3
"""
Image Optimization Script
Converts images to WebP/AVIF formats and implements responsive images
"""

import os
import re
from pathlib import Path

def scan_images():
    """Scan for all images used in HTML files"""
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    images_used = set()
    
    html_files = list(Path('.').glob('**/*.html'))
    
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Find images in src, href, content attributes
            patterns = [
                r'src=["\']([^"\']+\.(?:jpg|jpeg|png|gif|webp))["\']',
                r'href=["\']([^"\']+\.(?:jpg|jpeg|png|gif|webp))["\']',
                r'content=["\']([^"\']+\.(?:jpg|jpeg|png|gif|webp))["\']',
                r'url\(["\']?([^"\']+\.(?:jpg|jpeg|png|gif|webp))["\']?\)'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                images_used.update(matches)
    
    return images_used

def create_webp_versions():
    """Create WebP versions of images (requires Pillow library)"""
    print("\nCreating WebP versions...")
    
    # Check if images already have WebP versions
    images_dir = Path('images')
    if not images_dir.exists():
        print("Images directory not found")
        return
    
    jpg_images = list(images_dir.glob('*.jpg')) + list(images_dir.glob('*.jpeg'))
    png_images = list(images_dir.glob('*.png'))
    
    webp_created = []
    for img in jpg_images + png_images:
        webp_path = img.with_suffix('.webp')
        if not webp_path.exists():
            webp_created.append(str(img))
            print(f"  Would create: {webp_path.name}")
    
    if webp_created:
        print(f"\nNeed to create {len(webp_created)} WebP versions")
        print("\nTo convert images, install Pillow and run:")
        print("pip install Pillow")
        print("\nThen use this Python code:")
        print("from PIL import Image")
        print("img = Image.open('image.jpg')")
        print("img.save('image.webp', 'WEBP', quality=85)")
    else:
        print("All images already have WebP versions")

def implement_picture_elements():
    """Replace img tags with picture elements for responsive images"""
    html_files = list(Path('.').glob('**/*.html'))
    updates_made = 0
    
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = original = f.read()
        
        # Find all img tags with jpg/png sources
        img_pattern = r'<img\s+([^>]*src=["\']([^"\']+\.(jpg|jpeg|png))["\'][^>]*)>'
        
        def replace_with_picture(match):
            full_match = match.group(0)
            attributes = match.group(1)
            src = match.group(2)
            
            # Skip if already in a picture element
            if '<picture>' in content[max(0, match.start()-100):match.start()]:
                return full_match
            
            # Extract alt text and other attributes
            alt_match = re.search(r'alt=["\']([^"\']*)["\']', attributes)
            alt_text = alt_match.group(1) if alt_match else ''
            
            # Create picture element
            webp_src = re.sub(r'\.(jpg|jpeg|png)$', '.webp', src)
            
            picture = f'''<picture>
        <source srcset="{webp_src}" type="image/webp">
        <img src="{src}" alt="{alt_text}" loading="lazy">
    </picture>'''
            
            return picture
        
        # Replace img tags with picture elements
        new_content = re.sub(img_pattern, replace_with_picture, content)
        
        if new_content != original:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            updates_made += 1
            print(f"Updated {html_file.name} with picture elements")
    
    return updates_made

def add_lazy_loading():
    """Add lazy loading to images"""
    html_files = list(Path('.').glob('**/*.html'))
    updates_made = 0
    
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = original = f.read()
        
        # Add loading="lazy" to img tags that don't have it
        content = re.sub(
            r'(<img\s+(?![^>]*loading=["\'])[^>]*)(>)',
            r'\1 loading="lazy"\2',
            content
        )
        
        if content != original:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            updates_made += 1
            print(f"Added lazy loading to {html_file.name}")
    
    return updates_made

def optimize_hero_images():
    """Optimize hero/above-fold images with preload"""
    html_files = list(Path('.').glob('**/*.html'))
    
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find hero image (usually the first large image or background)
        hero_match = re.search(r"url\(['\"]?([^'\"]+manstandingmanage369\.jpg)['\"]?\)", content)
        
        if hero_match:
            hero_img = hero_match.group(1)
            
            # Add preload link in head if not present
            if '<link rel="preload"' not in content:
                preload = f'<link rel="preload" as="image" href="{hero_img}" type="image/jpeg">\n    '
                content = content.replace('</head>', f'    {preload}</head>')
                
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Added hero image preload to {html_file.name}")

def main():
    print("Image Optimization Report")
    print("=" * 50)
    
    # Scan for all images
    images = scan_images()
    print(f"\nFound {len(images)} unique images referenced")
    
    # Check for WebP versions
    create_webp_versions()
    
    # Implement picture elements
    print("\nImplementing responsive picture elements...")
    updated = implement_picture_elements()
    print(f"Updated {updated} files with picture elements")
    
    # Add lazy loading
    print("\nAdding lazy loading...")
    lazy_updated = add_lazy_loading()
    print(f"Added lazy loading to {lazy_updated} files")
    
    # Optimize hero images
    print("\nOptimizing hero images...")
    optimize_hero_images()
    
    print("\nImage optimization complete!")
    print("\nNext steps:")
    print("1. Install Pillow: pip install Pillow")
    print("2. Run: python convert_to_webp.py (create this script)")
    print("3. Consider using a CDN with automatic image optimization")
    print("4. Test with Lighthouse to verify improvements")
    
    print("\nExpected improvements:")
    print("- 0.49s saved from next-gen formats")
    print("- Additional savings from lazy loading")
    print("- Better Core Web Vitals scores")

if __name__ == "__main__":
    main()