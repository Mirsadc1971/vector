// Stellar Forms - JavaScript Handler
// Complete form validation and submission system

class FormHandler {
    constructor() {
        this.initializeForms();
        this.loadStats();
        this.setupValidation();
    }
    
    initializeForms() {
        // Contact Form
        const contactForm = document.getElementById('contactForm');
        if (contactForm) {
            contactForm.addEventListener('submit', (e) => this.handleContactSubmit(e));
        }
        
        // Lead Form
        const leadForm = document.getElementById('leadForm');
        if (leadForm) {
            leadForm.addEventListener('submit', (e) => this.handleLeadSubmit(e));
        }
        
        // Format phone input
        const phoneInputs = document.querySelectorAll('input[type="tel"]');
        phoneInputs.forEach(input => {
            input.addEventListener('input', (e) => this.formatPhone(e));
        });
    }
    
    formatPhone(e) {
        let value = e.target.value.replace(/\D/g, '');
        if (value.length > 0) {
            if (value.length <= 3) {
                value = `(${value}`;
            } else if (value.length <= 6) {
                value = `(${value.slice(0, 3)}) ${value.slice(3)}`;
            } else {
                value = `(${value.slice(0, 3)}) ${value.slice(3, 6)}-${value.slice(6, 10)}`;
            }
        }
        e.target.value = value;
    }
    
    async handleContactSubmit(e) {
        e.preventDefault();
        const form = e.target;
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);
        
        // Show loading
        this.showLoading('contactLoading', true);
        this.hideMessages('contact');
        
