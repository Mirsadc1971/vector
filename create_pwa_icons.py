from PIL import Image, ImageDraw, ImageFont
import os

# Create images directory if it doesn't exist
os.makedirs('images', exist_ok=True)

# Create a simple icon with M369 text
def create_icon(size, is_maskable=False):
    # Create image with blue background
    img = Image.new('RGB', (size, size), '#1e40af')
    draw = ImageDraw.Draw(img)
    
    # Add white text
    text = "M369"
    # Use a basic font - adjust size based on icon size
    font_size = size // 4
    
    # Try to use a better font if available
    try:
        from PIL import ImageFont
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    # Calculate text position
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    position = ((size - text_width) // 2, (size - text_height) // 2)
    
    # Draw text
    draw.text(position, text, fill='white', font=font)
    
    # Add padding for maskable icon (safe area is 80% of icon)
    if is_maskable:
        # Create a new image with more padding
        maskable_img = Image.new('RGB', (size, size), '#1e40af')
        maskable_draw = ImageDraw.Draw(maskable_img)
        
        # Scale down text for safe area
        safe_size = int(size * 0.6)
        safe_font_size = safe_size // 4
        
        try:
            safe_font = ImageFont.truetype("arial.ttf", safe_font_size)
        except:
            safe_font = ImageFont.load_default()
        
        bbox = maskable_draw.textbbox((0, 0), text, font=safe_font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        position = ((size - text_width) // 2, (size - text_height) // 2)
        maskable_draw.text(position, text, fill='white', font=safe_font)
        
        return maskable_img
    
    return img

# Create required icons
print("Creating PWA icons...")

# 192x192 icon
icon_192 = create_icon(192)
icon_192.save('images/icon-192x192.png')
print("[OK] Created icon-192x192.png")

# 512x512 icon
icon_512 = create_icon(512)
icon_512.save('images/icon-512x512.png')
print("[OK] Created icon-512x512.png")

# 512x512 maskable icon
icon_512_maskable = create_icon(512, is_maskable=True)
icon_512_maskable.save('images/icon-512x512-maskable.png')
print("[OK] Created icon-512x512-maskable.png")

print("\nAll PWA icons created successfully!")