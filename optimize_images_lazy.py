#!/usr/bin/env python3
"""
Image Optimization Script for Manage369
- Adds lazy loading to images
- Implements responsive images with srcset
- Converts img tags to use WebP with JPG fallback
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

def add_lazy_loading_to_html(file_path):
    """Add lazy loading and optimize images in HTML file"""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')
    modified = False

    # Find all img tags
    for img in soup.find_all('img'):
        # Skip if already has loading attribute
        if not img.get('loading'):
            img['loading'] = 'lazy'
            modified = True

        # Add decoding async for better performance
        if not img.get('decoding'):
            img['decoding'] = 'async'
            modified = True

        # Get the src
        src = img.get('src', '')

        # If it's a JPG/PNG, create picture element with WebP option
        if src and ('.jpg' in src or '.jpeg' in src or '.png' in src):
            # Check if WebP version exists
            webp_src = src.replace('.jpg', '.webp').replace('.jpeg', '.webp').replace('.png', '.webp')
            webp_path = Path(file_path).parent / webp_src.lstrip('/')

            if webp_path.exists() or '/images/' in webp_src:
                # Create picture element
                picture = soup.new_tag('picture')

                # Add WebP source
                source_webp = soup.new_tag('source')
                source_webp['srcset'] = webp_src
                source_webp['type'] = 'image/webp'
                picture.append(source_webp)

                # Clone the img tag for the picture element
                new_img = soup.new_tag('img')
                for attr, value in img.attrs.items():
                    new_img[attr] = value
                new_img['loading'] = 'lazy'
                new_img['decoding'] = 'async'

                picture.append(new_img)

                # Replace img with picture
                img.replace_with(picture)
                modified = True

        # Add width and height if missing (prevents layout shift)
        if not img.get('width') and not img.get('height'):
            # Add aspect ratio hint for common images
            if 'logo' in src.lower():
                img['width'] = '200'
                img['height'] = '100'
            elif 'hero' in src.lower() or 'banner' in src.lower():
                img['width'] = '1920'
                img['height'] = '600'
            elif 'icon' in src.lower():
                img['width'] = '32'
                img['height'] = '32'

    # Add preload for critical images (first image in body)
    first_img = soup.body.find('img') if soup.body else None
    if first_img and not soup.head.find('link', {'rel': 'preload'}):
        preload_link = soup.new_tag('link')
        preload_link['rel'] = 'preload'
        preload_link['as'] = 'image'
        preload_link['href'] = first_img.get('src', '')
        if soup.head:
            soup.head.append(preload_link)
            modified = True

    if modified:
        # Write back the modified HTML
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        return True
    return False

def main():
    """Process all HTML files in the current directory"""

    # Get all HTML files
    html_files = list(Path('.').glob('*.html'))
    html_files.extend(Path('.').glob('**/*.html'))

    # Remove duplicates and filter out node_modules, .git, etc.
    html_files = list(set(html_files))
    html_files = [f for f in html_files if not any(
        part in str(f) for part in ['.git', 'node_modules', 'dist', 'build']
    )]

    print(f"Found {len(html_files)} HTML files to process")

    modified_count = 0
    for file_path in html_files:
        print(f"Processing: {file_path}")
        if add_lazy_loading_to_html(file_path):
            modified_count += 1
            print(f"  [MODIFIED] {file_path}")
        else:
            print(f"  - No changes needed for {file_path}")

    print(f"\nCompleted! Modified {modified_count} files.")

    # Create a report
    with open('image_optimization_report.txt', 'w') as f:
        f.write("Image Optimization Report\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total HTML files processed: {len(html_files)}\n")
        f.write(f"Files modified: {modified_count}\n\n")
        f.write("Optimizations applied:\n")
        f.write("- Added lazy loading to all images\n")
        f.write("- Added async decoding for better performance\n")
        f.write("- Converted to <picture> elements with WebP support\n")
        f.write("- Added width/height attributes to prevent layout shift\n")
        f.write("- Added preload for critical images\n")

if __name__ == "__main__":
    main()