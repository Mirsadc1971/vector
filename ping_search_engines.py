#!/usr/bin/env python3
"""
Ping search engines to notify them of sitemap updates
"""

import urllib.parse
import urllib.request
import sys

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

def ping_search_engines():
    """Ping Google and Bing with sitemap URL"""
    
    sitemap_url = "https://www.manage369.com/sitemap.xml"
    
    # Search engine ping URLs
    ping_urls = {
        "Google": f"https://www.google.com/ping?sitemap={urllib.parse.quote(sitemap_url)}",
        "Bing": f"https://www.bing.com/ping?sitemap={urllib.parse.quote(sitemap_url)}"
    }
    
    print("🔔 Pinging search engines with updated sitemap...")
    print("=" * 60)
    
    for engine, url in ping_urls.items():
        try:
            print(f"📡 Pinging {engine}...")
            response = urllib.request.urlopen(url, timeout=10)
            if response.status == 200:
                print(f"✅ {engine}: Successfully notified")
            else:
                print(f"⚠️  {engine}: Received status code {response.status}")
        except Exception as e:
            print(f"❌ {engine}: Failed - {str(e)}")
    
    print("\n" + "=" * 60)
    print("✨ Search engine notification complete!")
    print("\nNote: It may take time for search engines to process the updates.")
    print("You can also manually submit your sitemap at:")
    print("  • Google: https://search.google.com/search-console")
    print("  • Bing: https://www.bing.com/webmasters")

if __name__ == "__main__":
    ping_search_engines()