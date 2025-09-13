#!/usr/bin/env python3
"""
Comprehensive Image Optimization Script for Manage369
Optimizes all images over 100KB by:
1. Converting to WebP format (keeping originals)
2. Resizing images larger than 1920px wide
3. Compressing images to reduce file size by 50-70%
"""

import os
import sys
from PIL import Image, ImageOps
import glob

# Configuration
MAX_WIDTH = 1920
MAX_HEIGHT = 1080
WEBP_QUALITY = 85  # Good balance between quality and size
JPEG_QUALITY = 85
MIN_SIZE_KB = 100

def get_file_size_kb(filepath):
    """Get file size in KB"""
    return os.path.getsize(filepath) / 1024

def optimize_image(input_path, output_path, format='WEBP', quality=85, max_width=1920, max_height=1080):
    """
    Optimize a single image
    """
    try:
        with Image.open(input_path) as img:
            # Convert to RGB if necessary (for WebP)
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')

            # Get original dimensions
            original_width, original_height = img.size

            # Calculate new dimensions if resizing needed
            if original_width > max_width or original_height > max_height:
                # Calculate aspect ratio
                ratio = min(max_width / original_width, max_height / original_height)
                new_width = int(original_width * ratio)
                new_height = int(original_height * ratio)

                # Resize with high quality resampling
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                print(f"  Resized from {original_width}x{original_height} to {new_width}x{new_height}")

            # Apply additional optimization
            if format == 'WEBP':
                img.save(output_path, 'WEBP', quality=quality, optimize=True, method=6)
            elif format == 'JPEG':
                img.save(output_path, 'JPEG', quality=quality, optimize=True, progressive=True)

            return True

    except Exception as e:
        print(f"  Error processing {input_path}: {e}")
        return False

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(script_dir, 'images')

    if not os.path.exists(images_dir):
        print(f"Images directory not found: {images_dir}")
        return

    print("COMPREHENSIVE IMAGE OPTIMIZATION")
    print("=" * 50)

    # Find all images over 100KB
    large_images = []
    for ext in ['*.jpg', '*.jpeg', '*.png']:
        pattern = os.path.join(images_dir, ext)
        for filepath in glob.glob(pattern):
            size_kb = get_file_size_kb(filepath)
            if size_kb > MIN_SIZE_KB:
                large_images.append((filepath, size_kb))

    # Sort by size (largest first)
    large_images.sort(key=lambda x: x[1], reverse=True)

    if not large_images:
        print("No images over 100KB found.")
        return

    print(f"Found {len(large_images)} images over {MIN_SIZE_KB}KB:")
    print("-" * 50)

    total_original_size = 0
    total_optimized_size = 0

    for filepath, size_kb in large_images:
        filename = os.path.basename(filepath)
        print(f"\nProcessing: {filename} ({size_kb:.1f}KB)")

        total_original_size += size_kb

        # Skip if already has _compressed or _optimized suffix
        if '_compressed' in filename or '_optimized' in filename:
            print("  Already processed, skipping...")
            continue

        # Create optimized versions
        base_name, ext = os.path.splitext(filename)

        # 1. Create WebP version
        webp_path = os.path.join(images_dir, f"{base_name}_optimized.webp")
        if optimize_image(filepath, webp_path, 'WEBP', WEBP_QUALITY, MAX_WIDTH, MAX_HEIGHT):
            webp_size = get_file_size_kb(webp_path)
            print(f"  WebP created: {webp_size:.1f}KB ({((size_kb - webp_size) / size_kb * 100):.1f}% reduction)")
            total_optimized_size += webp_size
        else:
            print("  WebP creation failed")

        # 2. Create optimized JPEG version (for fallback)
        if ext.lower() in ['.jpg', '.jpeg']:
            jpeg_path = os.path.join(images_dir, f"{base_name}_optimized.jpg")
            if optimize_image(filepath, jpeg_path, 'JPEG', JPEG_QUALITY, MAX_WIDTH, MAX_HEIGHT):
                jpeg_size = get_file_size_kb(jpeg_path)
                print(f"  JPEG optimized: {jpeg_size:.1f}KB ({((size_kb - jpeg_size) / size_kb * 100):.1f}% reduction)")

        # 3. For PNG files, create both WebP and optimized JPEG
        elif ext.lower() == '.png':
            jpeg_path = os.path.join(images_dir, f"{base_name}_optimized.jpg")
            if optimize_image(filepath, jpeg_path, 'JPEG', JPEG_QUALITY, MAX_WIDTH, MAX_HEIGHT):
                jpeg_size = get_file_size_kb(jpeg_path)
                print(f"  JPEG version created: {jpeg_size:.1f}KB ({((size_kb - jpeg_size) / size_kb * 100):.1f}% reduction)")

    # Summary
    print("\n" + "=" * 50)
    print("OPTIMIZATION SUMMARY")
    print("=" * 50)
    print(f"Images processed: {len(large_images)}")
    print(f"Original total size: {total_original_size:.1f}KB")
    if total_optimized_size > 0:
        print(f"WebP total size: {total_optimized_size:.1f}KB")
        print(f"Total reduction: {((total_original_size - total_optimized_size) / total_original_size * 100):.1f}%")

    # Show remaining large images
    print("\nCURRENT LARGE IMAGES (>100KB):")
    print("-" * 50)
    remaining_large = []
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.webp']:
        pattern = os.path.join(images_dir, ext)
        for filepath in glob.glob(pattern):
            size_kb = get_file_size_kb(filepath)
            if size_kb > MIN_SIZE_KB:
                remaining_large.append((os.path.basename(filepath), size_kb))

    remaining_large.sort(key=lambda x: x[1], reverse=True)
    for filename, size_kb in remaining_large:
        print(f"  {filename}: {size_kb:.1f}KB")

    print("\nImage optimization complete!")
    print("\nNext steps:")
    print("1. Update HTML to use _optimized.webp versions with JPEG fallbacks")
    print("2. Add lazy loading for images below the fold")
    print("3. Test page load times")

if __name__ == "__main__":
    main()