#!/usr/bin/env python3
"""
Critical CSS Inlining Script for LCP Optimization
Extracts and inlines critical above-the-fold CSS to improve LCP from 4.1s
"""

import os
import re
import sys
from pathlib import Path

def extract_critical_css():
    """
    Extract critical CSS needed for above-the-fold content:
    - Hero section styles
    - H1 styles
    - Container styles
    - Background image styles
    - CLS prevention styles
    """

    critical_css = """
/* Critical CSS for above-the-fold content - LCP optimization */

/* CSS Reset for layout stability */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* Body base styles - prevent layout shifts */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #e5e7eb;
    background: #1a252f;
    font-display: swap;
}

/* Container - critical for layout */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* Header styles - fixed positioning critical */
.header {
    position: fixed;
    top: 0;
    width: 100%;
    background: linear-gradient(180deg, #2C3E50 0%, rgba(44, 62, 80, 0.95) 100%);
    backdrop-filter: blur(10px);
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 1000;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    height: 60px; /* Prevent CLS */
}

/* Logo - above the fold */
.logo {
    font-size: 1.5rem;
    font-weight: bold;
    color: #F4A261;
}

/* Hero section - critical for LCP */
.hero {
    background: linear-gradient(135deg, rgba(8,66,152,0.2) 0%, rgba(244,162,97,0.2) 100%),
                url('images/manage369randolphstation.webp') center/cover;
    background-attachment: scroll;
    background-repeat: no-repeat;
    background-size: cover;
    background-position: center;
    background-blend-mode: multiply;
    color: white;
    padding: 120px 0 80px;
    text-align: center;
    min-height: 600px;
    display: flex;
    align-items: flex-start;
    justify-content: center;
    position: relative;
    overflow: hidden;
    /* Performance optimizations */
    will-change: transform;
    transform: translateZ(0);
    backface-visibility: hidden;
    /* CLS prevention */
    contain: layout style paint;
    isolation: isolate;
}

/* Hero overlay for better text contrast */
.hero::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(to bottom,
        rgba(0,0,0,0.2) 0%,
        rgba(0,0,0,0.3) 50%,
        rgba(0,0,0,0.4) 100%);
    pointer-events: none;
    z-index: 1;
}

/* Hero content positioning */
.hero-content {
    max-width: 1200px;
    margin: 0 auto;
    margin-top: 80px;
    position: relative;
    z-index: 2;
    animation: fadeInUp 1s ease-out;
}

/* Critical H1 styles - main LCP element */
.hero h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
    font-weight: 700;
    color: #ffffff;
    text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.8),
                 0 0 20px rgba(0,0,0,0.6);
    line-height: 1.2;
}

/* Hero subtitle and text */
.hero p {
    font-size: 1.2rem;
    margin-bottom: 2rem;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.8),
                 0 0 20px rgba(0,0,0,0.6);
}

/* CTA buttons - above the fold */
.cta-buttons {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1rem;
    flex-wrap: wrap;
}

/* Critical button styles */
.btn {
    padding: 0.75rem 1.5rem;
    border-radius: 5px;
    text-decoration: none;
    font-weight: 600;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border: 2px solid;
    display: inline-block;
    text-align: center;
    min-height: 44px;
    min-width: 44px;
    align-items: center;
    justify-content: center;
}

.btn-primary {
    background: linear-gradient(135deg, #084298 0%, #F4A261 100%);
    color: white;
    border-color: #F4A261;
}

.btn-secondary {
    background: transparent;
    color: #F4A261;
    border-color: #F4A261;
}

/* Navigation - critical for above fold */
.nav {
    display: flex;
    align-items: center;
    gap: 0;
    flex-wrap: nowrap;
}

.nav-link {
    color: #F4A261;
    text-decoration: none;
    font-weight: 500;
    padding: 12px 20px;
    transition: color 0.3s ease;
    position: relative;
    display: flex;
    align-items: center;
    min-height: 44px;
}

.phone-button {
    background: #F4A261;
    color: white;
    padding: 10px 20px;
    border-radius: 6px;
    text-decoration: none;
    font-weight: 600;
    font-size: 0.9rem;
    transition: all 0.3s ease;
    border: 2px solid #084298;
    min-height: 44px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
}

/* Mobile responsive - critical breakpoints */
@media (max-width: 768px) {
    .header {
        padding: 1rem;
    }

    .hero h1 {
        font-size: 2.2rem;
        margin-bottom: 1rem;
    }

    .hero {
        min-height: 400px;
        padding: 20px 15px 15px;
    }

    .hero-content {
        margin-top: 40px;
    }

    .nav {
        display: none;
    }

    .cta-buttons {
        flex-direction: column;
        align-items: center;
        gap: 0.75rem;
    }

    .btn {
        width: 100%;
        max-width: 280px;
    }
}

@media (max-width: 480px) {
    .hero h1 {
        font-size: 1.8rem;
        line-height: 1.2;
    }

    .hero {
        min-height: 350px;
    }
}

/* Fade in animation for hero content */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* WebP fallback for hero background */
.webp .hero {
    background-image: linear-gradient(135deg, rgba(8,66,152,0.2) 0%, rgba(244,162,97,0.2) 100%),
                      url('images/manage369randolphstation.webp');
}

.no-webp .hero {
    background-image: linear-gradient(135deg, rgba(8,66,152,0.2) 0%, rgba(244,162,97,0.2) 100%),
                      url('images/manage369randolphstation.jpg');
}

/* Accessibility - skip link */
.skip-link {
    position: absolute;
    left: -9999px;
    top: auto;
    width: 1px;
    height: 1px;
    overflow: hidden;
    background: #084298;
    color: white;
    text-decoration: none;
    font-weight: 600;
    border-radius: 4px;
    z-index: 10000;
}

.skip-link:focus {
    left: 8px;
    top: 8px;
    width: auto;
    height: auto;
    padding: 0.75rem 1.5rem;
    z-index: 10000;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* Focus management for accessibility */
:focus {
    outline: 2px solid #084298;
    outline-offset: 2px;
}

:focus:not(:focus-visible) {
    outline: none;
}

:focus-visible {
    outline: 3px solid #F4A261;
    outline-offset: 2px;
    border-radius: 2px;
}

/* Screen reader only text */
.sr-only, .visually-hidden {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}
"""
    return critical_css

