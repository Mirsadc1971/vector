#!/usr/bin/env python3
"""
Fix broken property management pages
"""

import os
from pathlib import Path
import re

def fix_broken_page(file_path):
    """Fix a single broken HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if page is broken (missing proper HTML structure)
        if '<body>' not in content or '</body>' not in content:
            print(f"Fixing broken page: {file_path}")
            
            # The files got truncated after the JSON-LD script
            # We need to add back the missing HTML structure
            
            # Find where the content was cut off (usually after </script>)
            if '</script>' in content and not '</head>' in content:
                # Insert missing closing head and body structure
                parts = content.rsplit('</script>', 1)
                if len(parts) == 2:
                    before_script = parts[0] + '</script>'
                    
                    # Add the missing structure
                    missing_html = '''
</head>
<body>
    <header class="header">
        <div class="header-content">
            <a href="../../index.html" class="logo">MANAGE369</a>
        
        <!-- Mobile Menu Toggle -->
        <button class="mobile-menu-toggle" onclick="toggleMobileMenu()">☰</button>
        
        <nav class="nav">
            <a href="../../index.html">Home</a>
            <div class="services-dropdown">
                <a href="../../services.html">Services <span>▼</span></a>
                <div class="dropdown-content">
                    <div class="dropdown-header">Property Types</div>
                    <a href="../../services/condominium-management/index.html">Condominium Management</a>
                    <a href="../../services/hoa-management/index.html">HOA Management</a>
                    <a href="../../services/townhome-management/index.html">Townhome Management</a>
                    <div class="dropdown-header">Service Offerings</div>
                    <a href="../../services/financial-management/index.html">Financial Management</a>
                    <a href="../../services/maintenance-coordination/index.html">Maintenance Coordination</a>
                    <a href="../../services/board-support/index.html">Board Support</a>
                    <a href="../../services/administrative-services/index.html">Administrative Services</a>
                    <a href="../../services/capital-project-management/index.html">Capital Project Management</a>
                    <a href="../../services/resident-relations/index.html">Resident Relations</a>
                </div>
            </div>
            <a href="../">Areas We Serve</a>
            <a href="../../pay-dues.html">Pay Dues</a>
            <a href="../../contact.html">Contact</a>
        </nav>
        
        <a href="tel:8476522338" class="phone">Call (847) 652-2338</a>
        </div>
    </header>
    
    <section class="hero">
        <div class="hero-content">
            <h1>Property Management Services</h1>
            <p>Professional Property Management Excellence</p>
        </div>
    </section>
    
    <section class="content">
        <h2>Professional Property Management Services</h2>
        <p>Manage369 provides comprehensive property management services with 18+ years of experience managing properties throughout Chicago and the North Shore.</p>
        
        <div class="services-grid">
            <div class="service-card">
                <h3>Condominium Management</h3>
                <p>Expert management for condominium associations.</p>
                <a href="../../services/condominium-management/index.html">Learn More →</a>
            </div>
            <div class="service-card">
                <h3>HOA Management</h3>
                <p>Comprehensive homeowner association management.</p>
                <a href="../../services/hoa-management/index.html">Learn More →</a>
            </div>
            <div class="service-card">
                <h3>Financial Management</h3>
                <p>Professional financial reporting and budget management.</p>
                <a href="../../services/financial-management/index.html">Learn More →</a>
            </div>
        </div>
    </section>
    
    <section class="contact-section">
        <h2>Ready for Professional Property Management?</h2>
        <p>Contact us today for a free consultation.</p>
        <p>📞 <a href="tel:8476522338">(847) 652-2338</a> | ✉️ <a href="mailto:service@manage369.com">service@manage369.com</a></p>
    </section>
    
    <footer>
        <div class="footer-main">
            <div class="footer-column">
                <div class="footer-logo">Manage369</div>
                <div class="footer-description">Premier Chicago & North Shore Property Management</div>
                <div class="footer-contact-line">
                    📞 <a href="tel:8476522338">(847) 652-2338</a>
                </div>
                <div class="footer-contact-line">
                    ✉️ <a href="mailto:service@manage369.com">service@manage369.com</a>
                </div>
            </div>
            
            <div class="footer-column">
                <h3>Quick Links</h3>
                <ul class="footer-links">
                    <li><a href="../../services.html">Services</a></li>
                    <li><a href="../">Areas We Serve</a></li>
                    <li><a href="../../contact.html">Contact</a></li>
                </ul>
            </div>
        </div>
        
        <div class="footer-bottom">
            <div class="footer-copyright">
                © 2025 Manage369. All Rights Reserved.
            </div>
        </div>
    </footer>
    
    <script>
        function toggleMobileMenu() {
            const mobileMenu = document.getElementById('mobileMenu');
            mobileMenu.classList.toggle('active');
        }
    </script>
</body>
</html>'''
                    
                    # Create fixed content
                    fixed_content = before_script + missing_html
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(fixed_content)
                    
                    return True
        
        return False
        
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False

def main():
    base_dir = Path(r"C:\Users\mirsa\manage369-live\property-management")
    
    broken_count = 0
    fixed_count = 0
    
    # Check all property management pages
    for location_dir in base_dir.iterdir():
        if location_dir.is_dir():
            index_file = location_dir / "index.html"
            if index_file.exists():
                if fix_broken_page(index_file):
                    fixed_count += 1
                    broken_count += 1
    
    print(f"\nFound {broken_count} broken pages")
    print(f"Fixed {fixed_count} pages")

if __name__ == "__main__":
    main()