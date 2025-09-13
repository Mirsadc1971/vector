#!/usr/bin/env python3
"""
Fix Google Analytics to truly delay loading until after page is fully loaded
"""

import re

# Read index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove ALL existing Google Analytics implementations
# Pattern to match the entire optimized block
pattern = r'<!-- Optimized Google Analytics.*?</script>'
content = re.sub(pattern, '', content, flags=re.DOTALL)

# Also remove any remaining gtag references
content = re.sub(r'<script[^>]*googletagmanager\.com/gtag[^>]*>.*?</script>', '', content, flags=re.DOTALL)

# Add the TRULY delayed version right before </body>
new_analytics = '''<!-- Ultra-Delayed Google Analytics - Loads after 5 seconds or user interaction -->
<script>
(function() {
  let analyticsLoaded = false;

  function loadAnalytics() {
    if (analyticsLoaded) return;
    analyticsLoaded = true;

    // Create and inject the script
    const script = document.createElement('script');
    script.async = true;
    script.defer = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=G-LCX4DTB57C';

    script.onload = function() {
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-LCX4DTB57C', {
        'send_page_view': true,
        'transport_type': 'beacon'
      });
    };

    document.body.appendChild(script);
  }

  // Only load after DOM is fully ready and page has been idle
  if (document.readyState === 'complete') {
    setTimeout(loadAnalytics, 5000);
  } else {
    window.addEventListener('load', function() {
      setTimeout(loadAnalytics, 5000);
    });
  }

  // Also load on any user interaction (as backup)
  let interactionEvents = ['scroll', 'click', 'touchstart', 'mousemove'];
  interactionEvents.forEach(function(event) {
    window.addEventListener(event, function() {
      setTimeout(loadAnalytics, 100);
    }, {once: true, passive: true});
  });
})();
</script>
</body>'''

# Replace </body> with analytics + </body>
content = content.replace('</body>', new_analytics)

# Write back
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed Google Analytics to load after 5 seconds minimum")