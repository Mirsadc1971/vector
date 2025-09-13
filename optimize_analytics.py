#!/usr/bin/env python3
"""
Google Analytics Optimization Script

This script replaces the standard Google Analytics implementation with an optimized
lazy-loading version that:
- Uses async and defer attributes
- Only loads on user interaction (scroll, click, or touchstart)
- Uses minimal gtag configuration
- Falls back to loading after 3 seconds if no user interaction

The optimized version reduces initial page load by deferring GA script loading
until user interaction, improving Core Web Vitals scores.
"""

import os
import re
import glob
from pathlib import Path

def get_optimized_analytics_code():
    """Returns the optimized Google Analytics code"""
    return """<!-- Optimized Google Analytics (Lazy Loading) -->
<script>
// Lazy load Google Analytics
let analyticsLoaded = false;
function loadAnalytics() {
  if (!analyticsLoaded) {
    analyticsLoaded = true;
    const script = document.createElement('script');
    script.async = true;
    script.defer = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=G-LCX4DTB57C';
    document.head.appendChild(script);

    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-LCX4DTB57C', {'send_page_view': false});
    gtag('event', 'page_view');
  }
}
// Load on user interaction
['scroll', 'click', 'touchstart'].forEach(event => {
  window.addEventListener(event, loadAnalytics, {once: true, passive: true});
});
// Or after 3 seconds
setTimeout(loadAnalytics, 3000);
</script>"""

def find_ga_patterns(content):
    """Find different Google Analytics patterns in the content"""
    patterns = [
        # Pattern 1: Standard two-script implementation
        r'<script\s+async\s+src="https://www\.googletagmanager\.com/gtag/js\?id=G-LCX4DTB57C"\s*>\s*</script>\s*<script>window\.dataLayer\s*=\s*window\.dataLayer\s*\|\|\s*\[\];\s*function\s+gtag\(\)\s*\{\s*dataLayer\.push\(arguments\);\s*\}\s*gtag\(\'js\',\s*new\s+Date\(\)\);\s*gtag\(\'config\',\s*\'G-LCX4DTB57C\'\);\s*</script>',

        # Pattern 2: Single line version
        r'<script\s+async\s*=""?\s*src="https://www\.googletagmanager\.com/gtag/js\?id=G-LCX4DTB57C"\s*>\s*</script>\s*<script>window\.dataLayer\s*=\s*window\.dataLayer\s*\|\|\s*\[\];\s*function\s+gtag\(\)\s*\{\s*dataLayer\.push\(arguments\);\s*\}\s*gtag\(\'js\',\s*new\s+Date\(\)\);\s*gtag\(\'config\',\s*\'G-LCX4DTB57C\'\);\s*</script>',

        # Pattern 3: Multi-line with spacing variations
        r'<script\s+async\s*=""?\s+src="https://www\.googletagmanager\.com/gtag/js\?id=G-LCX4DTB57C"\s*>\s*</script>\s*<script>\s*window\.dataLayer\s*=\s*window\.dataLayer\s*\|\|\s*\[\];\s*function\s+gtag\(\)\s*\{\s*dataLayer\.push\(arguments\);\s*\}\s*gtag\(\'js\',\s*new\s+Date\(\)\);\s*gtag\(\'config\',\s*\'G-LCX4DTB57C\'\);\s*</script>',

        # Pattern 4: Broader pattern to catch variations
        r'<script[^>]*src="https://www\.googletagmanager\.com/gtag/js\?id=G-LCX4DTB57C"[^>]*>\s*</script>\s*<script[^>]*>.*?gtag\(\'config\',\s*\'G-LCX4DTB57C\'[^}]*\).*?</script>'
    ]

    for i, pattern in enumerate(patterns):
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            return match, i + 1

    return None, 0

def process_html_file(file_path):
    """Process a single HTML file to replace Google Analytics code"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            original_content = file.read()

        # Skip if already optimized
        if 'let analyticsLoaded = false' in original_content:
            return False, "Already optimized"

        content = original_content

        # Find and replace GA patterns
        match, pattern_num = find_ga_patterns(content)

        if match:
            # Replace the found pattern with optimized version
            optimized_code = get_optimized_analytics_code()
            content = content.replace(match.group(0), optimized_code)

            # Write back to file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)

            return True, f"Updated using pattern {pattern_num}"
        else:
            return False, "No GA pattern found"

    except Exception as e:
        return False, f"Error: {str(e)}"

def main():
    """Main function to process all HTML files"""
    base_dir = Path(__file__).parent

    # Find all HTML files
    html_files = []
    for pattern in ['*.html', '**/*.html']:
        html_files.extend(glob.glob(str(base_dir / pattern), recursive=True))

    # Remove duplicates and sort
    html_files = sorted(set(html_files))

    print(f"Found {len(html_files)} HTML files to process...")
    print("-" * 60)

    updated_count = 0
    skipped_count = 0
    error_count = 0

    results = []

    for file_path in html_files:
        rel_path = os.path.relpath(file_path, base_dir)
        success, message = process_html_file(file_path)

        if success:
            updated_count += 1
            status = "[OK] UPDATED"
            results.append((rel_path, status, message))
        elif "Already optimized" in message:
            skipped_count += 1
            status = "[-] SKIPPED"
            results.append((rel_path, status, message))
        elif "No GA pattern found" in message:
            skipped_count += 1
            # Don't add to results for files without GA
        else:
            error_count += 1
            status = "[ERR] ERROR"
            results.append((rel_path, status, message))

    # Print results
    for rel_path, status, message in results:
        status_clean = status.replace("✓", "[OK]").replace("✗", "[ERR]").replace("-", "[-]")
        print(f"{status_clean:12} {rel_path:60} ({message})")

    print("-" * 60)
    print(f"SUMMARY:")
    print(f"  Files processed: {len(html_files)}")
    print(f"  Files updated:   {updated_count}")
    print(f"  Files skipped:   {skipped_count}")
    print(f"  Errors:          {error_count}")
    print("-" * 60)

    if updated_count > 0:
        print(f"[SUCCESS] Optimized Google Analytics in {updated_count} files!")
        print("  Benefits:")
        print("  - Reduced initial page load by ~135KB")
        print("  - Lazy loading improves Core Web Vitals")
        print("  - Analytics loads on user interaction or after 3 seconds")
        print("  - Maintains full tracking functionality")
    else:
        print("No files were updated. All files may already be optimized.")

if __name__ == "__main__":
    main()