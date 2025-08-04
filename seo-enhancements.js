// SEO Enhancement JavaScript for Manage369
// Implements advanced SEO features and tracking

document.addEventListener('DOMContentLoaded', function() {
    // Initialize SEO enhancements
    initSEOEnhancements();
    initPerformanceOptimizations();
    initLocalSEO();
    initClickTracking();
});

function initSEOEnhancements() {
    // Add structured data for page views
    addPageViewSchema();
    
    // Enhance internal linking
    enhanceInternalLinks();
    
    // Add breadcrumb navigation
    updateBreadcrumbs();
    
    // Optimize images for SEO
    optimizeImages();
}

function addPageViewSchema() {
    // Add WebPage schema for current page
    const pageSchema = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": document.title,
        "description": document.querySelector('meta[name="description"]')?.content || "",
        "url": window.location.href,
        "mainEntity": {
            "@type": "LocalBusiness",
            "name": "Manage369"
        },
        "breadcrumb": {
            "@type": "BreadcrumbList",
            "itemListElement": generateBreadcrumbSchema()
        }
    };
    
    const script = document.createElement('script');
    script.type = 'application/ld+json';
    script.textContent = JSON.stringify(pageSchema);
    document.head.appendChild(script);
}

function generateBreadcrumbSchema() {
    const path = window.location.pathname;
    const breadcrumbs = [];
    
    // Always start with home
    breadcrumbs.push({
        "@type": "ListItem",
        "position": 1,
        "name": "Home",
        "item": "https://manage369.com/"
    });
    
    // Add current page if not home
    if (path !== '/' && path !== '/index.html') {
        const pageName = document.title.split('|')[0].trim();
        breadcrumbs.push({
            "@type": "ListItem",
            "position": 2,
            "name": pageName,
            "item": window.location.href
        });
    }
    
    return breadcrumbs;
}

function enhanceInternalLinks() {
    // Add rel attributes to internal links for SEO
    const internalLinks = document.querySelectorAll('a[href^="/"], a[href^="./"], a[href^="../"]');
    
    internalLinks.forEach(link => {
        // Add noopener for security
        if (link.target === '_blank') {
            link.rel = 'noopener';
        }
        
        // Add title attributes if missing
        if (!link.title && link.textContent.trim()) {
            link.title = link.textContent.trim();
        }
    });
    
    // Add rel="nofollow" to external links
    const externalLinks = document.querySelectorAll('a[href^="http"]:not([href*="manage369.com"])');
    externalLinks.forEach(link => {
        link.rel = 'nofollow noopener';
        if (link.target !== '_blank') {
            link.target = '_blank';
        }
    });
}

function updateBreadcrumbs() {
    // Create visual breadcrumb navigation if it doesn't exist
    const existingBreadcrumb = document.querySelector('.breadcrumb');
    if (existingBreadcrumb) return;
    
    const path = window.location.pathname;
    if (path === '/' || path === '/index.html') return;
    
    const breadcrumbContainer = document.createElement('nav');
    breadcrumbContainer.className = 'breadcrumb';
    breadcrumbContainer.setAttribute('aria-label', 'Breadcrumb');
    
    const breadcrumbList = document.createElement('ol');
    breadcrumbList.className = 'breadcrumb-list';
    
    // Home link
    const homeItem = document.createElement('li');
    homeItem.className = 'breadcrumb-item';
    homeItem.innerHTML = '<a href="/">Home</a>';
    breadcrumbList.appendChild(homeItem);
    
    // Current page
    const currentItem = document.createElement('li');
    currentItem.className = 'breadcrumb-item active';
    currentItem.setAttribute('aria-current', 'page');
    currentItem.textContent = document.title.split('|')[0].trim();
    breadcrumbList.appendChild(currentItem);
    
    breadcrumbContainer.appendChild(breadcrumbList);
    
    // Insert after header
    const header = document.querySelector('header');
    if (header && header.nextSibling) {
        header.parentNode.insertBefore(breadcrumbContainer, header.nextSibling);
    }
}

