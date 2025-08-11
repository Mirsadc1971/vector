import os
import re

def update_service_cards(directory):
    """Update service cards on all property pages with new design"""
    
    updated_files = []
    
    for filename in os.listdir(directory):
        if filename == 'index.html':
            continue
            
        filepath = os.path.join(directory, filename, 'index.html')
        
        if not os.path.exists(filepath):
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if page has the old service cards
        if '<div class="services-grid">' in content:
            print(f"Updating service cards in {filename}...")
            
            # Find and replace the entire services-grid section
            old_pattern = r'<div class="services-grid">.*?</div>\s*</div>\s*</div>'
            
            # New service cards HTML with emojis
            new_cards_html = '''<div class="services-grid">
            <div class="service-card">
                <h3>🏢 Condominium Management</h3>
                <p>Expert management for high-rise and mid-rise condominium buildings, honoring the unique character of each North Shore and Chicago community.</p>
                <a href="../../services/condominium-management/index.html">Explore Services →</a>
            </div>
            <div class="service-card">
                <h3>🏘️ HOA Management</h3>
                <p>Thoughtful homeowner association management that respects the heritage and values of North Shore suburban communities.</p>
                <a href="../../services/hoa-management/index.html">Explore Services →</a>
            </div>
            <div class="service-card">
                <h3>🏡 Townhome Management</h3>
                <p>Dedicated management for townhome communities and mixed-use developments with established municipal relationships.</p>
                <a href="../../services/townhome-management/index.html">Explore Services →</a>
            </div>
        </div>'''
            
            # Replace the old cards with new ones
            if re.search(old_pattern, content, flags=re.DOTALL):
                content = re.sub(old_pattern, new_cards_html, content, flags=re.DOTALL)
                
                # Save the updated file
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                updated_files.append(filename)
            else:
                # Try a more specific pattern if the general one doesn't match
                # Look for the three individual service cards
                if 'Condominium Management' in content and 'HOA Management' in content:
                    # Replace individual cards
                    
                    # Card 1 - Condominium Management
                    card1_pattern = r'<div class="service-card">\s*<h3>Condominium Management</h3>.*?</div>'
                    card1_new = '''<div class="service-card">
                <h3>🏢 Condominium Management</h3>
                <p>Expert management for high-rise and mid-rise condominium buildings, honoring the unique character of each North Shore and Chicago community.</p>
                <a href="../../services/condominium-management/index.html">Explore Services →</a>
            </div>'''
                    content = re.sub(card1_pattern, card1_new, content, flags=re.DOTALL)
                    
                    # Card 2 - HOA Management
                    card2_pattern = r'<div class="service-card">\s*<h3>HOA Management</h3>.*?</div>'
                    card2_new = '''<div class="service-card">
                <h3>🏘️ HOA Management</h3>
                <p>Thoughtful homeowner association management that respects the heritage and values of North Shore suburban communities.</p>
                <a href="../../services/hoa-management/index.html">Explore Services →</a>
            </div>'''
                    content = re.sub(card2_pattern, card2_new, content, flags=re.DOTALL)
                    
                    # Card 3 - Financial/Townhome Management
                    # First check if it's Financial Management
                    if 'Financial Management' in content:
                        card3_pattern = r'<div class="service-card">\s*<h3>Financial Management</h3>.*?</div>'
                        card3_new = '''<div class="service-card">
                <h3>🏡 Townhome Management</h3>
                <p>Dedicated management for townhome communities and mixed-use developments with established municipal relationships.</p>
                <a href="../../services/townhome-management/index.html">Explore Services →</a>
            </div>'''
                        content = re.sub(card3_pattern, card3_new, content, flags=re.DOTALL)
                    
                    # Save the updated file
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    updated_files.append(filename)
    
    return updated_files

# Run the update
directory = r'C:\Users\mirsa\manage369-live\property-management'
updated = update_service_cards(directory)

print(f"\nUpdated {len(updated)} pages:")
for page in updated:
    print(f"  - {page}")

print("\nAll service cards have been updated with emojis and new descriptions!")