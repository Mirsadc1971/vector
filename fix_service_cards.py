import os
import re
from pathlib import Path

# Get all property management subdirectories
property_dirs = []
property_management_path = Path("property-management")
if property_management_path.exists():
    property_dirs = [d for d in property_management_path.iterdir() if d.is_dir()]

# Sort directories for consistent processing
property_dirs.sort()

print(f"Found {len(property_dirs)} property directories to update")

# New service offerings section with proper card links
service_offerings_html = '''    <!-- Service Offerings Section -->
    <section class="why-choose-section">
        <div class="container">
            <h2>Our Service Offerings</h2>
            <div class="services-grid">
                <div class="service-card">
                    <h3>💰 Financial Management</h3>
                    <p>Professional financial reporting, budget development, and reserve studies to protect your investment.</p>
                    <a href="../../services/financial-management/index.html">Learn More →</a>
                </div>
                
                <div class="service-card">
                    <h3>🔧 Maintenance Coordination</h3>
                    <p>24/7 emergency response and proactive maintenance programs with trusted local contractors.</p>
                    <a href="../../services/maintenance-coordination/index.html">Learn More →</a>
                </div>
                
                <div class="service-card">
                    <h3>📋 Board Support</h3>
                    <p>Expert guidance for board meetings, elections, and governance to ensure smooth operations.</p>
                    <a href="../../services/board-support/index.html">Learn More →</a>
                </div>
                
                <div class="service-card">
                    <h3>📊 Administrative Services</h3>
                    <p>Complete administrative support including document management and regulatory compliance.</p>
                    <a href="../../services/administrative-services/index.html">Learn More →</a>
                </div>
                
                <div class="service-card">
                    <h3>🏗️ Capital Project Management</h3>
                    <p>Professional oversight of major repairs and improvements from planning through completion.</p>
                    <a href="../../services/capital-project-management/index.html">Learn More →</a>
                </div>
                
                <div class="service-card">
                    <h3>🤝 Resident Relations</h3>
                    <p>Fostering positive community relationships through clear communication and prompt issue resolution.</p>
                    <a href="../../services/resident-relations/index.html">Learn More →</a>
                </div>
            </div>
        </div>
    </section>'''

success_count = 0
error_count = 0

for directory in property_dirs:
    try:
        index_file = directory / "index.html"
        if index_file.exists():
            with open(index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove the existing service offerings section
            content = re.sub(
                r'<!-- Service Offerings Section -->.*?</section>',
                '',
                content,
                flags=re.DOTALL
            )
            
            # Insert the new service offerings section with proper cards
            if '<section class="contact-section">' in content:
                content = content.replace(
                    '<section class="contact-section">',
                    service_offerings_html + '\n\n    <section class="contact-section">'
                )
            else:
                # If no contact section found, add before footer
                content = content.replace(
                    '<footer>',
                    service_offerings_html + '\n\n    <footer>'
                )
            
            # Write back the updated content
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"[OK] {directory.name} - updated with linked service cards")
            success_count += 1
            
    except Exception as e:
        print(f"[ERROR] {directory.name}: {str(e)}")
        error_count += 1

print(f"\n[COMPLETE] Service cards update complete!")
print(f"Successfully updated: {success_count} pages")
print(f"Errors: {error_count} pages")