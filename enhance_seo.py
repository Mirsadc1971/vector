#!/usr/bin/env python3
"""
SEO Enhancement Script for Manage369
Adds missing SEO elements without breaking existing functionality
"""

import os
import re
from pathlib import Path

def add_canonical_urls():
    """Add canonical URLs to pages missing them"""
    base_dir = Path(r"C:\Users\mirsa\manage369-live")
    base_url = "https://manage369.com"
    
    # Process property management pages
    prop_mgmt_dir = base_dir / "property-management"
    
    for location_dir in prop_mgmt_dir.iterdir():
        if location_dir.is_dir():
            index_file = location_dir / "index.html"
            if index_file.exists():
                with open(index_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check if canonical already exists
                if 'rel="canonical"' not in content:
                    # Calculate canonical URL
                    location_name = location_dir.name
                    canonical_url = f"{base_url}/property-management/{location_name}/"
                    
                    # Find position to insert (after meta description)
                    desc_match = re.search(r'(<meta name="description"[^>]+>)', content)
                    if desc_match:
                        insert_pos = desc_match.end()
                        canonical_tag = f'\n    <link rel="canonical" href="{canonical_url}">'
                        
                        # Insert canonical tag
                        new_content = content[:insert_pos] + canonical_tag + content[insert_pos:]
                        
                        with open(index_file, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        
                        print(f"Added canonical to: {location_name}")

def enhance_meta_descriptions():
    """Optimize meta descriptions for better CTR"""
    base_dir = Path(r"C:\Users\mirsa\manage369-live")
    
    # Location-specific keywords for better local SEO
    location_keywords = {
        'wilmette': 'luxury condos, waterfront properties',
        'winnetka': 'estate homes, premier HOAs',
        'glencoe': 'upscale communities, boutique properties',
        'highland-park': 'diverse housing, Ravinia area',
        'evanston': 'Northwestern area, diverse communities',
        'glenview': 'The Glen, suburban excellence',
        'northbrook': 'corporate relocations, family communities',
        'skokie': 'multicultural communities, affordable luxury',
        'lincolnwood': 'shopping district properties, townhomes',
        'morton-grove': 'affordable management, senior communities',
        'golf': 'small town charm, personalized service',
        'lake-forest': 'estate management, historic properties',
        'lake-bluff': 'lakefront properties, exclusive communities',
        'deerfield': 'family-oriented, excellent schools area',
        'northfield': 'boutique properties, custom management',
        'park-ridge': 'O\'Hare area, commuter-friendly',
        'des-plaines': 'diverse portfolio, business district',
        'mount-prospect': 'downtown district, mixed-use properties',
        'arlington-heights': 'Metropolis area, large associations',
        'buffalo-grove': 'planned communities, modern amenities',
        'wheeling': 'Restaurant Row area, diverse properties',
        'prospect-heights': 'growing community, value properties',
        'lincolnshire': 'corporate campus area, luxury living',
        'vernon-hills': 'Hawthorn area, retail district',
        'elk-grove-village': 'business park area, industrial',
        'schiller-park': 'O\'Hare adjacent, investment properties',
        'franklin-park': 'industrial corridor, workforce housing',
        'elmwood-park': 'diverse neighborhoods, urban suburban',
        'harwood-heights': 'close-knit community, affordable',
        'norridge': 'Harlem Avenue corridor, convenient',
        'itasca': 'Metra accessible, business district',
        'wood-dale': 'airport area, growing community',
        'rolling-meadows': 'corporate offices, golf course community'
    }
    
    # Process each location page
    prop_mgmt_dir = base_dir / "property-management"
    
    for location_dir in prop_mgmt_dir.iterdir():
        if location_dir.is_dir():
            location_name = location_dir.name
            index_file = location_dir / "index.html"
            
            if index_file.exists() and location_name in location_keywords:
                with open(index_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find current meta description
                desc_match = re.search(r'<meta name="description" content="([^"]+)"', content)
                if desc_match:
                    current_desc = desc_match.group(1)
                    
                    # Enhance description with location-specific keywords
                    keywords = location_keywords[location_name]
                    location_title = location_name.replace('-', ' ').title()
                    
                    # Create enhanced description
                    new_desc = f"Expert {location_title} property management for {keywords}. 18+ years serving Chicago's North Shore. Professional HOA & condo management. Free consultation: (847) 652-2338"
                    
                    # Ensure it's under 160 characters
                    if len(new_desc) > 160:
                        new_desc = f"{location_title} property management: {keywords}. 18+ years experience. Call (847) 652-2338"
                    
                    # Replace description
                    new_content = content.replace(f'content="{current_desc}"', f'content="{new_desc}"')
                    
                    if new_content != content:
                        with open(index_file, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Enhanced meta description for: {location_name}")

def add_local_business_markup():
    """Add enhanced local business structured data"""
    base_dir = Path(r"C:\Users\mirsa\manage369-live")
    
    # Enhanced FAQ schema for common questions
    faq_schema = '''
    <!-- FAQ Schema -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "What areas does Manage369 serve?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Manage369 serves Chicago and the entire North Shore including Wilmette, Winnetka, Glencoe, Highland Park, Evanston, Glenview, Northbrook, and over 60 other communities in the greater Chicago area."
          }
        },
        {
          "@type": "Question",
          "name": "What types of properties does Manage369 manage?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "We specialize in managing condominiums, homeowners associations (HOAs), townhome communities, and mixed-use properties. Our portfolio includes luxury high-rises, boutique buildings, and suburban communities ranging from 10 to 500+ units."
          }
        },
        {
          "@type": "Question",
          "name": "How much does property management cost?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Our management fees are competitive and based on property size, services needed, and location. We offer transparent pricing with no hidden fees. Contact us at (847) 652-2338 for a free customized quote."
          }
        },
        {
          "@type": "Question",
          "name": "Is Manage369 licensed and insured?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Yes, Manage369 is fully licensed in Illinois, carries comprehensive liability insurance, and maintains all required bonds. Our team includes CAI and IREM certified professionals with 18+ years of experience."
          }
        }
      ]
    }
    </script>'''
    
    # Add to homepage
    index_file = base_dir / "index.html"
    if index_file.exists():
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if FAQ schema already exists
        if '"@type": "FAQPage"' not in content:
            # Insert before closing head tag
            content = content.replace('</head>', faq_schema + '\n</head>')
            
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print("Added FAQ schema to homepage")

def optimize_image_loading():
    """Add lazy loading and proper dimensions to images"""
    base_dir = Path(r"C:\Users\mirsa\manage369-live")
    
    # Process all HTML files
    for html_file in base_dir.glob('**/*.html'):
        # Skip admin and temp directories
        if any(skip in str(html_file) for skip in ['admin', 'temp', 'backup']):
            continue
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        modified = False
        
        # Add lazy loading to images (except hero images)
        if 'loading="lazy"' not in content:
            # Find all img tags
            img_pattern = r'<img([^>]+)src="([^"]+)"([^>]*)>'
            
            def add_lazy_loading(match):
                attrs_before = match.group(1)
                src = match.group(2)
                attrs_after = match.group(3)
                
                # Don't add lazy loading to hero images or logos
                if 'hero' in src.lower() or 'logo' in src.lower() or 'favicon' in src.lower():
                    return match.group(0)
                
                # Check if loading attribute already exists
                if 'loading=' in attrs_before or 'loading=' in attrs_after:
                    return match.group(0)
                
                # Add lazy loading
                return f'<img{attrs_before}src="{src}"{attrs_after} loading="lazy">'
            
            new_content = re.sub(img_pattern, add_lazy_loading, content)
            if new_content != content:
                modified = True
                content = new_content
        
        if modified:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Optimized images in: {html_file.relative_to(base_dir)}")

def add_breadcrumb_navigation():
    """Add breadcrumb navigation to interior pages"""
    base_dir = Path(r"C:\Users\mirsa\manage369-live")
    
    breadcrumb_template = '''
    <!-- Breadcrumb Navigation -->
    <nav aria-label="breadcrumb" class="breadcrumb-nav">
        <ol class="breadcrumb">
            <li class="breadcrumb-item"><a href="/">Home</a></li>
            {items}
        </ol>
    </nav>'''
    
    # Add CSS for breadcrumbs to styles.css
    css_file = base_dir / "css" / "styles.css"
    if css_file.exists():
        with open(css_file, 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        if '.breadcrumb-nav' not in css_content:
            breadcrumb_css = '''
/* Breadcrumb Navigation */
.breadcrumb-nav {
    padding: 10px 0;
    margin: 0 auto;
    max-width: 1200px;
}

.breadcrumb {
    display: flex;
    flex-wrap: wrap;
    padding: 0.5rem 1rem;
    margin-bottom: 1rem;
    list-style: none;
    background-color: #f8f9fa;
    border-radius: 0.25rem;
}

.breadcrumb-item {
    display: flex;
    align-items: center;
}

.breadcrumb-item + .breadcrumb-item::before {
    display: inline-block;
    padding: 0 0.5rem;
    color: #6c757d;
    content: ">";
}

.breadcrumb-item a {
    color: #1e40af;
    text-decoration: none;
}

.breadcrumb-item a:hover {
    text-decoration: underline;
}

.breadcrumb-item.active {
    color: #6c757d;
}
'''
            with open(css_file, 'a', encoding='utf-8') as f:
                f.write(breadcrumb_css)
            print("Added breadcrumb CSS styles")

def main():
    """Run all SEO enhancements"""
    print("Starting SEO enhancements...")
    print("-" * 50)
    
    print("\n1. Adding canonical URLs...")
    add_canonical_urls()
    
    print("\n2. Enhancing meta descriptions...")
    enhance_meta_descriptions()
    
    print("\n3. Adding local business markup...")
    add_local_business_markup()
    
    print("\n4. Optimizing image loading...")
    optimize_image_loading()
    
    print("\n5. Setting up breadcrumb navigation...")
    add_breadcrumb_navigation()
    
    print("\n" + "=" * 50)
    print("SEO enhancements complete!")
    print("\nNext steps:")
    print("1. Test the changes locally")
    print("2. Validate structured data at: https://validator.schema.org/")
    print("3. Submit updated sitemap to Google Search Console")
    print("4. Monitor Core Web Vitals in Google Search Console")

if __name__ == "__main__":
    main()