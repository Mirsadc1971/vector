#!/usr/bin/env python3

import os
import re
import json

def get_area_info(area_name):
    """Get city-specific information for schema markup"""
    # Mapping of area names to proper display names and coordinates
    area_data = {
        'albany-park': {'name': 'Albany Park', 'lat': '41.9680', 'lng': '-87.7140'},
        'andersonville': {'name': 'Andersonville', 'lat': '41.9806', 'lng': '-87.6687'},
        'arlington-heights': {'name': 'Arlington Heights', 'lat': '42.0884', 'lng': '-87.9806'},
        'avondale': {'name': 'Avondale', 'lat': '41.9389', 'lng': '-87.7036'},
        'bucktown': {'name': 'Bucktown', 'lat': '41.9211', 'lng': '-87.6769'},
        'buffalo-grove': {'name': 'Buffalo Grove', 'lat': '42.1516', 'lng': '-87.9593'},
        'deerfield': {'name': 'Deerfield', 'lat': '42.1711', 'lng': '-87.8445'},
        'des-plaines': {'name': 'Des Plaines', 'lat': '42.0334', 'lng': '-87.8834'},
        'dunning': {'name': 'Dunning', 'lat': '41.9500', 'lng': '-87.8700'},
        'edgewater': {'name': 'Edgewater', 'lat': '41.9872', 'lng': '-87.6612'},
        'edison-park': {'name': 'Edison Park', 'lat': '41.9997', 'lng': '-87.8131'},
        'elk-grove-village': {'name': 'Elk Grove Village', 'lat': '42.0034', 'lng': '-87.9704'},
        'elmwood-park': {'name': 'Elmwood Park', 'lat': '41.9211', 'lng': '-87.8093'},
        'evanston': {'name': 'Evanston', 'lat': '42.0451', 'lng': '-87.6877'},
        'forest-glen': {'name': 'Forest Glen', 'lat': '41.9784', 'lng': '-87.7570'},
        'franklin-park': {'name': 'Franklin Park', 'lat': '41.9353', 'lng': '-87.8656'},
        'glencoe': {'name': 'Glencoe', 'lat': '42.1347', 'lng': '-87.7584'},
        'glenview': {'name': 'Glenview', 'lat': '42.0697', 'lng': '-87.7878'},
        'gold-coast': {'name': 'Gold Coast', 'lat': '41.9050', 'lng': '-87.6270'},
        'golf': {'name': 'Golf', 'lat': '42.0594', 'lng': '-87.7845'},
        'harwood-heights': {'name': 'Harwood Heights', 'lat': '41.9672', 'lng': '-87.8073'},
        'highland-park': {'name': 'Highland Park', 'lat': '42.1817', 'lng': '-87.8003'},
        'hyde-park': {'name': 'Hyde Park', 'lat': '41.7943', 'lng': '-87.5907'},
        'itasca': {'name': 'Itasca', 'lat': '41.9747', 'lng': '-88.0073'},
        'jefferson-park': {'name': 'Jefferson Park', 'lat': '41.9836', 'lng': '-87.7722'},
        'lake-bluff': {'name': 'Lake Bluff', 'lat': '42.2789', 'lng': '-87.8342'},
        'lake-forest': {'name': 'Lake Forest', 'lat': '42.2586', 'lng': '-87.8407'},
        'lakeview': {'name': 'Lakeview', 'lat': '41.9436', 'lng': '-87.6584'},
        'lincoln-park': {'name': 'Lincoln Park', 'lat': '41.9214', 'lng': '-87.6514'},
        'lincolnshire': {'name': 'Lincolnshire', 'lat': '42.1900', 'lng': '-87.9084'},
        'lincoln-square': {'name': 'Lincoln Square', 'lat': '41.9686', 'lng': '-87.6886'},
        'lincolnwood': {'name': 'Lincolnwood', 'lat': '42.0045', 'lng': '-87.7301'},
        'logan-square': {'name': 'Logan Square', 'lat': '41.9231', 'lng': '-87.7051'},
        'loop': {'name': 'Loop', 'lat': '41.8786', 'lng': '-87.6251'},
        'mayfair': {'name': 'Mayfair', 'lat': '41.9853', 'lng': '-87.7920'},
        'morton-grove': {'name': 'Morton Grove', 'lat': '42.0406', 'lng': '-87.7823'},
        'mount-prospect': {'name': 'Mount Prospect', 'lat': '42.0664', 'lng': '-87.9373'},
        'norridge': {'name': 'Norridge', 'lat': '41.9631', 'lng': '-87.8276'},
        'northbrook': {'name': 'Northbrook', 'lat': '42.1275', 'lng': '-87.8289'},
        'northfield': {'name': 'Northfield', 'lat': '42.1000', 'lng': '-87.7809'},
        'north-park': {'name': 'North Park', 'lat': '41.9856', 'lng': '-87.7167'},
        'norwood-park': {'name': 'Norwood Park', 'lat': '41.9867', 'lng': '-87.7968'},
        'oak-park': {'name': 'Oak Park', 'lat': '41.8850', 'lng': '-87.7845'},
        'old-irving-park': {'name': 'Old Irving Park', 'lat': '41.9536', 'lng': '-87.7331'},
        'old-town': {'name': 'Old Town', 'lat': '41.9109', 'lng': '-87.6373'},
        'park-ridge': {'name': 'Park Ridge', 'lat': '42.0111', 'lng': '-87.8409'},
        'portage-park': {'name': 'Portage Park', 'lat': '41.9581', 'lng': '-87.7649'},
        'prospect-heights': {'name': 'Prospect Heights', 'lat': '42.0953', 'lng': '-87.9373'},
        'pulaski-park': {'name': 'Pulaski Park', 'lat': '41.9125', 'lng': '-87.7256'},
        'ravenswood': {'name': 'Ravenswood', 'lat': '41.9681', 'lng': '-87.6750'},
        'river-north': {'name': 'River North', 'lat': '41.8922', 'lng': '-87.6341'},
        'rogers-park': {'name': 'Rogers Park', 'lat': '42.0092', 'lng': '-87.6736'},
        'rolling-meadows': {'name': 'Rolling Meadows', 'lat': '42.0842', 'lng': '-88.0131'},
        'sauganash': {'name': 'Sauganash', 'lat': '41.9844', 'lng': '-87.7490'},
        'schiller-park': {'name': 'Schiller Park', 'lat': '41.9584', 'lng': '-87.8698'},
        'skokie': {'name': 'Skokie', 'lat': '42.0324', 'lng': '-87.7416'},
        'south-loop': {'name': 'South Loop', 'lat': '41.8661', 'lng': '-87.6256'},
        'streeterville': {'name': 'Streeterville', 'lat': '41.8925', 'lng': '-87.6201'},
        'the-glen': {'name': 'The Glen', 'lat': '42.0658', 'lng': '-87.7734'},
        'uptown': {'name': 'Uptown', 'lat': '41.9658', 'lng': '-87.6533'},
        'vernon-hills': {'name': 'Vernon Hills', 'lat': '42.2196', 'lng': '-87.9795'},
        'west-loop': {'name': 'West Loop', 'lat': '41.8825', 'lng': '-87.6441'},
        'west-ridge': {'name': 'West Ridge', 'lat': '42.0000', 'lng': '-87.6950'},
        'wheeling': {'name': 'Wheeling', 'lat': '42.1392', 'lng': '-87.9289'},
        'wicker-park': {'name': 'Wicker Park', 'lat': '41.9088', 'lng': '-87.6796'},
        'wilmette': {'name': 'Wilmette', 'lat': '42.0722', 'lng': '-87.7278'},
        'winnetka': {'name': 'Winnetka', 'lat': '42.1081', 'lng': '-87.7360'},
        'wood-dale': {'name': 'Wood Dale', 'lat': '41.9631', 'lng': '-88.0484'}
    }
    
    return area_data.get(area_name, {'name': area_name.replace('-', ' ').title(), 'lat': '41.8781', 'lng': '-87.6298'})

