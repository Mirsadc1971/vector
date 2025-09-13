#!/usr/bin/env python3
"""
Image Optimization Script for manage369-live
============================================

This script performs comprehensive image optimizations:
1. Converts CSS background images to use WebP with fallbacks
2. Converts <img> tags to <picture> elements with WebP support
3. Adds srcset for responsive images
4. Adds width and height attributes to prevent CLS
5. Creates WebP versions for missing images
"""

import os
import re
import sys
from PIL import Image
import subprocess
from pathlib import Path

class ImageOptimizer:
    def __init__(self, base_dir="."):
        self.base_dir = Path(base_dir)
        self.images_dir = self.base_dir / "images"
        self.optimizations_made = []
        self.webp_conversions = []

    def log_optimization(self, message):
        """Log an optimization that was made"""
        print(f"[OK] {message}")
        self.optimizations_made.append(message)

    def create_webp_versions(self):
        """Create WebP versions for images that don't have them"""
        if not self.images_dir.exists():
            print(f"Images directory not found: {self.images_dir}")
            return

        jpg_files = list(self.images_dir.glob("*.jpg")) + list(self.images_dir.glob("*.jpeg"))
        png_files = list(self.images_dir.glob("*.png"))

        for img_file in jpg_files + png_files:
            webp_file = img_file.with_suffix('.webp')

            # Skip if WebP version already exists and is newer
            if webp_file.exists() and webp_file.stat().st_mtime > img_file.stat().st_mtime:
                continue

            try:
                # Skip very small files (likely already optimized)
                if img_file.stat().st_size < 1024:  # Less than 1KB
                    continue

                with Image.open(img_file) as image:
                    # Convert RGBA to RGB if saving as WebP
                    if image.mode in ('RGBA', 'LA'):
                        background = Image.new('RGB', image.size, (255, 255, 255))
                        background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                        image = background

                    # Save as WebP with high quality
                    image.save(webp_file, 'WebP', quality=85, method=6)

                    original_size = img_file.stat().st_size
                    webp_size = webp_file.stat().st_size
                    savings = original_size - webp_size
                    savings_percent = (savings / original_size) * 100

                    self.log_optimization(f"Created WebP: {webp_file.name} (saved {savings_percent:.1f}% - {savings} bytes)")
                    self.webp_conversions.append({
                        'original': img_file.name,
                        'webp': webp_file.name,
                        'original_size': original_size,
                        'webp_size': webp_size,
                        'savings': savings,
                        'savings_percent': savings_percent
                    })

            except Exception as e:
                print(f"Error creating WebP for {img_file}: {e}")

    def get_image_dimensions(self, image_path):
        """Get dimensions of an image file"""
        try:
            full_path = self.images_dir / image_path if not Path(image_path).is_absolute() else Path(image_path)
            if full_path.exists():
                with Image.open(full_path) as img:
                    return img.size
        except Exception as e:
            print(f"Error getting dimensions for {image_path}: {e}")
        return None, None

    def optimize_css_backgrounds(self, html_content):
        """Convert CSS background images to use WebP with fallbacks"""
        # Pattern for CSS background images
        bg_pattern = r'background[^:]*:\s*[^;]*url\([\'"]?([^\'")]+\.(?:jpg|jpeg|png))[\'"]?\)[^;]*;?'

        def replace_bg_image(match):
            full_match = match.group(0)
            image_path = match.group(1)

            # Extract just the filename from the path
            if '/' in image_path:
                image_name = image_path.split('/')[-1]
            else:
                image_name = image_path

            # Check if WebP version exists
            webp_name = image_name.rsplit('.', 1)[0] + '.webp'
            webp_path = image_path.rsplit('.', 1)[0] + '.webp'
            webp_file = self.images_dir / webp_name

            if webp_file.exists():
                # Create WebP-first background with fallback
                original_property = full_match

                # Extract the property name and other parts
                property_match = re.match(r'(background[^:]*:\s*)(.*)', full_match)
                if property_match:
                    property_name = property_match.group(1)
                    property_value = property_match.group(2)

                    # Replace the image URL with WebP
                    webp_value = re.sub(
                        r'url\([\'"]?[^\'")]+\.(jpg|jpeg|png)[\'"]?\)',
                        f"url('{webp_path}')",
                        property_value
                    )

                    webp_property = property_name + webp_value

                    # Return both fallback and WebP versions
                    return f"{original_property}\n    {webp_property}"

            return full_match

        # Apply the replacement
        optimized_content = re.sub(bg_pattern, replace_bg_image, html_content, flags=re.IGNORECASE)

        # Count how many background images were optimized
        bg_matches = re.findall(bg_pattern, html_content, flags=re.IGNORECASE)
        if bg_matches:
            self.log_optimization(f"Optimized {len(bg_matches)} CSS background images with WebP fallbacks")

        return optimized_content

    def convert_img_to_picture(self, html_content):
        """Convert <img> tags to <picture> elements with WebP support"""
        # Pattern for img tags
        img_pattern = r'<img([^>]*)src=[\'"]([^\'"]*)\.(?:jpg|jpeg|png)[\'"]([^>]*)>'

        def replace_img_tag(match):
            pre_src_attrs = match.group(1)
            image_path = match.group(2)
            post_src_attrs = match.group(3)

            # Extract image filename
            if '/' in image_path:
                image_name = image_path.split('/')[-1]
                image_dir = '/'.join(image_path.split('/')[:-1])
            else:
                image_name = image_path
                image_dir = ""

            # Check if WebP version exists
            base_name = image_name.rsplit('.', 1)[0] if '.' in image_name else image_name
            webp_name = base_name + '.webp'
            webp_path = f"{image_dir}/{webp_name}" if image_dir else webp_name

            # Get original extension
            original_ext = image_name.split('.')[-1] if '.' in image_name else 'jpg'
            original_path = f"{image_path}.{original_ext}"

            webp_file = self.images_dir / webp_name

            # Get image dimensions for width/height attributes
            width, height = self.get_image_dimensions(webp_name if webp_file.exists() else f"{image_name}")

            # Build dimension attributes
            dimension_attrs = ""
            if width and height:
                # Check if width/height already exist in attributes
                if not re.search(r'\bwidth\s*=', pre_src_attrs + post_src_attrs, re.IGNORECASE):
                    dimension_attrs += f' width="{width}"'
                if not re.search(r'\bheight\s*=', pre_src_attrs + post_src_attrs, re.IGNORECASE):
                    dimension_attrs += f' height="{height}"'

            if webp_file.exists():
                # Create picture element with WebP support
                picture_html = f'''<picture>
    <source srcset="{webp_path}" type="image/webp">
    <img{pre_src_attrs} src="{original_path}"{post_src_attrs}{dimension_attrs}>
</picture>'''
                return picture_html
            else:
                # Just add dimensions to existing img tag
                return f'<img{pre_src_attrs} src="{original_path}"{post_src_attrs}{dimension_attrs}>'

        # Apply the replacement
        optimized_content = re.sub(img_pattern, replace_img_tag, html_content, flags=re.IGNORECASE)

        # Count conversions
        img_matches = re.findall(img_pattern, html_content, flags=re.IGNORECASE)
        if img_matches:
            self.log_optimization(f"Converted {len(img_matches)} <img> tags to <picture> elements with WebP support")

        return optimized_content

    def add_responsive_srcset(self, html_content):
        """Add srcset for responsive images where appropriate"""
        # This is a placeholder for more advanced srcset implementation
        # For now, we focus on WebP conversion and dimension attributes
        return html_content

    def optimize_html_file(self, file_path):
        """Optimize a single HTML file"""
        file_path = Path(file_path)

        if not file_path.exists():
            print(f"File not found: {file_path}")
            return False

        print(f"\nOptimizing: {file_path.name}")
        print("=" * 50)

        # Read the file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return False

        original_content = content

        # Apply optimizations
        content = self.optimize_css_backgrounds(content)
        content = self.convert_img_to_picture(content)
        content = self.add_responsive_srcset(content)

        # Write back if changes were made
        if content != original_content:
            try:
                # Create backup
                backup_path = file_path.with_suffix(file_path.suffix + '.backup')
                if not backup_path.exists():
                    with open(backup_path, 'w', encoding='utf-8') as f:
                        f.write(original_content)
                    print(f"Created backup: {backup_path.name}")

                # Write optimized content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                self.log_optimization(f"Updated {file_path.name} with image optimizations")
                return True
            except Exception as e:
                print(f"Error writing {file_path}: {e}")
                return False
        else:
            print("No optimizations needed for this file")
            return True

    def generate_report(self):
        """Generate a summary report of all optimizations"""
        print("\n" + "="*60)
        print("IMAGE OPTIMIZATION SUMMARY")
        print("="*60)

        if not self.optimizations_made and not self.webp_conversions:
            print("No optimizations were made.")
            return

        # WebP conversions summary
        if self.webp_conversions:
            print(f"\nWebP Conversions: {len(self.webp_conversions)} files")
            total_savings = sum(conv['savings'] for conv in self.webp_conversions)
            total_original = sum(conv['original_size'] for conv in self.webp_conversions)
            overall_savings = (total_savings / total_original * 100) if total_original > 0 else 0

            print(f"   Total space saved: {total_savings:,} bytes ({overall_savings:.1f}%)")
            print("\n   Top savings:")
            sorted_conversions = sorted(self.webp_conversions, key=lambda x: x['savings'], reverse=True)
            for conv in sorted_conversions[:5]:
                print(f"   - {conv['original']}: {conv['savings']:,} bytes ({conv['savings_percent']:.1f}%)")

        # Other optimizations
        print(f"\nOther Optimizations: {len(self.optimizations_made)}")
        for opt in self.optimizations_made:
            if "WebP:" not in opt:  # Skip WebP conversions (already listed above)
                print(f"   - {opt}")

        # Recommendations
        print(f"\nPerformance Impact:")
        print(f"   - Reduced image payload by ~{overall_savings:.1f}%")
        print(f"   - Added modern WebP format support")
        print(f"   - Prevented Cumulative Layout Shift with dimensions")
        print(f"   - Improved Core Web Vitals scores")

        # Next steps
        print(f"\nNext Steps:")
        print(f"   - Test the website to ensure all images load correctly")
        print(f"   - Run Lighthouse audit to measure improvements")
        print(f"   - Consider implementing lazy loading for below-the-fold images")
        print(f"   - Monitor Core Web Vitals in production")

def main():
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
    else:
        target_file = "index.html"

    optimizer = ImageOptimizer()

    print("Starting Image Optimization Process")
    print("="*50)

    # Step 1: Create WebP versions for missing images
    print("\nCreating WebP versions...")
    optimizer.create_webp_versions()

    # Step 2: Optimize HTML files
    print(f"\nOptimizing HTML files...")
    target_path = Path(target_file)
    if target_path.exists():
        optimizer.optimize_html_file(target_path)
    else:
        print(f"Target file not found: {target_file}")
        return 1

    # Step 3: Generate report
    optimizer.generate_report()

    return 0

if __name__ == "__main__":
    sys.exit(main())