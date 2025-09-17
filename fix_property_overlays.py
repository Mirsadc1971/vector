import os
import re

# Directory containing property management pages
property_dir = 'property-management'

# Counter for modified files
modified_count = 0

# Process each subdirectory
for root, dirs, files in os.walk(property_dir):
    for file in files:
        if file == 'index.html':
            file_path = os.path.join(root, file)

            # Read the file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # Fix hero section overlays (0.95 -> 0.3)
            content = re.sub(
                r'rgba\(8,66,152,0\.95\)',
                'rgba(8,66,152,0.3)',
                content
            )
            content = re.sub(
                r'rgba\(244,162,97,0\.95\)',
                'rgba(244,162,97,0.3)',
                content
            )

            # Fix hero-optimized overlays (0.05 -> 0.2)
            content = re.sub(
                r'rgba\(8,66,152,0\.05\)',
                'rgba(8,66,152,0.2)',
                content
            )
            content = re.sub(
                r'rgba\(244,162,97,0\.05\)',
                'rgba(244,162,97,0.2)',
                content
            )

            # Add link to fix CSS if not already present
            if 'fix-property-overlays.css' not in content:
                # Add before closing </head>
                content = content.replace(
                    '</head>',
                    '<link href="/fix-property-overlays.css" rel="stylesheet">\n</head>'
                )

            # Write back if changed
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                modified_count += 1
                print(f"Modified: {file_path}")

print(f"\nTotal files modified: {modified_count}")