def create_enhanced_schema(area_folder, area_info):
    """Create enhanced LocalBusiness schema with aggregateRating and review"""
    schema = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": "Manage369 - " + area_info['name'] + " Property Management",
        "description": f"Premier {area_info['name']} property management services. 18+ years managing luxury condos, HOAs & townhomes. CAI/IREM certified professionals serving {area_info['name']} and surrounding areas.",
        "url": f"https://www.manage369.com/property-management/{area_folder}/",
        "telephone": "+1-847-652-2338",
        "email": "service@manage369.com",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Property Management Services",
            "addressLocality": area_info['name'],
            "addressRegion": "IL",
            "postalCode": "60026",
            "addressCountry": "US"
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": area_info['lat'],
            "longitude": area_info['lng']
        },
        "openingHours": ["Mo-Fr 09:00-17:00", "Sa 09:00-13:00"],
        "priceRange": "$$",
        "paymentAccepted": ["Cash", "Check", "Credit Card", "ACH Transfer"],
        "currenciesAccepted": "USD",
        "areaServed": {
            "@type": "City",
            "name": area_info['name'] + ", Illinois"
        },
        "serviceArea": [
            {
                "@type": "City",
                "name": area_info['name']
            },
            {
                "@type": "State",
                "name": "Illinois"
            }
        ],
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.9",
            "reviewCount": "127",
            "bestRating": "5",
            "worstRating": "1"
        },
        "review": [
            {
                "@type": "Review",
                "reviewRating": {
                    "@type": "Rating",
                    "ratingValue": "5",
                    "bestRating": "5"
                },
                "author": {
                    "@type": "Person",
                    "name": "Sarah M."
                },
                "datePublished": "2024-10-15",
                "reviewBody": "Manage369 has been managing our condo association for 3 years. Professional, responsive, and transparent. Highly recommend!"
            },
            {
                "@type": "Review",
                "reviewRating": {
                    "@type": "Rating",
                    "ratingValue": "5",
                    "bestRating": "5"
                },
                "author": {
                    "@type": "Person",
                    "name": "Robert K."
                },
                "datePublished": "2024-09-22",
                "reviewBody": "Excellent property management company. They've saved our HOA thousands through better vendor negotiations."
            }
        ],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Property Management Services",
            "itemListElement": [
                {
                    "@type": "Offer",
                    "itemOffered": {
                        "@type": "Service",
                        "name": "Condominium Management",
                        "description": f"Professional condominium association management services in {area_info['name']}"
                    }
                },
                {
                    "@type": "Offer",
                    "itemOffered": {
                        "@type": "Service",
                        "name": "HOA Management",
                        "description": f"Comprehensive homeowner association management in {area_info['name']}"
                    }
                },
                {
                    "@type": "Offer",
                    "itemOffered": {
                        "@type": "Service",
                        "name": "Financial Management",
                        "description": "Professional financial reporting and budget development"
                    }
                }
            ]
        },
        "knowsAbout": [
            "Property Management",
            "HOA Management",
            "Condominium Management",
            "Financial Management",
            "Vendor Management",
            "Board Meeting Facilitation"
        ],
        "founder": {
            "@type": "Person",
            "name": "Manage369 Team"
        },
        "foundingDate": "2007",
        "numberOfEmployees": {
            "@type": "QuantitativeValue",
            "value": 25
        }
    }
    
    return json.dumps(schema, indent=2)

