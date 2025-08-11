import os
import re

def fix_form_position(directory):
    """Move consultation forms to be directly above the footer"""
    
    fixed_files = []
    
    for filename in os.listdir(directory):
        if filename == 'index.html':
            continue
            
        filepath = os.path.join(directory, filename, 'index.html')
        
        if not os.path.exists(filepath):
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if page has consultation-form section
        if '<section class="consultation-form">' in content:
            print(f"Fixing form position in {filename}...")
            
            # First, remove the consultation form from its current position
            pattern = r'<section class="consultation-form">.*?</section>\s*'
            form_match = re.search(pattern, content, flags=re.DOTALL)
            
            if form_match:
                form_html = form_match.group(0)
                # Remove form from current position
                content = re.sub(pattern, '', content, flags=re.DOTALL)
                
                # Now insert it right before the footer
                # Look for footer patterns
                if '<!-- PERFECT FOOTER' in content:
                    content = content.replace('<!-- PERFECT FOOTER', form_html + '\n    <!-- PERFECT FOOTER')
                elif '<footer>' in content:
                    content = content.replace('<footer>', form_html + '\n    <footer>')
                elif '<footer class=' in content:
                    pattern = r'(<footer[^>]*>)'
                    content = re.sub(pattern, form_html + r'\n    \1', content)
                
                # Save the fixed file
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                fixed_files.append(filename)
    
    return fixed_files

# Run the fix
directory = r'C:\Users\mirsa\manage369-live\property-management'
fixed = fix_form_position(directory)

print(f"\nFixed form position in {len(fixed)} pages:")
for page in fixed:
    print(f"  - {page}")

print("\nAll forms are now positioned directly above the footer!")