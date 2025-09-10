#!/usr/bin/env python3
"""
Fix phone number styling to match premium dark theme
"""

import re
from pathlib import Path

def fix_phone_styling(content):
    """Fix all phone number styling to match dark theme"""
    
    original = content
    
    # Fix header phone button - dark background with gold text (inverse)
    content = re.sub(
        r'(<a href="(?:sms|tel):8476522338"[^>]*class="phone-button"[^>]*style="[^"]*)(background:\s*#F4A261[^"]*color:\s*#2C3E50)',
        r'\1background: #2C3E50; color: #F4A261; border: 1px solid #F4A261',
        content
    )
    
    # Fix mobile menu phone button
    content = re.sub(
        r'(<a href="(?:tel|sms):8476522338"[^>]*style="[^"]*)(background:\s*#F4A261[^"]*color:\s*#2C3E50)',
        r'\1background: #2C3E50; color: #F4A261; border: 1px solid #F4A261',
        content
    )
    
    # Fix any inline phone links with wrong colors
    content = re.sub(
        r'(<a href="(?:tel|sms):8476522338"[^>]*style="[^"]*)(background:\s*#F4A261[^;]*;[^"]*color:\s*white)',
        r'\1background: #2C3E50; color: #F4A261; border: 1px solid #F4A261',
        content
    )
    
    # Fix phone button hover effects
    if '.phone-button' in content:
        # Update CSS for phone button
        content = re.sub(
            r'(\.phone-button\s*\{[^}]*background:\s*)#F4A261([^}]*color:\s*)#2C3E50',
            r'\1#2C3E50\2#F4A261',
            content
        )
        
        # Add hover effect if not present
        if '.phone-button:hover' not in content and '.phone-button' in content:
            hover_style = """
    .phone-button:hover {
        background: #1a252f !important;
        color: #F1C40F !important;
        border-color: #F1C40F !important;
        box-shadow: 0 0 15px rgba(244, 162, 97, 0.4);
        transform: translateY(-2px);
    }
"""
            content = re.sub(
                r'(\.phone-button\s*\{[^}]*\})',
                r'\1' + hover_style,
                content
            )
    
    # Fix any phone number text that's orange/wrong color in content
    content = re.sub(
        r'(<a[^>]*href="tel:8476522338"[^>]*)(>)(\(847\) 652-2338)',
        r'\1 style="color: #F4A261; text-decoration: none;">\3',
        content
    )
    
    # Fix footer phone numbers
    content = re.sub(
        r'(📱 Text:\s*<a href="sms:8476522338"[^>]*style="[^"]*)(color:\s*#60a5fa)',
        r'\1color: #F4A261',
        content
    )
    
    # Add consistent styling for all phone links
    phone_style = 'style="color: #F4A261; text-decoration: none; font-weight: 600;"'
    
    # Apply to any plain phone links without styling
    content = re.sub(
        r'<a href="(tel|sms):8476522338">',
        f'<a href="\\1:8476522338" {phone_style}>',
        content
    )
    
    return content, content != original

def add_phone_css(content):
    """Add CSS for consistent phone styling"""
    
    phone_css = """
    /* Premium Phone Number Styling */
    .phone-button, a[href^="tel:"], a[href^="sms:"] {
        background: #2C3E50 !important;
        color: #F4A261 !important;
        border: 1px solid #F4A261 !important;
        padding: 10px 20px;
        border-radius: 8px;
        font-weight: 600;
        text-decoration: none;
        display: inline-block;
        transition: all 0.3s ease;
    }
    
    .phone-button:hover, a[href^="tel:"]:hover, a[href^="sms:"]:hover {
        background: #1a252f !important;
        color: #F1C40F !important;
        border-color: #F1C40F !important;
        box-shadow: 0 0 20px rgba(241, 196, 15, 0.4);
        transform: translateY(-2px);
    }
    
    /* Inline phone numbers */
    .phone-inline {
        color: #F4A261 !important;
        font-weight: 600;
    }
"""
    
    if "Premium Phone Number Styling" not in content:
        if '</style>' in content:
            content = re.sub(
                r'(</style>)',
                f'{phone_css}\\1',
                content
            )
    
    return content

def process_file(file_path):
    """Process a single HTML file"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content, changed1 = fix_phone_styling(content)
    content = add_phone_css(content)
    
    return content, changed1

def main():
    """Process all HTML files"""
    
    root_dir = Path('C:/Users/mirsa/manage369-live')
    updated_files = []
    
    html_files = list(root_dir.rglob('*.html'))
    html_files = [f for f in html_files if not any(
        skip in str(f) for skip in ['.git', 'node_modules', 'dist', 'build']
    )]
    
    print(f"Fixing phone number styling in {len(html_files)} files...")
    print("Applying: Navy background with gold text for all phone numbers")
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
    print(f"Fixed phone styling in {len(updated_files)} files")
    print("\nPhone number styling:")
    print("- Background: Navy (#2C3E50)")
    print("- Text: Gold (#F4A261)")
    print("- Border: Gold 1px")
    print("- Hover: Darker navy with yellow glow")

if __name__ == "__main__":
    main()