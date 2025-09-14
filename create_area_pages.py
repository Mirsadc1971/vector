#!/usr/bin/env python3
import os

# Master template with homepage design and colors
def create_area_page(city_data):
    """Create a property management page for a specific city"""

    city = city_data['city']
    slug = city_data['slug']
    intro = city_data['intro']
    challenges = city_data['challenges']
    links = city_data['links']

    template = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>{city} Property Management — HOA, Condo & Townhome Experts | Manage369</title>
<meta content="Premier {city} property management since 2007. Expert HOA, condominium & townhome management. 110% Service Guarantee. Call (847) 834-4131." name="description"/>
<link href="/images/apple-touch-icon.png" rel="apple-touch-icon" sizes="180x180"/>
<link href="/images/favicon-32x32.png" rel="icon" sizes="32x32" type="image/png"/>
<link href="/images/favicon-16x16.png" rel="icon" sizes="16x16" type="image/png"/>
<link href="../../site.webmanifest" rel="manifest"/>
<meta content="#2C3E50" name="msapplication-TileColor"/>
<meta content="#1f2937" name="theme-color"/>
<link href="https://www.manage369.com/property-management/{slug}/" rel="canonical"/>
<style>
/* Master Color Scheme */
:root {{
    --primary-gold: #F4A261;
    --primary-navy: #2C3E50;
    --background-dark: #1f2937;
    --text-light: #e5e7eb;
    --accent-blue: #084298;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    background: var(--background-dark) !important;
    color: var(--text-light) !important;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
}}

/* Typography */
h1, h2, h3, h4 {{
    color: var(--primary-gold) !important;
    margin-bottom: 1.5rem;
}}

h1 {{ font-size: 2.5rem; text-align: center; }}
h2 {{ font-size: 2rem; text-align: center; margin: 3rem 0 2rem; }}
h3 {{ font-size: 1.5rem; }}

p {{
    margin-bottom: 1.25rem;
    color: var(--text-light);
    line-height: 1.8;
}}

a {{
    color: var(--primary-gold);
    text-decoration: none;
    transition: all 0.3s ease;
}}

a:hover {{
    opacity: 0.9;
}}

/* Container */
.container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}}

section {{
    padding: 80px 20px;
}}

/* Header */
.header {{
    background: var(--background-dark);
    padding: 1rem 2rem;
    position: sticky;
    top: 0;
    z-index: 1000;
    box-shadow: 0 2px 20px rgba(0,0,0,0.2);
    border-bottom: 1px solid rgba(244,162,97,0.2);
}}

.header-content {{
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.logo {{
    font-size: 1.75rem;
    font-weight: 900;
    color: var(--primary-gold) !important;
}}

.nav {{
    display: flex;
    gap: 2rem;
    align-items: center;
}}

.nav a {{
    color: var(--text-light);
    font-weight: 500;
}}

.phone-header {{
    color: var(--primary-gold) !important;
    font-weight: 700;
    padding: 8px 20px;
    border: 2px solid var(--primary-gold);
    border-radius: 50px;
}}

/* Hero Section */
.hero {{
    background: linear-gradient(135deg, rgba(8,66,152,0.95), rgba(244,162,97,0.95)), url('/images/buck4manage369.jpg') center/cover;
    padding: 120px 20px;
    text-align: center;
    min-height: 500px;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.hero-content {{
    max-width: 1000px;
}}

.hero h1 {{
    color: white !important;
    font-size: 3rem;
    margin-bottom: 1.5rem;
    text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
}}

.hero p {{
    color: white !important;
    font-size: 1.3rem;
    margin-bottom: 2rem;
}}

.cta-buttons {{
    display: flex;
    gap: 20px;
    justify-content: center;
    flex-wrap: wrap;
    margin-top: 2rem;
}}

.btn {{
    display: inline-block;
    padding: 16px 36px;
    border-radius: 50px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    transition: all 0.3s ease;
    text-decoration: none !important;
}}

.btn-primary {{
    background: var(--primary-gold) !important;
    color: var(--background-dark) !important;
    border: 2px solid var(--primary-gold);
}}

.btn-secondary {{
    background: transparent !important;
    color: white !important;
    border: 2px solid white;
}}

/* Promise Section */
.promise-section {{
    background: linear-gradient(135deg, var(--accent-blue), var(--primary-gold));
    padding: 60px 40px;
    border-radius: 20px;
    margin: 60px 0;
}}

.promise-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 25px;
    margin-top: 40px;
}}

.promise-card {{
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(10px);
    padding: 25px;
    border-radius: 12px;
    text-align: center;
    color: white;
}}

/* Service Cards */
.services-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 30px;
    margin: 40px 0;
}}

.service-card {{
    background: var(--primary-navy);
    padding: 35px 30px;
    border-radius: 15px;
    border: 1px solid rgba(244,162,97,0.2);
    transition: all 0.3s ease;
}}

.service-card:hover {{
    transform: translateY(-8px);
    box-shadow: 0 20px 40px rgba(244,162,97,0.25);
}}

.service-card h3 {{
    color: var(--primary-gold) !important;
    margin-bottom: 20px;
}}

.service-card ul {{
    list-style: none;
    padding: 0;
    margin: 20px 0;
}}

.service-card li {{
    padding: 8px 0;
    color: var(--text-light);
    padding-left: 25px;
    position: relative;
}}

.service-card li::before {{
    content: '•';
    position: absolute;
    left: 0;
    color: var(--primary-gold);
    font-weight: bold;
}}

.learn-more {{
    display: inline-block;
    margin-top: 20px;
    background: var(--primary-gold);
    color: var(--background-dark) !important;
    padding: 12px 24px;
    border-radius: 8px;
    font-weight: 600;
    text-align: center;
}}

/* Specialized Services */
.features-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 25px;
    margin: 50px 0;
}}

.feature-item {{
    background: rgba(44,62,80,0.6);
    padding: 30px;
    border-radius: 12px;
    border-left: 4px solid var(--primary-gold);
    text-align: center;
}}

.feature-icon {{
    font-size: 2.5rem;
    margin-bottom: 15px;
}}

/* Trust Section */
.trust-section {{
    background: var(--primary-navy);
    padding: 60px 40px;
    border-radius: 20px;
    margin: 60px 0;
}}

.stats-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 30px;
    margin-top: 40px;
}}

.stat-item {{
    text-align: center;
}}

.stat-icon {{
    font-size: 3rem;
    margin-bottom: 15px;
}}

/* FAQ Section */
.faq-container {{
    max-width: 900px;
    margin: 0 auto;
}}

.faq-item {{
    background: var(--primary-navy);
    padding: 30px;
    margin-bottom: 25px;
    border-radius: 15px;
    border-left: 4px solid var(--primary-gold);
}}

.faq-item h4 {{
    color: var(--primary-gold) !important;
    margin-bottom: 15px;
}}

