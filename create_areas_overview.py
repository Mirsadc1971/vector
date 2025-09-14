#!/usr/bin/env python3
import os

os.chdir('C:\\Users\\mirsa\\Documents\\manage369-live\\property-management')

# Get all area directories
areas = []
for d in sorted(os.listdir('.')):
    if os.path.isdir(d) and os.path.exists(os.path.join(d, 'index.html')):
        # Convert directory name to proper title
        title = d.replace('-', ' ').title()
        areas.append({'slug': d, 'title': title})

print(f"Found {len(areas)} areas")

# Create the areas overview page
html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Areas We Serve — Property Management in Chicago & Suburbs | Manage369</title>
<meta content="Professional property management services across 84 Chicago neighborhoods and suburbs. HOA, condominium & townhome experts since 2007." name="description"/>
<link href="/images/apple-touch-icon.png" rel="apple-touch-icon" sizes="180x180"/>
<link href="/images/favicon-32x32.png" rel="icon" sizes="32x32" type="image/png"/>
<link href="/images/favicon-16x16.png" rel="icon" sizes="16x16" type="image/png"/>
<meta content="#1f2937" name="theme-color"/>
<style>
:root {
    --primary-gold: #F4A261;
    --primary-navy: #2C3E50;
    --background-dark: #1f2937;
    --text-light: #e5e7eb;
    --accent-blue: #084298;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    background: var(--background-dark) !important;
    color: var(--text-light) !important;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
}

h1, h2 {
    color: var(--primary-gold) !important;
    text-align: center;
    margin-bottom: 2rem;
}

h1 { font-size: 2.5rem; }
h2 { font-size: 2rem; margin: 3rem 0 2rem; }

.container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 20px;
}

.header {
    background: var(--background-dark);
    padding: 1rem 2rem;
    position: sticky;
    top: 0;
    z-index: 1000;
    box-shadow: 0 2px 20px rgba(0,0,0,0.2);
    border-bottom: 1px solid rgba(244,162,97,0.2);
}

.header-content {
    max-width: 1400px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--primary-gold);
}

.nav-menu {
    display: flex;
    gap: 2rem;
    list-style: none;
}

.nav-menu a {
    color: var(--text-light);
    text-decoration: none;
    font-weight: 500;
    transition: color 0.3s ease;
}

.nav-menu a:hover {
    color: var(--primary-gold);
}

/* Areas Grid - 21 rows x 4 columns */
.areas-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin: 40px 0;
}

@media (max-width: 1200px) {
    .areas-grid {
        grid-template-columns: repeat(3, 1fr);
    }
}

@media (max-width: 768px) {
    .areas-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 480px) {
    .areas-grid {
        grid-template-columns: 1fr;
    }
}

.area-card {
    background: rgba(44, 62, 80, 0.3);
    border: 1px solid rgba(244, 162, 97, 0.3);
    border-radius: 8px;
    padding: 25px;
    text-align: center;
    transition: all 0.3s ease;
    text-decoration: none;
    display: block;
}

.area-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(244, 162, 97, 0.3);
    border-color: var(--primary-gold);
    background: rgba(244, 162, 97, 0.1);
}

.area-card h3 {
    color: var(--primary-gold);
    margin-bottom: 10px;
    font-size: 1.2rem;
}

.area-card p {
    color: var(--text-light);
    font-size: 0.9rem;
}

.hero-section {
    background: linear-gradient(135deg, rgba(244,162,97,0.1), rgba(44,62,80,0.2));
    padding: 100px 20px;
    text-align: center;
}

.stats-bar {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 30px;
    margin: 60px 0;
    padding: 40px;
    background: rgba(44, 62, 80, 0.2);
    border-radius: 12px;
}

@media (max-width: 768px) {
    .stats-bar {
        grid-template-columns: repeat(2, 1fr);
    }
}

.stat {
    text-align: center;
}

.stat-number {
    font-size: 3rem;
    color: var(--primary-gold);
    font-weight: bold;
}

.stat-label {
    color: var(--text-light);
    margin-top: 10px;
}
</style>
</head>
<body>

<!-- Header -->
<header class="header">
<div class="header-content">
<div class="logo">MANAGE369</div>
<nav>
<ul class="nav-menu">
<li><a href="/">Home</a></li>
<li><a href="/services">Services</a></li>
<li><a href="/property-management">Areas</a></li>
<li><a href="/contact">Contact</a></li>
</ul>
</nav>
</div>
</header>

<!-- Hero Section -->
<section class="hero-section">
<div class="container">
<h1>Property Management Services Across Chicagoland</h1>
<p style="font-size: 1.3rem; color: var(--primary-gold); margin: 20px 0;">
84 Communities. One Trusted Partner.
</p>
<p style="max-width: 800px; margin: 0 auto; font-size: 1.1rem;">
From Chicago's vibrant neighborhoods to the North Shore's prestigious suburbs, Manage369 delivers professional HOA, condominium, and townhome management services tailored to each community's unique needs.
</p>
</div>
</section>

<!-- Stats Bar -->
<section>
<div class="container">
<div class="stats-bar">
<div class="stat">
<div class="stat-number">84</div>
<div class="stat-label">Communities Served</div>
</div>
<div class="stat">
<div class="stat-number">18+</div>
<div class="stat-label">Years Experience</div>
</div>
<div class="stat">
<div class="stat-number">200+</div>
<div class="stat-label">Associations Managed</div>
</div>
<div class="stat">
<div class="stat-number">24/7</div>
<div class="stat-label">Emergency Support</div>
</div>
</div>
</div>
</section>

<!-- Areas Grid -->
<section>
<div class="container">
<h2>Choose Your Community</h2>
<div class="areas-grid">
'''

# Add all 84 area cards
for area in areas:
    html_content += f'''<a href="./{area['slug']}" class="area-card">
<h3>{area['title']}</h3>
<p>Professional property management</p>
</a>
'''

html_content += '''</div>
</div>
</section>

<!-- CTA Section -->
<section style="background: rgba(44,62,80,0.1); padding: 80px 20px;">
<div class="container">
<div style="background: linear-gradient(135deg, rgba(244, 162, 97, 0.1), rgba(44, 62, 80, 0.2)); border: 2px solid var(--primary-gold); border-radius: 12px; padding: 60px 40px; text-align: center;">
<h2>Ready to Experience Better Property Management?</h2>
<p style="font-size: 1.2rem; margin: 30px 0;">
Join 200+ satisfied communities across Chicagoland
</p>
<a href="tel:8478344131" style="display: inline-block; background: var(--primary-gold); color: var(--background-dark); padding: 15px 40px; border-radius: 50px; font-weight: bold; font-size: 1.1rem; text-decoration: none; transition: all 0.3s ease;">
Call (847) 834-4131
</a>
</div>
</div>
</section>

<!-- Footer -->
<footer style="background: rgba(44,62,80,0.3); padding: 60px 20px;">
<div class="container">
<p style="text-align: center;">
© 2025 Manage369. All rights reserved. | Licensed Property Management Company | License: 291.000211
</p>
</div>
</footer>

</body>
</html>'''

# Write the index.html file
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Created areas overview page with {len(areas)} area cards in a 4-column grid (21 rows)")