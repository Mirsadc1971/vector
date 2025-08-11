import os
import re

def fix_form_placement(directory):
    """Fix form placement and structure in property management pages"""
    
    fixed_files = []
    
    for filename in os.listdir(directory):
        if filename == 'index.html':
            continue
            
        filepath = os.path.join(directory, filename, 'index.html')
        
        if not os.path.exists(filepath):
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if page has the old consultation-form-section structure
        if 'consultation-form-section' in content:
            print(f"Fixing form in {filename}...")
            
            # Remove the old consultation form section completely
            # Pattern to match the entire old form section
            pattern = r'<!-- Property Management Consultation Form Section -->.*?</section>\s*(?=<section class="faq-section"|<!-- PERFECT FOOTER|<footer>)'
            content = re.sub(pattern, '', content, flags=re.DOTALL)
            
            # Also remove any standalone consultation-form-section
            pattern2 = r'<section class="consultation-form-section">.*?</section>\s*'
            content = re.sub(pattern2, '', content, flags=re.DOTALL)
            
            # Now find where to insert the new form (before FAQ section)
            # The form should go AFTER the location-content section and BEFORE the FAQ section
            
            # Pattern to find the end of location-content section
            location_end_pattern = r'(</section>\s*)(</section>\s*)?(\s*<section class="faq-section">)'
            
            # New simple consultation form HTML
            new_form_html = '''
    <section class="consultation-form">
        <div class="consultation-form-content">
            <h2>Schedule Your Free {} Property Management Consultation</h2>
            <p>Discover how our 18+ years of experience and professional certifications can enhance your {} property. Get expert insights tailored to your community's unique needs.</p>
            
            <form action="https://formspree.io/f/xpznzgnk" method="POST" id="consultationForm">
                <div class="form-group">
                    <label for="name">Full Name *</label>
                    <input type="text" id="name" name="name" required>
                </div>
                
                <div class="form-group">
                    <label for="email">Email Address *</label>
                    <input type="email" id="email" name="email" required>
                </div>
                
                <div class="form-group">
                    <label for="phone">Phone Number *</label>
                    <input type="tel" id="phone" name="phone" required>
                </div>
                
                <div class="form-group">
                    <label for="property_type">Property Type</label>
                    <select id="property_type" name="property_type">
                        <option value="">Select Property Type</option>
                        <option value="condominium">Condominium Association</option>
                        <option value="hoa">Homeowner Association (HOA)</option>
                        <option value="townhome">Townhome Community</option>
                        <option value="mixed_use">Mixed Use Development</option>
                        <option value="other">Other</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="units">Number of Units</label>
                    <input type="number" id="units" name="units" placeholder="e.g., 24">
                </div>
                
                <div class="form-group">
                    <label for="current_management">Current Management Situation</label>
                    <select id="current_management" name="current_management">
                        <option value="">Select Current Situation</option>
                        <option value="self_managed">Self-Managed</option>
                        <option value="management_company">Have Management Company</option>
                        <option value="board_managed">Board-Managed</option>
                        <option value="new_development">New Development</option>
                        <option value="transition">In Transition</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="timeline">When are you looking to make a change?</label>
                    <select id="timeline" name="timeline">
                        <option value="">Select Timeline</option>
                        <option value="immediately">Immediately</option>
                        <option value="1_3_months">1-3 months</option>
                        <option value="3_6_months">3-6 months</option>
                        <option value="exploring">Just exploring options</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="challenges">What are your main property management challenges? (Optional)</label>
                    <textarea id="challenges" name="challenges" placeholder="e.g., Financial reporting, maintenance issues, board support, resident relations..."></textarea>
                </div>
                
                <div class="form-group">
                    <label for="location_specific">Specific to {}:</label>
                    <input type="text" name="location_specific" value="{} Property Management Inquiry" readonly>
                </div>
                
                <button type="submit" class="form-submit">Schedule Free Consultation</button>
            </form>
        </div>
    </section>
'''
            
            # Get the location name for the form
            location_name = filename.replace('-', ' ').title()
            
            # Format the form HTML with location name
            formatted_form = new_form_html.format(location_name, location_name, location_name, location_name)
            
            # Find the correct insertion point (after location-content, before FAQ)
            if '<section class="faq-section">' in content:
                # Insert before FAQ section
                content = content.replace('<section class="faq-section">', formatted_form + '\n    <section class="faq-section">')
            else:
                # If no FAQ section, insert before the why-choose section
                if '<section class="why-choose">' in content:
                    content = content.replace('<section class="why-choose">', formatted_form + '\n    <section class="why-choose">')
            
            # Save the fixed file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            fixed_files.append(filename)
    
    return fixed_files

# Run the fix
directory = r'C:\Users\mirsa\manage369-live\property-management'
fixed = fix_form_placement(directory)

print(f"\nFixed {len(fixed)} pages:")
for page in fixed:
    print(f"  - {page}")

print("\nAll forms have been fixed with proper placement and structure!")