import os
import re

def remove_duplicate_forms(directory):
    """Remove duplicate forms and inline styles from property pages"""
    
    fixed_files = []
    
    for filename in os.listdir(directory):
        if filename == 'index.html':
            continue
            
        filepath = os.path.join(directory, filename, 'index.html')
        
        if not os.path.exists(filepath):
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        modified = False
        
        # Remove any inline style blocks related to consultation forms
        style_pattern = r'<!-- Property Management Consultation Form Section -->.*?</style>\s*'
        if re.search(style_pattern, content, flags=re.DOTALL):
            content = re.sub(style_pattern, '', content, flags=re.DOTALL)
            modified = True
            print(f"Removed inline styles from {filename}")
        
        # Remove standalone style blocks for consultation forms
        style_pattern2 = r'<style>\s*/\*.*?Consultation Form Section.*?\*/.*?</style>\s*'
        if re.search(style_pattern2, content, flags=re.DOTALL):
            content = re.sub(style_pattern2, '', content, flags=re.DOTALL)
            modified = True
            print(f"Removed consultation form styles from {filename}")
        
        # Count how many consultation forms are on the page
        form_count = content.count('<section class="consultation-form">')
        
        if form_count > 1:
            print(f"Found {form_count} forms in {filename}, keeping only the one above footer")
            
            # Find all consultation form sections
            form_pattern = r'<section class="consultation-form">.*?</section>'
            forms = re.findall(form_pattern, content, flags=re.DOTALL)
            
            # Remove all forms first
            for form in forms:
                content = content.replace(form, '', 1)
            
            # Add back only one form right before the footer
            if forms:
                # Use the last form found (should be the correct one)
                correct_form = forms[-1]
                
                # Insert before footer
                if '<!-- PERFECT FOOTER' in content:
                    content = content.replace('<!-- PERFECT FOOTER', correct_form + '\n\n    <!-- PERFECT FOOTER')
                elif '<footer>' in content:
                    content = content.replace('<footer>', correct_form + '\n\n    <footer>')
                
                modified = True
        
        # Also check for the old consultation-form-section pattern and remove it
        if 'consultation-form-section' in content:
            # Remove the entire old form section
            old_form_pattern = r'<section class="consultation-form-section">.*?</section>\s*'
            content = re.sub(old_form_pattern, '', content, flags=re.DOTALL)
            modified = True
            print(f"Removed old consultation-form-section from {filename}")
        
        if modified:
            # Clean up any multiple blank lines
            content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            fixed_files.append(filename)
    
    return fixed_files

# Run the fix
directory = r'C:\Users\mirsa\manage369-live\property-management'
fixed = remove_duplicate_forms(directory)

print(f"\nFixed {len(fixed)} pages:")
for page in fixed:
    print(f"  - {page}")

if fixed:
    print("\nAll duplicate forms and inline styles have been removed!")
else:
    print("\nNo issues found - all pages are clean!")