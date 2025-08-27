#!/usr/bin/env python3
"""
Convert images to WebP format for better performance
Requires: pip install Pillow
"""

import os
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow library not installed!")
    print("Please run: pip install Pillow")
    exit(1)

def convert_to_webp(input_path, quality=85):
    """Convert a single image to WebP format"""
    try:
        # Open the image
        img = Image.open(input_path)
        
        # Convert RGBA to RGB if necessary (WebP handles transparency differently)
        if img.mode in ('RGBA', 'LA', 'P'):
            # Create a white background
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Create output path
        output_path = input_path.with_suffix('.webp')
        
        # Save as WebP
        img.save(output_path, 'WEBP', quality=quality, method=6)
        
        # Calculate size reduction
        original_size = os.path.getsize(input_path)
        new_size = os.path.getsize(output_path)
        reduction = (1 - new_size/original_size) * 100
        
        print(f"Converted: {input_path.name} -> {output_path.name}")
        print(f"   Size: {original_size//1024}KB -> {new_size//1024}KB ({reduction:.1f}% reduction)")
        
        return True
    except Exception as e:
        print(f"ERROR converting {input_path}: {e}")
        return False

def main():
    print("WebP Image Converter")
    print("=" * 50)
    
    # Find all images
    images_dir = Path('images')
    if not images_dir.exists():
        print("ERROR: Images directory not found!")
        return
    
    # Get all JPG and PNG files
    image_files = list(images_dir.glob('*.jpg')) + \
                  list(images_dir.glob('*.jpeg')) + \
                  list(images_dir.glob('*.png'))
    
    # Filter out files that already have WebP versions
    to_convert = []
    for img in image_files:
        webp_path = img.with_suffix('.webp')
        if not webp_path.exists():
            to_convert.append(img)
    
    if not to_convert:
        print("All images already have WebP versions!")
        return
    
    print(f"\nFound {len(to_convert)} images to convert:")
    for img in to_convert:
        print(f"  - {img.name}")
    
    print("\nStarting conversion...")
    print("-" * 30)
    
    success_count = 0
    total_original = 0
    total_new = 0
    
    for img in to_convert:
        if convert_to_webp(img):
            success_count += 1
            total_original += os.path.getsize(img)
            total_new += os.path.getsize(img.with_suffix('.webp'))
    
    print("-" * 30)
    print(f"\nConversion Summary:")
    print(f"  Successfully converted: {success_count}/{len(to_convert)}")
    
    if success_count > 0:
        total_reduction = (1 - total_new/total_original) * 100
        print(f"  Total size reduction: {total_reduction:.1f}%")
        print(f"  Space saved: {(total_original - total_new)//1024}KB")
    
    print("\nNext steps:")
    print("1. Run: python optimize_images.py")
    print("2. This will update HTML files to use WebP with fallbacks")
    print("3. Test with Lighthouse to verify improvements")

if __name__ == "__main__":
    main()