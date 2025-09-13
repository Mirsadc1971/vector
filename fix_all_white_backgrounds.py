#!/usr/bin/env python3
import os
import re

def fix_html_file(filepath):
    """Fix white backgrounds and apply dark theme to HTML file"""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    original_content = content

    # Replace all white backgrounds with dark theme
    patterns = [
        (r'background:\s*#fff(?:fff)?(?![\da-fA-F])', 'background: #2C3E50'),
        (r'background:\s*white', 'background: #2C3E50'),
        (r'background-color:\s*#fff(?:fff)?(?![\da-fA-F])', 'background-color: #2C3E50'),
        (r'background-color:\s*white', 'background-color: #2C3E50'),
        (r'background:\s*rgb\(255,\s*255,\s*255\)', 'background: #2C3E50'),
        (r'background-color:\s*rgb\(255,\s*255,\s*255\)', 'background-color: #2C3E50'),
        # Fix inline styles
        (r'style="([^"]*?)background:\s*#fff(?:fff)?(?![\da-fA-F])([^"]*?)"', r'style="\1background: #2C3E50\2"'),
        (r'style="([^"]*?)background:\s*white([^"]*?)"', r'style="\1background: #2C3E50\2"'),
        (r'style="([^"]*?)background-color:\s*#fff(?:fff)?(?![\da-fA-F])([^"]*?)"', r'style="\1background-color: #2C3E50\2"'),
        (r'style="([^"]*?)background-color:\s*white([^"]*?)"', r'style="\1background-color: #2C3E50\2"'),
        # Fix style attributes with single quotes
        (r"style='([^']*?)background:\s*#fff(?:fff)?(?![\da-fA-F])([^']*?)'", r"style='\1background: #2C3E50\2'"),
        (r"style='([^']*?)background:\s*white([^']*?)'", r"style='\1background: #2C3E50\2'"),
        (r"style='([^']*?)background-color:\s*#fff(?:fff)?(?![\da-fA-F])([^']*?)'", r"style='\1background-color: #2C3E50\2'"),
        (r"style='([^']*?)background-color:\s*white([^']*?)'", r"style='\1background-color: #2C3E50\2'"),
    ]

    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

    # Also ensure body has dark background if it doesn't already
    if '<body' in content and 'background' not in content.split('<body')[1].split('>')[0]:
        content = re.sub(r'<body([^>]*?)>', r'<body\1 style="background: #2C3E50; color: #e5e7eb;">', content)

    # Fix any remaining color issues for readability
    # Ensure dark text on light backgrounds becomes light text
    content = re.sub(r'color:\s*#333(?:333)?(?![\da-fA-F])', 'color: #e5e7eb', content)
    content = re.sub(r'color:\s*#000(?:000)?(?![\da-fA-F])', 'color: #e5e7eb', content)
    content = re.sub(r'color:\s*black', 'color: #e5e7eb', content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8', errors='ignore') as f:
            f.write(content)
        return True
    return False

def main():
    # Get all HTML files
    html_files = []

    # Root directory files
    for f in os.listdir('.'):
        if f.endswith('.html'):
            html_files.append(f)

    # Subdirectory files
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories and node_modules
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
        for f in files:
            if f.endswith('.html'):
                filepath = os.path.join(root, f)
                if filepath not in html_files:
                    html_files.append(filepath)

    print(f"Found {len(html_files)} HTML files to process")

    fixed_count = 0
    for filepath in html_files:
        try:
            if fix_html_file(filepath):
                fixed_count += 1
                print(f"Fixed: {filepath}")
        except Exception as e:
            print(f"Error processing {filepath}: {e}")

    print(f"\nFixed {fixed_count} files")

if __name__ == "__main__":
    os.chdir('C:\\Users\\mirsa\\Documents\\manage369-live')
    main()