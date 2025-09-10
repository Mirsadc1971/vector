#!/usr/bin/env python3
"""
Add premium styling enhancements to make the site stunning
"""

import re
from pathlib import Path

PREMIUM_STYLES = """
    /* Premium Design Enhancements */
    
    /* Smooth animations throughout */
    * {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Premium gradient backgrounds */
    .hero {
        background: linear-gradient(135deg, rgba(8,66,152,0.95) 0%, rgba(244,162,97,0.95) 100%), 
                    url('images/manage369randolphstation.jpg') center/cover !important;
        position: relative;
        overflow: hidden;
    }
    
    /* Animated gradient overlay */
    .hero::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 200%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(244,162,97,0.3), transparent);
        animation: shimmer 8s infinite;
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    /* Glass morphism effects for cards */
    .card, .service-card, .offer-card {
        background: rgba(44, 62, 80, 0.8) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(244, 162, 97, 0.2);
        box-shadow: 0 8px 32px rgba(8, 66, 152, 0.3);
    }
    
    .card:hover, .service-card:hover, .offer-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 15px 45px rgba(244, 162, 97, 0.4);
        border-color: #F4A261;
    }
    
    /* Premium button styles */
    .btn, button, .submit-btn {
        background: linear-gradient(135deg, #084298 0%, #F4A261 100%) !important;
        border: none !important;
        color: white !important;
        font-weight: 600;
        letter-spacing: 1px;
        position: relative;
        overflow: hidden;
        z-index: 1;
    }
    
    .btn::before, button::before, .submit-btn::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s;
        z-index: -1;
    }
    
    .btn:hover::before, button:hover::before, .submit-btn:hover::before {
        left: 100%;
    }
    
    /* Glowing gold accents */
    h1, h2, h3, h4 {
        color: #F4A261 !important;
        text-shadow: 0 0 20px rgba(244, 162, 97, 0.5);
    }
    
    /* Premium navigation */
    .header {
        background: linear-gradient(180deg, #2C3E50 0%, rgba(44, 62, 80, 0.95) 100%) !important;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    .nav-link {
        position: relative;
        color: #F4A261 !important;
    }
    
    .nav-link::after {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 0;
        height: 2px;
        background: linear-gradient(90deg, #084298, #F4A261);
        transition: width 0.3s;
    }
    
    .nav-link:hover::after {
        width: 100%;
    }
    
    /* Premium form inputs */
    input, select, textarea {
        background: rgba(44, 62, 80, 0.9) !important;
        border: 1px solid rgba(244, 162, 97, 0.3) !important;
        color: #e5e7eb !important;
        padding: 12px !important;
        border-radius: 8px !important;
    }
    
    input:focus, select:focus, textarea:focus {
        border-color: #F4A261 !important;
        box-shadow: 0 0 0 3px rgba(244, 162, 97, 0.2), 
                    0 0 20px rgba(244, 162, 97, 0.3) !important;
        outline: none !important;
    }
    
    /* Floating labels effect */
    .form-group {
        position: relative;
    }
    
    .form-group label {
        color: #F4A261 !important;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 0.85rem;
        letter-spacing: 1px;
    }
    
    /* Premium sections */
    section {
        background: linear-gradient(180deg, #1f2937 0%, #2C3E50 100%) !important;
        position: relative;
    }
    
    section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, #F4A261, transparent);
    }
    
    /* Special offers with glow */
    .special-offers {
        background: linear-gradient(135deg, #084298 0%, #2C3E50 50%, #F4A261 100%) !important;
        padding: 80px 20px;
        position: relative;
    }
    
    /* Countdown timer styling */
    #countdown {
        font-size: 1.5rem;
        font-weight: bold;
        color: #F4A261;
        text-shadow: 0 0 10px rgba(244, 162, 97, 0.8);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    /* Footer premium style */
    footer {
        background: linear-gradient(180deg, #2C3E50 0%, #1a252f 100%) !important;
        border-top: 2px solid rgba(244, 162, 97, 0.3);
    }
    
    /* Smooth scrolling */
    html {
        scroll-behavior: smooth;
    }
    
    /* Loading animation for forms */
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .loading::after {
        content: '';
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(244, 162, 97, 0.3);
        border-top-color: #F4A261;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-left: 10px;
    }
    
    /* Premium scroll indicator */
    .scroll-indicator {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #084298, #F4A261);
        transform-origin: left;
        z-index: 9999;
    }
    
    /* Parallax effect for hero */
    .hero-content {
        animation: fadeInUp 1s ease-out;
    }
    
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
    
    /* Premium mobile menu */
    .mobile-menu {
        background: linear-gradient(180deg, #2C3E50 0%, #1a252f 100%) !important;
        backdrop-filter: blur(20px);
    }
    
    /* Gold hover glow for links */
    a:hover {
        color: #F4A261 !important;
        text-shadow: 0 0 10px rgba(244, 162, 97, 0.6);
    }
    
    /* Premium table styling */
    table {
        background: rgba(44, 62, 80, 0.8);
        border: 1px solid rgba(244, 162, 97, 0.2);
        border-radius: 8px;
        overflow: hidden;
    }
    
    th {
        background: linear-gradient(135deg, #084298 0%, #F4A261 100%);
        color: white;
        padding: 15px;
    }
    
    tr:hover {
        background: rgba(244, 162, 97, 0.1);
    }
"""

