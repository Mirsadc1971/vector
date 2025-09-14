#!/usr/bin/env python3
import os
import re

def restore_service_offer(content):
    """Restore the missing service offer content"""

    # Find the Special Offers Section
    pattern = r'(<!-- Special Offers Section.*?<section[^>]*>.*?<div id="countdown"[^>]*>.*?</div>)(.*?)(</section>)'

    def add_offer_content(match):
        start = match.group(1)
        middle = match.group(2)
        end = match.group(3)

        # Add the service offer content
        offer_content = '''
                </div>

                <h2 style="color: #F4A261; font-size: 2.5rem; font-weight: 700; margin-bottom: 1rem;">
                    Limited Time Offer for New HOA Clients
                </h2>
                <p style="color: #e5e7eb; font-size: 1.25rem; max-width: 800px; margin: 0 auto 3rem;">
                    Switch to Manage369 and save big on professional property management
                </p>
            </div>

            <!-- Offer Cards Grid -->
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; margin-bottom: 3rem;">

                <!-- Year 1 Card -->
                <div style="background: linear-gradient(135deg, #F4A261, #e8974f); border-radius: 12px; padding: 2rem; position: relative; overflow: hidden;">
                    <div style="position: absolute; top: 10px; right: 10px; background: #ff4444; color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.875rem; font-weight: 600;">
                        BEST VALUE
                    </div>
                    <h3 style="color: #1f2937; font-size: 1.5rem; margin-bottom: 1rem;">Year 1</h3>
                    <div style="font-size: 3rem; font-weight: 800; color: #1f2937; margin-bottom: 0.5rem;">35% OFF</div>
                    <p style="color: #1f2937; font-size: 1.125rem;">Your current management fee</p>
                </div>

                <!-- Year 2 Card -->
                <div style="background: rgba(44, 62, 80, 0.3); border: 2px solid #F4A261; border-radius: 12px; padding: 2rem;">
                    <h3 style="color: #F4A261; font-size: 1.5rem; margin-bottom: 1rem;">Year 2</h3>
                    <div style="font-size: 3rem; font-weight: 800; color: #F4A261; margin-bottom: 0.5rem;">15% OFF</div>
                    <p style="color: #e5e7eb; font-size: 1.125rem;">Your current management fee</p>
                </div>

                <!-- Year 3 Card -->
                <div style="background: rgba(44, 62, 80, 0.3); border: 2px solid #F4A261; border-radius: 12px; padding: 2rem;">
                    <h3 style="color: #F4A261; font-size: 1.5rem; margin-bottom: 1rem;">Year 3+</h3>
                    <div style="font-size: 2rem; font-weight: 800; color: #F4A261; margin-bottom: 0.5rem;">REGULAR PRICE</div>
                    <p style="color: #e5e7eb; font-size: 1.125rem;">50% total savings over 2 years!</p>
                </div>
            </div>

            <!-- CTA Button -->
            <div style="text-align: center;">
                <a href="tel:8478344131" style="display: inline-block; background: #F4A261; color: #1f2937; padding: 1rem 3rem; border-radius: 8px; font-size: 1.25rem; font-weight: 700; text-decoration: none; transition: all 0.3s;">
                    📞 Call (847) 834-4131 to Claim Your Discount
                </a>
            </div>
        </div>'''

        return start + offer_content + end

    content = re.sub(pattern, add_offer_content, content, flags=re.DOTALL)

    return content

# Process main pages
print("Restoring service offer content...")

# Fix homepage
if os.path.exists('index.html'):
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    content = restore_service_offer(content)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Restored service offer in index.html")

print("\nService offer restored with 35% off Year 1!")