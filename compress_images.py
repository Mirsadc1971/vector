#!/usr/bin/env python3
"""
Image Compression Script for manage369-live website
Compresses large JPG/PNG images while maintaining quality at 85%
Creates compressed versions with '_compressed' suffix and generates a report
"""

import os
from PIL import Image
import sys
from pathlib import Path

def get_file_size(file_path):
    """Get file size in bytes and return formatted string"""
    size_bytes = os.path.getsize(file_path)

    # Convert to human readable format
    if size_bytes >= 1024*1024:  # MB
        return f"{size_bytes / (1024*1024):.1f}MB ({size_bytes:,} bytes)"
    elif size_bytes >= 1024:  # KB
        return f"{size_bytes / 1024:.1f}KB ({size_bytes:,} bytes)"
    else:
        return f"{size_bytes} bytes"

def compress_image(input_path, output_path, quality=85):
    """
    Compress an image file

    Args:
        input_path: Path to input image
        output_path: Path for compressed output
        quality: JPEG quality (1-100, where 100 is best quality)

    Returns:
        tuple: (original_size, compressed_size, success)
    """
    try:
        original_size = os.path.getsize(input_path)

        # Open and process image
        with Image.open(input_path) as img:
            # Convert to RGB if necessary (for PNG with transparency)
            if img.mode in ('RGBA', 'P'):
                # Create white background for transparent images
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            # Save compressed version
            img.save(output_path, 'JPEG', quality=quality, optimize=True)

        compressed_size = os.path.getsize(output_path)
        return original_size, compressed_size, True

    except Exception as e:
        print(f"Error compressing {input_path}: {e}")
        return 0, 0, False

def main():
    # Define the images directory
    script_dir = Path(__file__).parent
    images_dir = script_dir / "images"

    if not images_dir.exists():
        print(f"Error: Images directory not found at {images_dir}")
        sys.exit(1)

    # Priority images to compress (large files mentioned in task)
    priority_images = [
        "manage369favicon1.png",
        "chestnutmanage369.jpg",
        "chestnutmanage3692.jpg",
        "northbrook2manage369.jpg",
        "manage369livingroomskokie.jpg",
        "manage369randolphstation.jpg"
    ]

    # Also process other large JPG/PNG files
    large_image_extensions = {'.jpg', '.jpeg', '.png'}
    min_size_kb = 100  # Process files larger than 100KB

    print("=" * 60)
    print("IMAGE COMPRESSION REPORT")
    print("=" * 60)
    print(f"Target directory: {images_dir}")
    print(f"Compression quality: 85%")
    print()

    total_original_size = 0
    total_compressed_size = 0
    processed_files = 0
    failed_files = 0

    # Get all image files to process
    files_to_process = []

    # Add priority files first
    for filename in priority_images:
        file_path = images_dir / filename
        if file_path.exists():
            files_to_process.append(file_path)
        else:
            print(f"Priority file not found: {filename}")

    # Add other large image files
    for file_path in images_dir.iterdir():
        if (file_path.is_file() and
            file_path.suffix.lower() in large_image_extensions and
            file_path not in files_to_process):

            file_size = os.path.getsize(file_path)
            if file_size > min_size_kb * 1024:  # Convert KB to bytes
                files_to_process.append(file_path)

    print(f"Found {len(files_to_process)} image files to process")
    print()

    # Process each file
    for file_path in files_to_process:
        filename = file_path.name
        file_ext = file_path.suffix.lower()

        # Create output filename with _compressed suffix
        name_without_ext = file_path.stem
        output_filename = f"{name_without_ext}_compressed.jpg"
        output_path = file_path.parent / output_filename

        # Skip if compressed version already exists
        if output_path.exists():
            print(f"[SKIP] Skipping {filename} (compressed version already exists)")
            continue

        print(f"[PROCESSING] {filename}")
        print(f"   Original size: {get_file_size(file_path)}")

        # Compress the image
        original_size, compressed_size, success = compress_image(file_path, output_path, quality=85)

        if success:
            savings = original_size - compressed_size
            savings_percent = (savings / original_size) * 100 if original_size > 0 else 0

            print(f"   Compressed size: {get_file_size(output_path)}")
            print(f"   Space saved: {savings / (1024*1024):.1f}MB ({savings_percent:.1f}%)")
            print(f"   [SUCCESS] Saved as: {output_filename}")

            total_original_size += original_size
            total_compressed_size += compressed_size
            processed_files += 1
        else:
            print(f"   [FAILED] Failed to compress")
            failed_files += 1

        print()

    # Final summary
    print("=" * 60)
    print("COMPRESSION SUMMARY")
    print("=" * 60)

    if processed_files > 0:
        total_savings = total_original_size - total_compressed_size
        total_savings_percent = (total_savings / total_original_size) * 100

        print(f"Files processed successfully: {processed_files}")
        print(f"Files failed: {failed_files}")
        print(f"Total original size: {total_original_size / (1024*1024):.1f}MB ({total_original_size:,} bytes)")
        print(f"Total compressed size: {total_compressed_size / (1024*1024):.1f}MB ({total_compressed_size:,} bytes)")
        print(f"Total space saved: {total_savings / (1024*1024):.1f}MB ({total_savings_percent:.1f}%)")

        # Save report to file
        report_path = script_dir / "image_compression_report.txt"
        with open(report_path, "w") as f:
            f.write("IMAGE COMPRESSION REPORT\n")
            f.write("=" * 40 + "\n")
            f.write(f"Date: {Path(__file__).stat().st_mtime}\n")
            f.write(f"Files processed: {processed_files}\n")
            f.write(f"Files failed: {failed_files}\n")
            f.write(f"Total original size: {total_original_size / (1024*1024):.1f}MB\n")
            f.write(f"Total compressed size: {total_compressed_size / (1024*1024):.1f}MB\n")
            f.write(f"Total space saved: {total_savings / (1024*1024):.1f}MB ({total_savings_percent:.1f}%)\n")

        print(f"\n[REPORT] Detailed report saved to: {report_path}")

    else:
        print("No files were processed successfully.")

    print("\n[COMPLETE] Image compression finished!")

if __name__ == "__main__":
    main()