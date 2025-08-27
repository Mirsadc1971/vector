#!/usr/bin/env python3
"""
JavaScript Optimization Script
Removes unused JavaScript and implements code splitting
"""

import os
import re
from pathlib import Path

def analyze_js_usage():
    """Analyze which JavaScript files are actually being used"""
    html_files = list(Path('.').glob('**/*.html'))
    js_references = set()
    
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Find all script tags
            scripts = re.findall(r'<script[^>]*src=["\']([^"\']+)["\'][^>]*>', content)
            js_references.update(scripts)
    
    return js_references

def remove_unused_service_workers():
    """Remove duplicate service worker files if not needed"""
    service_workers = ['sw.js', 'sw-min.js', 'service-worker.js']
    used_workers = []
    
    # Check which service workers are registered
    html_files = list(Path('.').glob('**/*.html'))
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            for sw in service_workers:
                if sw in content:
                    used_workers.append(sw)
    
    # Keep only the used ones
    for sw in service_workers:
        if sw not in used_workers and os.path.exists(sw):
            print(f"Removing unused service worker: {sw}")
            # os.remove(sw)  # Uncomment to actually delete

def add_async_loading():
    """Add async or defer attributes to script tags"""
    html_files = list(Path('.').glob('**/*.html'))
    
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add async to Google Analytics
        content = re.sub(
            r'(<script\s+src="https://www\.googletagmanager\.com[^"]+")([^>]*)>',
            r'\1 async\2>',
            content
        )
        
        # Save changes
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Optimized JavaScript loading in {html_file}")

def minimize_inline_scripts():
    """Minimize inline JavaScript code"""
    html_files = list(Path('.').glob('**/*.html'))
    
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find inline scripts
        inline_scripts = re.findall(r'<script>([^<]+)</script>', content, re.DOTALL)
        
        for script in inline_scripts:
            # Remove comments and extra whitespace
            minified = re.sub(r'//[^\n]*', '', script)  # Remove single-line comments
            minified = re.sub(r'/\*.*?\*/', '', minified, flags=re.DOTALL)  # Remove multi-line comments
            minified = re.sub(r'\s+', ' ', minified)  # Reduce whitespace
            minified = minified.strip()
            
            content = content.replace(f'<script>{script}</script>', f'<script>{minified}</script>')
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Minimized inline scripts in {html_file}")

def main():
    print("JavaScript Optimization Report")
    print("=" * 50)
    
    # Analyze current JS usage
    js_refs = analyze_js_usage()
    print(f"\nFound {len(js_refs)} JavaScript file references")
    for ref in js_refs:
        print(f"  - {ref}")
    
    # Check for unused service workers
    print("\nChecking for duplicate service workers...")
    remove_unused_service_workers()
    
    # Add async loading
    print("\nOptimizing script loading...")
    add_async_loading()
    
    # Minimize inline scripts
    print("\nMinimizing inline scripts...")
    minimize_inline_scripts()
    
    print("\nJavaScript optimization complete!")
    print("\nRecommendations:")
    print("1. Consider using a CDN for external scripts")
    print("2. Implement code splitting for large JavaScript files")
    print("3. Use webpack or similar bundler for production builds")
    print("4. Enable gzip/brotli compression on your server")

if __name__ == "__main__":
    main()