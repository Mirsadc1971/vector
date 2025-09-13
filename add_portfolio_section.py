#!/usr/bin/env python3
"""
Add a portfolio section with property images to demonstrate lazy loading
"""

import os

def add_portfolio_section():
    """Add a portfolio section with lazy-loaded images"""

    portfolio_html = '''
    <!-- Portfolio Section with Lazy Loading -->
    <section id="portfolio" style="padding: 4rem 2rem; background: #2C3E50;">
        <div class="container" style="max-width: 1200px; margin: 0 auto;">
            <h2 style="text-align: center; margin-bottom: 2rem; color: #F4A261; font-size: 2.5rem; font-weight: 700;">Our Managed Properties</h2>
            <p style="text-align: center; margin-bottom: 3rem; color: #e5e7eb; font-size: 1.2rem; max-width: 800px; margin-left: auto; margin-right: auto;">See examples of the high-quality properties we manage throughout Chicago and North Shore communities.</p>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 2rem; margin-bottom: 3rem;">

                <!-- Property 1 -->
                <div style="background: #1f2937; border-radius: 12px; overflow: hidden; box-shadow: 0 8px 20px rgba(0,0,0,0.3); transition: transform 0.3s ease;">
                    <div style="height: 250px; position: relative; overflow: hidden;">
                        <img
                            class="lazy property-image"
                            data-src="images/manage369livingroomskokie_optimized.webp"
                            src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='250'%3E%3Crect width='100%25' height='100%25' fill='%23f3f4f6'/%3E%3C/svg%3E"
                            alt="Luxury Living Room - Skokie Property Management"
                            style="width: 100%; height: 100%; object-fit: cover; transition: opacity 0.3s ease;"
                            loading="lazy"
                        />
                    </div>
                    <div style="padding: 1.5rem;">
                        <h3 style="color: #F4A261; margin-bottom: 0.5rem; font-size: 1.3rem;">Luxury Condo - Skokie</h3>
                        <p style="color: #e5e7eb; line-height: 1.6;">Modern amenities and professional management ensure residents enjoy premium living experiences.</p>
                    </div>
                </div>

                <!-- Property 2 -->
                <div style="background: #1f2937; border-radius: 12px; overflow: hidden; box-shadow: 0 8px 20px rgba(0,0,0,0.3); transition: transform 0.3s ease;">
                    <div style="height: 250px; position: relative; overflow: hidden;">
                        <img
                            class="lazy property-image"
                            data-src="images/manage369bedroom1740maplewood_optimized.webp"
                            src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='250'%3E%3Crect width='100%25' height='100%25' fill='%23f3f4f6'/%3E%3C/svg%3E"
                            alt="Master Bedroom - Maplewood Property"
                            style="width: 100%; height: 100%; object-fit: cover; transition: opacity 0.3s ease;"
                            loading="lazy"
                        />
                    </div>
                    <div style="padding: 1.5rem;">
                        <h3 style="color: #F4A261; margin-bottom: 0.5rem; font-size: 1.3rem;">Executive Home - Maplewood</h3>
                        <p style="color: #e5e7eb; line-height: 1.6;">Sophisticated bedroom design reflecting our attention to quality and resident satisfaction.</p>
                    </div>
                </div>

                <!-- Property 3 -->
                <div style="background: #1f2937; border-radius: 12px; overflow: hidden; box-shadow: 0 8px 20px rgba(0,0,0,0.3); transition: transform 0.3s ease;">
                    <div style="height: 250px; position: relative; overflow: hidden;">
                        <img
                            class="lazy property-image"
                            data-src="images/northbrook2manage369_optimized.webp"
                            src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='250'%3E%3Crect width='100%25' height='100%25' fill='%23f3f4f6'/%3E%3C/svg%3E"
                            alt="Northbrook Community Property"
                            style="width: 100%; height: 100%; object-fit: cover; transition: opacity 0.3s ease;"
                            loading="lazy"
                        />
                    </div>
                    <div style="padding: 1.5rem;">
                        <h3 style="color: #F4A261; margin-bottom: 0.5rem; font-size: 1.3rem;">Community - Northbrook</h3>
                        <p style="color: #e5e7eb; line-height: 1.6;">Well-maintained exteriors and landscaping show our commitment to property value preservation.</p>
                    </div>
                </div>

                <!-- Property 4 -->
                <div style="background: #1f2937; border-radius: 12px; overflow: hidden; box-shadow: 0 8px 20px rgba(0,0,0,0.3); transition: transform 0.3s ease;">
                    <div style="height: 250px; position: relative; overflow: hidden;">
                        <img
                            class="lazy property-image"
                            data-src="images/chestnutmanage369_optimized.webp"
                            src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='250'%3E%3Crect width='100%25' height='100%25' fill='%23f3f4f6'/%3E%3C/svg%3E"
                            alt="Chestnut Street Property Management"
                            style="width: 100%; height: 100%; object-fit: cover; transition: opacity 0.3s ease;"
                            loading="lazy"
                        />
                    </div>
                    <div style="padding: 1.5rem;">
                        <h3 style="color: #F4A261; margin-bottom: 0.5rem; font-size: 1.3rem;">Urban Living - Chestnut</h3>
                        <p style="color: #e5e7eb; line-height: 1.6;">Downtown properties combining city convenience with professional management excellence.</p>
                    </div>
                </div>

                <!-- Property 5 -->
                <div style="background: #1f2937; border-radius: 12px; overflow: hidden; box-shadow: 0 8px 20px rgba(0,0,0,0.3); transition: transform 0.3s ease;">
                    <div style="height: 250px; position: relative; overflow: hidden;">
                        <img
                            class="lazy property-image"
                            data-src="images/buck4manage369_optimized.webp"
                            src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='250'%3E%3Crect width='100%25' height='100%25' fill='%23f3f4f6'/%3E%3C/svg%3E"
                            alt="Buck Street Property"
                            style="width: 100%; height: 100%; object-fit: cover; transition: opacity 0.3s ease;"
                            loading="lazy"
                        />
                    </div>
                    <div style="padding: 1.5rem;">
                        <h3 style="color: #F4A261; margin-bottom: 0.5rem; font-size: 1.3rem;">Residential - Buck Street</h3>
                        <p style="color: #e5e7eb; line-height: 1.6;">Family-oriented properties with comprehensive maintenance and community management services.</p>
                    </div>
                </div>

                <!-- Property 6 -->
                <div style="background: #1f2937; border-radius: 12px; overflow: hidden; box-shadow: 0 8px 20px rgba(0,0,0,0.3); transition: transform 0.3s ease;">
                    <div style="height: 250px; position: relative; overflow: hidden;">
                        <img
                            class="lazy property-image"
                            data-src="images/kenmore2manage369_optimized.webp"
                            src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='250'%3E%3Crect width='100%25' height='100%25' fill='%23f3f4f6'/%3E%3C/svg%3E"
                            alt="Kenmore Property Management"
                            style="width: 100%; height: 100%; object-fit: cover; transition: opacity 0.3s ease;"
                            loading="lazy"
                        />
                    </div>
                    <div style="padding: 1.5rem;">
                        <h3 style="color: #F4A261; margin-bottom: 0.5rem; font-size: 1.3rem;">Community - Kenmore</h3>
                        <p style="color: #e5e7eb; line-height: 1.6;">Established neighborhood properties maintained to the highest standards of excellence.</p>
                    </div>
                </div>

            </div>

            <div style="text-align: center;">
                <a href="contact.html" style="display: inline-block; background: linear-gradient(135deg, #F4A261 0%, #e76f51 100%); color: white; padding: 1rem 2rem; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 1.1rem; transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(244, 162, 97, 0.3);">
                    View All Properties
                </a>
            </div>
        </div>
    </section>

    <style>
    .property-image {
        transition: transform 0.3s ease, opacity 0.3s ease;
    }

    .property-image.loaded {
        opacity: 1;
    }

    .property-image:hover {
        transform: scale(1.05);
    }

    @media (max-width: 768px) {
        #portfolio .container > div {
            grid-template-columns: 1fr;
            gap: 1.5rem;
        }
    }
    </style>
'''

    return portfolio_html

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    index_path = os.path.join(script_dir, 'index.html')

    if not os.path.exists(index_path):
        print("index.html not found")
        return

    print("Adding portfolio section with lazy-loaded images...")

    # Read the file
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find a good place to insert the portfolio section - after the services section
    portfolio_section = add_portfolio_section()

    # Look for the FAQ section and insert before it
    if '<!-- FAQ Section -->' in content:
        content = content.replace('<!-- FAQ Section -->', portfolio_section + '\n    <!-- FAQ Section -->')
        print("Inserted portfolio section before FAQ")
    elif '<section style="padding: 4rem 2rem; background: #2C3E50; text-align: center;">' in content:
        # Insert before the first matching section
        content = content.replace('<section style="padding: 4rem 2rem; background: #2C3E50; text-align: center;">',
                                 portfolio_section + '\n    <section style="padding: 4rem 2rem; background: #2C3E50; text-align: center;">', 1)
        print("Inserted portfolio section before existing section")
    else:
        # Insert before closing body tag
        content = content.replace('</body>', portfolio_section + '\n</body>')
        print("Inserted portfolio section before closing body tag")

    # Update the lazy loading script to handle the new images
    lazy_script_addition = '''
    // Enhanced lazy loading for portfolio images
    function initPortfolioLazyLoading() {
        const portfolioImages = document.querySelectorAll('.property-image.lazy');

        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        img.classList.add('loaded');
                        observer.unobserve(img);
                    }
                });
            }, {
                rootMargin: '50px 0px',
                threshold: 0.01
            });

            portfolioImages.forEach(img => imageObserver.observe(img));
        } else {
            // Fallback for older browsers
            portfolioImages.forEach(img => {
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                img.classList.add('loaded');
            });
        }
    }

    // Call on DOM ready
    document.addEventListener('DOMContentLoaded', function() {
        initPortfolioLazyLoading();
    });
'''

    # Add to existing script
    if 'addLazyLoading();' in content:
        content = content.replace('addLazyLoading();', 'addLazyLoading();\n        initPortfolioLazyLoading();')

    # Save the file
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("✅ Portfolio section added successfully!")
    print("\nFeatures added:")
    print("- 6 property images with lazy loading")
    print("- WebP format for optimized loading")
    print("- Placeholder images for instant loading")
    print("- Responsive grid layout")
    print("- Hover effects and transitions")
    print("- Below-the-fold positioning for lazy loading benefit")

if __name__ == "__main__":
    main()