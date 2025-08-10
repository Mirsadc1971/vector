#!/usr/bin/env python3
import re

# Pages that need fixing based on the grep results
pages_to_fix = ['loop', 'hyde-park', 'logan-square']

for page in pages_to_fix:
    file_path = rf"C:\Users\mirsa\manage369-live\property-management\{page}\index.html"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the colored gradient with a simple dark overlay like other pages use
        # Pattern 1: Blue to orange gradient
        content = re.sub(
            r'background:\s*linear-gradient\(rgba\(43, 91, 160, [0-9.]+\), rgba\(255, 107, 53, [0-9.]+\)\),',
            'background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.5)),',
            content
        )
        
        # Pattern 2: Any other colored gradients
        content = re.sub(
            r'background:\s*linear-gradient\(rgba\(255, 107, 53, [0-9.]+\), rgba\(43, 91, 160, [0-9.]+\)\),',
            'background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.5)),',
            content
        )
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed gradient overlay in: {page}")
        
    except Exception as e:
        print(f"Error with {page}: {e}")

print("\nAll gradient overlays fixed to use standard dark overlay")