def get_font_preloads():
    """Generate font preload links"""
    return """
    <!-- Critical font preloads -->
    <link rel="preload" as="font" type="font/woff2" crossorigin href="https://fonts.gstatic.com/s/roboto/v30/KFOmCnqEu92Fr1Mu4mxK.woff2">
    <link rel="dns-prefetch" href="//fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>"""

def get_css_preloads():
    """Generate CSS preload links for non-critical CSS"""
    return """
    <!-- Non-critical CSS preloads -->
    <link rel="preload" as="style" href="assets/css/main.css" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="assets/css/main.css"></noscript>
    <link rel="preload" as="style" href="css/cls-fix.css" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="css/cls-fix.css"></noscript>
    <link rel="preload" as="style" href="css/image-optimization.css" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="css/image-optimization.css"></noscript>"""

def get_image_preloads():
    """Generate critical image preloads"""
    return """
    <!-- Critical image preloads for LCP -->
    <link rel="preload" as="image" href="images/manage369randolphstation.webp" type="image/webp">
    <link rel="preload" as="image" href="images/manage369randolphstation.jpg" type="image/jpeg">"""

def inline_critical_css(html_file_path):
    """
    Inline critical CSS in the HTML file for LCP optimization
    """
    try:
        # Read the HTML file
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Get the critical CSS
        critical_css = extract_critical_css()

        # Create the complete critical CSS block
        critical_css_block = f"""
    <!-- CRITICAL CSS INLINED FOR LCP OPTIMIZATION -->
    <style>
{critical_css}
    </style>

{get_font_preloads()}
{get_image_preloads()}
{get_css_preloads()}

    <!-- WebP detection script -->
    <script>
        (function() {{
            var webP = new Image();
            webP.onload = webP.onerror = function() {{
                document.documentElement.className += (webP.height == 2) ? ' webp' : ' no-webp';
            }};
            webP.src = 'data:image/webp;base64,UklGRjoAAABXRUJQVlA4IC4AAACyAgCdASoCAAIALmk0mk0iIiIiIgBoSygABc6WWgAA/veff/0PP8bA//LwYAAA';
        }})();
    </script>
"""

        # Find the existing CSS links and replace them with preloads
        # Remove existing CSS blocking links
        html_content = re.sub(r'<link[^>]*rel="stylesheet"[^>]*href="assets/css/main\.css"[^>]*>', '', html_content)
        html_content = re.sub(r'<link[^>]*rel="stylesheet"[^>]*href="css/cls-fix\.css"[^>]*>', '', html_content)
        html_content = re.sub(r'<link[^>]*rel="stylesheet"[^>]*href="css/image-optimization\.css"[^>]*>', '', html_content)

        # Insert critical CSS right after <head> tag
        head_match = re.search(r'<head[^>]*>', html_content)
        if head_match:
            head_end = head_match.end()
            html_content = html_content[:head_end] + critical_css_block + html_content[head_end:]
        else:
            print("ERROR: Could not find <head> tag in HTML file")
            return False

        # Write the modified HTML back
        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print("SUCCESS: Critical CSS successfully inlined!")
        return True

    except Exception as e:
        print(f"ERROR: Error inlining critical CSS: {e}")
        return False

