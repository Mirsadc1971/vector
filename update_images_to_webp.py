import os
import re

def update_image_to_picture(html_content, img_src):
    """Convert img tag to picture element with WebP source"""
    # Extract just the filename
    if '../images/' in img_src:
        filename = img_src.replace('../images/', '')
        prefix = '../images/'
    elif '../../images/' in img_src:
        filename = img_src.replace('../../images/', '')
        prefix = '../../images/'
    elif '/images/' in img_src:
        filename = img_src.replace('/images/', '')
        prefix = '/images/'
    else:
        return html_content
    
    # Skip if it's a PNG logo (they don't exist)
    if '-logo.png' in filename:
        return html_content
        
    # Check if this is a JPG that has a WebP version
    if filename.endswith('.jpg'):
        webp_filename = filename.replace('.jpg', '.webp')
        webp_path = f'images/{webp_filename}'
        
        # Only update if WebP exists
        if os.path.exists(webp_path):
            # Find the img tag with this src
            img_pattern = f'<img src="{re.escape(img_src)}"([^>]*)>'
            
            def replace_with_picture(match):
                attributes = match.group(1)
                # Extract alt, class, loading attributes
                alt_match = re.search(r'alt="([^"]*)"', attributes)
                class_match = re.search(r'class="([^"]*)"', attributes)
                loading_match = re.search(r'loading="([^"]*)"', attributes)
                
                alt = alt_match.group(1) if alt_match else ''
                class_attr = f' class="{class_match.group(1)}"' if class_match else ''
                loading = f' loading="{loading_match.group(1)}"' if loading_match else ''
                
                picture_element = f'''<picture>
                    <source srcset="{prefix}{webp_filename}" type="image/webp">
                    <img src="{img_src}" alt="{alt}"{class_attr}{loading}>
                </picture>'''
                
                return picture_element
            
            html_content = re.sub(img_pattern, replace_with_picture, html_content)
            
    return html_content

# Update blog pages
blog_files = [
    'blog/index.html',
    'blog/2025-illinois-hoa-law-changes.html',
    'blog/top-5-financial-mistakes-hoa-boards-avoid.html'
]

updated_count = 0

for file_path in blog_files:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Find all image sources
        img_srcs = re.findall(r'<img src="([^"]*\.jpg)"', content)
        
        for img_src in img_srcs:
            content = update_image_to_picture(content, img_src)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            updated_count += 1
            print(f"[OK] Updated {file_path}")
        else:
            print(f"[SKIP] No changes needed for {file_path}")

print(f"\nUpdated {updated_count} files to use WebP with fallback!")