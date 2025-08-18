import os
import re
from pathlib import Path

def fix_form_accessibility(file_path):
    """Fix form accessibility issues including labels, autocomplete, and error handling"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes_made = False
    changes = []
    
    # 1. Fix form tags - add novalidate for custom validation
    form_pattern = r'<form([^>]*?)>'
    form_matches = list(re.finditer(form_pattern, content, re.IGNORECASE))
    
    for match in reversed(form_matches):
        form_tag = match.group(0)
        if 'novalidate' not in form_tag:
            new_form_tag = form_tag.replace('>', ' novalidate>')
            content = content[:match.start()] + new_form_tag + content[match.end():]
            changes_made = True
            changes.append("Added novalidate to form")
    
    # 2. Fix input fields with proper autocomplete and aria attributes
    input_fixes = {
        # Name fields
        r'id="name"': ('autocomplete="name"', 'Full name'),
        r'id="ownerName"': ('autocomplete="name"', 'Owner name'),
        r'id="mgmt-name"': ('autocomplete="name"', 'Your name'),
        r'id="maint-name"': ('autocomplete="name"', 'Your name'),
        
        # Email fields
        r'id="email"': ('autocomplete="email" aria-describedby="email-error"', 'Email address'),
        r'id="mgmt-email"': ('autocomplete="email" aria-describedby="mgmt-email-error"', 'Email address'),
        
        # Phone fields
        r'id="phone"': ('autocomplete="tel"', 'Phone number'),
        r'id="mgmt-phone"': ('autocomplete="tel"', 'Phone number'),
        r'id="maint-phone"': ('autocomplete="tel"', 'Phone number'),
        r'id="contractorPhone"': ('autocomplete="tel"', 'Contractor phone'),
        r'id="agentPhone"': ('autocomplete="tel"', 'Agent phone'),
        
        # Address fields
        r'id="mgmt-location"': ('autocomplete="address-level2"', 'Property location'),
        r'id="unitNumber"': ('autocomplete="address-line2"', 'Unit number'),
        r'id="maint-unit"': ('autocomplete="address-line2"', 'Unit number'),
    }
    
    for field_id, (attributes, label_text) in input_fixes.items():
        # Find input fields matching the ID
        input_pattern = rf'<input([^>]*?{field_id}[^>]*?)>'
        input_matches = list(re.finditer(input_pattern, content, re.IGNORECASE))
        
        for match in reversed(input_matches):
            input_tag = match.group(0)
            
            # Add autocomplete if not present
            if 'autocomplete=' not in input_tag:
                autocomplete_attr = attributes.split(' ')[0]
                if autocomplete_attr and 'autocomplete=' in autocomplete_attr:
                    new_input = input_tag.replace('>', f' {autocomplete_attr}>')
                    content = content[:match.start()] + new_input + content[match.end():]
                    changes_made = True
                    changes.append(f"Added autocomplete to {field_id}")
            
            # Add aria-describedby for fields that need error messages
            if 'aria-describedby=' in attributes and 'aria-describedby=' not in input_tag:
                aria_attr = [a for a in attributes.split(' ') if 'aria-describedby=' in a][0]
                new_input = input_tag.replace('>', f' {aria_attr}>')
                content = content[:match.start()] + new_input + content[match.end():]
                changes_made = True
                changes.append(f"Added aria-describedby to {field_id}")
    
    # 3. Add error message containers after email/required fields
    error_messages = {
        'mgmt-email': 'mgmt-email-error',
        'email': 'email-error',
        'phone': 'phone-error',
        'maint-phone': 'maint-phone-error'
    }
    
    for field_id, error_id in error_messages.items():
        # Check if error message already exists
        if f'id="{error_id}"' not in content:
            # Find the input field
            input_pattern = rf'<input[^>]*?id="{field_id}"[^>]*?>'
            input_match = re.search(input_pattern, content, re.IGNORECASE)
            
            if input_match:
                # Find the closing of the parent div (form-group)
                insert_pos = content.find('</div>', input_match.end())
                if insert_pos > 0:
                    error_html = f'\n                    <p id="{error_id}" role="alert" class="error-message" hidden>Please enter a valid {"email address" if "email" in field_id else "phone number"}.</p>'
                    content = content[:insert_pos] + error_html + content[insert_pos:]
                    changes_made = True
                    changes.append(f"Added error message for {field_id}")
    
    # 4. Fix select elements with proper labels
    select_pattern = r'<select([^>]*?)>'
    select_matches = list(re.finditer(select_pattern, content, re.IGNORECASE))
    
    for match in reversed(select_matches):
        select_tag = match.group(0)
        select_attrs = match.group(1)
        
        # Extract id
        id_match = re.search(r'id=["\'](.*?)["\']', select_attrs)
        if id_match:
            select_id = id_match.group(1)
            
            # Add aria-label if no associated label
            if 'aria-label=' not in select_attrs:
                # Determine appropriate label based on ID
                if 'type' in select_id.lower():
                    aria_label = 'Property type'
                elif 'urgency' in select_id.lower():
                    aria_label = 'Urgency level'
                elif 'timeline' in select_id.lower():
                    aria_label = 'Timeline'
                elif 'management' in select_id.lower():
                    aria_label = 'Current management situation'
                else:
                    aria_label = 'Select option'
                
                # Check if there's already a label element
                label_pattern = rf'<label[^>]*?for=["\']?{select_id}["\']?[^>]*?>'
                if not re.search(label_pattern, content[:match.start()]):
                    new_select = select_tag.replace('>', f' aria-label="{aria_label}">')
                    content = content[:match.start()] + new_select + content[match.end():]
                    changes_made = True
                    changes.append(f"Added aria-label to select {select_id}")
    
    # 5. Fix iframe titles
    iframe_pattern = r'<iframe([^>]*?)>'
    iframe_matches = list(re.finditer(iframe_pattern, content, re.IGNORECASE))
    
    for match in reversed(iframe_matches):
        iframe_tag = match.group(0)
        iframe_attrs = match.group(1)
        
        # Check if title exists
        if 'title=' not in iframe_attrs:
            # Determine title based on src
            src_match = re.search(r'src=["\'](.*?)["\']', iframe_attrs)
            if src_match:
                src = src_match.group(1)
                if 'google' in src.lower() and 'map' in src.lower():
                    title = 'Google Map of Manage369 office location'
                elif 'youtube' in src.lower():
                    title = 'YouTube video player'
                elif 'form' in src.lower():
                    title = 'Contact form'
                else:
                    title = 'Embedded content'
                
                new_iframe = iframe_tag.replace('>', f' title="{title}">')
                content = content[:match.start()] + new_iframe + content[match.end():]
                changes_made = True
                changes.append(f"Added title to iframe")
    
    # 6. Add validation script if forms exist and no validation present
    if '<form' in content and 'addEventListener(\'submit\'' not in content and '</body>' in content:
        validation_script = '''
    <!-- Form Validation for Accessibility -->
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Add validation to all forms
            const forms = document.querySelectorAll('form');
            forms.forEach(form => {
                form.addEventListener('submit', function(e) {
                    let isValid = true;
                    
                    // Validate email fields
                    const emailFields = form.querySelectorAll('input[type="email"], input[id*="email"]');
                    emailFields.forEach(field => {
                        const errorId = field.getAttribute('aria-describedby');
                        if (errorId) {
                            const errorElement = document.getElementById(errorId);
                            if (errorElement) {
                                if (!field.value || !field.value.includes('@')) {
                                    errorElement.hidden = false;
                                    field.setAttribute('aria-invalid', 'true');
                                    if (isValid) field.focus();
                                    isValid = false;
                                } else {
                                    errorElement.hidden = true;
                                    field.setAttribute('aria-invalid', 'false');
                                }
                            }
                        }
                    });
                    
                    // Validate required fields
                    const requiredFields = form.querySelectorAll('[required]');
                    requiredFields.forEach(field => {
                        if (!field.value.trim()) {
                            field.setAttribute('aria-invalid', 'true');
                            if (isValid) field.focus();
                            isValid = false;
                        } else {
                            field.setAttribute('aria-invalid', 'false');
                        }
                    });
                    
                    if (!isValid) {
                        e.preventDefault();
                    }
                });
            });
        });
    </script>
'''
        # Insert before closing body tag
        content = content.replace('</body>', validation_script + '\n</body>')
        changes_made = True
        changes.append("Added form validation script")
    
    # Write back if changes were made
    if changes_made:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, changes
    return False, []

# Process HTML files with forms
form_files = [
    'forms.html',
    'forms-clean.html',
    'contact.html',
    'ho6-insurance.html',
    'construction-request.html',
    'move-permit.html',
    'repair-request.html',
    'violation-report.html',
    'manage369-forms.html'
]

# Add consultation forms in property pages
for file in Path('property-management').rglob('index.html'):
    form_files.append(str(file))

# Add service pages that might have forms
for file in Path('services').rglob('index.html'):
    form_files.append(str(file))

print(f"Checking {len(form_files)} files with forms for accessibility")
print("-" * 50)

updated = 0
skipped = 0
errors = 0

for file in form_files:
    try:
        if os.path.exists(file):
            result, changes = fix_form_accessibility(file)
            if result:
                print(f"[FIXED] {file}")
                for change in changes[:5]:  # Show first 5 changes
                    print(f"  - {change}")
                if len(changes) > 5:
                    print(f"  ... and {len(changes) - 5} more changes")
                updated += 1
            else:
                skipped += 1
    except Exception as e:
        errors += 1
        print(f"[ERROR] {file}: {str(e)}")

print("-" * 50)
print(f"\n[COMPLETE] Form accessibility fixes complete!")
print(f"\nResults:")
print(f"  Files updated: {updated}")
print(f"  Files unchanged: {skipped}")
print(f"  Errors: {errors}")