        try {
            // Validate form
            if (!this.validateContactForm(data)) {
                throw new Error('Please fill in all required fields correctly');
            }
            
            // Send to backend (replace with your actual endpoint)
            const response = await this.sendFormData('contact', data);
            
            if (response.success) {
                this.showSuccess('contactSuccess');
                form.reset();
                this.incrementStats('contact');
            } else {
                throw new Error(response.message || 'Submission failed');
            }
        } catch (error) {
            this.showError('contactError', error.message);
        } finally {
            this.showLoading('contactLoading', false);
        }
    }
    
    async handleLeadSubmit(e) {
        e.preventDefault();
        const form = e.target;
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);
        
        // Show loading
        this.showLoading('leadLoading', true);
        this.hideMessages('lead');
        
        try {
            // Validate form
            if (!this.validateLeadForm(data)) {
                throw new Error('Please fill in all required fields correctly');
            }
            
            // Send to backend
            const response = await this.sendFormData('lead', data);
            
            if (response.success) {
                this.showSuccess('leadSuccess');
                form.reset();
                this.incrementStats('lead');
                
                // Track conversion
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'generate_lead', {
                        'event_category': 'engagement',
                        'event_label': 'Lead Form Submission'
                    });
                }
            } else {
                throw new Error(response.message || 'Submission failed');
            }
        } catch (error) {
            this.showError('leadError', error.message);
        } finally {
            this.showLoading('leadLoading', false);
        }
    }
    
    validateContactForm(data) {
        // Check required fields
        if (!data.firstName || !data.lastName || !data.email || !data.subject || !data.message) {
            return false;
        }
        
        // Validate email
        if (!this.isValidEmail(data.email)) {
            return false;
        }
        
        // Validate phone if provided
        if (data.phone && !this.isValidPhone(data.phone)) {
            return false;
        }
        
        return true;
    }
    
    validateLeadForm(data) {
        // Check required fields
        if (!data.leadName || !data.leadEmail || !data.companySize) {
            return false;
        }
        
        // Validate email
        if (!this.isValidEmail(data.leadEmail)) {
            return false;
        }
        
        return true;
    }
    
    isValidEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }
    
    isValidPhone(phone) {
        const cleaned = phone.replace(/\D/g, '');
        return cleaned.length === 10;
    }
    
    async sendFormData(formType, data) {
        // Add metadata
        data.formType = formType;
        data.timestamp = new Date().toISOString();
        data.source = window.location.href;
        data.userAgent = navigator.userAgent;
        
        // Get IP and location (optional)
        try {
            const ipResponse = await fetch('https://api.ipify.org?format=json');
            const ipData = await ipResponse.json();
            data.ip = ipData.ip;
        } catch (e) {
            // Continue without IP
        }
        
        // For demo purposes, simulate API call
        // Replace this with your actual API endpoint
        return new Promise((resolve) => {
            setTimeout(() => {
                // Store in localStorage for demo
                this.storeSubmission(data);
                
                // Log to console for debugging
                console.log('Form Submission:', data);
                
                resolve({ success: true });
            }, 1500);
        });
        
        /* 
        // Actual API call example:
        const response = await fetch('https://your-api.com/forms/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        return await response.json();
        */
    }
    
    storeSubmission(data) {
        // Store in localStorage for demo
        const submissions = JSON.parse(localStorage.getItem('formSubmissions') || '[]');
        submissions.push(data);
        localStorage.setItem('formSubmissions', JSON.stringify(submissions));
    }
    
    showLoading(elementId, show) {
        const element = document.getElementById(elementId);
        if (element) {
            element.style.display = show ? 'block' : 'none';
        }
    }
    
    showSuccess(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.style.display = 'block';
            setTimeout(() => {
                element.style.display = 'none';
            }, 5000);
        }
    }
    
    showError(elementId, message) {
        const element = document.getElementById(elementId);
        if (element) {
            if (message && message !== 'Submission failed') {
                element.textContent = message;
            }
            element.style.display = 'block';
            setTimeout(() => {
                element.style.display = 'none';
            }, 5000);
        }
    }
    
    hideMessages(formPrefix) {
        const success = document.getElementById(`${formPrefix}Success`);
        const error = document.getElementById(`${formPrefix}Error`);
        if (success) success.style.display = 'none';
        if (error) error.style.display = 'none';
    }
    
    incrementStats(formType) {
        // Update total submissions
        const total = parseInt(localStorage.getItem('totalSubmissions') || '0') + 1;
        localStorage.setItem('totalSubmissions', total);
        
        // Update today's submissions
        const today = new Date().toDateString();
        const todayKey = `submissions_${today}`;
        const todayCount = parseInt(localStorage.getItem(todayKey) || '0') + 1;
        localStorage.setItem(todayKey, todayCount);
        
        // Clear old daily stats
        this.clearOldStats();
        
        // Update display
        this.loadStats();
    }
    
    loadStats() {
        // Total submissions
        const total = localStorage.getItem('totalSubmissions') || '0';
        const totalElement = document.getElementById('totalSubmissions');
        if (totalElement) {
            totalElement.textContent = total;
        }
        
        // Today's submissions
        const today = new Date().toDateString();
        const todayKey = `submissions_${today}`;
        const todayCount = localStorage.getItem(todayKey) || '0';
        const todayElement = document.getElementById('todaySubmissions');
        if (todayElement) {
            todayElement.textContent = todayCount;
        }
        
        // Conversion rate (mock calculation)
        const conversionElement = document.getElementById('conversionRate');
        if (conversionElement) {
            const rate = total > 0 ? Math.min(15 + parseInt(total) * 2, 95) : 0;
            conversionElement.textContent = `${rate}%`;
        }
    }
    
    clearOldStats() {
        const today = new Date().toDateString();
        const keys = Object.keys(localStorage);
        keys.forEach(key => {
            if (key.startsWith('submissions_') && !key.includes(today)) {
                localStorage.removeItem(key);
            }
        });
    }
    
    setupValidation() {
        // Real-time validation
        const inputs = document.querySelectorAll('input[required], select[required], textarea[required]');
        inputs.forEach(input => {
            input.addEventListener('blur', (e) => {
                this.validateField(e.target);
            });
        });
    }
    
    validateField(field) {
        const value = field.value.trim();
        
        if (field.hasAttribute('required') && !value) {
            this.setFieldError(field, 'This field is required');
            return false;
        }
        
        if (field.type === 'email' && value && !this.isValidEmail(value)) {
            this.setFieldError(field, 'Please enter a valid email');
            return false;
        }
        
        this.clearFieldError(field);
        return true;
    }
    
    setFieldError(field, message) {
        field.style.borderColor = '#e74c3c';
        
        // Remove existing error message
        const existing = field.parentElement.querySelector('.field-error');
        if (existing) existing.remove();
        
        // Add error message
        const error = document.createElement('div');
        error.className = 'field-error';
        error.style.cssText = 'color: #e74c3c; font-size: 0.85rem; margin-top: 5px;';
        error.textContent = message;
        field.parentElement.appendChild(error);
    }
    
    clearFieldError(field) {
        field.style.borderColor = '#e0e0e0';
        const error = field.parentElement.querySelector('.field-error');
        if (error) error.remove();
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new FormHandler();
    
    // Animate stats on load
    animateStats();
});

// Animate stats numbers
function animateStats() {
    const stats = document.querySelectorAll('.stat-number');
    stats.forEach(stat => {
        const text = stat.textContent;
        if (!text.includes('%') && !text.includes('<')) {
            const target = parseInt(text) || 0;
            let current = 0;
            const increment = target / 30;
            
            const timer = setInterval(() => {
                current += increment;
                if (current >= target) {
                    current = target;
                    clearInterval(timer);
                }
                stat.textContent = Math.floor(current);
            }, 50);
        }
    });
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FormHandler;
}