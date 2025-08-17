import os
import re
from pathlib import Path
import json

def analyze_page_content(file_path):
    """Analyze a single page for quality signals"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # Extract key elements
        title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
        title = title_match.group(1).strip() if title_match else ''
        
        meta_desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html, re.IGNORECASE)
        meta_desc = meta_desc_match.group(1) if meta_desc_match else ''
        
        # Remove scripts, styles, and HTML tags for word count
        text_content = html
        text_content = re.sub(r'<script.*?</script>', '', text_content, flags=re.IGNORECASE | re.DOTALL)
        text_content = re.sub(r'<style.*?</style>', '', text_content, flags=re.IGNORECASE | re.DOTALL)
        text_content = re.sub(r'<!--.*?-->', '', text_content, flags=re.DOTALL)
        text_content = re.sub(r'<[^>]+>', '', text_content)
        text_content = ' '.join(text_content.split())
        
        word_count = len(text_content.split())
        
        # Count important elements
        h1_count = len(re.findall(r'<h1[^>]*>', html, re.IGNORECASE))
        h2_count = len(re.findall(r'<h2[^>]*>', html, re.IGNORECASE))
        img_count = len(re.findall(r'<img[^>]*>', html, re.IGNORECASE))
        
        # Check for alt text on images
        images = re.findall(r'<img[^>]*>', html, re.IGNORECASE)
        images_without_alt = sum(1 for img in images if 'alt=' not in img.lower())
        
        # Count internal and external links
        links = re.findall(r'href=["\'](.*?)["\']', html, re.IGNORECASE)
        internal_links = sum(1 for link in links if not link.startswith('http') and not link.startswith('mailto:') and not link.startswith('tel:'))
        external_links = sum(1 for link in links if link.startswith('http'))
        
        # Check for structured data
        has_schema = 'application/ld+json' in html or 'itemscope' in html
        
        # Check for Open Graph tags
        has_og = 'property="og:' in html
        
        # Check viewport meta
        has_viewport = 'viewport' in html.lower()
        
        return {
            'file': str(file_path).replace('\\', '/'),
            'title': title,
            'title_length': len(title),
            'meta_description': meta_desc,
            'meta_desc_length': len(meta_desc),
            'word_count': word_count,
            'h1_count': h1_count,
            'h2_count': h2_count,
            'img_count': img_count,
            'images_without_alt': images_without_alt,
            'internal_links': internal_links,
            'external_links': external_links,
            'has_schema': has_schema,
            'has_og': has_og,
            'has_viewport': has_viewport
        }
    except Exception as e:
        return None

def evaluate_page_quality(page_data):
    """Evaluate page quality and identify issues"""
    issues = []
    score = 100
    
    # Title checks
    if not page_data['title']:
        issues.append("CRITICAL: Missing title tag")
        score -= 20
    elif page_data['title_length'] < 30:
        issues.append("Title too short (< 30 chars)")
        score -= 10
    elif page_data['title_length'] > 60:
        issues.append("Title too long (> 60 chars)")
        score -= 5
    
    # Meta description checks
    if not page_data['meta_description']:
        issues.append("CRITICAL: Missing meta description")
        score -= 15
    elif page_data['meta_desc_length'] < 120:
        issues.append("Meta description too short (< 120 chars)")
        score -= 10
    elif page_data['meta_desc_length'] > 160:
        issues.append("Meta description too long (> 160 chars)")
        score -= 5
    
    # Content checks
    if page_data['word_count'] < 300:
        issues.append(f"CRITICAL: Thin content ({page_data['word_count']} words < 300)")
        score -= 25
    elif page_data['word_count'] < 500:
        issues.append(f"Low content ({page_data['word_count']} words < 500)")
        score -= 10
    
    # Structure checks
    if page_data['h1_count'] == 0:
        issues.append("Missing H1 tag")
        score -= 10
    elif page_data['h1_count'] > 1:
        issues.append(f"Multiple H1 tags ({page_data['h1_count']})")
        score -= 5
    
    if page_data['h2_count'] == 0 and page_data['word_count'] > 300:
        issues.append("No H2 tags for content structure")
        score -= 5
    
    # Image checks
    if page_data['images_without_alt'] > 0:
        issues.append(f"{page_data['images_without_alt']} images missing alt text")
        score -= 5
    
    # Link checks
    if page_data['internal_links'] < 3:
        issues.append("Low internal linking (< 3 links)")
        score -= 10
    
    # Technical SEO
    if not page_data['has_schema']:
        issues.append("No structured data (Schema.org)")
        score -= 5
    
    if not page_data['has_og']:
        issues.append("Missing Open Graph tags")
        score -= 5
    
    if not page_data['has_viewport']:
        issues.append("Missing viewport meta tag")
        score -= 10
    
    return {
        'score': max(0, score),
        'issues': issues,
        'is_indexable': score >= 50 and page_data['word_count'] >= 300
    }

def analyze_all_pages():
    """Analyze all HTML pages for quality"""
    print("=" * 70)
    print("PAGE QUALITY ANALYSIS REPORT")
    print("=" * 70)
    
    # Categories for pages
    thin_content_pages = []
    poor_meta_pages = []
    low_quality_pages = []
    good_pages = []
    
    # Get all HTML files
    html_files = list(Path('.').glob('**/*.html'))
    analyzed_count = 0
    
    print(f"\nAnalyzing {len(html_files)} HTML files for quality signals...")
    print("-" * 40)
    
    for file_path in html_files:
        # Skip certain directories
        if any(skip in str(file_path) for skip in ['node_modules', '.git', 'stellar-repo', 'tinggi', 'forms-BACKUP']):
            continue
        
        # Skip template and error pages
        file_name = os.path.basename(str(file_path))
        if file_name in ['404.html', '500.html', 'perfect-footer.html']:
            continue
        
        analyzed_count += 1
        page_data = analyze_page_content(file_path)
        
        if not page_data:
            continue
        
        quality = evaluate_page_quality(page_data)
        page_data['quality_score'] = quality['score']
        page_data['issues'] = quality['issues']
        page_data['is_indexable'] = quality['is_indexable']
        
        # Categorize pages
        if page_data['word_count'] < 300:
            thin_content_pages.append(page_data)
        elif not page_data['meta_description'] or page_data['meta_desc_length'] < 120:
            poor_meta_pages.append(page_data)
        elif quality['score'] < 60:
            low_quality_pages.append(page_data)
        else:
            good_pages.append(page_data)
    
    # Report findings
    print(f"\n[SUMMARY]")
    print("-" * 40)
    print(f"Total pages analyzed: {analyzed_count}")
    print(f"High quality pages: {len(good_pages)}")
    print(f"Thin content pages: {len(thin_content_pages)}")
    print(f"Poor meta descriptions: {len(poor_meta_pages)}")
    print(f"Low quality pages: {len(low_quality_pages)}")
    
    # Detailed reports
    print(f"\n[CRITICAL: THIN CONTENT PAGES] ({len(thin_content_pages)} pages)")
    print("-" * 40)
    print("These pages have < 300 words and likely won't be indexed:")
    for page in thin_content_pages[:10]:
        print(f"\n{page['file']}")
        print(f"  Words: {page['word_count']}")
        print(f"  Quality Score: {page['quality_score']}/100")
        print(f"  Main issues: {', '.join(page['issues'][:3])}")
    
    print(f"\n[POOR META DESCRIPTIONS] ({len(poor_meta_pages)} pages)")
    print("-" * 40)
    for page in poor_meta_pages[:10]:
        print(f"\n{page['file']}")
        print(f"  Meta length: {page['meta_desc_length']} chars")
        print(f"  Current: {page['meta_description'][:50]}..." if page['meta_description'] else "  Missing meta description")
    
    print(f"\n[LOW QUALITY PAGES] ({len(low_quality_pages)} pages)")
    print("-" * 40)
    for page in low_quality_pages[:10]:
        print(f"\n{page['file']}")
        print(f"  Quality Score: {page['quality_score']}/100")
        print(f"  Issues: {', '.join(page['issues'][:3])}")
    
    return thin_content_pages, poor_meta_pages, low_quality_pages, good_pages

def generate_improvements():
    """Generate improvement recommendations"""
    print("\n" + "=" * 70)
    print("PAGE QUALITY IMPROVEMENT RECOMMENDATIONS")
    print("=" * 70)
    
    improvements = {
        "IMMEDIATE ACTIONS": [
            "Add 300+ words of unique content to thin pages",
            "Write compelling meta descriptions (120-160 chars)",
            "Add missing H1 tags to structure content",
            "Include 3+ internal links per page",
            "Add alt text to all images"
        ],
        "CONTENT ENHANCEMENTS": [
            "Expand property management pages to 500+ words",
            "Add local area information and statistics",
            "Include service benefits and features",
            "Add customer testimonials or case studies",
            "Create FAQ sections for common questions"
        ],
        "TECHNICAL IMPROVEMENTS": [
            "Add Schema.org structured data to all pages",
            "Implement Open Graph tags for social sharing",
            "Ensure all pages have viewport meta tag",
            "Add breadcrumb navigation",
            "Optimize images with descriptive file names"
        ],
        "META DESCRIPTION FORMULA": [
            "Start with action verb (Discover, Get, Learn)",
            "Include location (Chicago, North Shore)",
            "Mention key benefit or USP",
            "Add call-to-action",
            "Include phone number when relevant"
        ]
    }
    
    for category, items in improvements.items():
        print(f"\n[{category}]")
        print("-" * 40)
        for item in items:
            print(f"  • {item}")
    
    # Sample improved meta descriptions
    print("\n[SAMPLE IMPROVED META DESCRIPTIONS]")
    print("-" * 40)
    
    samples = [
        {
            'page': 'property-management/glenview/',
            'meta': 'Expert Glenview property management since 2006. Professional condo & HOA services, 24/7 support, transparent pricing. Call (847) 652-2338 for free consultation.'
        },
        {
            'page': 'services/hoa-management/',
            'meta': 'Professional HOA management in Chicago & North Shore. Board support, financial management, vendor coordination. 50+ communities managed. Get quote: (847) 652-2338'
        },
        {
            'page': 'contact.html',
            'meta': 'Contact Manage369 property management experts. Serving Chicago & North Shore with 18+ years experience. Available 24/7. Call (847) 652-2338 or email today.'
        }
    ]
    
    for sample in samples:
        print(f"\n{sample['page']}")
        print(f"  {sample['meta']}")
        print(f"  Length: {len(sample['meta'])} chars")

# Run analysis
if __name__ == "__main__":
    thin, poor_meta, low_quality, good = analyze_all_pages()
    generate_improvements()
    
    print("\n" + "=" * 70)
    print("INDEXABILITY ASSESSMENT")
    print("=" * 70)
    
    likely_not_indexed = len(thin) + len(low_quality)
    print(f"\nPages likely NOT indexed by Google: {likely_not_indexed}")
    print(f"Main reasons:")
    print(f"  1. Thin content (< 300 words): {len(thin)} pages")
    print(f"  2. Low quality signals: {len(low_quality)} pages")
    print(f"  3. Poor/missing meta descriptions: {len(poor_meta)} pages")
    print(f"\nEstimated indexable pages after fixes: {len(good) + len(poor_meta)}")