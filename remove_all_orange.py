#!/usr/bin/env python3
"""
Remove all orange colors and replace with dark theme gold design
"""

import re
from pathlib import Path

# Orange colors to replace
ORANGE_BG = "#9a3412"
ORANGE_TEXT = "#c4490c"
ORANGE_VARIANTS = ["#ea580c", "#d97706", "#dc2626"]

# Brand colors
DARK_NAVY = "#2C3E50"
PRIMARY_GOLD = "#F4A261"
DARK_GRAY = "#1f2937"
LIGHT_GRAY = "#e5e7eb"

def remove_orange_colors(content):
    """Replace all orange with brand colors"""
    
    original = content
    
    # Replace orange backgrounds with dark navy
    content = re.sub(
        r'background:\s*#9a3412',
        f'background: {DARK_NAVY}',
        content,
        flags=re.IGNORECASE
    )
    
    # Replace orange text with gold
    content = re.sub(
        r'color:\s*#c4490c',
        f'color: {PRIMARY_GOLD}',
        content,
        flags=re.IGNORECASE
    )
    
    # Replace other orange variants
    for orange in ORANGE_VARIANTS:
        content = re.sub(
            f'background:\\s*{orange}',
            f'background: {DARK_NAVY}',
            content,
            flags=re.IGNORECASE
        )
        content = re.sub(
            f'color:\\s*{orange}',
            f'color: {PRIMARY_GOLD}',
            content,
            flags=re.IGNORECASE
        )
    
    # Fix the specific Manage369 Difference section
    if "Discover the Manage369 Difference" in content:
        # Replace the entire section styling
        content = re.sub(
            r'<div style="background:\s*#9a3412[^"]*">(\s*<h3[^>]*>Discover the Manage369 Difference</h3>)',
            f'<div style="background: linear-gradient(135deg, #084298 0%, #2C3E50 100%); padding: 2rem; border-radius: 15px; margin-top: 3rem; border: 1px solid rgba(244,162,97,0.3); box-shadow: 0 10px 30px rgba(0,0,0,0.3);">\\1',
            content
        )
        
        # Fix the contact button in this section
        content = re.sub(
            r'(<a href="tel:8476522338"[^>]*style="[^"]*)(background:\s*#1f2937[^"]*color:\s*#c4490c)',
            f'\\1background: {PRIMARY_GOLD}; color: {DARK_NAVY}; border: 2px solid {PRIMARY_GOLD}',
            content
        )
    
    # Fix star ratings (often orange)
    content = re.sub(
        r'(<div[^>]*style="[^"]*color:\s*)#c4490c([^"]*★)',
        f'\\1{PRIMARY_GOLD}\\2',
        content
    )
    
    # Fix any remaining orange hex codes
    orange_codes = ['#9a3412', '#c4490c', '#ea580c', '#d97706', '#dc2626', '#f97316']
    for code in orange_codes:
        content = re.sub(
            code,
            PRIMARY_GOLD,
            content,
            flags=re.IGNORECASE
        )
    
    return content, content != original

def fix_statistics_section(content):
    """Fix the statistics boxes to match dark theme"""
    
    # Fix stat number colors
    content = re.sub(
        r'(<div style="font-size:\s*3rem;\s*color:\s*)#c4490c',
        f'\\1{PRIMARY_GOLD}',
        content
    )
    
    # Fix testimonial sections background
    content = re.sub(
        r'(section[^>]*style="[^"]*background:\s*)#f5f7fa',
        f'\\1{DARK_GRAY}',
        content
    )
    
    # Fix testimonial cards
    content = re.sub(
        r'(<div style="background:\s*)#1f2937([^"]*color:\s*)#333',
        f'\\1{DARK_NAVY}\\2{LIGHT_GRAY}',
        content
    )
    
    # Fix testimonial text colors
    content = re.sub(
        r'color:\s*#666',
        f'color: {LIGHT_GRAY}',
        content
    )
    
    content = re.sub(
        r'color:\s*#333',
        f'color: {LIGHT_GRAY}',
        content
    )
    
    # Fix blue links to gold
    content = re.sub(
        r'color:\s*#0a58ca',
        f'color: {PRIMARY_GOLD}',
        content
    )
    
    return content

def add_gradient_to_cta(content):
    """Add premium gradient to CTA sections"""
    
    if "Discover the Manage369 Difference" in content:
        # Add enhanced styling
        enhanced_style = """
    /* Enhanced CTA Section */
    .cta-section {
        background: linear-gradient(135deg, #084298 0%, #2C3E50 100%);
        position: relative;
        overflow: hidden;
    }
    
    .cta-section::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(244,162,97,0.1), transparent);
        animation: shimmer 3s infinite;
    }
"""
        
        if '</style>' in content and enhanced_style not in content:
            content = re.sub(
                r'(</style>)',
                f'{enhanced_style}\\1',
                content
            )
    
    return content

def process_file(file_path):
    """Process a single HTML file"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content, changed = remove_orange_colors(content)
    content = fix_statistics_section(content)
    content = add_gradient_to_cta(content)
    
    return content, changed

def main():
    """Process all HTML files"""
    
    root_dir = Path('C:/Users/mirsa/manage369-live')
    updated_files = []
    
    html_files = list(root_dir.rglob('*.html'))
    html_files = [f for f in html_files if not any(
        skip in str(f) for skip in ['.git', 'node_modules', 'dist', 'build']
    )]
    
    print(f"Removing all orange colors from {len(html_files)} files...")
    print("Replacing with dark navy and gold theme")
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
    print(f"Removed orange from {len(updated_files)} files")
    print("\nColor replacements:")
    print("- Orange backgrounds -> Dark navy (#2C3E50)")
    print("- Orange text -> Gold (#F4A261)")
    print("- CTA section -> Blue-to-navy gradient")
    print("- All orange variants removed")

if __name__ == "__main__":
    main()