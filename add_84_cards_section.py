#!/usr/bin/env python3
import os

os.chdir('C:\\Users\\mirsa\\Documents\\manage369-live\\property-management')

# Create the 84 cards content (21 rows x 4 cards)
cards_html = '''
<!-- 84 Cards Section (21 rows x 4 columns) -->
<section style="background: rgba(44,62,80,0.1);">
<div class="container">
<h2>Our Complete Service Offerings</h2>
<div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin: 40px 0;">
'''

# Generate 84 cards (21 rows of 4)
card_titles = [
    # Row 1
    "Financial Management", "Budget Planning", "Reserve Studies", "Assessment Collection",
    # Row 2
    "Vendor Management", "Contract Negotiation", "Bid Analysis", "Vendor Oversight",
    # Row 3
    "Board Support", "Meeting Coordination", "Minutes & Records", "Board Training",
    # Row 4
    "Maintenance Planning", "Preventive Maintenance", "Emergency Repairs", "Capital Projects",
    # Row 5
    "Compliance Management", "Violation Tracking", "Legal Coordination", "Document Management",
    # Row 6
    "Communication Services", "Resident Portals", "Newsletter Creation", "Website Management",
    # Row 7
    "Accounting Services", "Monthly Reporting", "Annual Audits", "Tax Preparation",
    # Row 8
    "Insurance Support", "Claims Processing", "Risk Assessment", "Policy Review",
    # Row 9
    "Landscape Management", "Snow Removal", "Seasonal Planning", "Irrigation Systems",
    # Row 10
    "Pool Management", "Amenity Scheduling", "Fitness Centers", "Clubhouse Management",
    # Row 11
    "Parking Management", "Permit Systems", "Towing Coordination", "Guest Parking",
    # Row 12
    "Energy Management", "Utility Audits", "Cost Reduction", "Green Initiatives",
    # Row 13
    "Construction Oversight", "Project Management", "Permit Coordination", "Quality Control",
    # Row 14
    "Emergency Response", "24/7 Hotline", "Disaster Planning", "Crisis Management",
    # Row 15
    "Technology Solutions", "Online Payments", "Mobile Apps", "Cloud Storage",
    # Row 16
    "Inspection Services", "Annual Inspections", "Move-in/Move-out", "Property Audits",
    # Row 17
    "Collection Services", "Delinquency Management", "Payment Plans", "Legal Referrals",
    # Row 18
    "Architectural Review", "Design Standards", "Modification Requests", "Compliance Checks",
    # Row 19
    "Transition Services", "Developer Turnover", "New Board Training", "Document Transfer",
    # Row 20
    "Special Assessments", "Project Planning", "Funding Options", "Owner Communication",
    # Row 21
    "Community Events", "Social Planning", "Holiday Celebrations", "Community Building"
]

for i, title in enumerate(card_titles):
    cards_html += f'''<div style="background: rgba(44, 62, 80, 0.3); border: 1px solid rgba(244, 162, 97, 0.3); border-radius: 8px; padding: 20px; text-align: center;">
<h4 style="color: var(--primary-gold); margin-bottom: 10px; font-size: 1rem;">{title}</h4>
<p style="color: var(--text-light); font-size: 0.9rem;">Professional {title.lower()} services for your community</p>
</div>
'''

cards_html += '''</div>
</div>
</section>
'''

# Update all pages
dirs = [d for d in os.listdir('.') if os.path.isdir(d)]
print(f"Adding 84 cards section to {len(dirs)} pages...")

for directory in dirs:
    file_path = os.path.join(directory, 'index.html')
    if not os.path.exists(file_path):
        continue

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Insert the 84 cards section before the FAQ section
    if '<!-- FAQ Section -->' in content:
        content = content.replace('<!-- FAQ Section -->', cards_html + '\n\n<!-- FAQ Section -->')
    elif '<h2>Frequently Asked Questions</h2>' in content:
        # Find the section containing FAQ
        import re
        pattern = r'(<section[^>]*>[\s\S]*?<h2>Frequently Asked Questions</h2>)'
        content = re.sub(pattern, cards_html + '\n\n\\1', content)
    else:
        # Add before footer if no FAQ section
        content = content.replace('<footer', cards_html + '\n\n<footer')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Added to {directory}")

print("\nAll pages now have 84 cards (21 rows x 4 columns)!")