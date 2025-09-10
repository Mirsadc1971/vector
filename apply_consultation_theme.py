#!/usr/bin/env python3
"""
Apply the consultation section's dark theme with blue-to-gold gradient across entire site
"""

import os
import re
from pathlib import Path

# Color palette from consultation section
DARK_BLUE = "#084298"
PRIMARY_GOLD = "#F4A261"
BACKGROUND_NAVY = "#2C3E50"
DARK_GRAY = "#1f2937"
LIGHT_GRAY = "#e5e7eb"
WHITE = "#ffffff"
GRADIENT = "linear-gradient(135deg, #084298 0%, #F4A261 100%)"

def apply_dark_theme_to_sections(content):
    """Apply dark theme to all major sections"""
    
    # Special Offers Section - Dark background with gradient accent
    content = re.sub(
        r'(<section[^>]*style="background:\s*)#f7f9fc',
        f'\\1{DARK_GRAY}',
        content,
        flags=re.IGNORECASE
    )
    
    # Update section backgrounds to dark
    content = re.sub(
        r'(background:\s*)#FEF9E7',  # Light yellow
        f'\\1{BACKGROUND_NAVY}',
        content,
        flags=re.IGNORECASE
    )
    
    # Service sections - dark theme
    content = re.sub(
        r'(section[^>]*style="[^"]*background:\s*)white',
        f'\\1{DARK_GRAY}',
        content,
        flags=re.IGNORECASE
    )
    
    # Cards and boxes - dark with gradient borders
    content = re.sub(
        r'(background:\s*)white([^;]*box-shadow)',
        f'\\1{BACKGROUND_NAVY}\\2',
        content,
        flags=re.IGNORECASE
    )
    
    # Update text colors for dark backgrounds
    content = re.sub(
        r'(color:\s*)#1e293b',  # Dark text
        f'\\1{LIGHT_GRAY}',
        content
    )
    
    content = re.sub(
        r'(color:\s*)#111827',  # Very dark text
        f'\\1{LIGHT_GRAY}',
        content
    )
    
    content = re.sub(
        r'(color:\s*)#64748b',  # Medium gray text
        f'\\1#cbd5e1',  # Lighter gray for dark bg
        content
    )
    
    # Add gradient to key sections
    # Hero overlays
    content = re.sub(
        r'(linear-gradient\(rgba\(0,\s*0,\s*0,\s*0\.5\),\s*rgba\(0,\s*0,\s*0,\s*0\.6\)\))',
        f'linear-gradient(135deg, rgba(8,66,152,0.8) 0%, rgba(244,162,97,0.8) 100%)',
        content
    )
    
    return content

def apply_form_styling(content):
    """Apply consultation form styling to all forms"""
    
    # Form backgrounds - dark inputs
    content = re.sub(
        r'(input\[type[^}]*\{[^}]*background:\s*)#[a-fA-F0-9]+',
        f'\\1{BACKGROUND_NAVY}',
        content
    )
    
    content = re.sub(
        r'(input\[type[^}]*\{[^}]*color:\s*)#[a-fA-F0-9]+',
        f'\\1{LIGHT_GRAY}',
        content
    )
    
    # Select dropdowns
    content = re.sub(
        r'(select\s*\{[^}]*background:\s*)#[a-fA-F0-9]+',
        f'\\1{BACKGROUND_NAVY}',
        content
    )
    
    content = re.sub(
        r'(textarea\s*\{[^}]*background:\s*)#[a-fA-F0-9]+',
        f'\\1{BACKGROUND_NAVY}',
        content
    )
    
    return content

def apply_button_gradient(content):
    """Apply gradient styling to buttons"""
    
    # Primary buttons get gradient
    content = re.sub(
        r'(\.btn-primary\s*\{[^}]*background:\s*)#[a-fA-F0-9]+',
        f'\\1linear-gradient(135deg, {DARK_BLUE} 0%, {PRIMARY_GOLD} 100%)',
        content
    )
    
    # CTA buttons
    content = re.sub(
        r'(\.cta-button[^}]*\{[^}]*background:\s*)#[a-fA-F0-9]+',
        f'\\1linear-gradient(135deg, {DARK_BLUE} 0%, {PRIMARY_GOLD} 100%)',
        content
    )
    
    return content