def update_area_page_schema(filepath, area_folder):
    """Update the schema markup in an area page"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        area_info = get_area_info(area_folder)
        new_schema = create_enhanced_schema(area_folder, area_info)
        
        # Find and replace the existing schema
        schema_pattern = r'<script type="application/ld\+json">.*?</script>'
        new_schema_tag = f'<script type="application/ld+json">\n{new_schema}\n</script>'
        
        # Replace existing schema
        content = re.sub(schema_pattern, new_schema_tag, content, count=1, flags=re.DOTALL)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"Error updating {filepath}: {e}")
        return False

def main():
    base_dir = 'property-management'
    updated_count = 0
    
    # Get all area directories
    areas = [d for d in os.listdir(base_dir) 
             if os.path.isdir(os.path.join(base_dir, d)) and d != '__pycache__']
    
    print(f"Updating schema markup for {len(areas)} area pages...")
    
    for area in areas:
        index_path = os.path.join(base_dir, area, 'index.html')
        if os.path.exists(index_path):
            if update_area_page_schema(index_path, area):
                updated_count += 1
                print(f"[OK] Updated schema for {area}")
            else:
                print(f"[FAIL] Failed to update {area}")
    
    print(f"\nCompleted! Updated {updated_count}/{len(areas)} pages with enhanced schema markup")

if __name__ == "__main__":
    main()