function optimizeImages() {
    // Add loading="lazy" to images below the fold
    const images = document.querySelectorAll('img');
    
    images.forEach((img, index) => {
        // Add lazy loading to images after the first 3
        if (index > 2 && !img.hasAttribute('loading')) {
            img.loading = 'lazy';
        }
        
        // Add alt text if missing
        if (!img.alt && img.src) {
            const filename = img.src.split('/').pop().split('.')[0];
            img.alt = filename.replace(/[-_]/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        }
        
        // Add width and height if missing (helps with CLS)
        if (!img.width && !img.height) {
            img.onload = function() {
                if (!this.width) this.width = this.naturalWidth;
                if (!this.height) this.height = this.naturalHeight;
            };
        }
    });
}

function initPerformanceOptimizations() {
    // Preload critical resources
    preloadCriticalResources();
    
    // Optimize font loading
    optimizeFontLoading();
    
    // Add performance monitoring
    monitorPerformance();
}

function preloadCriticalResources() {
    // Preload hero image if it exists
    const heroImage = document.querySelector('.hero img, .hero-section img');
    if (heroImage && heroImage.src) {
        const preloadLink = document.createElement('link');
        preloadLink.rel = 'preload';
        preloadLink.as = 'image';
        preloadLink.href = heroImage.src;
        document.head.appendChild(preloadLink);
    }
}

function optimizeFontLoading() {
    // Add font-display: swap to improve loading performance
    const style = document.createElement('style');
    style.textContent = `
        @font-face {
            font-family: system-ui, -apple-system, sans-serif;
            font-display: swap;
        }
    `;
    document.head.appendChild(style);
}

function monitorPerformance() {
    // Monitor Core Web Vitals
    if ('PerformanceObserver' in window) {
        // Monitor LCP (Largest Contentful Paint)
        const lcpObserver = new PerformanceObserver((list) => {
            const entries = list.getEntries();
            const lastEntry = entries[entries.length - 1];
            
            // Send to analytics if available
            if (typeof gtag !== 'undefined') {
                gtag('event', 'LCP', {
                    value: Math.round(lastEntry.startTime),
                    custom_parameter: 'core_web_vitals'
                });
            }
        });
        
        try {
            lcpObserver.observe({ entryTypes: ['largest-contentful-paint'] });
        } catch (e) {
            // Browser doesn't support LCP
        }
        
        // Monitor CLS (Cumulative Layout Shift)
        let clsValue = 0;
        const clsObserver = new PerformanceObserver((list) => {
            for (const entry of list.getEntries()) {
                if (!entry.hadRecentInput) {
                    clsValue += entry.value;
                }
            }
            
            // Send to analytics
            if (typeof gtag !== 'undefined') {
                gtag('event', 'CLS', {
                    value: Math.round(clsValue * 1000),
                    custom_parameter: 'core_web_vitals'
                });
            }
        });
        
        try {
            clsObserver.observe({ entryTypes: ['layout-shift'] });
        } catch (e) {
            // Browser doesn't support CLS
        }
    }
}

function initLocalSEO() {
    // Add local business markup to contact information
    enhanceContactInfo();
    
    // Add location-based content
    addLocationContext();
    
    // Track local search queries
    trackLocalSearches();
}

function enhanceContactInfo() {
    // Find phone numbers and add tel: links
    const phoneRegex = /\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}/g;
    const textNodes = getTextNodes(document.body);
    
    textNodes.forEach(node => {
        const text = node.textContent;
        if (phoneRegex.test(text)) {
            const parent = node.parentNode;
            const newHTML = text.replace(phoneRegex, (match) => {
                const cleanPhone = match.replace(/[^\d]/g, '');
                return `<a href="tel:+1${cleanPhone}" class="phone-link">${match}</a>`;
            });
            
            const wrapper = document.createElement('span');
            wrapper.innerHTML = newHTML;
            parent.replaceChild(wrapper, node);
        }
    });
    
    // Add microdata to address information
    const addressElements = document.querySelectorAll('.address, .contact-address');
    addressElements.forEach(element => {
        element.setAttribute('itemscope', '');
        element.setAttribute('itemtype', 'https://schema.org/PostalAddress');
    });
}

function getTextNodes(element) {
    const textNodes = [];
    const walker = document.createTreeWalker(
        element,
        NodeFilter.SHOW_TEXT,
        null,
        false
    );
    
    let node;
    while (node = walker.nextNode()) {
        if (node.textContent.trim()) {
            textNodes.push(node);
        }
    }
    
    return textNodes;
}

function addLocationContext() {
    // Add location-specific content hints
    const locationKeywords = [
        'Chicago', 'North Shore', 'Glenview', 'Highland Park', 
        'Evanston', 'Winnetka', 'Wilmette', 'Illinois'
    ];
    
    // Check if page mentions locations
    const pageText = document.body.textContent.toLowerCase();
    const mentionedLocations = locationKeywords.filter(location => 
        pageText.includes(location.toLowerCase())
    );
    
    // Add location context to page schema
    if (mentionedLocations.length > 0) {
        const locationSchema = {
            "@context": "https://schema.org",
            "@type": "Place",
            "name": mentionedLocations[0],
            "containedInPlace": {
                "@type": "State",
                "name": "Illinois"
            }
        };
        
        const script = document.createElement('script');
        script.type = 'application/ld+json';
        script.textContent = JSON.stringify(locationSchema);
        document.head.appendChild(script);
    }
}

