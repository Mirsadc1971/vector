#!/usr/bin/env python3
"""
Complete brand color overhaul - Apply dark navy theme throughout
"""

import os
import re
from pathlib import Path

# Brand colors from instructions
PRIMARY_GOLD = "#F4A261"
BACKGROUND_NAVY = "#2C3E50"
ACCENT_YELLOW = "#F1C40F"
DARK_NAVY = "#1a252f"  # Darker variant for depth
WHITE = "#ffffff"

def fix_header_section(content):
    """Fix header to have navy background with gold accents"""
    
    # Fix header background - white to navy
    content = re.sub(
        r'(\.header\s*\{[^}]*background:\s*)white',
        f'\\1{BACKGROUND_NAVY}',
        content
    )
    content = re.sub(
        r'(\.header\s*\{[^}]*background:\s*)#ffffff',
        f'\\1{BACKGROUND_NAVY}',
        content,
        flags=re.IGNORECASE
    )
    
    # Fix logo color - should be gold
    content = re.sub(
        r'(\.logo\s*\{[^}]*color:\s*)#[a-fA-F0-9]+',
        f'\\1{PRIMARY_GOLD}',
        content
    )
    
    # Fix nav links - should be gold on navy
    content = re.sub(
        r'(\.nav-link\s*\{[^}]*color:\s*)#333',
        f'\\1{PRIMARY_GOLD}',
        content
    )
    content = re.sub(
        r'(\.nav-link\s*\{[^}]*color:\s*)#[a-fA-F0-9]+',
        f'\\1{PRIMARY_GOLD}',
        content
    )
    
    # Fix phone button to match
    content = re.sub(
        r'(\.phone-button\s*\{[^}]*background:\s*)#[a-fA-F0-9]+',
        f'\\1{PRIMARY_GOLD}',
        content
    )
    content = re.sub(
        r'(\.phone-button\s*\{[^}]*color:\s*)#[a-fA-F0-9]+',
        f'\\1{BACKGROUND_NAVY}',
        content
    )
    
    # Fix dropdown background
    content = re.sub(
        r'(\.dropdown-content\s*\{[^}]*background:\s*)white',
        f'\\1{BACKGROUND_NAVY}',
        content
    )
    content = re.sub(
        r'(\.dropdown-content\s*\{[^}]*background:\s*)#ffffff',
        f'\\1{BACKGROUND_NAVY}',
        content,
        flags=re.IGNORECASE
    )
    
    # Fix dropdown links
    content = re.sub(
        r'(\.dropdown-content\s+a\s*\{[^}]*color:\s*)#[a-fA-F0-9]+',
        f'\\1{PRIMARY_GOLD}',
        content
    )
    
    # Fix mobile menu
    content = re.sub(
        r'(\.mobile-menu\s*\{[^}]*background:\s*)#[a-fA-F0-9]+',
        f'\\1{BACKGROUND_NAVY}',
        content
    )
    
    return content

def fix_hero_buttons(content):
    """Fix hero section Request Consultation button"""
    
    # Fix Request a Consultation button in hero - should be gold
    pattern = r'(Request a Consultation</a>)'
    if "Request a Consultation" in content:
        # Find the button and update its inline style
        content = re.sub(
            r'(href="sms:8476522338"[^>]*style="[^"]*background:\s*)#ffffff([^"]*color:\s*)#[a-fA-F0-9]+',
            f'\\1{PRIMARY_GOLD}\\2{BACKGROUND_NAVY}',
            content
        )
    
    return content

def apply_dark_theme_sections(content):
    """Apply dark navy to more sections"""
    
    # Special offers section - darker background
    content = re.sub(
        r'(section style="background:\s*)#f7f9fc',
        f'\\1{DARK_NAVY}',
        content,
        flags=re.IGNORECASE
    )
    
    # Service cards section
    content = re.sub(
        r'(background:\s*)#f8fafc',
        f'\\1{BACKGROUND_NAVY}',
        content,
        flags=re.IGNORECASE
    )
    
    # Update text colors on dark backgrounds
    content = re.sub(
        r'(color:\s*)#1e293b',  # Dark text on light bg
        f'\\1{WHITE}',
        content
    )
    
    content = re.sub(
        r'(color:\s*)#64748b',  # Gray text
        f'\\1#cbd5e1',  # Light gray for dark bg
        content
    )
    
    return content

def fix_inline_styles(content):
    """Fix inline style attributes"""
    
    # Fix header inline styles
    content = re.sub(
        r'(<header[^>]*class="header"[^>]*>)',
        r'<header class="header" style="background: #2C3E50;">',
        content
    )
    
    # Fix logo inline color
    content = re.sub(
        r'(<div class="logo"[^>]*>)',
        r'<div class="logo" style="color: #F4A261;">',
        content
    )
    
    # Fix phone button inline styles - both desktop and mobile
    content = re.sub(
        r'(href="(?:sms|tel):8476522338"[^>]*style="[^"]*)(background:\s*#[a-fA-F0-9]+)',
        f'\\1background: {PRIMARY_GOLD}; color: {BACKGROUND_NAVY}',
        content
    )
    
    # Fix nav link colors if inline
    content = re.sub(
        r'(class="nav-link"[^>]*style="[^"]*)(color:\s*#[a-fA-F0-9]+)',
        f'\\1color: {PRIMARY_GOLD}',
        content
    )
    
    return content

def process_file(file_path):
    """Process a single HTML file"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Apply all fixes
    content = fix_header_section(content)
    content = fix_hero_buttons(content)
    content = apply_dark_theme_sections(content)
    content = fix_inline_styles(content)
    
    # Additional specific fixes
    # Make sure header has navy background
    if '<header' in content and 'class="header"' in content:
        # Add inline style to force navy background
        if 'style="background:' not in content:
            content = re.sub(
                r'(<header[^>]*class="header"[^>]*)(>)',
                f'\\1 style="background: {BACKGROUND_NAVY};"\\2',
                content
            )
    
    return content, content != original

def main():
    """Process all files"""
    
    root_dir = Path('C:/Users/mirsa/manage369-live')
    updated_files = []
    
    html_files = list(root_dir.rglob('*.html'))
    html_files = [f for f in html_files if not any(
        skip in str(f) for skip in ['.git', 'node_modules', 'dist', 'build']
    )]
    
    print(f"Applying complete brand color overhaul to {len(html_files)} files...")
    print(f"Colors: Navy={BACKGROUND_NAVY}, Gold={PRIMARY_GOLD}, Yellow={ACCENT_YELLOW}")
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
    print(f"Fixed {len(updated_files)} files")
    print("Header: Navy background with gold text")
    print("Phone/Logo: Matching gold color")
    print("Sections: More dark navy throughout")

if __name__ == "__main__":
    main()