def add_premium_styles(file_path):
    """Add premium styles to HTML file"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if styles already added
    if "Premium Design Enhancements" in content:
        return content, False
    
    # Add premium styles before closing </style> tag
    if '</style>' in content:
        content = re.sub(
            r'(</style>)',
            f'{PREMIUM_STYLES}\\1',
            content
        )
    elif '</head>' in content:
        # Add new style block if none exists
        style_block = f'<style>{PREMIUM_STYLES}</style>'
        content = re.sub(
            r'(</head>)',
            f'{style_block}\\1',
            content
        )
    
    # Add scroll indicator div after body
    if '<body' in content:
        scroll_indicator = '<div class="scroll-indicator" id="scrollIndicator"></div>'
        content = re.sub(
            r'(<body[^>]*>)',
            f'\\1\\n{scroll_indicator}',
            content
        )
    
    # Add scroll indicator script
    scroll_script = """
<script>
// Scroll progress indicator
window.addEventListener('scroll', () => {
    const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (winScroll / height) * 100;
    const indicator = document.getElementById('scrollIndicator');
    if (indicator) {
        indicator.style.transform = `scaleX(${scrolled / 100})`;
    }
});

// Add loading class to forms on submit
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function() {
        const btn = this.querySelector('button[type="submit"]');
        if (btn) btn.classList.add('loading');
    });
});
</script>
"""
    
    if '</body>' in content:
        content = re.sub(
            r'(</body>)',
            f'{scroll_script}\\1',
            content
        )
    
    return content, True

def main():
    """Process all HTML files"""
    
    root_dir = Path('C:/Users/mirsa/manage369-live')
    updated_files = []
    
    html_files = list(root_dir.rglob('*.html'))
    html_files = [f for f in html_files if not any(
        skip in str(f) for skip in ['.git', 'node_modules', 'dist', 'build']
    )]
    
    print(f"Adding premium styling to {len(html_files)} files...")
    print("-" * 60)
    
    for file_path in html_files:
        try:
            content, was_updated = add_premium_styles(file_path)
            
            if was_updated:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                updated_files.append(file_path.relative_to(root_dir))
                print(f"[PREMIUM] {file_path.relative_to(root_dir)}")
                
        except Exception as e:
            print(f"[ERROR] {file_path}: {e}")
    
    print("\n" + "=" * 60)
    print(f"Added premium styling to {len(updated_files)} files")
    print("\nPremium features added:")
    print("- Glass morphism effects")
    print("- Gradient animations")
    print("- Smooth transitions")
    print("- Glowing gold accents")
    print("- Scroll progress indicator")
    print("- Hover animations")
    print("- Loading states")

if __name__ == "__main__":
    main()