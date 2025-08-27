import xml.etree.ElementTree as ET
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

def validate_sitemap():
    """Validate all pages in sitemap.xml by checking if files exist locally."""
    
    # Parse sitemap
    sitemap_path = 'sitemap.xml'
    if not os.path.exists(sitemap_path):
        print(f"❌ Sitemap file not found: {sitemap_path}")
        return
    
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    
    # XML namespace for sitemap
    namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    
    # Extract all URLs
    urls = []
    for url_element in root.findall('ns:url', namespace):
        loc = url_element.find('ns:loc', namespace)
        if loc is not None:
            urls.append(loc.text)
    
    print(f"📋 Found {len(urls)} URLs in sitemap.xml")
    print("=" * 60)
    
    # Validation results
    valid_pages = []
    missing_pages = []
    errors = []
    
    # Base URL to strip
    base_url = "https://www.manage369.com"
    
    # Check each URL
    for i, url in enumerate(urls, 1):
        # Convert URL to local file path
        if url.startswith(base_url):
            path = url[len(base_url):]
            if path == "/":
                local_path = "index.html"
            elif path.endswith("/"):
                # Directory URLs should have index.html
                local_path = path[1:] + "index.html"
            elif not path.endswith(".html"):
                # Non-HTML paths might be directories
                local_path = path[1:] + "/index.html"
            else:
                local_path = path[1:]
            
            # Check if file exists
            if os.path.exists(local_path):
                valid_pages.append({
                    'url': url,
                    'path': local_path,
                    'size': os.path.getsize(local_path)
                })
                print(f"✅ [{i}/{len(urls)}] {path} → {local_path}")
            else:
                # Try alternative paths
                alt_paths = []
                if local_path.endswith("/index.html"):
                    # Try without trailing slash
                    alt_path = local_path[:-11] + ".html"
                    alt_paths.append(alt_path)
                
                found = False
                for alt_path in alt_paths:
                    if os.path.exists(alt_path):
                        valid_pages.append({
                            'url': url,
                            'path': alt_path,
                            'size': os.path.getsize(alt_path)
                        })
                        print(f"✅ [{i}/{len(urls)}] {path} → {alt_path} (alternative)")
                        found = True
                        break
                
                if not found:
                    missing_pages.append({
                        'url': url,
                        'expected_path': local_path
                    })
                    print(f"❌ [{i}/{len(urls)}] {path} → {local_path} NOT FOUND")
        else:
            errors.append({
                'url': url,
                'error': 'URL does not match expected base URL'
            })
            print(f"⚠️  [{i}/{len(urls)}] {url} - unexpected URL format")
    
    # Summary report
    print("\n" + "=" * 60)
    print("📊 VALIDATION SUMMARY")
    print("=" * 60)
    print(f"✅ Valid pages: {len(valid_pages)}/{len(urls)} ({len(valid_pages)*100//len(urls)}%)")
    print(f"❌ Missing pages: {len(missing_pages)}/{len(urls)} ({len(missing_pages)*100//len(urls)}%)")
    print(f"⚠️  Errors: {len(errors)}")
    
    # List missing pages
    if missing_pages:
        print("\n" + "=" * 60)
        print("❌ MISSING PAGES:")
        print("=" * 60)
        for page in missing_pages:
            print(f"  • {page['url']}")
            print(f"    Expected at: {page['expected_path']}")
    
    # List errors
    if errors:
        print("\n" + "=" * 60)
        print("⚠️  ERRORS:")
        print("=" * 60)
        for error in errors:
            print(f"  • {error['url']}")
            print(f"    {error['error']}")
    
    # File size statistics
    if valid_pages:
        total_size = sum(p['size'] for p in valid_pages)
        avg_size = total_size // len(valid_pages)
        print("\n" + "=" * 60)
        print("📁 FILE STATISTICS:")
        print("=" * 60)
        print(f"  Total size: {total_size:,} bytes ({total_size//1024:,} KB)")
        print(f"  Average file size: {avg_size:,} bytes")
        
        # Find largest and smallest files
        valid_pages.sort(key=lambda x: x['size'])
        print(f"\n  Smallest file: {valid_pages[0]['path']} ({valid_pages[0]['size']:,} bytes)")
        print(f"  Largest file: {valid_pages[-1]['path']} ({valid_pages[-1]['size']:,} bytes)")
    
    # Save detailed report
    report_path = f"sitemap_validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"Sitemap Validation Report\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")
        
        f.write(f"SUMMARY:\n")
        f.write(f"Total URLs: {len(urls)}\n")
        f.write(f"Valid: {len(valid_pages)}\n")
        f.write(f"Missing: {len(missing_pages)}\n")
        f.write(f"Errors: {len(errors)}\n\n")
        
        if missing_pages:
            f.write("MISSING PAGES:\n")
            for page in missing_pages:
                f.write(f"  {page['url']}\n")
                f.write(f"    Expected: {page['expected_path']}\n")
        
        if errors:
            f.write("\nERRORS:\n")
            for error in errors:
                f.write(f"  {error['url']}: {error['error']}\n")
    
    print(f"\n💾 Detailed report saved to: {report_path}")
    
    return {
        'total': len(urls),
        'valid': len(valid_pages),
        'missing': len(missing_pages),
        'errors': len(errors)
    }

if __name__ == "__main__":
    print("🔍 Starting Sitemap Validation...")
    print("=" * 60)
    result = validate_sitemap()
    print("\n✨ Validation complete!")