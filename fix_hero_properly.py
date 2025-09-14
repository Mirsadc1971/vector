#!/usr/bin/env python3
import os
import re

# Process all area pages
os.chdir('property-management')
dirs = [d for d in os.listdir('.') if os.path.isdir(d)]
print(f"Fixing hero sections in {len(dirs)} area pages...")

for directory in dirs:
    file_path = os.path.join(directory, 'index.html')
    if not os.path.exists(file_path):
        continue

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix the webp background specifically
    content = re.sub(
        r'\.webp \.hero-optimized \{[^}]*\}',
        '''.webp .hero-optimized {
    background: linear-gradient(135deg, rgba(8,66,152,0.05) 0%, rgba(244,162,97,0.05) 100%),
                url('/images/buck4manage369_compressed.webp') center/cover !important;
}''',
        content,
        flags=re.DOTALL
    )

    # Fix the no-webp jpg background
    content = re.sub(
        r'\.no-webp \.hero-optimized \{[^}]*\}',
        '''.no-webp .hero-optimized {
    background: linear-gradient(135deg, rgba(8,66,152,0.05) 0%, rgba(244,162,97,0.05) 100%),
                url('/images/buck4manage369_optimized.jpg') center/cover !important;
}''',
        content,
        flags=re.DOTALL
    )

    # Also add a fallback background directly on .hero-optimized
    content = re.sub(
        r'(\.hero-optimized \{[^}]*)(})',
        r'''\1    background: linear-gradient(135deg, rgba(8,66,152,0.05) 0%, rgba(244,162,97,0.05) 100%),
                url('/images/buck4manage369_optimized.jpg') center/cover;
\2''',
        content,
        flags=re.DOTALL
    )

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Fixed {directory}")

print("\nAll hero sections properly fixed!")