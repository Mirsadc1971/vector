import re

# Read the file
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the last FAQ question and add more questions after it
old_text = '''        {
          "@type": "Question",
          "name": "What maintenance services do you provide?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "We provide comprehensive maintenance coordination for all managed properties in Chicago and North Shore communities. Our professional service line ensures prompt response to maintenance needs and property care."
          }
        }
      ]
    }
    </script>'''

new_text = '''        {
          "@type": "Question",
          "name": "What maintenance services do you provide?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "We provide comprehensive maintenance coordination for all managed properties in Chicago and North Shore communities. Our professional service line ensures prompt response to maintenance needs and property care."
          }
        },
        {
          "@type": "Question",
          "name": "How much does property management cost in Chicago?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Property management fees in Chicago typically range from 5-10% of monthly collected rent for residential properties. For HOAs and condominiums, fees are based on the number of units and services required. Manage369 offers competitive rates with transparent pricing and no hidden fees. Contact us for a custom quote tailored to your property's needs."
          }
        },
        {
          "@type": "Question",
          "name": "What services are included in professional property management?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Our comprehensive property management includes: financial management (budgeting, collections, reporting), 24/7 maintenance coordination, vendor management, board meeting support, legal compliance assistance, resident communications, capital project management, and emergency response. We customize our services based on your property's specific requirements."
          }
        },
        {
          "@type": "Question",
          "name": "How quickly can you take over management of our property?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "We can typically begin managing your property within 30 days. Our onboarding process includes a comprehensive property audit, financial review, document transfer, vendor evaluation, and resident communication plan. We'll work with your current management company to ensure a smooth transition with zero disruption to residents."
          }
        },
        {
          "@type": "Question",
          "name": "Do you provide 24/7 emergency services?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "We provide 24/7 emergency response through our dedicated hotline. Our network of pre-screened, licensed contractors can respond within 2 hours for true emergencies. We handle everything from burst pipes to elevator breakdowns, coordinating repairs while keeping boards and residents informed throughout the process."
          }
        }
      ]
    }
    </script>'''

content = content.replace(old_text, new_text)

# Write back
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('FAQ schema updated successfully')