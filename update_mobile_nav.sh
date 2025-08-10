#!/bin/bash

# Script to add mobile navigation to property-management pages
# This script updates all property-management index.html files to include mobile menu functionality

echo "Starting mobile navigation update for property-management pages..."

# Find all property-management index.html files (excluding the ones we already updated)
find "property-management" -name "index.html" -path "*/property-management/*" | while read -r file; do
    # Skip the ones we already updated
    if [[ "$file" == *"evanston/index.html"* ]] || [[ "$file" == *"glencoe/index.html"* ]] || [[ "$file" == *"wilmette/index.html"* ]]; then
        echo "Skipping already updated file: $file"
        continue
    fi
    
    # Check if file already has mobile menu (skip if it does)
    if grep -q "mobile-menu-toggle" "$file"; then
        echo "Skipping file with existing mobile menu: $file"
        continue
    fi
    
    echo "Updating $file..."
    
    # Create a backup
    cp "$file" "$file.backup"
    
    # Update the CSS section - replace the mobile media query
    sed -i 's|@media (max-width: 768px) {[[:space:]]*\.header {[[:space:]]*flex-direction: column;[[:space:]]*padding: 1rem;[[:space:]]*}[[:space:]]*\.nav {[[:space:]]*margin-top: 1rem;[[:space:]]*flex-wrap: wrap;[[:space:]]*justify-content: center;[[:space:]]*gap: 1rem;[[:space:]]*}|/* Mobile Navigation */\
        .mobile-menu-toggle {\
            display: none;\
            background: none;\
            border: none;\
            font-size: 1.5rem;\
            color: #333;\
            cursor: pointer;\
        }\
        \
        .mobile-menu {\
            display: none;\
            position: absolute;\
            top: 100%;\
            left: 0;\
            right: 0;\
            background: white;\
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);\
            padding: 1rem;\
            z-index: 1001;\
        }\
        \
        .mobile-menu.active {\
            display: block;\
        }\
        \
        .mobile-menu a {\
            display: block;\
            padding: 0.75rem 0;\
            border-bottom: 1px solid #eee;\
            color: #333;\
            text-decoration: none;\
        }\
        \
        @media (max-width: 768px) {\
            .header {\
                flex-direction: row;\
                padding: 1rem;\
                justify-content: space-between;\
            }\
            \
            .nav {\
                display: none;\
            }\
            \
            .mobile-menu-toggle {\
                display: block;\
            }\
            \
            .phone {\
                display: none;\
            }|' "$file"
    
    # Add mobile menu toggle button and menu HTML
    sed -i 's|<nav class="nav">|<!-- Mobile Menu Toggle -->\
        <button class="mobile-menu-toggle" onclick="toggleMobileMenu()">☰</button>\
        \
        <nav class="nav">|' "$file"
    
    # Add mobile menu after the closing nav tag
    sed -i 's|</nav>[[:space:]]*<a href="tel:8476522338" class="phone">Call (847) 652-2338</a>|</nav>\
        \
        <a href="tel:8476522338" class="phone">Call (847) 652-2338</a>\
        \
        <!-- Mobile Menu -->\
        <div class="mobile-menu" id="mobileMenu">\
            <a href="../../index.html">Home</a>\
            <a href="../../services.html">Services</a>\
            <a href="../">Areas We Serve</a>\
            <a href="../../pay-dues.html">Pay Dues</a>\
            <a href="../../contact.html">Contact</a>\
            <a href="tel:8476522338" style="background: #4a90e2; color: white; padding: 0.75rem; border-radius: 5px; margin-top: 1rem; text-align: center;">Call (847) 652-2338</a>\
        </div>|' "$file"
    
    # Add JavaScript before closing body tag
    sed -i 's|</body>[[:space:]]*</html>|    <script>\
        function toggleMobileMenu() {\
            const mobileMenu = document.getElementById('"'"'mobileMenu'"'"');\
            mobileMenu.classList.toggle('"'"'active'"'"');\
        }\
        \
        // Close mobile menu when clicking outside\
        document.addEventListener('"'"'click'"'"', function(event) {\
            const mobileMenu = document.getElementById('"'"'mobileMenu'"'"');\
            const toggle = document.querySelector('"'"'.mobile-menu-toggle'"'"');\
            \
            if (!mobileMenu.contains(event.target) \&\& !toggle.contains(event.target)) {\
                mobileMenu.classList.remove('"'"'active'"'"');\
            }\
        });\
    </script>\
</body>\
</html>|' "$file"
    
    echo "Updated $file"
done

echo "Mobile navigation update completed!"