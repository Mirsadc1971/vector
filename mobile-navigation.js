/* Mobile Navigation JavaScript for manage369.com */
/* Add this JavaScript file to your GitHub repository and link it in your HTML */

document.addEventListener('DOMContentLoaded', function() {
  
  // Initialize mobile navigation
  initMobileNavigation();
  
  function initMobileNavigation() {
    // Create hamburger menu if it doesn't exist
    createHamburgerMenu();
    
    // Improve touch targets
    improveTouchTargets();
    
    // Add smooth scrolling
    addSmoothScrolling();
    
    // Handle window resize
    handleWindowResize();
  }
  
  function createHamburgerMenu() {
    // Find the navigation container
    const navContainer = document.querySelector('nav') || 
                        document.querySelector('.navbar') ||
                        document.querySelector('header nav') ||
                        document.querySelector('header');
    
    if (!navContainer) {
      console.log('Navigation container not found');
      return;
    }
    
    // Check if hamburger menu already exists
    if (document.querySelector('.hamburger')) {
      setupExistingHamburger();
      return;
    }
    
    // Find the navigation menu
    const navMenu = document.querySelector('nav ul') || 
                   document.querySelector('.nav-menu') ||
                   navContainer.querySelector('ul');
    
    if (!navMenu) {
      console.log('Navigation menu not found');
      return;
    }
    
    // Add classes for styling
    navMenu.classList.add('nav-menu');
    
    // Create hamburger button
    const hamburgerButton = document.createElement('div');
    hamburgerButton.className = 'hamburger';
    hamburgerButton.setAttribute('aria-label', 'Toggle navigation menu');
    hamburgerButton.innerHTML = `
      <span class="bar"></span>
      <span class="bar"></span>
      <span class="bar"></span>
    `;
    
    // Add hamburger button to navigation
    navContainer.appendChild(hamburgerButton);
    
    // Setup event listeners
    setupHamburgerEvents(hamburgerButton, navMenu);
  }
  
  function setupExistingHamburger() {
    const hamburgerButton = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu') || 
                   document.querySelector('nav ul');
    
    if (hamburgerButton && navMenu) {
      setupHamburgerEvents(hamburgerButton, navMenu);
    }
  }
  
  function setupHamburgerEvents(hamburgerButton, navMenu) {
    // Add click event listener
    hamburgerButton.addEventListener('click', function() {
      toggleMobileMenu(hamburgerButton, navMenu);
    });
    
    // Close menu when clicking outside
    document.addEventListener('click', function(event) {
      if (!hamburgerButton.contains(event.target) && !navMenu.contains(event.target)) {
        closeMobileMenu(hamburgerButton, navMenu);
      }
    });
    
    // Close menu when clicking on navigation links
    const navLinks = navMenu.querySelectorAll('a');
    navLinks.forEach(function(link) {
      link.addEventListener('click', function() {
        closeMobileMenu(hamburgerButton, navMenu);
      });
    });
    
    // Close menu when window is resized to desktop
    window.addEventListener('resize', function() {
      if (window.innerWidth > 768) {
        closeMobileMenu(hamburgerButton, navMenu);
      }
    });
  }
  
  function toggleMobileMenu(hamburgerButton, navMenu) {
    hamburgerButton.classList.toggle('active');
    navMenu.classList.toggle('active');
    
    // Update aria-expanded attribute for accessibility
    const isExpanded = navMenu.classList.contains('active');
    hamburgerButton.setAttribute('aria-expanded', isExpanded);
    
    // Prevent body scroll when menu is open
    if (isExpanded) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
  }
  
  function closeMobileMenu(hamburgerButton, navMenu) {
    hamburgerButton.classList.remove('active');
    navMenu.classList.remove('active');
    hamburgerButton.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  }
  
  function improveTouchTargets() {
    // Ensure all clickable elements meet touch target size
    const clickableElements = document.querySelectorAll('a, button, input[type="submit"], input[type="button"]');
    
    clickableElements.forEach(function(element) {
      const rect = element.getBoundingClientRect();
      if (rect.height < 44 || rect.width < 44) {
        element.style.minHeight = '44px';
        element.style.minWidth = '44px';
        element.style.display = 'flex';
        element.style.alignItems = 'center';
        element.style.justifyContent = 'center';
      }
    });
  }
  
  function addSmoothScrolling() {
    // Add smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    
    anchorLinks.forEach(function(link) {
      link.addEventListener('click', function(e) {
        const targetId = this.getAttribute('href').substring(1);
        const targetElement = document.getElementById(targetId);
        
        if (targetElement) {
          e.preventDefault();
          targetElement.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
          
          // Close mobile menu after clicking a link
          const hamburgerButton = document.querySelector('.hamburger');
          const navMenu = document.querySelector('.nav-menu') || document.querySelector('nav ul');
          if (hamburgerButton && navMenu) {
            closeMobileMenu(hamburgerButton, navMenu);
          }
        }
      });
    });
  }
  
  function handleWindowResize() {
    let resizeTimer;
    window.addEventListener('resize', function() {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function() {
        improveTouchTargets();
        
        // Close mobile menu on desktop
        if (window.innerWidth > 768) {
          const hamburgerButton = document.querySelector('.hamburger');
          const navMenu = document.querySelector('.nav-menu') || document.querySelector('nav ul');
          if (hamburgerButton && navMenu) {
            closeMobileMenu(hamburgerButton, navMenu);
          }
        }
      }, 250);
    });
  }
  
  // Add mobile-friendly class to body
  document.body.classList.add('mobile-optimized');
  
  // Ensure viewport meta tag exists
  ensureViewportMeta();
});

// Utility functions
function isMobileDevice() {
  return window.innerWidth <= 768 || 
         /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
}

function ensureViewportMeta() {
  if (!document.querySelector('meta[name="viewport"]')) {
    const meta = document.createElement('meta');
    meta.name = 'viewport';
    meta.content = 'width=device-width, initial-scale=1.0';
    document.head.appendChild(meta);
  }
}

// Initialize immediately if DOM is already loaded
if (document.readyState === 'loading') {
  // DOM is still loading, wait for DOMContentLoaded
} else {
  // DOM is already loaded
  setTimeout(function() {
    if (!document.querySelector('.hamburger')) {
      initMobileNavigation();
    }
  }, 100);
}