def update_inline_styles(content):
    """Update inline styles to match dark theme"""
    
    # Update white backgrounds to dark
    content = re.sub(
        r'(style="[^"]*background:\s*)#ffffff',
        f'\\1{DARK_GRAY}',
        content,
        flags=re.IGNORECASE
    )
    
    content = re.sub(
        r'(style="[^"]*background:\s*)white',
        f'\\1{DARK_GRAY}',
        content,
        flags=re.IGNORECASE
    )
    
    # Update text colors for dark backgrounds
    content = re.sub(
        r'(style="[^"]*color:\s*)#000000',
        f'\\1{LIGHT_GRAY}',
        content,
        flags=re.IGNORECASE
    )
    
    content = re.sub(
        r'(style="[^"]*color:\s*)black',
        f'\\1{LIGHT_GRAY}',
        content,
        flags=re.IGNORECASE
    )
    
    # Special offer cards - dark theme
    content = re.sub(
        r'(style="background:\s*)white([^"]*border-radius[^"]*">)',
        f'\\1{BACKGROUND_NAVY}\\2',
        content,
        flags=re.IGNORECASE
    )
    
    # Update offer section backgrounds
    if "Special Offers Section" in content:
        # The main offers container
        content = re.sub(
            r'(<section[^>]*Special Offers[^>]*style="background:\s*)#[a-fA-F0-9]+',
            f'\\1{DARK_GRAY}',
            content
        )
        
        # Individual offer cards
        content = re.sub(
            r'(div[^>]*style="[^"]*background:\s*)white([^"]*shadow[^"]*Limited Time)',
            f'\\1{BACKGROUND_NAVY}\\2',
            content,
            flags=re.IGNORECASE
        )
    
    # Service type cards
    content = re.sub(
        r'(<div[^>]*class="service-type[^>]*style="[^"]*background:\s*)#[a-fA-F0-9]+',
        f'\\1{BACKGROUND_NAVY}',
        content
    )
    
    return content

def add_gradient_accents(content):
    """Add gradient accents to key elements"""
    
    # Add gradient to section headers
    if '<style>' in content:
        # Insert gradient styles
        gradient_styles = """
    /* Gradient Accents from Consultation Theme */
    .section-header::after {
        content: '';
        display: block;
        width: 100px;
        height: 4px;
        background: linear-gradient(135deg, #084298 0%, #F4A261 100%);
        margin: 1rem auto;
    }
    
    .primary-gradient {
        background: linear-gradient(135deg, #084298 0%, #F4A261 100%);
    }
    
    .card:hover {
        border: 2px solid #F4A261;
        transform: translateY(-5px);
    }
    
    /* Dark theme for all sections */
    body {
        background: #1a252f;
        color: #e5e7eb;
    }
    
    section {
        background: #1f2937;
        color: #e5e7eb;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #F4A261;
    }
    
    /* Form inputs dark theme */
    input, select, textarea {
        background: #2C3E50;
        color: #e5e7eb;
        border: 1px solid #374151;
    }
    
    input:focus, select:focus, textarea:focus {
        border-color: #F4A261;
        outline: none;
        box-shadow: 0 0 0 3px rgba(244,162,97,0.1);
    }
"""
        content = re.sub(
            r'(</style>)',
            f'{gradient_styles}\\1',
            content
        )
    
    return content

def process_file(file_path):
    """Process a single HTML file"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Apply all theme updates
    content = apply_dark_theme_to_sections(content)
    content = apply_form_styling(content)
    content = apply_button_gradient(content)
    content = update_inline_styles(content)
    content = add_gradient_accents(content)
    
    return content, content != original

def main():
    """Process all HTML files"""
    
    root_dir = Path('C:/Users/mirsa/manage369-live')
    updated_files = []
    
    html_files = list(root_dir.rglob('*.html'))
    html_files = [f for f in html_files if not any(
        skip in str(f) for skip in ['.git', 'node_modules', 'dist', 'build']
    )]
    
    print(f"Applying consultation section dark theme to {len(html_files)} files...")
    print(f"Theme: Dark backgrounds with blue-to-gold gradient")
    print("-" * 60)
    
    for file_path in html_files:
        try:
            content, was_updated = process_file(file_path)
            
            if was_updated:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                updated_files.append(file_path.relative_to(root_dir))
                print(f"[THEMED] {file_path.relative_to(root_dir)}")
                
        except Exception as e:
            print(f"[ERROR] {file_path}: {e}")
    
    print("\n" + "=" * 60)
    print(f"Applied dark consultation theme to {len(updated_files)} files")
    print("\nTheme applied:")
    print("- Dark gray/navy backgrounds throughout")
    print("- Blue-to-gold gradient accents")
    print("- Light text on dark backgrounds")
    print("- Form inputs with dark theme")
    print("- Gold headings and highlights")

if __name__ == "__main__":
    main()