"""
Fix broken consultation forms across all property management pages
"""

import os
from bs4 import BeautifulSoup

def get_correct_form_html(location_display):
    """Return the correct consultation form HTML"""
    return f'''<section class="consultation-form">
   <div class="consultation-form-content">
    <h2>
     Schedule Your Free {location_display} Property Management Consultation
    </h2>
    <p>
     Discover how our many years of experience and professional certifications can enhance your {location_display} property. Get expert insights tailored to your community's unique needs.
    </p>
    <form action="https://formspree.io/f/xpznzgnk" id="consultationForm" method="POST">
     <div class="form-group">
      <label for="name">
       Full Name *
      </label>
      <input id="name" name="name" required="" type="text"/>
     </div>
     <div class="form-group">
      <label for="email">
       Email Address *
      </label>
      <input id="email" name="email" required="" type="email"/>
     </div>
     <div class="form-group">
      <label for="phone">
       Phone Number *
      </label>
      <input id="phone" name="phone" required="" type="tel"/>
     </div>
     <div class="form-group">
      <label for="property_type">
       Property Type
      </label>
      <select id="property_type" name="property_type">
       <option value="">
        Select Property Type
       </option>
       <option value="condominium">
        Condominium Association
       </option>
       <option value="hoa">
        Homeowner Association (HOA)
       </option>
       <option value="townhome">
        Townhome Community
       </option>
       <option value="mixed_use">
        Mixed Use Development
       </option>
       <option value="other">
        Other
       </option>
      </select>
     </div>
     <div class="form-group">
      <label for="units">
       Number of Units
      </label>
      <input id="units" name="units" placeholder="e.g., 24" type="number"/>
     </div>
     <div class="form-group">
      <label for="current_management">
       Current Management Situation
      </label>
      <select id="current_management" name="current_management">
       <option value="">
        Select Current Situation
       </option>
       <option value="self_managed">
        Self-Managed
       </option>
       <option value="management_company">
        Have Management Company
       </option>
       <option value="board_managed">
        Board-Managed
       </option>
       <option value="new_development">
        New Development
       </option>
       <option value="transition">
        In Transition
       </option>
      </select>
     </div>
     <div class="form-group">
      <label for="timeline">
       When are you looking to make a change?
      </label>
      <select id="timeline" name="timeline">
       <option value="">
        Select Timeline
       </option>
       <option value="immediately">
        Immediately
       </option>
       <option value="1_3_months">
        1-3 months
       </option>
       <option value="3_6_months">
        3-6 months
       </option>
       <option value="exploring">
        Just exploring options
       </option>
      </select>
     </div>
     <div class="form-group">
      <label for="challenges">
       What are your main property management challenges? (Optional)
      </label>
      <textarea id="challenges" name="challenges" placeholder="e.g., Financial reporting, maintenance issues, board support, resident relations..."></textarea>
     </div>
     <div class="form-group">
      <label for="location_specific">
       Specific to {location_display}:
      </label>
      <input name="location_specific" readonly="" type="text" value="{location_display} Property Management Inquiry"/>
     </div>
     <button class="form-submit" type="submit">
      Schedule Free Consultation
     </button>
    </form>
   </div>
  </section>'''

def fix_consultation_form(filepath, location_display):
    """Fix the consultation form on a page"""
    
    print(f"Processing: {location_display}")
    
    try:
        # Read the file
        with open(filepath, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find any broken consultation form section
        broken_form = None
        for section in soup.find_all('section'):
            # Check for the broken form indicators
            h2 = section.find('h2')
            if h2 and 'Schedule Your Professional Consultation' in h2.get_text():
                broken_form = section
                break
        
        # Also check for section with class consultation-section
        if not broken_form:
            broken_form = soup.find('section', class_='consultation-section')
        
        if broken_form:
            print(f"  Found broken form - replacing with correct form")
            # Create new correct form
            correct_form_html = get_correct_form_html(location_display)
            new_form = BeautifulSoup(correct_form_html, 'html.parser')
            
            # Replace the broken form
            broken_form.replace_with(new_form)
            
            # Save the fixed file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            
            print(f"  [SUCCESS] Fixed {location_display}")
            return True
        else:
            # Check if there's already a correct form
            correct_form = soup.find('section', class_='consultation-form')
            if correct_form:
                print(f"  [SKIP] Already has correct form")
            else:
                print(f"  [SKIP] No consultation form found")
            return False
            
    except Exception as e:
        print(f"  [ERROR] Error processing {filepath}: {e}")
        return None

def main():
    """Main function to fix all pages"""
    
    print("Fixing consultation forms across all pages")
    print("=" * 50)
    
    success_count = 0
    skipped_count = 0
    failed_files = []
    
    # Get all property management directories
    base_dir = 'C:\\Users\\mirsa\\manage369-live\\property-management'
    
    for community_dir in os.listdir(base_dir):
        filepath = os.path.join(base_dir, community_dir, 'index.html')
        
        if not os.path.exists(filepath):
            continue
        
        location_display = community_dir.replace('-', ' ').title()
        
        result = fix_consultation_form(filepath, location_display)
        if result is True:
            success_count += 1
        elif result is False:
            skipped_count += 1
        else:
            failed_files.append(community_dir)
    
    print("=" * 50)
    print(f"Process Complete!")
    print(f"Successfully fixed: {success_count} pages")
    print(f"Skipped: {skipped_count} pages")
    
    if failed_files:
        print(f"\nFailed to process {len(failed_files)} pages:")
        for f in failed_files:
            print(f"  - {f}")

if __name__ == "__main__":
    main()