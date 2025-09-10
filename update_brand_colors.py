#!/usr/bin/env python3
"""
Update entire site color scheme to match brand guidelines
Primary Gold: #F4A261
Background Navy: #2C3E50
Accent Yellow: #F1C40F
"""

import os
import re
from pathlib import Path

# Brand color palette
PRIMARY_GOLD = "#F4A261"
BACKGROUND_NAVY = "#2C3E50"
ACCENT_YELLOW = "#F1C40F"
WHITE = "#ffffff"
LIGHT_GRAY = "#e5e7eb"

def update_colors(content):
    """Update all color references to match brand palette"""
    
    # Track if changes were made
    original_content = content
    
    # 1. UPDATE HEADER/NAVIGATION COLORS
    # Change header background to navy
    content = re.sub(
        r'background:\s*#1e3a8a',  # Old blue
        f'background: {BACKGROUND_NAVY}',
        content,
        flags=re.IGNORECASE
    )
    
    # Update navigation background colors
    content = re.sub(
        r'background:\s*#f3f4f6',  # Old light gray
        f'background: {BACKGROUND_NAVY}',
        content,
        flags=re.IGNORECASE
    )
    
    # Update nav link colors to gold
    content = re.sub(
        r'color:\s*#111827(?![0-9a-fA-F])',  # Dark gray text
        f'color: {PRIMARY_GOLD}',
        content
    )
    
    # 2. UPDATE BUTTON COLORS
    # Primary buttons - Gold background
    content = re.sub(
        r'background:\s*#0a58ca',  # Old blue buttons
        f'background: {PRIMARY_GOLD}',
        content,
        flags=re.IGNORECASE
    )
    
    # Button hover states
    content = re.sub(
        r'background:\s*#0b5ed7',  # Old blue hover
        f'background: {ACCENT_YELLOW}',
        content,
        flags=re.IGNORECASE
    )
    
    # 3. UPDATE LINK COLORS
    # Blue links to gold
    content = re.sub(
        r'color:\s*#2563eb(?![0-9a-fA-F])',  # Blue links
        f'color: {PRIMARY_GOLD}',
        content
    )
    
    content = re.sub(
        r'color:\s*#1d4ed8(?![0-9a-fA-F])',  # Darker blue links
        f'color: {ACCENT_YELLOW}',
        content
    )
    
    # 4. UPDATE SECTION BACKGROUNDS
    # Light backgrounds to use accent yellow (subtle)
    content = re.sub(
        r'background:\s*#f7f9fc',  # Very light blue-gray
        f'background: #FEF9E7',  # Very light yellow tint
        content,
        flags=re.IGNORECASE
    )
    
    # 5. UPDATE HERO SECTION CTA BUTTONS
    # Update hero primary button (white button with blue text -> gold button with navy text)
    content = re.sub(
        r'color:\s*#1e3a8a(["\';])',  # Blue text in buttons
        f'color: {BACKGROUND_NAVY}\\1',
        content
    )
    
    # 6. UPDATE MOBILE MENU COLORS
    # Mobile menu background
    content = re.sub(
        r'\.mobile-nav\s*\{[^}]*background:\s*#[a-fA-F0-9]+',
        f'.mobile-nav {{ background: {BACKGROUND_NAVY}',
        content
    )
    
    # 7. UPDATE HEADER CTA BUTTON
    # Phone button in header
    pattern = r'(href="tel:8476522338"[^>]*style="[^"]*background:\s*)#0a58ca'
    content = re.sub(pattern, f'\\1{PRIMARY_GOLD}', content, flags=re.IGNORECASE)
    
    # 8. UPDATE DROPDOWN MENU COLORS
    # Dropdown headers
    content = re.sub(
        r'(\.dropdown-header[^{]*\{[^}]*color:\s*)#[a-fA-F0-9]+',
        f'\\1{PRIMARY_GOLD}',
        content
    )
    
    # 9. UPDATE SERVICE CARD COLORS
    # Service card hover effects
    content = re.sub(
        r'border-color:\s*#3b82f6',  # Blue border
        f'border-color: {PRIMARY_GOLD}',
        content
    )
    
    # 10. UPDATE SPECIAL OFFERS SECTION
    # Limited time badges
    content = re.sub(
        r'background:\s*#1e3a8a(["\';])',  # Dark blue badge
        f'background: {BACKGROUND_NAVY}\\1',
        content
    )
    
    # Green success badges to gold
    content = re.sub(
        r'background:\s*#16a34a(["\';])',  # Green
        f'background: {PRIMARY_GOLD}\\1',
        content
    )
    
    return content, content != original_content

def update_css_in_style_tags(content):
    """Update CSS within <style> tags"""
    
    def replace_in_style(match):
        style_content = match.group(1)
        
        # Update nav colors
        style_content = re.sub(r'#1e3a8a', BACKGROUND_NAVY, style_content)
        style_content = re.sub(r'#f3f4f6', BACKGROUND_NAVY, style_content)
        style_content = re.sub(r'#111827', PRIMARY_GOLD, style_content)
        style_content = re.sub(r'#0a58ca', PRIMARY_GOLD, style_content)
        style_content = re.sub(r'#2563eb', PRIMARY_GOLD, style_content)
        style_content = re.sub(r'#3b82f6', PRIMARY_GOLD, style_content)
        
        # Update hover states
        style_content = re.sub(r'#0b5ed7', ACCENT_YELLOW, style_content)
        style_content = re.sub(r'#1d4ed8', ACCENT_YELLOW, style_content)
        
        return f'<style>{style_content}</style>'
    
    content = re.sub(r'<style[^>]*>(.*?)</style>', replace_in_style, content, flags=re.DOTALL)
    return content

def process_html_file(file_path):
    """Process a single HTML file"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update inline styles
    content, changed1 = update_colors(content)
    
    # Update CSS in style tags
    original = content
    content = update_css_in_style_tags(content)
    changed2 = content != original
    
    return content, (changed1 or changed2)

def main():
    """Process all HTML files"""
    
    root_dir = Path('C:/Users/mirsa/manage369-live')
    updated_files = []
    
    # Find all HTML files
    html_files = list(root_dir.rglob('*.html'))
    # Filter out build directories
    html_files = [f for f in html_files if not any(
        skip in str(f) for skip in ['.git', 'node_modules', 'dist', 'build']
    )]
    
    print(f"Processing {len(html_files)} HTML files...")
    print(f"Updating to brand colors:")
    print(f"  Primary Gold: {PRIMARY_GOLD}")
    print(f"  Background Navy: {BACKGROUND_NAVY}")
    print(f"  Accent Yellow: {ACCENT_YELLOW}")
    print("-" * 60)
    
    for file_path in html_files:
        try:
            content, was_updated = process_html_file(file_path)
            
            if was_updated:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                updated_files.append(file_path.relative_to(root_dir))
                print(f"[UPDATED] {file_path.relative_to(root_dir)}")
                
        except Exception as e:
            print(f"[ERROR] {file_path}: {e}")
    
    print("\n" + "=" * 60)
    print(f"Updated {len(updated_files)} files with new brand colors")
    
    if updated_files:
        print("\nFirst 10 updated files:")
        for f in updated_files[:10]:
            print(f"  - {f}")
        if len(updated_files) > 10:
            print(f"  ... and {len(updated_files) - 10} more")

if __name__ == "__main__":
    main()