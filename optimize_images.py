from PIL import Image
import os

# List of JPG images that need WebP versions
jpg_images = [
    'Manage3693.jpg',
    'buck4manage369.jpg', 
    'businessman-skyline.jpg',
    'chestnut2manage369.jpg',
    'kenmore2manage369.jpg',
    'manstandingmanage369.jpg',
    'northbrook2manage369.jpg',
    'northfield1manage369.jpg',
    'northfield2manage369.jpg'
]

print("Converting JPG images to WebP format...")

for jpg_file in jpg_images:
    jpg_path = f'images/{jpg_file}'
    webp_path = jpg_path.replace('.jpg', '.webp')
    
    # Skip if WebP already exists
    if os.path.exists(webp_path):
        print(f"[SKIP] {jpg_file} - WebP already exists")
        continue
    
    if os.path.exists(jpg_path):
        try:
            # Open and convert to WebP
            img = Image.open(jpg_path)
            
            # Convert RGBA to RGB if necessary
            if img.mode == 'RGBA':
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                rgb_img.paste(img, mask=img.split()[3])
                img = rgb_img
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Save as WebP with high quality
            img.save(webp_path, 'WEBP', quality=85, method=6)
            
            # Get file sizes for comparison
            jpg_size = os.path.getsize(jpg_path) / 1024
            webp_size = os.path.getsize(webp_path) / 1024
            savings = ((jpg_size - webp_size) / jpg_size) * 100
            
            print(f"[OK] {jpg_file} -> WebP (saved {savings:.1f}% - {jpg_size:.1f}KB to {webp_size:.1f}KB)")
            
        except Exception as e:
            print(f"[ERROR] Failed to convert {jpg_file}: {str(e)}")
    else:
        print(f"[MISSING] {jpg_file} not found")

print("\nOptimizing existing JPG images...")

# Optimize JPG compression
for jpg_file in jpg_images:
    jpg_path = f'images/{jpg_file}'
    
    if os.path.exists(jpg_path):
        try:
            img = Image.open(jpg_path)
            
            # Get original size
            original_size = os.path.getsize(jpg_path) / 1024
            
            # Save with optimized settings
            temp_path = jpg_path + '.tmp'
            
            # Convert RGBA to RGB if necessary
            if img.mode == 'RGBA':
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                rgb_img.paste(img, mask=img.split()[3])
                img = rgb_img
            elif img.mode != 'RGB':
                img = img.convert('RGB')
                
            img.save(temp_path, 'JPEG', quality=85, optimize=True, progressive=True)
            
            # Check new size
            new_size = os.path.getsize(temp_path) / 1024
            
            # Only replace if smaller
            if new_size < original_size:
                os.replace(temp_path, jpg_path)
                savings = ((original_size - new_size) / original_size) * 100
                print(f"[OPTIMIZED] {jpg_file} - saved {savings:.1f}% ({original_size:.1f}KB to {new_size:.1f}KB)")
            else:
                os.remove(temp_path)
                print(f"[SKIP] {jpg_file} - already optimized")
                
        except Exception as e:
            print(f"[ERROR] Failed to optimize {jpg_file}: {str(e)}")
            if os.path.exists(temp_path):
                os.remove(temp_path)

print("\nImage optimization complete!")