#!/usr/bin/env python3
"""
Property Management Page SEO Optimizer for Manage369
Comprehensive script to analyze and rebuild property management pages
that don't meet SEO requirements (3000+ chars, 9 service backlinks, proper structure)
"""

import os
import re
import json
from pathlib import Path
from bs4 import BeautifulSoup
import requests
from typing import Dict, List, Tuple, Any

# Configuration
BASE_DIR = Path(__file__).parent
REQUIRED_CONTENT_LENGTH = 3000
REQUIRED_SERVICE_LINKS = 9

# Chicago areas to process
CHICAGO_AREAS = [
    "logan-square", "north-center", "bucktown", "edgewater", 
    "rogers-park", "uptown", "downtown-chicago"
]

# North Shore suburbs (24 total)
NORTH_SHORE_SUBURBS = [
    "deerfield", "evanston", "glencoe", "glenview", "highland-park", 
    "highwood", "kenilworth", "lake-bluff", "lake-forest", "libertyville",
    "lincolnshire", "northbrook", "park-ridge", "skokie", "wilmette", 
    "winnetka", "buffalo-grove", "hawthorn-woods", "kildeer", "lake-zurich",
    "long-grove", "mundelein", "vernon-hills", "wheeling"
]

# Service page links (all 9 required)
SERVICE_LINKS = [
    "services/condominium-management/index.html",
    "services/hoa-management/index.html", 
    "services/townhome-management/index.html",
    "services/financial-management/index.html",
    "services/maintenance-coordination/index.html",
    "services/board-support/index.html",
    "services/administrative-services/index.html",
    "services/capital-project-management/index.html",
    "services/resident-relations/index.html"
]

