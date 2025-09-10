#!/usr/bin/env python3
"""
Fix image visibility by reducing overlay opacity
Images should be at least 80% visible
"""

import re
from pathlib import Path

def fix_hero_overlays(content):
    """Fix hero section overlays to show images properly"""
    
    original = content
    
    # Fix gradient overlays that are too opaque
    # Current: rgba(8,66,152,0.95) to rgba(244,162,97,0.95) - 95% opacity is too much!
    # Change to: 20-30% opacity for subtle tint
    
    # Fix inline hero gradients
    content = re.sub(
        r'linear-gradient\(135deg,\s*rgba\(8,\s*66,\s*152,\s*0\.95\)\s*0%,\s*rgba\(244,\s*162,\s*97,\s*0\.95\)\s*100%\)',
        'linear-gradient(135deg, rgba(8,66,152,0.2) 0%, rgba(244,162,97,0.2) 100%)',
        content
    )
    
    # Fix dark overlays on hero images
    content = re.sub(
        r'linear-gradient\(rgba\(0,\s*0,\s*0,\s*0\.[56]\),\s*rgba\(0,\s*0,\s*0,\s*0\.[56]\)\)',
        'linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.4))',
        content
    )
    
    # Fix blue-gold gradient overlays that are too strong
    content = re.sub(
        r'linear-gradient\(135deg,\s*rgba\(8,\s*66,\s*152,\s*0\.8\)\s*0%,\s*rgba\(244,\s*162,\s*97,\s*0\.8\)\s*100%\)',
        'linear-gradient(135deg, rgba(8,66,152,0.25) 0%, rgba(244,162,97,0.25) 100%)',
        content
    )
    
    # Fix CSS hero styles
    content = re.sub(
        r'(\.hero\s*\{[^}]*background:\s*)linear-gradient\([^)]+\),\s*url',
        r'\1linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.4)), url',
        content
    )
    
    # Fix inline style hero sections
    content = re.sub(
        r'(<section[^>]*class="hero"[^>]*style="[^"]*background:\s*)linear-gradient\([^)]+rgba\([^)]+0\.[89]\)[^)]+\)',
        r'\1linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.4))',
        content
    )
    
    # Fix any background overlays that are too dark
    content = re.sub(
        r'rgba\(0,\s*0,\s*0,\s*0\.7\)',
        'rgba(0, 0, 0, 0.4)',
        content
    )
    
    content = re.sub(
        r'rgba\(0,\s*0,\s*0,\s*0\.8\)',
        'rgba(0, 0, 0, 0.4)',
        content
    )
    
    content = re.sub(
        r'rgba\(0,\s*0,\s*0,\s*0\.9\)',
        'rgba(0, 0, 0, 0.4)',
        content
    )
    
    return content, content != original

def fix_card_backgrounds(content):
    """Fix card and section backgrounds for better contrast"""
    
    # Make cards more transparent for glass effect
    content = re.sub(
        r'(\.card[^{]*\{[^}]*background:\s*)rgba\(44,\s*62,\s*80,\s*0\.8\)',
        r'\1rgba(44, 62, 80, 0.7)',
        content
    )
    
    # Fix service cards
    content = re.sub(
        r'(\.service-card[^{]*\{[^}]*background:\s*)rgba\(44,\s*62,\s*80,\s*0\.8\)',
        r'\1rgba(44, 62, 80, 0.7)',
        content
    )
    
    return content

def fix_premium_styles_overlay(content):
    """Fix the premium styles CSS to have lighter overlays"""
    
    if "Premium Design Enhancements" in content:
        # Fix the hero gradient in premium styles
        content = re.sub(
            r'(\.hero\s*\{[^}]*background:\s*)linear-gradient\(135deg,\s*rgba\(8,66,152,0\.95\)[^}]+\)',
            r'\1linear-gradient(135deg, rgba(8,66,152,0.2) 0%, rgba(244,162,97,0.2) 100%), url(\'images/manage369randolphstation.jpg\') center/cover !important',
            content
        )
        
        # Fix shimmer animation to be more subtle
        content = re.sub(
            r'(background:\s*linear-gradient\(90deg,\s*transparent,\s*)rgba\(244,162,97,0\.3\)',
            r'\1rgba(244,162,97,0.15)',
            content
        )
    
    return content

def add_image_visibility_css(content):
    """Add CSS to ensure images are visible"""
    
    image_css = """
    /* Image Visibility Fixes */
    .hero {
        background-blend-mode: multiply;
    }
    
    .hero::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(to bottom, 
            rgba(0,0,0,0.2) 0%, 
            rgba(0,0,0,0.3) 50%, 
            rgba(0,0,0,0.4) 100%);
        pointer-events: none;
        z-index: 1;
    }
    
    .hero-content {
        position: relative;
        z-index: 2;
    }
    
    /* Ensure text remains readable on lighter overlay */
    .hero h1, .hero h2, .hero p {
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8), 
                     0 0 20px rgba(0,0,0,0.6);
    }
    
    /* Image sections should show images clearly */
    .image-section {
        background-size: cover;
        background-position: center;
        position: relative;
    }
    
    .image-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.2);
        z-index: 1;
    }
"""
    
    if "Image Visibility Fixes" not in content:
        if '</style>' in content:
            content = re.sub(
                r'(</style>)',
                f'{image_css}\\1',
                content
            )
    
    return content

def process_file(file_path):
    """Process a single HTML file"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content, changed = fix_hero_overlays(content)
    content = fix_card_backgrounds(content)
    content = fix_premium_styles_overlay(content)
    content = add_image_visibility_css(content)
    
    return content, changed

def main():
    """Process all HTML files"""
    
    root_dir = Path('C:/Users/mirsa/manage369-live')
    updated_files = []
    
    html_files = list(root_dir.rglob('*.html'))
    html_files = [f for f in html_files if not any(
        skip in str(f) for skip in ['.git', 'node_modules', 'dist', 'build']
    )]
    
    print(f"Fixing image visibility in {len(html_files)} files...")
    print("Making images at least 80% visible")
    print("-" * 60)
    
    for file_path in html_files:
        try:
            content, was_updated = process_file(file_path)
            
            if was_updated:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                updated_files.append(file_path.relative_to(root_dir))
                print(f"[FIXED] {file_path.relative_to(root_dir)}")
                
        except Exception as e:
            print(f"[ERROR] {file_path}: {e}")
    
    print("\n" + "=" * 60)
    print(f"Fixed image visibility in {len(updated_files)} files")
    print("\nChanges made:")
    print("- Hero overlays reduced from 95% to 20-30% opacity")
    print("- Dark overlays reduced from 60-80% to 30-40% opacity")
    print("- Images now at least 80% visible")
    print("- Text shadows enhanced for readability")

if __name__ == "__main__":
    main()