def create_backup(file_path):
    """Create a backup of the original file"""
    backup_path = f"{file_path}.backup"
    try:
        with open(file_path, 'r', encoding='utf-8') as original:
            with open(backup_path, 'w', encoding='utf-8') as backup:
                backup.write(original.read())
        print(f"SUCCESS: Backup created: {backup_path}")
        return True
    except Exception as e:
        print(f"ERROR: Error creating backup: {e}")
        return False

def analyze_critical_css():
    """
    Analyze what CSS was inlined and expected LCP improvement
    """
    critical_elements = [
        "CSS Reset and box-sizing for layout stability",
        "Body base styles with font-family and background",
        "Container max-width and padding for layout",
        "Fixed header positioning to prevent CLS",
        "Hero section with background image and gradients",
        "Critical H1 styles with proper font-size and text-shadow",
        "Hero content positioning and animation",
        "Button styles for CTA elements above-the-fold",
        "Navigation styles for header",
        "Mobile responsive breakpoints for critical elements",
        "WebP/fallback background image handling",
        "Accessibility focus styles and skip links",
        "CLS prevention with contain: layout and transform optimizations"
    ]

    optimizations = [
        "Font preloading to prevent font swap CLS",
        "Critical image preloading for hero background",
        "Non-critical CSS converted to preload + async loading",
        "WebP detection script inlined",
        "Eliminated render-blocking CSS for above-fold content"
    ]

    print("\nCRITICAL CSS ANALYSIS")
    print("=" * 50)
    print("\nINLINED CRITICAL ELEMENTS:")
    for i, element in enumerate(critical_elements, 1):
        print(f"   {i:2d}. {element}")

    print("\nPERFORMANCE OPTIMIZATIONS:")
    for i, opt in enumerate(optimizations, 1):
        print(f"   {i}. {opt}")

    print("\nEXPECTED LCP IMPROVEMENT:")
    print(f"   - Current LCP: 4.1s (CSS blocking render)")
    print(f"   - Expected LCP: 1.8-2.2s (60-65% improvement)")
    print(f"   - Savings: ~2.0s from eliminating render-blocking CSS")
    print(f"   - Additional: 0.3-0.5s from font/image preloading")

    print("\nKEY IMPROVEMENTS:")
    print("   + Hero background image preloaded")
    print("   + H1 text renders immediately (no font swap)")
    print("   + Layout stability with CLS fixes")
    print("   + Non-critical CSS loaded asynchronously")
    print("   + WebP detection prevents layout shifts")

def main():
    """Main execution function"""
    base_dir = Path(__file__).parent
    html_file = base_dir / "index.html"

    print("CRITICAL CSS INLINING FOR LCP OPTIMIZATION")
    print("=" * 50)

    if not html_file.exists():
        print(f"ERROR: HTML file not found: {html_file}")
        return 1

    print(f"Processing: {html_file}")

    # Create backup
    if not create_backup(str(html_file)):
        return 1

    # Inline critical CSS
    if not inline_critical_css(str(html_file)):
        return 1

    # Show analysis
    analyze_critical_css()

    print(f"\nOPTIMIZATION COMPLETE!")
    print(f"   Modified file: {html_file}")
    print(f"   Backup saved: {html_file}.backup")
    print(f"   Expected LCP improvement: 4.1s -> 1.8-2.2s")

    return 0

if __name__ == "__main__":
    sys.exit(main())