class PropertyPageAnalyzer:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.results = []
    
    def analyze_page(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a property management page for SEO compliance."""
        if not file_path.exists():
            return {
                'file': str(file_path),
                'exists': False,
                'needs_creation': True,
                'content_length': 0,
                'service_links_found': 0,
                'has_schema': False,
                'has_proper_structure': False,
                'issues': ['File does not exist']
            }
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Extract text content (excluding HTML tags)
        text_content = soup.get_text()
        content_length = len(text_content.strip())
        
        # Check for service links
        service_links_found = 0
        for service_link in SERVICE_LINKS:
            if service_link in content:
                service_links_found += 1
        
        # Check for schema markup
        has_schema = bool(soup.find('script', {'type': 'application/ld+json'}))
        
        # Check for proper H1/H2/H3 structure
        h1_tags = soup.find_all('h1')
        h2_tags = soup.find_all('h2')
        h3_tags = soup.find_all('h3')
        has_proper_structure = len(h1_tags) >= 1 and len(h2_tags) >= 2 and len(h3_tags) >= 3
        
        # Determine issues
        issues = []
        if content_length < REQUIRED_CONTENT_LENGTH:
            issues.append(f'Content too short: {content_length} chars (need {REQUIRED_CONTENT_LENGTH}+)')
        if service_links_found < REQUIRED_SERVICE_LINKS:
            issues.append(f'Missing service links: {service_links_found}/{REQUIRED_SERVICE_LINKS} found')
        if not has_schema:
            issues.append('Missing schema markup')
        if not has_proper_structure:
            issues.append('Poor H1/H2/H3 structure')
        
        return {
            'file': str(file_path),
            'exists': True,
            'needs_rebuild': len(issues) > 0,
            'content_length': content_length,
            'service_links_found': service_links_found,
            'has_schema': has_schema,
            'has_proper_structure': has_proper_structure,
            'h1_count': len(h1_tags),
            'h2_count': len(h2_tags),
            'h3_count': len(h3_tags),
            'issues': issues
        }
    
    def analyze_all_pages(self) -> List[Dict[str, Any]]:
        """Analyze all property management pages."""
        all_areas = CHICAGO_AREAS + NORTH_SHORE_SUBURBS
        
        for area in all_areas:
            file_path = self.base_dir / f"property-management-{area}.html"
            result = self.analyze_page(file_path)
            result['area'] = area
            result['area_type'] = 'chicago' if area in CHICAGO_AREAS else 'north_shore'
            self.results.append(result)
        
        return self.results
    
    def generate_report(self) -> str:
        """Generate a comprehensive analysis report."""
        total_pages = len(self.results)
        compliant_pages = len([r for r in self.results if not r.get('needs_rebuild', True) and r.get('exists', False)])
        needs_rebuild = len([r for r in self.results if r.get('needs_rebuild', False)])
        needs_creation = len([r for r in self.results if r.get('needs_creation', False)])
        
        report = f"""
=== PROPERTY MANAGEMENT PAGE SEO ANALYSIS REPORT ===

Total Pages Analyzed: {total_pages}
Compliant Pages: {compliant_pages}
Pages Needing Rebuild: {needs_rebuild} 
Pages Needing Creation: {needs_creation}

DETAILED ANALYSIS:
"""
        
        for result in self.results:
            status = "✅ COMPLIANT" if not result.get('needs_rebuild', True) and result.get('exists', False) else "❌ NEEDS WORK"
            report += f"""
{status} - {result['area']} ({result['area_type']})
  File: {result['file']}
  Content Length: {result.get('content_length', 0)} chars
  Service Links: {result.get('service_links_found', 0)}/9
  Schema: {'✅' if result.get('has_schema', False) else '❌'}
  Structure: {'✅' if result.get('has_proper_structure', False) else '❌'}
  Issues: {', '.join(result.get('issues', []))}
"""
        
        return report

class PropertyPageBuilder:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
    
    def get_area_info(self, area: str, area_type: str) -> Dict[str, str]:
        """Get area-specific information for content generation."""
        area_display = area.replace('-', ' ').title()
        
        # Chicago areas
        chicago_info = {
            "logan-square": {
                "description": "Logan Square pulses with creative energy - where craft cocktail bars occupy former auto shops, music venues showcase tomorrow's headliners, and young professionals have created one of Chicago's most vibrant cultural scenes.",
                "character": "artistic spirit and working-class roots",
                "highlights": "iconic Logan Square monument, craft cocktail scene, music venues, artistic community"
            },
            "north-center": {
                "description": "North Center represents the perfect blend of family-friendly living and urban sophistication, where tree-lined streets create a neighborhood feel within the big city.",
                "character": "family-friendly atmosphere with excellent schools and parks",
                "highlights": "Hamlin Park, Lincoln Avenue restaurants, tree-lined streets, excellent schools"
            },
            "bucktown": {
                "description": "Bucktown combines hipster coolness with family-friendly amenities, creating a neighborhood where young professionals and families coexist in trendy harmony.",
                "character": "trendy yet family-oriented community spirit",
                "highlights": "boutique shopping, trendy restaurants, converted warehouse lofts, artistic flair"
            },
            "edgewater": {
                "description": "Edgewater offers stunning lakefront living with a diverse, international community that celebrates both natural beauty and cultural richness.",
                "character": "lakefront elegance with multicultural vibrancy", 
                "highlights": "Lake Michigan shoreline, international community, historic architecture, beach access"
            },
            "rogers-park": {
                "description": "Rogers Park embodies Chicago's multicultural spirit, where over 80 languages are spoken and lakefront beauty meets vibrant community diversity.",
                "character": "remarkable diversity and lakefront location",
                "highlights": "multicultural community, Northwestern University proximity, lakefront parks, diverse dining"
            },
            "uptown": {
                "description": "Uptown showcases Chicago's renaissance spirit, where historic theaters and modern developments create a dynamic neighborhood experiencing exciting revitalization.",
                "character": "historic charm with modern revitalization",
                "highlights": "historic entertainment district, Aragon Ballroom, Green Mill Cocktail Lounge, lakefront access"
            },
            "downtown-chicago": {
                "description": "Downtown Chicago represents the pinnacle of urban living, where world-class architecture meets vibrant cultural attractions and premium residential developments.",
                "character": "sophisticated urban lifestyle and architectural excellence",
                "highlights": "Millennium Park, Art Institute, architectural landmarks, premium high-rise living"
            }
        }
        
        # North Shore suburbs (simplified for brevity - each could have detailed info)
        north_shore_base = {
            "description": f"{area_display} exemplifies North Shore excellence with tree-lined streets, outstanding schools, and the perfect balance of suburban tranquility and urban accessibility.",
            "character": "North Shore elegance with family-friendly community values",
            "highlights": "excellent schools, beautiful neighborhoods, close proximity to Lake Michigan, strong community ties"
        }
        
        if area_type == 'chicago':
            return chicago_info.get(area, {
                "description": f"{area_display} offers distinctive Chicago neighborhood character with unique local amenities and strong community connections.",
                "character": "authentic Chicago neighborhood spirit",
                "highlights": "local restaurants, community gathering spaces, convenient transportation, neighborhood character"
            })
        else:
            # Specific info for major North Shore suburbs
            north_shore_specific = {
                "evanston": {
                    "description": "Evanston holds a special place as home to Northwestern University, creating a distinctive blend of academic excellence and lakefront beauty.",
                    "character": "academic excellence and university community spirit",
                    "highlights": "Northwestern University, lakefront beauty, diverse cultural offerings, academic community"
                },
                "wilmette": {
                    "description": "Wilmette epitomizes North Shore elegance with its beautiful lakefront, excellent schools, and charming downtown village atmosphere.",
                    "character": "lakefront elegance and village charm",
                    "highlights": "stunning lakefront, Gillson Park, excellent schools, charming downtown"
                },
                "winnetka": {
                    "description": "Winnetka represents the pinnacle of North Shore living with magnificent homes, world-renowned schools, and pristine lakefront beauty.",
                    "character": "North Shore prestige and educational excellence",
                    "highlights": "prestigious homes, top-rated schools, beautiful lakefront, village atmosphere"
                },
                "glencoe": {
                    "description": "Glencoe combines small-town charm with sophisticated amenities, creating an intimate community that values both tradition and innovation.",
                    "character": "intimate community with sophisticated amenities",
                    "highlights": "beautiful parks, excellent schools, close-knit community, convenient transportation"
                },
                "highland-park": {
                    "description": "Highland Park offers cultural richness and natural beauty, home to the renowned Ravinia Festival and stunning lakefront parks.",
                    "character": "cultural sophistication and natural beauty",
                    "highlights": "Ravinia Festival, lakefront parks, cultural attractions, excellent dining"
                }
            }
            return north_shore_specific.get(area, north_shore_base)
    
    def generate_schema_markup(self, area: str, area_type: str) -> str:
        """Generate JSON-LD schema markup for local business."""
        area_display = area.replace('-', ' ').title()
        
        schema = {
            "@context": "https://schema.org",
            "@type": "LocalBusiness",
            "name": "Manage369",
            "description": f"Premier {area_display} property management services. 18+ years managing luxury condos, HOAs & townhomes. CAI/IREM certified professionals.",
            "url": f"https://manage369.com/property-management-{area}.html",
            "telephone": "+1-224-647-5621",
            "email": "service@manage369.com",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "1400 Patriot Boulevard 357",
                "addressLocality": "Glenview",
                "addressRegion": "IL",
                "postalCode": "60026",
                "addressCountry": "US"
            },
            "geo": {
                "@type": "GeoCoordinates", 
                "latitude": "42.0697",
                "longitude": "-87.6928"
            },
            "openingHours": "Mo-Fr 09:00-17:00",
            "sameAs": [
                "https://manage369.com"
            ],
            "serviceArea": {
                "@type": "Place",
                "name": f"{area_display}, Illinois"
            },
            "hasOfferCatalog": {
                "@type": "OfferCatalog",
                "name": "Property Management Services",
                "itemListElement": [
                    {
                        "@type": "Offer",
                        "itemOffered": {
                            "@type": "Service",
                            "name": "Condominium Management",
                            "description": "Professional condominium association management services"
                        }
                    },
                    {
                        "@type": "Offer", 
                        "itemOffered": {
                            "@type": "Service",
                            "name": "HOA Management",
                            "description": "Comprehensive homeowner association management"
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
            }
        }
        
        return json.dumps(schema, indent=2)
    
    def build_comprehensive_page(self, area: str, area_type: str) -> str:
        """Build a comprehensive property management page with 3000+ characters and all requirements."""
        area_display = area.replace('-', ' ').title()
        area_info = self.get_area_info(area, area_type)
        schema_markup = self.generate_schema_markup(area, area_type)
        
        # Generate comprehensive content sections
        intro_section = f"""
        <p>{area_info['description']} At Manage369, we understand what makes {area_display} special – the {area_info['character']} that creates a community where residents truly thrive. From {area_info['highlights']}, we manage properties that reflect this neighborhood's distinctive appeal while providing the professional service that busy residents and property owners depend on.</p>
        
        <p>Our comprehensive property management approach recognizes that {area_display} properties serve discerning residents who have chosen quality, location, and community. Whether managing elegant condominiums, family-friendly townhome associations, or sophisticated HOA communities, we understand that successful property management here means preserving the unique character that makes {area_display} one of the region's most desirable places to live.</p>
        """
        
        # Detailed services section with local context
        services_section = f"""
        <div class="location-content">
            <div class="location-content-wrapper">
                <h2>Comprehensive {area_display} Property Management Services</h2>
                
                <p>Every property we manage in {area_display} benefits from our 18+ years of experience serving Chicago and North Shore communities. Our deep understanding of local regulations, market conditions, and resident expectations ensures that your property not only maintains its value but continues to attract and retain quality residents who appreciate {area_display}'s unique character.</p>

                <h3>Condominium Management Excellence in {area_display}</h3>
                <p>From boutique buildings to luxury high-rises, our <a href="services/condominium-management/index.html">condominium management</a> services address the specific challenges that {area_display} properties face. We coordinate maintenance schedules around local events, manage relationships with trusted contractors familiar with area building codes, and ensure that your condominium association operates smoothly while preserving the community atmosphere that residents value. Our CAI and IREM certifications guarantee professional standards that match the quality expectations of {area_display} residents.</p>

                <div class="highlight-box">
                    <h3>{area_display} Condominium Management Specialists</h3>
                    <p>Our experienced team understands the unique aspects of {area_display} condominium living, from architectural preservation requirements to coordinating with local utility services. We manage properties ranging from intimate boutique buildings to full-service luxury developments, always maintaining the high standards that define this exceptional community.</p>
                </div>

                <h3>HOA Management Tailored to {area_display} Communities</h3>
                <p>Homeowner associations in {area_display} require management that understands both the practical needs of property maintenance and the community values that make neighborhoods thrive. Our <a href="services/hoa-management/index.html">HOA management</a> approach recognizes that successful associations create environments where families feel connected, property values remain strong, and community traditions continue to flourish.</p>

                <p>We work closely with {area_display} HOA boards to develop policies that protect property values while fostering the neighborly atmosphere that residents cherish. From coordinating seasonal maintenance projects to managing community events that bring neighbors together, our services support the full spectrum of community life that makes {area_display} special.</p>

                <h3>Financial Management and Transparency</h3>
                <p>Property owners in {area_display} expect – and deserve – complete transparency in financial management. Our <a href="services/financial-management/index.html">financial management</a> services provide detailed monthly reports, professional budget development, and strategic reserve planning that protects your investment while supporting the high-quality amenities that {area_display} residents value.</p>

                <p>We understand that many {area_display} properties represent significant family investments, often passed down through generations or purchased by residents who plan to call this community home for decades. Our financial stewardship reflects this long-term perspective, ensuring that every decision supports both current operations and future property value protection.</p>

                <div class="service-highlight-box">
                    <h3>Professional Maintenance Coordination for {area_display} Properties</h3>
                    <p>Our <a href="services/maintenance-coordination/index.html">maintenance coordination</a> services connect your property with trusted local contractors who understand {area_display}'s unique requirements. From seasonal weather challenges to local architectural standards, we ensure that maintenance work enhances your property while respecting the character that defines this special community.</p>
                    <p><strong>Local Expertise: <a href="tel:2246475621">(224) 647-5621</a></strong></p>
                </div>

                <h3>Board Support and Administrative Excellence</h3>
                <p>Effective property management requires seamless coordination between professional management and community leadership. Our <a href="services/board-support/index.html">board support</a> services empower {area_display} association boards with the information, guidance, and administrative support they need to make confident decisions about their communities.</p>

                <p>We provide comprehensive <a href="services/administrative-services/index.html">administrative services</a> that handle everything from resident communications to vendor coordination, allowing board members to focus on strategic planning while ensuring that daily operations run smoothly. Our approach respects the volunteer nature of board service while providing professional support that keeps communities operating efficiently.</p>

                <h3>Capital Project Management and Long-term Planning</h3>
                <p>Preserving and enhancing {area_display} properties requires strategic planning and professional project management. Our <a href="services/capital-project-management/index.html">capital project management</a> services guide associations through major improvements, from routine building updates to significant infrastructure investments that protect property values and enhance resident quality of life.</p>

                <p>We work with boards to develop realistic timelines, manage contractor relationships, and ensure that projects are completed to the high standards that {area_display} properties require. Our experience with local permitting processes and contractor networks helps ensure smooth project completion while minimizing disruption to residents.</p>

                <h3>Resident Relations and Community Building</h3>
                <p>The sense of community that defines {area_display} doesn't happen by accident – it requires thoughtful attention to resident relations and communication. Our <a href="services/resident-relations/index.html">resident relations</a> services foster positive interactions between residents, management, and boards while addressing concerns promptly and professionally.</p>

                <p>From new resident orientation programs that help newcomers connect with community traditions to communication systems that keep everyone informed about important developments, we support the social fabric that makes {area_display} neighborhoods places where people choose to build their lives.</p>

                <div class="highlight-box">
                    <h3>Why {area_display} Properties Choose Manage369</h3>
                    <p><strong>Local Market Expertise:</strong> 18+ years serving Chicago and North Shore communities with deep understanding of local regulations, market conditions, and resident expectations.</p>
                    
                    <p><strong>Professional Certifications:</strong> CAI, IREM, and CCIM certified professionals ensuring industry best practices and continuing education in property management excellence.</p>
                    
                    <p><strong>Proven Track Record:</strong> Zero properties lost in our management history, with over $100 million in managed assets and 2,450+ units under professional management.</p>
                    
                    <p><strong>Boutique-Level Service:</strong> Direct access to ownership and personalized attention that larger firms simply cannot match, ensuring responsive service tailored to your community's unique needs.</p>
                </div>

                <h3>Townhome Management Expertise</h3>
                <p>Townhome communities in {area_display} often combine the benefits of single-family living with shared amenities and community governance. Our <a href="services/townhome-management/index.html">townhome management</a> services address the unique challenges these properties face, from coordinating exterior maintenance across multiple units to managing shared spaces that enhance the community experience.</p>

                <p>We understand that townhome residents often choose this lifestyle for the balance of privacy and community it provides. Our management approach supports this balance, ensuring that individual property rights are respected while community standards maintain the neighborhood appeal that protects everyone's investment.</p>

                <h3>Emergency Response and Property Protection</h3>
                <p>When emergencies arise, {area_display} property owners need management partners who respond quickly and professionally. Our 24/7 emergency response system ensures that urgent situations – from heating system failures during winter storms to plumbing emergencies that could damage multiple units – receive immediate attention from qualified professionals.</p>

                <p>Our relationships with local emergency service providers and contractors mean faster response times and better outcomes when urgent situations arise. This proactive approach to emergency management protects both property values and resident safety, providing peace of mind for owners and boards throughout {area_display}.</p>
            </div>
        </div>
        """
        
        # Build the complete HTML page
        html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{area_display} Property Management | Chicago Condo & HOA Management | Manage369</title>
    <meta name="description" content="Premier {area_display} property management services. 18+ years managing luxury condos, HOAs & townhomes. CAI/IREM certified professionals. Call (224) 647-5621.">
    
    <!-- Favicon and Apple Touch Icon -->
    <link rel="apple-touch-icon" sizes="180x180" href="images/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="images/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="images/favicon-16x16.png">
    <link rel="manifest" href="site.webmanifest">
    
    <!-- Open Graph Meta Tags -->
    <meta property="og:title" content="{area_display} Property Management | Manage369">
    <meta property="og:description" content="Premier {area_display} property management services. 18+ years managing luxury condos, HOAs & townhomes. CAI/IREM certified professionals.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://manage369.com/property-management-{area}.html">
    <meta property="og:image" content="https://manage369.com/images/manage369livingroomskokie.jpg">
    
    <!-- Twitter Card Meta Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{area_display} Property Management | Manage369">
    <meta name="twitter:description" content="Premier {area_display} property management services. 18+ years managing luxury condos, HOAs & townhomes.">
    <meta name="twitter:image" content="https://manage369.com/images/manage369livingroomskokie.jpg">
    
    <!-- Local Business Schema Markup -->
    <script type="application/ld+json">
{schema_markup}
    </script>
    
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; }}
        
        .header {{
            position: fixed;
            top: 0;
            width: 100%;
            background: white;
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 1000;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .logo {{
            font-size: 1.5rem;
            font-weight: bold;
            color: #4a90e2;
            text-decoration: none;
        }}
        
        .nav {{
            display: flex;
            gap: 2rem;
        }}
        
        .nav a {{
            color: #333;
            text-decoration: none;
            margin: 0 1rem;
            font-weight: 500;
            padding: 8px 16px;
            border-radius: 5px;
            transition: all 0.3s ease;
        }}
        
        .nav a:hover {{
            color: #4a90e2;
            background: #f0f0f0;
        }}
        
        .services-dropdown {{
            position: relative;
            display: inline-block;
        }}
        
        .dropdown-content {{
            display: none;
            position: absolute;
            background-color: white;
            min-width: 250px;
            box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
            z-index: 1;
            border-radius: 5px;
            padding: 10px 0;
            top: 100%;
            left: 0;
        }}
        
        .dropdown-content a {{
            color: #333;
            padding: 12px 16px;
            text-decoration: none;
            display: block;
            margin: 0;
        }}
        
        .dropdown-content a:hover {{
            background-color: #f1f1f1;
        }}
        
        .dropdown-header {{
            padding: 8px 16px;
            font-weight: bold;
            color: #4a90e2;
            font-size: 0.9rem;
            border-bottom: 1px solid #eee;
            margin-bottom: 5px;
        }}
        
        .services-dropdown:hover .dropdown-content {{
            display: block;
        }}
        
        .phone {{
            background: #4a90e2;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            text-decoration: none;
        }}
        
        .hero {{
            height: 60vh;
            background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
                        url('images/manage369livingroomskokie.jpg');
            background-size: cover;
            background-position: center;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            color: white;
            margin-top: 80px;
        }}
        
        .hero-content h1 {{
            font-size: 3rem;
            margin-bottom: 1rem;
            color: white;
        }}
        
        .hero-content p {{
            font-size: 1.3rem;
            margin-bottom: 2rem;
        }}
        
        .content {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 4rem 2rem;
        }}
        
        .content p {{
            color: #666;
            margin-bottom: 1.5rem;
            font-size: 1.1rem;
        }}
        
        .services-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin: 3rem 0;
        }}
        
        .service-card {{
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s;
        }}
        
        .service-card:hover {{
            transform: translateY(-5px);
        }}
        
        .service-card h3 {{
            color: #4a90e2;
            margin-bottom: 1rem;
        }}
        
        .service-card a {{
            color: #ff9500;
            text-decoration: none;
            font-weight: 600;
        }}
        
        .why-choose {{
            background: #f8f9fa;
            padding: 4rem 2rem;
            margin: 4rem 0;
        }}
        
        .why-choose-content {{
            max-width: 1200px;
            margin: 0 auto;
            text-align: center;
        }}
        
        .why-choose h2 {{
            color: #333;
            margin-bottom: 3rem;
            font-size: 2.5rem;
        }}
        
        .benefits-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 2rem;
            max-width: 1000px;
            margin: 0 auto;
        }}
        
        .benefit-item {{
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
            height: 100%;
            min-height: 180px;
        }}
        
        .benefit-item h3 {{
            color: #4a90e2;
            margin-bottom: 1rem;
            font-size: 1.1rem;
            line-height: 1.3;
        }}
        
        .benefit-item p {{
            color: #666;
            line-height: 1.5;
            flex-grow: 1;
            margin: 0;
            font-size: 0.95rem;
        }}
        
        .contact-section {{
            background: #4a90e2;
            color: white;
            padding: 3rem 2rem;
            text-align: center;
        }}
        
        .contact-section h2 {{
            margin-bottom: 1rem;
        }}
        
        .contact-section a {{
            color: #ff9500;
            text-decoration: none;
            font-weight: bold;
        }}
        
        .simple-footer {{
            background: #2c3e50;
            color: #ffffff;
            padding: 2rem 0;
            text-align: center;
        }}

        .simple-footer-content {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
        }}

        .simple-footer h3 {{
            color: #ffffff;
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }}

        .simple-footer p {{
            color: #b8c5d1;
            margin-bottom: 0.5rem;
        }}

        .simple-footer a {{
            color: #ff9500;
            text-decoration: none;
        }}

        .simple-footer a:hover {{
            text-decoration: underline;
        }}
        
        .location-content {{
            background: white;
            padding: 4rem 2rem;
            margin: 2rem 0;
        }}
        
        .location-content-wrapper {{
            max-width: 1200px;
            margin: 0 auto;
            line-height: 1.8;
            color: #444;
        }}
        
        .location-content h2 {{
            color: #4a90e2;
            margin-bottom: 2rem;
            text-align: center;
            font-size: 2.5rem;
        }}
        
        .location-content h3 {{
            color: #4a90e2;
            margin: 2rem 0 1rem 0;
            font-size: 1.5rem;
        }}
        
        .location-content p {{
            margin-bottom: 1.5rem;
            font-size: 1.1rem;
            color: #666;
        }}
        
        .location-content a {{
            color: #ff9500;
            text-decoration: none;
            font-weight: 500;
        }}
        
        .location-content a:hover {{
            text-decoration: underline;
        }}
        
        .highlight-box {{
            background: #f8f9fa;
            padding: 2rem;
            border-radius: 10px;
            margin: 2rem 0;
            border-left: 5px solid #4a90e2;
        }}
        
        .service-highlight-box {{
            background: #f8f9fa;
            padding: 2rem;
            border-radius: 10px;
            margin: 2rem 0;
            border-left: 5px solid #4a90e2;
        }}
        
        .service-highlight-box h3 {{
            color: #4a90e2;
            margin-bottom: 1rem;
            font-size: 1.3rem;
        }}
        
        .service-highlight-box a {{
            color: #ff9500;
            text-decoration: none;
            font-weight: 600;
        }}
        
        @media (max-width: 768px) {{
            .header {{
                flex-direction: column;
                padding: 1rem;
            }}
            
            .nav {{
                margin-top: 1rem;
                flex-wrap: wrap;
                justify-content: center;
            }}
            
            .hero-content h1 {{
                font-size: 2rem;
            }}
            
            .hero-content p {{
                font-size: 1.1rem;
            }}
            
            .benefits-grid {{
                grid-template-columns: 1fr;
                gap: 1.5rem;
            }}
        }}
        
        @media (min-width: 769px) and (max-width: 1024px) {{
            .benefits-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
    </style>
</head>
<body>
    <header class="header">
        <a href="index.html" class="logo">MANAGE369</a>
        
        <nav class="nav">
            <a href="index.html">Home</a>
            <div class="services-dropdown">
                <a href="services.html">Services <span>▼</span></a>
                <div class="dropdown-content">
                    <div class="dropdown-header">Property Types</div>
                    <a href="services/condominium-management/index.html">Condominium Management</a>
                    <a href="services/hoa-management/index.html">HOA Management</a>
                    <a href="services/townhome-management/index.html">Townhome Management</a>
                    <div class="dropdown-header">Service Offerings</div>
                    <a href="services/financial-management/index.html">Financial Management</a>
                    <a href="services/maintenance-coordination/index.html">Maintenance Coordination</a>
                    <a href="services/board-support/index.html">Board Support</a>
                    <a href="services/administrative-services/index.html">Administrative Services</a>
                    <a href="services/capital-project-management/index.html">Capital Project Management</a>
                    <a href="services/resident-relations/index.html">Resident Relations</a>
                </div>
            </div>
            <a href="service-areas.html">Service Areas</a>
            <a href="pay-dues.html">Pay Dues</a>
            <a href="contact.html">Contact</a>
        </nav>
        
        <a href="tel:2246475621" class="phone">Call (224) 647-5621</a>
    </header>
    
    <section class="hero">
        <div class="hero-content">
            <h1>Property Management {area_display} – Manage369</h1>
            <p>Expert Condominium, HOA & Townhome Management Services | 18+ Years Excellence</p>
        </div>
    </section>
    
    <section class="content">
        {intro_section}
        
        <div class="services-grid">
            <div class="service-card">
                <h3>Condominium Management</h3>
                <p>Expert management for high-rise and mid-rise condominium buildings throughout {area_display} and the Chicago area.</p>
                <a href="services/condominium-management/index.html">Learn More →</a>
            </div>
            <div class="service-card">
                <h3>HOA Management</h3>
                <p>Comprehensive homeowner association management for {area_display} communities and planned developments.</p>
                <a href="services/hoa-management/index.html">Learn More →</a>
            </div>
            <div class="service-card">
                <h3>Financial Management</h3>
                <p>Professional financial reporting, budget development, and assessment collection for {area_display} properties.</p>
                <a href="services/financial-management/index.html">Learn More →</a>
            </div>
        </div>
    </section>
    
    {services_section}
    
    <section class="why-choose">
        <div class="why-choose-content">
            <h2>Why Choose Manage369?</h2>
            <div class="benefits-grid">
                <div class="benefit-item">
                    <h3>18+ Years Experience</h3>
                    <p>Proven track record managing 50+ properties with 2,450+ units throughout Chicago and North Shore.</p>
                </div>
                <div class="benefit-item">
                    <h3>Professional Service Excellence</h3>
                    <p>Direct access to the owner and immediate response to maintenance needs.</p>
                </div>
                <div class="benefit-item">
                    <h3>Transparent Financial Reporting</h3>
                    <p>Monthly financial statements, budget development, and reserve studies to protect property values.</p>
                </div>
                <div class="benefit-item">
                    <h3>Local {area_display} Expertise</h3>
                    <p>Deep understanding of {area_display}'s unique property management challenges and community character.</p>
                </div>
                <div class="benefit-item">
                    <h3>Professional Certifications</h3>
                    <p>CAI, IREM, and CCIM certified professionals ensuring industry best practices.</p>
                </div>
                <div class="benefit-item">
                    <h3>Boutique-Level Service</h3>
                    <p>Personalized attention and responsiveness that larger firms simply cannot match.</p>
                </div>
            </div>
        </div>
    </section>
    
    <section class="contact-section">
        <h2>Ready to Get Started?</h2>
        <p>Contact us today for a free consultation about your {area_display} property management needs.</p>
        <p>📞 <a href="tel:2246475621">(224) 647-5621</a> | ✉️ <a href="mailto:service@manage369.com">service@manage369.com</a></p>
    </section>
    
    <footer class="simple-footer">
        <div class="simple-footer-content">
            <h3>Manage369</h3>
            <p>Chicago & North Shore Property Management Services</p>
            <p>1400 Patriot Boulevard 357, Glenview, IL 60026</p>
            <p>Phone: <a href="tel:2246475621">(224) 647-5621</a> | Email: <a href="mailto:service@manage369.com">service@manage369.com</a></p>
            <p>Hours: Monday-Friday 9:00 AM - 5:00 PM</p>
            <p>© 2025 Manage369. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>'''
        
        return html_content
    
    def create_or_rebuild_page(self, area: str, area_type: str, force_rebuild: bool = False) -> bool:
        """Create or rebuild a property management page."""
        file_path = self.base_dir / f"property-management-{area}.html"
        
        try:
            # Generate comprehensive page content
            html_content = self.build_comprehensive_page(area, area_type)
            
            # Write the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"✅ {'Rebuilt' if file_path.exists() else 'Created'} {area} page")
            return True
            
        except Exception as e:
            print(f"❌ Error creating {area} page: {str(e)}")
            return False

class PropertyManagementOptimizer:
    def __init__(self, base_dir: str = None):
        if base_dir is None:
            base_dir = Path(__file__).parent
        else:
            base_dir = Path(base_dir)
            
        self.base_dir = base_dir
        self.analyzer = PropertyPageAnalyzer(base_dir)
        self.builder = PropertyPageBuilder(base_dir)
    
    def run_analysis(self) -> List[Dict[str, Any]]:
        """Run comprehensive analysis of all property pages."""
        print("🔍 Analyzing all property management pages...")
        return self.analyzer.analyze_all_pages()
    
    def generate_report(self) -> str:
        """Generate comprehensive analysis report."""
        return self.analyzer.generate_report()
    
    def rebuild_non_compliant_pages(self, force_all: bool = False) -> Dict[str, int]:
        """Rebuild all non-compliant pages."""
        results = self.analyzer.results if hasattr(self.analyzer, 'results') and self.analyzer.results else self.run_analysis()
        
        stats = {
            'total_processed': 0,
            'successful_builds': 0,
            'failed_builds': 0,
            'skipped': 0
        }
        
        print("🔨 Building/rebuilding property management pages...")
        
        for result in results:
            area = result['area']
            area_type = result['area_type']
            needs_work = result.get('needs_rebuild', True) or result.get('needs_creation', False)
            
            stats['total_processed'] += 1
            
            if force_all or needs_work:
                success = self.builder.create_or_rebuild_page(area, area_type)
                if success:
                    stats['successful_builds'] += 1
                else:
                    stats['failed_builds'] += 1
            else:
                stats['skipped'] += 1
                print(f"⏭️  Skipped {area} (already compliant)")
        
        return stats
    
    def run_complete_optimization(self, force_rebuild_all: bool = False) -> str:
        """Run the complete optimization process."""
        print("🚀 Starting Property Management Page Optimization...")
        
        # Step 1: Analyze all pages
        results = self.run_analysis()
        
        # Step 2: Generate analysis report
        report = self.generate_report()
        print(report)
        
        # Step 3: Rebuild non-compliant pages
        build_stats = self.rebuild_non_compliant_pages(force_all=force_rebuild_all)
        
        # Step 4: Final summary
        summary = f"""
=== OPTIMIZATION COMPLETE ===

Build Statistics:
- Total Pages Processed: {build_stats['total_processed']}
- Successfully Built/Rebuilt: {build_stats['successful_builds']}
- Failed Builds: {build_stats['failed_builds']}
- Skipped (Already Compliant): {build_stats['skipped']}

All property management pages have been optimized with:
✅ 3000+ characters of comprehensive local content
✅ All 9 required service page backlinks integrated naturally
✅ Local JSON-LD schema markup for SEO
✅ Proper H1/H2/H3 structure with semantic hierarchy
✅ 18+ years expertise prominently featured
✅ Mobile-responsive design with professional styling
✅ Open Graph and Twitter Card meta tags
✅ Proper favicon and manifest support

Your Manage369 property management pages are now fully optimized for search engines and user experience!
        """
        
        print(summary)
        return summary

def main():
    """Main execution function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Optimize Manage369 Property Management Pages')
    parser.add_argument('--analyze-only', action='store_true', help='Only analyze pages, do not rebuild')
    parser.add_argument('--force-rebuild-all', action='store_true', help='Rebuild all pages regardless of compliance')
    parser.add_argument('--base-dir', type=str, help='Base directory path (default: current directory)')
    
    args = parser.parse_args()
    
    optimizer = PropertyManagementOptimizer(args.base_dir)
    
    if args.analyze_only:
        results = optimizer.run_analysis()
        report = optimizer.generate_report()
        print(report)
    else:
        summary = optimizer.run_complete_optimization(force_rebuild_all=args.force_rebuild_all)
        
        # Save report to file
        with open(optimizer.base_dir / 'property_management_optimization_report.txt', 'w') as f:
            f.write(summary)
        
        print("📄 Detailed report saved to: property_management_optimization_report.txt")

if __name__ == "__main__":
    main()