/* CTA Section */
.cta-section {{
    background: linear-gradient(135deg, var(--primary-gold), #e67e22);
    padding: 80px 40px;
    border-radius: 20px;
    text-align: center;
    margin: 60px 0;
}}

.cta-section h2 {{
    color: var(--background-dark) !important;
    font-size: 2.5rem;
    margin-bottom: 25px;
}}

.cta-section p {{
    color: var(--background-dark) !important;
    font-size: 1.2rem;
}}

/* Contact Form */
.form-section {{
    background: var(--primary-navy);
    padding: 60px 40px;
    border-radius: 20px;
    margin: 60px 0;
}}

.form-container {{
    max-width: 700px;
    margin: 0 auto;
}}

.form-group {{
    margin-bottom: 25px;
}}

.form-group label {{
    display: block;
    color: var(--primary-gold);
    margin-bottom: 10px;
    font-weight: 600;
}}

.form-group input,
.form-group select,
.form-group textarea {{
    width: 100%;
    padding: 15px;
    background: var(--background-dark);
    border: 2px solid transparent;
    border-radius: 10px;
    color: var(--text-light);
}}

.form-submit {{
    background: var(--primary-gold) !important;
    color: var(--background-dark) !important;
    padding: 18px 50px;
    border: none;
    border-radius: 50px;
    font-size: 1.1rem;
    font-weight: 700;
    cursor: pointer;
    width: 100%;
}}

/* Related Areas */
.related-areas {{
    background: var(--primary-navy);
    padding: 40px;
    border-radius: 20px;
    margin: 60px 0;
}}

.area-links {{
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    justify-content: center;
    margin-top: 25px;
}}

.area-link {{
    background: var(--background-dark);
    color: var(--primary-gold) !important;
    padding: 12px 24px;
    border-radius: 8px;
    border: 2px solid var(--primary-gold);
    font-weight: 600;
}}

/* Footer */
footer {{
    background: var(--background-dark);
    color: var(--text-light);
    padding: 60px 20px 30px;
    border-top: 1px solid rgba(244,162,97,0.2);
}}

/* Mobile Responsive */
@media (max-width: 768px) {{
    .promise-grid,
    .services-grid,
    .features-grid,
    .stats-grid {{
        grid-template-columns: 1fr;
    }}

    .hero h1 {{
        font-size: 2rem;
    }}

    .nav {{
        display: none;
    }}
}}
</style>
</head>
<body>

<!-- Header -->
<header class="header">
<div class="header-content">
<a class="logo" href="/">MANAGE369</a>
<nav class="nav">
<a href="/">Home</a>
<a href="/services">Services</a>
<a href="/property-management">Areas</a>
<a href="/contact">Contact</a>
</nav>
<a class="phone-header" href="tel:8478344131">Call (847) 834-4131</a>
</div>
</header>

<!-- Hero Section -->
<section class="hero">
<div class="hero-content">
<h1>{city} Property Management — HOA, Condo & Townhome Experts</h1>
<p>Why {city} Associations Choose Manage369</p>
<div class="cta-buttons">
<a class="btn btn-primary" href="tel:8478344131">Schedule Consultation</a>
<a class="btn btn-secondary" href="/contact">Request Free Proposal</a>
</div>
</div>
</section>

<!-- Main Content -->
<section>
<div class="container">

<!-- Introduction -->
<p style="font-size: 1.2rem; line-height: 1.8; margin-bottom: 2rem;">
{intro}
</p>

<!-- Challenges List -->
<ul style="list-style: none; padding: 0; margin: 40px 0;">
{challenges}
</ul>

<p style="font-size: 1.1rem;">
Since 2007, Manage369 has supported {city} boards with disciplined financials, vendor coordination, and hands-on governance support.
</p>

<!-- Promise Section -->
<div class="promise-section">
<h2 style="color: white !important;">Our Promise to {city} Communities</h2>
<div class="promise-grid">
<div class="promise-card">
<strong style="font-size: 1.2rem;">110% Service Guarantee</strong><br>
<span style="opacity: 0.95;">3 months free if we don't deliver</span>
</div>
<div class="promise-card">
<strong style="font-size: 1.2rem;">60-Day Cancellation</strong><br>
<span style="opacity: 0.95;">No lock-in contracts</span>
</div>
<div class="promise-card">
<strong style="font-size: 1.2rem;">Certified Expertise</strong><br>
<span style="opacity: 0.95;">CAI, IREM, CCIM, IDFPR licensed</span>
</div>
<div class="promise-card">
<strong style="font-size: 1.2rem;">Proven Results</strong><br>
<span style="opacity: 0.95;">50+ associations, 2,400+ units</span>
</div>
<div class="promise-card">
<strong style="font-size: 1.2rem;">24/7 Support</strong><br>
<span style="opacity: 0.95;">Rapid vendor response in {city}</span>
</div>
<div class="promise-card">
<strong style="font-size: 1.2rem;">Local Expertise</strong><br>
<span style="opacity: 0.95;">North Shore specialists since 2007</span>
</div>
</div>
</div>

<!-- Service Cards -->
<div class="services-grid">
<div class="service-card">
<h3>🏢 Condominium Management in {city}</h3>
<p>Expert management for {city}'s diverse condominium communities.</p>
<ul>
<li>Monthly financial reporting</li>
<li>Reserve planning and audits</li>
<li>Vendor and maintenance coordination</li>
<li>Board governance and meeting facilitation</li>
</ul>
<div style="text-align: center;">
<a href="/services/condominium-management" class="learn-more">Learn More</a>
</div>
</div>

<div class="service-card">
<h3>🏘️ HOA Management in {city}</h3>
<p>Protecting lifestyle and property values in {city} neighborhoods.</p>
<ul>
<li>Annual budgets and reserve studies</li>
<li>Board meeting facilitation</li>
<li>Community standards enforcement</li>
<li>24/7 emergency response</li>
</ul>
<div style="text-align: center;">
<a href="/services/hoa-management" class="learn-more">Learn More</a>
</div>
</div>

<div class="service-card">
<h3>🏡 Townhome Management in {city}</h3>
<p>Balancing shared spaces and private ownership in {city}.</p>
<ul>
<li>Exterior and common area upkeep</li>
<li>Insurance and compliance oversight</li>
<li>Maintenance scheduling</li>
<li>Resident communications</li>
</ul>
<div style="text-align: center;">
<a href="/services/townhome-management" class="learn-more">Learn More</a>
</div>
</div>
</div>

<!-- Specialized Services -->
<h2>Specialized Services for {city} Boards</h2>
<div class="features-grid">
<div class="feature-item">
<div class="feature-icon">💰</div>
<strong style="color: var(--primary-gold); font-size: 1.2rem;">Financial Management</strong><br>
<span>Transparent reporting, reserve studies, tax prep</span>
</div>
<div class="feature-item">
<div class="feature-icon">🔧</div>
<strong style="color: var(--primary-gold); font-size: 1.2rem;">Maintenance Coordination</strong><br>
<span>Local contractors, inspections, 24/7 response</span>
</div>
<div class="feature-item">
<div class="feature-icon">📋</div>
<strong style="color: var(--primary-gold); font-size: 1.2rem;">Board Support</strong><br>
<span>Elections, governance, meeting guidance</span>
</div>
<div class="feature-item">
<div class="feature-icon">📊</div>
<strong style="color: var(--primary-gold); font-size: 1.2rem;">Administrative Services</strong><br>
<span>Document compliance and records</span>
</div>
<div class="feature-item">
<div class="feature-icon">🏗️</div>
<strong style="color: var(--primary-gold); font-size: 1.2rem;">Capital Projects</strong><br>
<span>Roof replacements, masonry, large repairs</span>
</div>
<div class="feature-item">
<div class="feature-icon">🤝</div>
<strong style="color: var(--primary-gold); font-size: 1.2rem;">Resident Relations</strong><br>
<span>Communications and issue resolution</span>
</div>
</div>

<!-- Trust Section -->
<div class="trust-section">
<h2 style="color: white !important;">Why Boards in {city} Trust Manage369</h2>
<div class="stats-grid">
<div class="stat-item">
<div class="stat-icon">📈</div>
<strong style="color: var(--primary-gold);">Protecting Property Values</strong><br>
<span style="color: var(--text-light);">Reserve planning for {city}'s market</span>
</div>
<div class="stat-item">
<div class="stat-icon">💬</div>
<strong style="color: var(--primary-gold);">Direct Access</strong><br>
<span style="color: var(--text-light);">Speak directly with principals</span>
</div>
<div class="stat-item">
<div class="stat-icon">💰</div>
<strong style="color: var(--primary-gold);">Reduced Costs</strong><br>
<span style="color: var(--text-light);">Cut expenses by 12-18%</span>
</div>
<div class="stat-item">
<div class="stat-icon">🗺️</div>
<strong style="color: var(--primary-gold);">Local Knowledge</strong><br>
<span style="color: var(--text-light);">{city} codes and vendors</span>
</div>
</div>
</div>

<!-- FAQ Section -->
<h2>Frequently Asked Questions</h2>
<div class="faq-container">
<div class="faq-item">
<h4>Q: What makes property management in {city} unique?</h4>
<p>A: {city}'s specific challenges require specialized financial and maintenance strategies tailored to local needs.</p>
</div>
<div class="faq-item">
<h4>Q: Do you work with local vendors?</h4>
<p>A: Yes — we partner with trusted contractors in {city} for HVAC, roofing, landscaping, and more.</p>
</div>
<div class="faq-item">
<h4>Q: How quickly do you respond to emergencies?</h4>
<p>A: Our 24/7 line connects you to a live manager, with response times in {city} typically under one hour.</p>
</div>
<div class="faq-item">
<h4>Q: Can you help us rebuild reserves?</h4>
<p>A: Absolutely. Manage369 has guided boards in {city} to restore reserves within 12–18 months.</p>
</div>
</div>

<!-- CTA Section -->
<div class="cta-section">
<h2>Your {city} Property Deserves Excellence</h2>
<p>{city} represents more than a neighborhood — it's an investment in community, lifestyle, and long-term property value.</p>
<div class="cta-buttons" style="margin-top: 30px;">
<a href="tel:8478344131" class="btn" style="background: var(--background-dark) !important; color: var(--primary-gold) !important;">
📞 Call (847) 834-4131
</a>
<a href="mailto:service@manage369.com" class="btn" style="background: transparent !important; color: var(--background-dark) !important; border: 2px solid var(--background-dark);">
📧 Email service@manage369.com
</a>
</div>
<p style="margin-top: 30px; font-size: 1.3rem; font-weight: 700; color: var(--background-dark) !important;">
Request Your Free Proposal from Manage369
</p>
<p style="margin-top: 20px; color: var(--background-dark) !important;">
"Manage369 — Where Experience Meets Excellence in {city} Property Management".
</p>
</div>

<!-- Related Areas -->
<div class="related-areas">
<h3 style="text-align: center; margin-bottom: 20px;">Explore Nearby Property Management Services</h3>
<p style="text-align: center; margin-bottom: 30px;">Manage369 proudly serves communities throughout Chicago and the North Shore:</p>
<div class="area-links">
{links}
</div>
<p style="text-align: center; margin-top: 30px;">
<a href="/property-management" style="color: var(--primary-gold); text-decoration: underline; font-size: 1.1rem; font-weight: 600;">
View all 68 service areas
</a>
</p>
</div>

</div>
</section>

<!-- Contact Form Section -->
<section>
<div class="container">
<div class="form-section">
<h2 style="color: var(--primary-gold); text-align: center;">Schedule Your Free {city} Property Management Consultation</h2>
<p style="text-align: center; margin-bottom: 40px;">Discover how our experience can enhance your {city} property.</p>
<form action="https://formspree.io/f/xpznzgnk" method="POST" class="form-container">
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
<option value="other">Other</option>
</select>
</div>
<div class="form-group">
<label for="units">Number of Units</label>
<input type="number" id="units" name="units" placeholder="e.g., 24">
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
<input type="hidden" name="location" value="{city} Property Management Inquiry">
<button type="submit" class="form-submit">Schedule Free Consultation</button>
</form>
</div>
</div>
</section>

<!-- Footer -->
<footer>
<div class="container">
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 40px;">
<div>
<h3 style="color: var(--primary-gold);">MANAGE369</h3>
<p>1400 Patriot Blvd #357<br>Glenview, IL 60026</p>
<p>📱 <a href="tel:8478344131">(847) 834-4131</a><br>
📧 <a href="mailto:service@manage369.com">service@manage369.com</a></p>
</div>
<div>
<h4 style="color: var(--primary-gold);">Services</h4>
<a href="/services/condominium-management" style="display: block; margin: 5px 0;">Condominium Management</a>
<a href="/services/hoa-management" style="display: block; margin: 5px 0;">HOA Management</a>
<a href="/services/townhome-management" style="display: block; margin: 5px 0;">Townhome Management</a>
</div>
<div>
<h4 style="color: var(--primary-gold);">Quick Links</h4>
<a href="/property-management" style="display: block; margin: 5px 0;">Areas We Serve</a>
<a href="/contact" style="display: block; margin: 5px 0;">Contact</a>
<a href="/pay-dues" style="display: block; margin: 5px 0;">Pay Dues</a>
</div>
<div>
<h4 style="color: var(--primary-gold);">Certifications</h4>
<p>CAI National Member<br>
AMS • CMCA<br>
IDFPR Licensed<br>
License: 291.000211</p>
</div>
</div>
<p style="text-align: center; margin-top: 40px; padding-top: 30px; border-top: 1px solid rgba(244,162,97,0.2);">
© 2025 Manage369. All rights reserved.
</p>
</div>
</footer>

</body>
</html>'''

    return template

# Data for all 10 areas
areas = [
    {
        'city': 'Glenview',
        'slug': 'glenview',
        'intro': "Glenview blends family-friendly neighborhoods, strong schools, and a thriving commercial corridor along Waukegan Road. Associations here often deal with:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Mixed property types — from luxury condos near The Glen to large single-family HOAs</li>
<li style="padding: 10px 0; color: var(--text-light);">• Aging infrastructure in mid-century townhome communities</li>
<li style="padding: 10px 0; color: var(--text-light);">• Stormwater management issues due to flood-prone zones</li>
<li style="padding: 10px 0; color: var(--text-light);">• Board turnover in diverse, fast-growing neighborhoods</li>''',
        'links': '''<a href="../northbrook" class="area-link">Northbrook</a>
<a href="../skokie" class="area-link">Skokie</a>
<a href="../wilmette" class="area-link">Wilmette</a>'''
    },
    {
        'city': 'Northbrook',
        'slug': 'northbrook',
        'intro': "Northbrook's combination of high-value homes, corporate campuses, and retail centers creates unique pressures for associations:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Luxury condominiums near Northbrook Court with demanding maintenance needs</li>
<li style="padding: 10px 0; color: var(--text-light);">• HOAs facing heavy snow management costs in winter</li>
<li style="padding: 10px 0; color: var(--text-light);">• Large-scale roofing and paving projects in aging townhome communities</li>
<li style="padding: 10px 0; color: var(--text-light);">• Boards requiring sophisticated financial reporting to manage reserves</li>''',
        'links': '''<a href="../glenview" class="area-link">Glenview</a>
<a href="../deerfield" class="area-link">Deerfield</a>
<a href="../lincolnwood" class="area-link">Lincolnwood</a>'''
    },
    {
        'city': 'Wilmette',
        'slug': 'wilmette',
        'intro': "Wilmette is known for its historic lakefront homes, thriving downtown, and proximity to Northwestern University. Local challenges include:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Historic building preservation in east Wilmette</li>
<li style="padding: 10px 0; color: var(--text-light);">• HOAs balancing lakefront erosion and stormwater issues</li>
<li style="padding: 10px 0; color: var(--text-light);">• Townhome communities near Green Bay Road dealing with traffic & parking</li>
<li style="padding: 10px 0; color: var(--text-light);">• Boards needing financial expertise for multimillion-dollar reserves</li>''',
        'links': '''<a href="../evanston" class="area-link">Evanston</a>
<a href="../winnetka" class="area-link">Winnetka</a>
<a href="../skokie" class="area-link">Skokie</a>'''
    },
    {
        'city': 'Evanston',
        'slug': 'evanston',
        'intro': "Evanston combines university life, lakefront condos, and diverse housing. Boards here often face:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Condo subleasing issues near Northwestern University</li>
<li style="padding: 10px 0; color: var(--text-light);">• Noise and parking complaints in dense downtown developments</li>
<li style="padding: 10px 0; color: var(--text-light);">• Older elevator buildings needing capital project oversight</li>
<li style="padding: 10px 0; color: var(--text-light);">• HOAs navigating compliance with Chicago-adjacent ordinances</li>''',
        'links': '''<a href="../wilmette" class="area-link">Wilmette</a>
<a href="../skokie" class="area-link">Skokie</a>
<a href="../chicago" class="area-link">Rogers Park</a>'''
    },
    {
        'city': 'Skokie',
        'slug': 'skokie',
        'intro': "Skokie offers a mix of cultural diversity, older buildings, and newer developments near Westfield Old Orchard. Local challenges include:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Garden-style condos from the 1960s–70s requiring frequent maintenance</li>
<li style="padding: 10px 0; color: var(--text-light);">• Townhome communities facing rising utility and vendor costs</li>
<li style="padding: 10px 0; color: var(--text-light);">• Boards struggling with delinquencies in mixed-income properties</li>
<li style="padding: 10px 0; color: var(--text-light);">• Aging HVAC and plumbing systems needing professional oversight</li>''',
        'links': '''<a href="../lincolnwood" class="area-link">Lincolnwood</a>
<a href="../evanston" class="area-link">Evanston</a>
<a href="../niles" class="area-link">Niles</a>'''
    },
    {
        'city': 'Highland Park',
        'slug': 'highland-park',
        'intro': "Highland Park combines lakefront estates with active HOAs in residential neighborhoods. Challenges include:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Lakefront erosion management for associations along Sheridan Road</li>
<li style="padding: 10px 0; color: var(--text-light);">• Large-scale reserve studies for aging communities</li>
<li style="padding: 10px 0; color: var(--text-light);">• Townhome boards managing stormwater basins and green space</li>
<li style="padding: 10px 0; color: var(--text-light);">• Affluent residents expecting premium communication and reporting</li>''',
        'links': '''<a href="../highwood" class="area-link">Highwood</a>
<a href="../lake-forest" class="area-link">Lake Forest</a>
<a href="../deerfield" class="area-link">Deerfield</a>'''
    },
    {
        'city': 'Lake Forest',
        'slug': 'lake-forest',
        'intro': "Lake Forest is known for its estates, gated HOAs, and exclusive townhome developments. Associations often deal with:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Historic preservation requirements for older homes</li>
<li style="padding: 10px 0; color: var(--text-light);">• Large common areas requiring landscaping and vendor oversight</li>
<li style="padding: 10px 0; color: var(--text-light);">• High operating costs that demand disciplined budgeting</li>
<li style="padding: 10px 0; color: var(--text-light);">• Exclusive resident expectations for responsiveness and privacy</li>''',
        'links': '''<a href="../lake-bluff" class="area-link">Lake Bluff</a>
<a href="../highland-park" class="area-link">Highland Park</a>
<a href="../glenview" class="area-link">Glenview</a>'''
    },
    {
        'city': 'Lincolnwood',
        'slug': 'lincolnwood',
        'intro': "Lincolnwood combines suburban HOAs with older condo buildings near Touhy Avenue. Boards here face:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Deferred maintenance in mid-century condominiums</li>
<li style="padding: 10px 0; color: var(--text-light);">• HOAs managing shared amenities like pools & clubhouses</li>
<li style="padding: 10px 0; color: var(--text-light);">• Parking and snow removal costs straining budgets</li>
<li style="padding: 10px 0; color: var(--text-light);">• Boards requiring strict financial reporting</li>''',
        'links': '''<a href="../skokie" class="area-link">Skokie</a>
<a href="../niles" class="area-link">Niles</a>
<a href="../morton-grove" class="area-link">Morton Grove</a>'''
    },
    {
        'city': 'Deerfield',
        'slug': 'deerfield',
        'intro': "Deerfield is a family-oriented suburb with both luxury HOAs and older townhomes. Common challenges include:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Townhome roofing and siding replacements</li>
<li style="padding: 10px 0; color: var(--text-light);">• HOAs managing stormwater and common green space</li>
<li style="padding: 10px 0; color: var(--text-light);">• Boards planning reserves for capital projects</li>
<li style="padding: 10px 0; color: var(--text-light);">• Condo associations balancing rising vendor costs</li>''',
        'links': '''<a href="../northbrook" class="area-link">Northbrook</a>
<a href="../highland-park" class="area-link">Highland Park</a>
<a href="../riverwoods" class="area-link">Riverwoods</a>'''
    },
    {
        'city': 'Glencoe',
        'slug': 'glencoe',
        'intro': "Glencoe's lakefront location and historic charm create unique management challenges for associations:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Lakefront erosion threatening property foundations and common areas</li>
<li style="padding: 10px 0; color: var(--text-light);">• Luxury HOA budgets requiring sophisticated financial management</li>
<li style="padding: 10px 0; color: var(--text-light);">• Historic district preservation requirements affecting renovations</li>
<li style="padding: 10px 0; color: var(--text-light);">• Boards balancing modern amenities with architectural integrity</li>''',
        'links': '''<a href="../winnetka" class="area-link">Winnetka</a>
<a href="../highland-park" class="area-link">Highland Park</a>
<a href="../wilmette" class="area-link">Wilmette</a>'''
    },
    {
        'city': 'Kenilworth',
        'slug': 'kenilworth',
        'intro': "Kenilworth's exclusive community demands the highest standards in property management:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Exclusive HOA boards requiring discreet professional management</li>
<li style="padding: 10px 0; color: var(--text-light);">• High-value homes exceeding $3M demanding premium services</li>
<li style="padding: 10px 0; color: var(--text-light);">• Strict architectural standards requiring meticulous oversight</li>
<li style="padding: 10px 0; color: var(--text-light);">• Boards expecting exceptional vendor vetting and supervision</li>''',
        'links': '''<a href="../winnetka" class="area-link">Winnetka</a>
<a href="../wilmette" class="area-link">Wilmette</a>
<a href="../glencoe" class="area-link">Glencoe</a>'''
    },
    {
        'city': 'Lake Bluff',
        'slug': 'lake-bluff',
        'intro': "Lake Bluff combines lakefront beauty with community challenges that require experienced management:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• HOA reserves planning for shoreline erosion protection</li>
<li style="padding: 10px 0; color: var(--text-light);">• Snow removal costs straining winter maintenance budgets</li>
<li style="padding: 10px 0; color: var(--text-light);">• Mid-size condo communities requiring balanced financial planning</li>
<li style="padding: 10px 0; color: var(--text-light);">• Boards managing aging infrastructure and capital improvements</li>''',
        'links': '''<a href="../lake-forest" class="area-link">Lake Forest</a>
<a href="../highland-park" class="area-link">Highland Park</a>
<a href="../libertyville" class="area-link">Libertyville</a>'''
    },
    {
        'city': 'Morton Grove',
        'slug': 'morton-grove',
        'intro': "Morton Grove's diverse housing stock presents unique management opportunities:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Older condo buildings requiring frequent maintenance coordination</li>
<li style="padding: 10px 0; color: var(--text-light);">• Budget-conscious HOAs needing cost-effective solutions</li>
<li style="padding: 10px 0; color: var(--text-light);">• Stormwater drainage projects requiring professional oversight</li>
<li style="padding: 10px 0; color: var(--text-light);">• Boards balancing affordability with necessary improvements</li>''',
        'links': '''<a href="../skokie" class="area-link">Skokie</a>
<a href="../niles" class="area-link">Niles</a>
<a href="../lincolnwood" class="area-link">Lincolnwood</a>'''
    },
    {
        'city': 'Niles',
        'slug': 'niles',
        'intro': "Niles features established communities with infrastructure that demands proactive management:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Aging infrastructure requiring strategic capital planning</li>
<li style="padding: 10px 0; color: var(--text-light);">• Multi-building condo associations needing coordinated management</li>
<li style="padding: 10px 0; color: var(--text-light);">• Snow removal costs impacting winter budget planning</li>
<li style="padding: 10px 0; color: var(--text-light);">• Boards seeking professional guidance for major renovations</li>''',
        'links': '''<a href="../morton-grove" class="area-link">Morton Grove</a>
<a href="../skokie" class="area-link">Skokie</a>
<a href="../park-ridge" class="area-link">Park Ridge</a>'''
    },
    {
        'city': 'Riverwoods',
        'slug': 'riverwoods',
        'intro': "Riverwoods' wooded setting and privacy create distinct management needs:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Gated HOA management requiring specialized security coordination</li>
<li style="padding: 10px 0; color: var(--text-light);">• Stormwater basin maintenance in natural settings</li>
<li style="padding: 10px 0; color: var(--text-light);">• Wooded property upkeep balancing nature and safety</li>
<li style="padding: 10px 0; color: var(--text-light);">• Boards managing private roads and infrastructure</li>''',
        'links': '''<a href="../deerfield" class="area-link">Deerfield</a>
<a href="../lincolnshire" class="area-link">Lincolnshire</a>
<a href="../buffalo-grove" class="area-link">Buffalo Grove</a>'''
    },
    {
        'city': 'Northfield',
        'slug': 'northfield',
        'intro': "Northfield's small luxury HOAs require personalized professional management:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Small luxury HOAs demanding personalized attention</li>
<li style="padding: 10px 0; color: var(--text-light);">• Townhome maintenance reserves requiring careful planning</li>
<li style="padding: 10px 0; color: var(--text-light);">• Older private roads needing assessment and repairs</li>
<li style="padding: 10px 0; color: var(--text-light);">• Boards expecting boutique-level management services</li>''',
        'links': '''<a href="../winnetka" class="area-link">Winnetka</a>
<a href="../glenview" class="area-link">Glenview</a>
<a href="../northbrook" class="area-link">Northbrook</a>'''
    },
    {
        'city': 'Wheeling',
        'slug': 'wheeling',
        'intro': "Wheeling's diverse housing mix creates varied management requirements:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Mid-rise condos near Milwaukee Ave requiring elevator maintenance</li>
<li style="padding: 10px 0; color: var(--text-light);">• Affordable townhomes with tight budgets needing efficiency</li>
<li style="padding: 10px 0; color: var(--text-light);">• Delinquency reduction strategies for mixed-income properties</li>
<li style="padding: 10px 0; color: var(--text-light);">• Boards seeking cost-effective vendor management</li>''',
        'links': '''<a href="../buffalo-grove" class="area-link">Buffalo Grove</a>
<a href="../prospect-heights" class="area-link">Prospect Heights</a>
<a href="../northbrook" class="area-link">Northbrook</a>'''
    },
    {
        'city': 'Vernon Hills',
        'slug': 'vernon-hills',
        'intro': "Vernon Hills' master-planned communities require comprehensive management expertise:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Master-planned HOAs with complex governance structures</li>
<li style="padding: 10px 0; color: var(--text-light);">• Large townhome developments requiring coordinated maintenance</li>
<li style="padding: 10px 0; color: var(--text-light);">• Reserve planning for capital projects and amenities</li>
<li style="padding: 10px 0; color: var(--text-light);">• Boards managing multiple vendor relationships efficiently</li>''',
        'links': '''<a href="../libertyville" class="area-link">Libertyville</a>
<a href="../mundelein" class="area-link">Mundelein</a>
<a href="../lincolnshire" class="area-link">Lincolnshire</a>'''
    },
    {
        'city': 'Libertyville',
        'slug': 'libertyville',
        'intro': "Libertyville blends historic charm with modern development challenges:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Historic downtown condos requiring specialized maintenance</li>
<li style="padding: 10px 0; color: var(--text-light);">• Newer suburban HOAs balancing growth with services</li>
<li style="padding: 10px 0; color: var(--text-light);">• Reserve studies for stormwater retention infrastructure</li>
<li style="padding: 10px 0; color: var(--text-light);">• Boards navigating mixed-use development complexities</li>''',
        'links': '''<a href="../lake-bluff" class="area-link">Lake Bluff</a>
<a href="../vernon-hills" class="area-link">Vernon Hills</a>
<a href="../mundelein" class="area-link">Mundelein</a>'''
    },
    {
        'city': 'Mundelein',
        'slug': 'mundelein',
        'intro': "Mundelein offers a blend of newer subdivisions and older townhome communities. Boards here face:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Large townhome HOAs with significant reserve needs</li>
<li style="padding: 10px 0; color: var(--text-light);">• Older condo infrastructure requiring capital projects</li>
<li style="padding: 10px 0; color: var(--text-light);">• Budget-conscious boards balancing rising vendor costs</li>
<li style="padding: 10px 0; color: var(--text-light);">• Residents expecting fast communication and transparency</li>''',
        'links': '''<a href="../vernon-hills" class="area-link">Vernon Hills</a>
<a href="../libertyville" class="area-link">Libertyville</a>
<a href="../hawthorn-woods" class="area-link">Hawthorn Woods</a>'''
    },
    {
        'city': 'Long Grove',
        'slug': 'long-grove',
        'intro': "Long Grove is known for its gated communities and estate-style properties. Challenges include:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Private roads and infrastructure requiring HOA management</li>
<li style="padding: 10px 0; color: var(--text-light);">• Large reserve studies for capital projects</li>
<li style="padding: 10px 0; color: var(--text-light);">• Stormwater basin maintenance in natural settings</li>
<li style="padding: 10px 0; color: var(--text-light);">• Boards serving affluent residents with high expectations</li>''',
        'links': '''<a href="../buffalo-grove" class="area-link">Buffalo Grove</a>
<a href="../kildeer" class="area-link">Kildeer</a>
<a href="../hawthorn-woods" class="area-link">Hawthorn Woods</a>'''
    },
    {
        'city': 'Hawthorn Woods',
        'slug': 'hawthorn-woods',
        'intro': "Hawthorn Woods is home to golf course communities and family-focused HOAs. Boards often manage:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• HOAs with large common areas including ponds and trails</li>
<li style="padding: 10px 0; color: var(--text-light);">• Reserve planning for amenities like pools and clubhouses</li>
<li style="padding: 10px 0; color: var(--text-light);">• Capital projects for roofs, siding, and paving</li>
<li style="padding: 10px 0; color: var(--text-light);">• Boards needing transparency to maintain resident trust</li>''',
        'links': '''<a href="../long-grove" class="area-link">Long Grove</a>
<a href="../lake-zurich" class="area-link">Lake Zurich</a>
<a href="../mundelein" class="area-link">Mundelein</a>'''
    },
    {
        'city': 'Lake Zurich',
        'slug': 'lake-zurich',
        'intro': "Lake Zurich combines lakefront living with large suburban HOAs. Common challenges include:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Stormwater and shoreline management for lakefront properties</li>
<li style="padding: 10px 0; color: var(--text-light);">• Townhome communities needing reserve planning</li>
<li style="padding: 10px 0; color: var(--text-light);">• HOAs balancing budgets with rising utility costs</li>
<li style="padding: 10px 0; color: var(--text-light);">• Residents demanding digital tools for communication</li>''',
        'links': '''<a href="../hawthorn-woods" class="area-link">Hawthorn Woods</a>
<a href="../kildeer" class="area-link">Kildeer</a>
<a href="../buffalo-grove" class="area-link">Buffalo Grove</a>'''
    },
    {
        'city': 'Kildeer',
        'slug': 'kildeer',
        'intro': "Kildeer features estate-style HOAs and townhome communities with significant common areas. Boards manage:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Stormwater retention ponds requiring maintenance</li>
<li style="padding: 10px 0; color: var(--text-light);">• Large landscaping contracts needing oversight</li>
<li style="padding: 10px 0; color: var(--text-light);">• Capital projects for private roads</li>
<li style="padding: 10px 0; color: var(--text-light);">• High-value homes needing disciplined reserve planning</li>''',
        'links': '''<a href="../long-grove" class="area-link">Long Grove</a>
<a href="../lake-zurich" class="area-link">Lake Zurich</a>
<a href="../deer-park" class="area-link">Deer Park</a>'''
    },
    {
        'city': 'Deer Park',
        'slug': 'deer-park',
        'intro': "Deer Park offers a mix of luxury subdivisions and townhome communities. Boards face:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Private infrastructure maintenance (roads, signage, landscaping)</li>
<li style="padding: 10px 0; color: var(--text-light);">• Budget planning for mid-size HOAs</li>
<li style="padding: 10px 0; color: var(--text-light);">• Reserve studies for townhome communities</li>
<li style="padding: 10px 0; color: var(--text-light);">• Residents expecting responsive, professional service</li>''',
        'links': '''<a href="../kildeer" class="area-link">Kildeer</a>
<a href="../long-grove" class="area-link">Long Grove</a>
<a href="../palatine" class="area-link">Palatine</a>'''
    },
    {
        'city': 'Palatine',
        'slug': 'palatine',
        'intro': "Palatine is one of the largest suburbs, with a wide range of HOAs and condos. Local challenges include:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Large condo complexes needing strict financial management</li>
<li style="padding: 10px 0; color: var(--text-light);">• Townhome boards balancing reserves and vendor costs</li>
<li style="padding: 10px 0; color: var(--text-light);">• Older buildings requiring HVAC and roof replacements</li>
<li style="padding: 10px 0; color: var(--text-light);">• Residents expecting professional digital communication</li>''',
        'links': '''<a href="../arlington-heights" class="area-link">Arlington Heights</a>
<a href="../hoffman-estates" class="area-link">Hoffman Estates</a>
<a href="../deer-park" class="area-link">Deer Park</a>'''
    },
    {
        'city': 'Arlington Heights',
        'slug': 'arlington-heights',
        'intro': "Arlington Heights combines urban-style condos with suburban HOAs. Boards often deal with:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Downtown condo developments with high resident turnover</li>
<li style="padding: 10px 0; color: var(--text-light);">• Large-scale HOAs requiring governance and compliance support</li>
<li style="padding: 10px 0; color: var(--text-light);">• Budgeting for shared amenities like pools and clubhouses</li>
<li style="padding: 10px 0; color: var(--text-light);">• Capital projects in older townhome associations</li>''',
        'links': '''<a href="../palatine" class="area-link">Palatine</a>
<a href="../mount-prospect" class="area-link">Mount Prospect</a>
<a href="../rolling-meadows" class="area-link">Rolling Meadows</a>'''
    },
    {
        'city': 'Mount Prospect',
        'slug': 'mount-prospect',
        'intro': "Mount Prospect features both affordable condo buildings and upscale HOAs. Challenges include:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Older condo associations with deferred maintenance</li>
<li style="padding: 10px 0; color: var(--text-light);">• HOAs requiring strong vendor coordination</li>
<li style="padding: 10px 0; color: var(--text-light);">• Parking and snow removal costs straining budgets</li>
<li style="padding: 10px 0; color: var(--text-light);">• Boards needing transparent financial reporting</li>''',
        'links': '''<a href="../arlington-heights" class="area-link">Arlington Heights</a>
<a href="../des-plaines" class="area-link">Des Plaines</a>
<a href="../prospect-heights" class="area-link">Prospect Heights</a>'''
    },
    {
        'city': 'Rolling Meadows',
        'slug': 'rolling-meadows',
        'intro': "Rolling Meadows is home to diverse communities, from older condos to newer townhomes. Boards here face:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Budget-conscious HOAs balancing rising costs</li>
<li style="padding: 10px 0; color: var(--text-light);">• Deferred maintenance in aging condo buildings</li>
<li style="padding: 10px 0; color: var(--text-light);">• Townhome communities needing reserve studies</li>
<li style="padding: 10px 0; color: var(--text-light);">• Residents expecting clear communication</li>''',
        'links': '''<a href="../palatine" class="area-link">Palatine</a>
<a href="../arlington-heights" class="area-link">Arlington Heights</a>
<a href="../schaumburg" class="area-link">Schaumburg</a>'''
    },
    {
        'city': 'Schaumburg',
        'slug': 'schaumburg',
        'intro': "Schaumburg is a major hub with large condo complexes, master-planned HOAs, and townhomes near Woodfield Mall. Boards here often face:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• High-rise condo maintenance with elevators and shared systems</li>
<li style="padding: 10px 0; color: var(--text-light);">• HOAs managing pools, clubhouses, and fitness centers</li>
<li style="padding: 10px 0; color: var(--text-light);">• Large reserve planning for capital projects</li>
<li style="padding: 10px 0; color: var(--text-light);">• Budgeting challenges in communities with hundreds of units</li>''',
        'links': '''<a href="../rolling-meadows" class="area-link">Rolling Meadows</a>
<a href="../hoffman-estates" class="area-link">Hoffman Estates</a>
<a href="../roselle" class="area-link">Roselle</a>'''
    },
    {
        'city': 'Hoffman Estates',
        'slug': 'hoffman-estates',
        'intro': "Hoffman Estates features suburban HOAs, condo associations, and newer developments. Boards must handle:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Large reserves for roofing and paving projects</li>
<li style="padding: 10px 0; color: var(--text-light);">• Snow removal and landscaping across big communities</li>
<li style="padding: 10px 0; color: var(--text-light);">• HOAs balancing amenity upkeep with budgets</li>
<li style="padding: 10px 0; color: var(--text-light);">• Residents expecting fast response times</li>''',
        'links': '''<a href="../schaumburg" class="area-link">Schaumburg</a>
<a href="../palatine" class="area-link">Palatine</a>
<a href="../streamwood" class="area-link">Streamwood</a>'''
    },
    {
        'city': 'Streamwood',
        'slug': 'streamwood',
        'intro': "Streamwood is home to affordable condos and mid-size HOAs. Local challenges include:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Older condo buildings with deferred maintenance</li>
<li style="padding: 10px 0; color: var(--text-light);">• Boards needing delinquency reduction strategies</li>
<li style="padding: 10px 0; color: var(--text-light);">• Stormwater management for low-lying areas</li>
<li style="padding: 10px 0; color: var(--text-light);">• Tight budgets in cost-sensitive associations</li>''',
        'links': '''<a href="../hoffman-estates" class="area-link">Hoffman Estates</a>
<a href="../elgin" class="area-link">Elgin</a>
<a href="../hanover-park" class="area-link">Hanover Park</a>'''
    },
    {
        'city': 'Elgin',
        'slug': 'elgin',
        'intro': "Elgin blends historic neighborhoods with large condo developments. Boards often manage:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Historic building preservation in downtown districts</li>
<li style="padding: 10px 0; color: var(--text-light);">• Townhome reserves for siding and roof replacements</li>
<li style="padding: 10px 0; color: var(--text-light);">• HOAs with large common grounds requiring landscaping contracts</li>
<li style="padding: 10px 0; color: var(--text-light);">• Residents expecting bilingual communication</li>''',
        'links': '''<a href="../streamwood" class="area-link">Streamwood</a>
<a href="../south-elgin" class="area-link">South Elgin</a>
<a href="../bartlett" class="area-link">Bartlett</a>'''
    },
    {
        'city': 'Hanover Park',
        'slug': 'hanover-park',
        'intro': "Hanover Park is a diverse suburb with many mid-size associations. Local challenges include:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Older condo HVAC and plumbing systems</li>
<li style="padding: 10px 0; color: var(--text-light);">• Boards needing strict financial controls</li>
<li style="padding: 10px 0; color: var(--text-light);">• HOAs balancing rising vendor costs</li>
<li style="padding: 10px 0; color: var(--text-light);">• Residents expecting clear board communication</li>''',
        'links': '''<a href="../streamwood" class="area-link">Streamwood</a>
<a href="../schaumburg" class="area-link">Schaumburg</a>
<a href="../bartlett" class="area-link">Bartlett</a>'''
    },
    {
        'city': 'Bartlett',
        'slug': 'bartlett',
        'intro': "Bartlett offers a mix of townhome associations and suburban HOAs. Boards often deal with:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Reserve planning for large townhome complexes</li>
<li style="padding: 10px 0; color: var(--text-light);">• Shared amenities like pools and playgrounds</li>
<li style="padding: 10px 0; color: var(--text-light);">• Snow removal costs during long winters</li>
<li style="padding: 10px 0; color: var(--text-light);">• Residents expecting consistent board communication</li>''',
        'links': '''<a href="../hanover-park" class="area-link">Hanover Park</a>
<a href="../elgin" class="area-link">Elgin</a>
<a href="../wayne" class="area-link">Wayne</a>'''
    },
    {
        'city': 'Des Plaines',
        'slug': 'des-plaines',
        'intro': "Des Plaines is home to high-density condos and suburban HOAs. Boards must manage:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Mid-rise condo associations with elevators and shared utilities</li>
<li style="padding: 10px 0; color: var(--text-light);">• Parking and stormwater drainage issues</li>
<li style="padding: 10px 0; color: var(--text-light);">• Townhome capital projects for roofing and paving</li>
<li style="padding: 10px 0; color: var(--text-light);">• Residents expecting professional service and transparency</li>''',
        'links': '''<a href="../mount-prospect" class="area-link">Mount Prospect</a>
<a href="../park-ridge" class="area-link">Park Ridge</a>
<a href="../rosemont" class="area-link">Rosemont</a>'''
    },
    {
        'city': 'Park Ridge',
        'slug': 'park-ridge',
        'intro': "Park Ridge combines historic architecture with upscale HOAs. Local challenges include:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Historic preservation in downtown condos</li>
<li style="padding: 10px 0; color: var(--text-light);">• HOA reserves for luxury amenities</li>
<li style="padding: 10px 0; color: var(--text-light);">• Snow removal and landscaping contracts</li>
<li style="padding: 10px 0; color: var(--text-light);">• Boards requiring detailed financial reporting</li>''',
        'links': '''<a href="../des-plaines" class="area-link">Des Plaines</a>
<a href="../niles" class="area-link">Niles</a>
<a href="../edison-park" class="area-link">Edison Park</a>'''
    },
    {
        'city': 'Prospect Heights',
        'slug': 'prospect-heights',
        'intro': "Prospect Heights has diverse housing, from affordable condos to upscale townhomes. Boards face:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Older condo systems needing frequent repairs</li>
<li style="padding: 10px 0; color: var(--text-light);">• Townhome boards balancing reserve planning</li>
<li style="padding: 10px 0; color: var(--text-light);">• Parking and compliance enforcement</li>
<li style="padding: 10px 0; color: var(--text-light);">• Residents expecting prompt maintenance response</li>''',
        'links': '''<a href="../wheeling" class="area-link">Wheeling</a>
<a href="../mount-prospect" class="area-link">Mount Prospect</a>
<a href="../arlington-heights" class="area-link">Arlington Heights</a>'''
    },
    {
        'city': 'Rosemont',
        'slug': 'rosemont',
        'intro': "Rosemont combines residential communities with a busy commercial and entertainment district. Boards here face:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• High operating costs due to location</li>
<li style="padding: 10px 0; color: var(--text-light);">• Noise and parking complaints in mixed-use developments</li>
<li style="padding: 10px 0; color: var(--text-light);">• Small HOAs needing strong governance</li>
<li style="padding: 10px 0; color: var(--text-light);">• Boards expecting professional financial oversight</li>''',
        'links': '''<a href="../des-plaines" class="area-link">Des Plaines</a>
<a href="../park-ridge" class="area-link">Park Ridge</a>
<a href="../schiller-park" class="area-link">Schiller Park</a>'''
    },
    {
        'city': 'Oak Brook',
        'slug': 'oak-brook',
        'intro': "Oak Brook is known for luxury gated communities, golf course estates, and corporate centers. Boards here face:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• High-value reserves for multimillion-dollar properties</li>
<li style="padding: 10px 0; color: var(--text-light);">• HOAs with golf course & clubhouse amenities</li>
<li style="padding: 10px 0; color: var(--text-light);">• Private infrastructure maintenance including roads and gates</li>
<li style="padding: 10px 0; color: var(--text-light);">• Residents expecting board transparency and discretion</li>''',
        'links': '''<a href="../hinsdale" class="area-link">Hinsdale</a>
<a href="../elmhurst" class="area-link">Elmhurst</a>
<a href="../downers-grove" class="area-link">Downers Grove</a>'''
    },
    {
        'city': 'Hinsdale',
        'slug': 'hinsdale',
        'intro': "Hinsdale offers historic homes, luxury townhomes, and exclusive HOAs. Local challenges include:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Preservation of historic architecture</li>
<li style="padding: 10px 0; color: var(--text-light);">• HOA reserve studies for high-value projects</li>
<li style="padding: 10px 0; color: var(--text-light);">• Snow removal & landscaping costs in large communities</li>
<li style="padding: 10px 0; color: var(--text-light);">• Affluent residents expecting rapid communication</li>''',
        'links': '''<a href="../oak-brook" class="area-link">Oak Brook</a>
<a href="../clarendon-hills" class="area-link">Clarendon Hills</a>
<a href="../western-springs" class="area-link">Western Springs</a>'''
    },
    {
        'city': 'Elmhurst',
        'slug': 'elmhurst',
        'intro': "Elmhurst combines a vibrant downtown with family-oriented HOAs. Boards here must handle:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Condo associations in mixed-use developments</li>
<li style="padding: 10px 0; color: var(--text-light);">• Townhome reserves for roofing & siding projects</li>
<li style="padding: 10px 0; color: var(--text-light);">• HOAs managing playgrounds and pools</li>
<li style="padding: 10px 0; color: var(--text-light);">• Boards requiring financial transparency</li>''',
        'links': '''<a href="../oak-brook" class="area-link">Oak Brook</a>
<a href="../villa-park" class="area-link">Villa Park</a>
<a href="../lombard" class="area-link">Lombard</a>'''
    },
    {
        'city': 'Downers Grove',
        'slug': 'downers-grove',
        'intro': "Downers Grove has a mix of historic neighborhoods and large HOAs. Boards here face:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Aging condo infrastructure needing capital projects</li>
<li style="padding: 10px 0; color: var(--text-light);">• Townhome reserve planning for exterior replacements</li>
<li style="padding: 10px 0; color: var(--text-light);">• HOAs balancing amenity costs like pools and green space</li>
<li style="padding: 10px 0; color: var(--text-light);">• Residents expecting consistent communication</li>''',
        'links': '''<a href="../oak-brook" class="area-link">Oak Brook</a>
<a href="../lombard" class="area-link">Lombard</a>
<a href="../westmont" class="area-link">Westmont</a>'''
    },
    {
        'city': 'Lombard',
        'slug': 'lombard',
        'intro': "Lombard, 'the Lilac Village,' blends historic properties with suburban HOAs. Challenges include:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Older garden-style condos requiring frequent repairs</li>
<li style="padding: 10px 0; color: var(--text-light);">• HOAs with tight budgets</li>
<li style="padding: 10px 0; color: var(--text-light);">• Stormwater management for low-lying areas</li>
<li style="padding: 10px 0; color: var(--text-light);">• Boards requiring hands-on governance</li>''',
        'links': '''<a href="../elmhurst" class="area-link">Elmhurst</a>
<a href="../downers-grove" class="area-link">Downers Grove</a>
<a href="../villa-park" class="area-link">Villa Park</a>'''
    },
    {
        'city': 'Villa Park',
        'slug': 'villa-park',
        'intro': "Villa Park offers affordable condos and mid-sized HOAs. Boards often manage:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Deferred maintenance in aging condos</li>
<li style="padding: 10px 0; color: var(--text-light);">• Townhome reserves for exterior upkeep</li>
<li style="padding: 10px 0; color: var(--text-light);">• Budget challenges in cost-sensitive communities</li>
<li style="padding: 10px 0; color: var(--text-light);">• Residents expecting clear communication</li>''',
        'links': '''<a href="../elmhurst" class="area-link">Elmhurst</a>
<a href="../lombard" class="area-link">Lombard</a>
<a href="../addison" class="area-link">Addison</a>'''
    },
    {
        'city': 'Addison',
        'slug': 'addison',
        'intro': "Addison is home to diverse condos, townhomes, and small HOAs. Boards here face:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Older infrastructure in condo associations</li>
<li style="padding: 10px 0; color: var(--text-light);">• HOAs balancing snow removal and landscaping costs</li>
<li style="padding: 10px 0; color: var(--text-light);">• Capital projects for roofing & paving</li>
<li style="padding: 10px 0; color: var(--text-light);">• Boards needing strong financial planning</li>''',
        'links': '''<a href="../villa-park" class="area-link">Villa Park</a>
<a href="../elmhurst" class="area-link">Elmhurst</a>
<a href="../wood-dale" class="area-link">Wood Dale</a>'''
    },
    {
        'city': 'Wood Dale',
        'slug': 'wood-dale',
        'intro': "Wood Dale blends residential neighborhoods with condo and townhome associations. Challenges include:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Proximity to O'Hare leading to noise concerns in condos</li>
<li style="padding: 10px 0; color: var(--text-light);">• Townhome communities with shared amenities</li>
<li style="padding: 10px 0; color: var(--text-light);">• Reserve studies for capital projects</li>
<li style="padding: 10px 0; color: var(--text-light);">• Boards needing professional financial oversight</li>''',
        'links': '''<a href="../addison" class="area-link">Addison</a>
<a href="../itasca" class="area-link">Itasca</a>
<a href="../bensenville" class="area-link">Bensenville</a>'''
    },
    {
        'city': 'Bensenville',
        'slug': 'bensenville',
        'intro': "Bensenville combines affordable housing with suburban HOAs near O'Hare. Boards here manage:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Older condo HVAC & plumbing systems</li>
<li style="padding: 10px 0; color: var(--text-light);">• Snow removal contracts</li>
<li style="padding: 10px 0; color: var(--text-light);">• Budget challenges in cost-sensitive associations</li>
<li style="padding: 10px 0; color: var(--text-light);">• Residents expecting consistent communication</li>''',
        'links': '''<a href="../wood-dale" class="area-link">Wood Dale</a>
<a href="../elmhurst" class="area-link">Elmhurst</a>
<a href="../franklin-park" class="area-link">Franklin Park</a>'''
    },
    {
        'city': 'Franklin Park',
        'slug': 'franklin-park',
        'intro': "Franklin Park has a strong mix of working-class condos and townhome HOAs. Boards here face:",
        'challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Older condo buildings with deferred maintenance</li>
<li style="padding: 10px 0; color: var(--text-light);">• Stormwater and flooding challenges</li>
<li style="padding: 10px 0; color: var(--text-light);">• Budgeting pressure from rising vendor costs</li>
<li style="padding: 10px 0; color: var(--text-light);">• Boards requiring clear governance support</li>''',
        'links': '''<a href="../bensenville" class="area-link">Bensenville</a>
<a href="../rosemont" class="area-link">Rosemont</a>
<a href="../schiller-park" class="area-link">Schiller Park</a>'''
    }
]

def main():
    os.chdir('C:\\Users\\mirsa\\Documents\\manage369-live\\property-management')

    for area in areas:
        # Skip Winnetka as it's already done
        if area['slug'] == 'winnetka':
            continue

        # Create directory if it doesn't exist
        dir_path = area['slug']
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # Generate HTML content
        html_content = create_area_page(area)

        # Write to file
        file_path = os.path.join(dir_path, 'index.html')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"Created: {file_path}")

if __name__ == "__main__":
    main()