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

print(f"Found {len(property_dirs)} property directories to standardize")

# Template for the service offerings section (replacing Why Choose Manage369)
service_offerings_html = '''    <!-- Service Offerings Section -->
    <section class="why-choose-section">
        <div class="container">
            <h2>Our Service Offerings</h2>
            <div class="features-grid">
                <div class="feature-item">
                    <div class="feature-icon">💰</div>
                    <div class="feature-content">
                        <h3>Financial Management</h3>
                        <p>Professional financial reporting, budget development, and reserve studies to protect your investment.</p>
                    </div>
                </div>
                
                <div class="feature-item">
                    <div class="feature-icon">🔧</div>
                    <div class="feature-content">
                        <h3>Maintenance Coordination</h3>
                        <p>24/7 emergency response and proactive maintenance programs with trusted local contractors.</p>
                    </div>
                </div>
                
                <div class="feature-item">
                    <div class="feature-icon">📋</div>
                    <div class="feature-content">
                        <h3>Board Support</h3>
                        <p>Expert guidance for board meetings, elections, and governance to ensure smooth operations.</p>
                    </div>
                </div>
                
                <div class="feature-item">
                    <div class="feature-icon">📊</div>
                    <div class="feature-content">
                        <h3>Administrative Services</h3>
                        <p>Complete administrative support including document management and regulatory compliance.</p>
                    </div>
                </div>
                
                <div class="feature-item">
                    <div class="feature-icon">🏗️</div>
                    <div class="feature-content">
                        <h3>Capital Project Management</h3>
                        <p>Professional oversight of major repairs and improvements from planning through completion.</p>
                    </div>
                </div>
                
                <div class="feature-item">
                    <div class="feature-icon">🤝</div>
                    <div class="feature-content">
                        <h3>Resident Relations</h3>
                        <p>Fostering positive community relationships through clear communication and prompt issue resolution.</p>
                    </div>
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
            
            # Fix the JSON schema error (missing comma after serviceArea)
            content = re.sub(
                r'("serviceArea":\s*\{[^}]+\})\s*("hasOfferCatalog")',
                r'\1,\n  \2',
                content
            )
            
            # Remove any existing Why Choose section
            # Look for various patterns
            content = re.sub(
                r'<section class="why-choose[^"]*"[^>]*>.*?</section>',
                '',
                content,
                flags=re.DOTALL
            )
            
            # Also remove the simpler version
            content = re.sub(
                r'<!-- Why Choose Section -->.*?</section>',
                '',
                content,
                flags=re.DOTALL
            )
            
            # Insert the new service offerings section before the contact section
            if '<section class="contact-section">' in content:
                content = content.replace(
                    '<section class="contact-section">',
                    service_offerings_html + '\n\n    <section class="contact-section">'
                )
            elif '<!-- Contact Form Section -->' in content:
                content = content.replace(
                    '<!-- Contact Form Section -->',
                    service_offerings_html + '\n\n    <!-- Contact Form Section -->'
                )
            else:
                # If no contact section found, add before footer
                content = content.replace(
                    '<!-- PERFECT FOOTER',
                    service_offerings_html + '\n\n    <!-- PERFECT FOOTER'
                )
            
            # Write back the updated content
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"[OK] {directory.name} - standardized with service offerings")
            success_count += 1
            
    except Exception as e:
        print(f"[ERROR] {directory.name}: {str(e)}")
        error_count += 1

print(f"\n[COMPLETE] Standardization complete!")
print(f"Successfully updated: {success_count} pages")
print(f"Errors: {error_count} pages")