function trackLocalSearches() {
    // Track searches that include location terms
    const searchForms = document.querySelectorAll('form[role="search"], .search-form');
    
    searchForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const searchInput = form.querySelector('input[type="search"], input[name*="search"]');
            if (searchInput && searchInput.value) {
                const query = searchInput.value.toLowerCase();
                const isLocalSearch = ['chicago', 'glenview', 'north shore', 'illinois'].some(term => 
                    query.includes(term)
                );
                
                if (isLocalSearch && typeof gtag !== 'undefined') {
                    gtag('event', 'local_search', {
                        search_term: searchInput.value,
                        custom_parameter: 'local_seo'
                    });
                }
            }
        });
    });
}

function initClickTracking() {
    // Track important clicks for SEO insights
    trackServiceClicks();
    trackContactClicks();
    trackLocationClicks();
}

function trackServiceClicks() {
    // Track clicks on service pages
    const serviceLinks = document.querySelectorAll('a[href*="management"], a[href*="services"]');
    
    serviceLinks.forEach(link => {
        link.addEventListener('click', function() {
            const serviceName = this.textContent.trim() || this.href.split('/').pop();
            
            if (typeof gtag !== 'undefined') {
                gtag('event', 'service_click', {
                    service_name: serviceName,
                    custom_parameter: 'user_engagement'
                });
            }
        });
    });
}

function trackContactClicks() {
    // Track contact method usage
    const phoneLinks = document.querySelectorAll('a[href^="tel:"]');
    const emailLinks = document.querySelectorAll('a[href^="mailto:"]');
    
    phoneLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (typeof gtag !== 'undefined') {
                gtag('event', 'phone_click', {
                    phone_number: this.href.replace('tel:', ''),
                    custom_parameter: 'contact_method'
                });
            }
        });
    });
    
    emailLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (typeof gtag !== 'undefined') {
                gtag('event', 'email_click', {
                    custom_parameter: 'contact_method'
                });
            }
        });
    });
}

function trackLocationClicks() {
    // Track clicks on location-specific pages
    const locationLinks = document.querySelectorAll('a[href*="property-management-"]');
    
    locationLinks.forEach(link => {
        link.addEventListener('click', function() {
            const location = this.href.split('property-management-')[1]?.split('.')[0];
            
            if (location && typeof gtag !== 'undefined') {
                gtag('event', 'location_page_click', {
                    location: location.replace(/-/g, ' '),
                    custom_parameter: 'local_seo'
                });
            }
        });
    });
}

// Add CSS for breadcrumbs and enhanced elements
const seoStyles = document.createElement('style');
seoStyles.textContent = `
    .breadcrumb {
        background: #f8f9fa;
        padding: 0.75rem 1rem;
        margin-bottom: 1rem;
        border-radius: 0.25rem;
    }
    
    .breadcrumb-list {
        display: flex;
        list-style: none;
        margin: 0;
        padding: 0;
        flex-wrap: wrap;
    }
    
    .breadcrumb-item {
        display: flex;
        align-items: center;
    }
    
    .breadcrumb-item + .breadcrumb-item::before {
        content: ">";
        margin: 0 0.5rem;
        color: #6c757d;
    }
    
    .breadcrumb-item a {
        color: #007bff;
        text-decoration: none;
    }
    
    .breadcrumb-item a:hover {
        text-decoration: underline;
    }
    
    .breadcrumb-item.active {
        color: #6c757d;
    }
    
    .phone-link {
        color: inherit;
        text-decoration: none;
        border-bottom: 1px dotted;
    }
    
    .phone-link:hover {
        color: #007bff;
        text-decoration: none;
    }
    
    @media (max-width: 768px) {
        .breadcrumb {
            padding: 0.5rem;
            font-size: 0.875rem;
        }
        
        .breadcrumb-item + .breadcrumb-item::before {
            margin: 0 0.25rem;
        }
    }
`;

document.head.appendChild(seoStyles);

// Export functions for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initSEOEnhancements,
        addPageViewSchema,
        enhanceInternalLinks,
        optimizeImages
    };
}

