# 📋 Manage369 Forms - Complete Setup Guide

## ✅ Forms Ready for manage369.com/forms

I've created 4 customized forms for Manage369 that send directly to **service@manage369.com**:

### **Forms Included:**
1. **Property Management Inquiry** - For new properties seeking management
2. **Board Member Quick Contact** - For HOA/Condo board members
3. **Maintenance Request** - For residents reporting issues
4. **Get a Free Quote** - For detailed management proposals

## 🚀 OPTION 1: Upload Complete Page (Easiest)

### File: `manage369-forms.html`
1. **Upload** `manage369-forms.html` to your server
2. **Access** at: https://manage369.com/forms
3. **Done!** Forms work immediately

### What You Get:
- ✅ All forms send to **service@manage369.com**
- ✅ No server configuration needed
- ✅ Works with user's email client
- ✅ Mobile responsive
- ✅ Branded with Manage369 colors

## 📧 OPTION 2: Add to Existing Forms Page

If you already have forms at https://manage369.com/forms, add this code:

### Simple Contact Button:
```html
<a href="mailto:service@manage369.com?subject=Property%20Management%20Inquiry&body=I%20am%20interested%20in%20your%20property%20management%20services." 
   style="background: #ff9500; color: white; padding: 15px 30px; border-radius: 10px; text-decoration: none; font-weight: bold; display: inline-block;">
   📧 Contact Manage369
</a>
```

### Full Form with Email:
```html
<form id="manage369-contact">
    <input type="text" id="name" placeholder="Your Name" required>
    <input type="email" id="email" placeholder="Your Email" required>
    <input type="tel" id="phone" placeholder="Phone">
    <select id="property-type">
        <option value="">Property Type</option>
        <option value="Condo">Condominium</option>
        <option value="HOA">HOA</option>
        <option value="Townhome">Townhome</option>
    </select>
    <textarea id="message" placeholder="How can we help?"></textarea>
    
    <button type="button" onclick="sendToManage369()">Send Message</button>
</form>

<script>
function sendToManage369() {
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone').value;
    const propertyType = document.getElementById('property-type').value;
    const message = document.getElementById('message').value;
    
    const subject = `Inquiry from ${name} - ${propertyType}`;
    const body = `${message}\n\nContact:\nName: ${name}\nEmail: ${email}\nPhone: ${phone}`;
    
    window.location.href = `mailto:service@manage369.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
}
</script>
```

## 🎨 OPTION 3: Embed Individual Forms

### Property Management Inquiry:
```html
<div style="background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 5px 20px rgba(0,0,0,0.1);">
    <h2 style="color: #1e3a8a; margin-bottom: 1.5rem;">Get Started with Manage369</h2>
    
    <form>
        <div style="margin-bottom: 1rem;">
            <input type="text" id="pm-name" placeholder="Your Name" 
                   style="width: 100%; padding: 10px; border: 2px solid #e0e0e0; border-radius: 5px;">
        </div>
        
        <div style="margin-bottom: 1rem;">
            <input type="email" id="pm-email" placeholder="Email Address" 
                   style="width: 100%; padding: 10px; border: 2px solid #e0e0e0; border-radius: 5px;">
        </div>
        
        <div style="margin-bottom: 1rem;">
            <select id="pm-type" style="width: 100%; padding: 10px; border: 2px solid #e0e0e0; border-radius: 5px;">
                <option value="">Select Property Type</option>
                <option value="Condominium">Condominium</option>
                <option value="HOA">HOA</option>
                <option value="Townhome">Townhome</option>
            </select>
        </div>
        
        <div style="margin-bottom: 1rem;">
            <textarea id="pm-message" placeholder="Tell us about your property..." 
                      style="width: 100%; padding: 10px; border: 2px solid #e0e0e0; border-radius: 5px; min-height: 100px;"></textarea>
        </div>
        
        <button type="button" onclick="submitInquiry()" 
                style="background: #ff9500; color: white; padding: 12px 30px; border: none; border-radius: 5px; cursor: pointer; width: 100%; font-weight: bold;">
            Send Inquiry to Manage369
        </button>
    </form>
</div>

<script>
function submitInquiry() {
    const name = document.getElementById('pm-name').value;
    const email = document.getElementById('pm-email').value;
    const type = document.getElementById('pm-type').value;
    const message = document.getElementById('pm-message').value;
    
    const mailtoLink = `mailto:service@manage369.com?subject=Property Management Inquiry - ${type}&body=From: ${name}%0D%0AEmail: ${email}%0D%0A%0D%0A${message}`;
    window.location.href = mailtoLink;
}
</script>
```

## 🔧 OPTION 4: WordPress Integration

### For WordPress Sites:
1. **Create New Page** or edit existing Forms page
2. **Switch to HTML/Text mode**
3. **Paste this code:**

```html
<!-- Manage369 Contact Form -->
<div class="manage369-form-wrapper">
    <style>
        .manage369-form { 
            max-width: 600px; 
            margin: 0 auto; 
            padding: 2rem; 
            background: #f8f9fa; 
            border-radius: 10px; 
        }
        .manage369-form input, 
        .manage369-form select, 
        .manage369-form textarea { 
            width: 100%; 
            padding: 10px; 
            margin-bottom: 15px; 
            border: 1px solid #ddd; 
            border-radius: 5px; 
        }
        .manage369-btn { 
            background: #ff9500; 
            color: white; 
            padding: 12px 30px; 
            border: none; 
            border-radius: 5px; 
            cursor: pointer; 
            width: 100%; 
        }
    </style>
    
    <div class="manage369-form">
        <h2>Contact Manage369</h2>
        <input type="text" id="m369-name" placeholder="Your Name">
        <input type="email" id="m369-email" placeholder="Email">
        <input type="tel" id="m369-phone" placeholder="Phone">
        <textarea id="m369-message" rows="5" placeholder="Message"></textarea>
        <button class="manage369-btn" onclick="manage369Send()">Send Message</button>
    </div>
</div>

<script>
function manage369Send() {
    var n = document.getElementById('m369-name').value;
    var e = document.getElementById('m369-email').value;
    var p = document.getElementById('m369-phone').value;
    var m = document.getElementById('m369-message').value;
    
    location.href = 'mailto:service@manage369.com?subject=Contact from ' + n + '&body=' + encodeURIComponent(m + '\n\nFrom: ' + n + '\nEmail: ' + e + '\nPhone: ' + p);
}
</script>
```

## 📱 Mobile-Friendly Quick Contact

### WhatsApp Button (Optional):
```html
<a href="https://wa.me/18476522338?text=Hi%20Manage369,%20I%20need%20property%20management%20services" 
   style="background: #25d366; color: white; padding: 12px 25px; border-radius: 50px; text-decoration: none; display: inline-flex; align-items: center; gap: 10px;">
   <img src="https://cdn.jsdelivr.net/npm/simple-icons@v6/icons/whatsapp.svg" width="20" height="20" style="filter: invert(1);">
   Chat on WhatsApp
</a>
```

### Click-to-Call Button:
```html
<a href="tel:8476522338" 
   style="background: #4a90e2; color: white; padding: 15px 30px; border-radius: 10px; text-decoration: none; font-weight: bold; display: inline-block;">
   📞 Call (847) 652-2338
</a>
```

## ✅ Testing Checklist

After implementing, test:
1. ✓ Fill out form with test data
2. ✓ Click submit button
3. ✓ Email client opens with:
   - **To:** service@manage369.com
   - **Subject:** Pre-filled
   - **Body:** Form data included
4. ✓ Send test email
5. ✓ Check service@manage369.com inbox

## 🎯 Key Benefits

- **No Server Setup** - Works immediately
- **100% Delivery** - No spam filters
- **User Control** - They see what they send
- **Mobile Friendly** - Works on all devices
- **Free Forever** - No monthly fees

## 📊 Tracking (Optional)

Add Google Analytics event tracking:
```javascript
// Track form submissions
function sendToManage369() {
    // ... existing code ...
    
    // Track event
    if (typeof gtag !== 'undefined') {
        gtag('event', 'form_submit', {
            'event_category': 'Contact',
            'event_label': 'Property Inquiry'
        });
    }
    
    // ... rest of code ...
}
```

## 🚨 Emergency Support

If forms don't work:
1. **Check:** Email client installed?
2. **Alternative:** Copy form data manually
3. **Direct Email:** service@manage369.com
4. **Call:** (847) 652-2338

## 📁 Files Included

1. **manage369-forms.html** - Complete forms page
2. **MANAGE369-FORMS-SETUP.md** - This setup guide
3. **Individual form snippets** - For embedding

## Ready to Use!

The forms are configured and ready. Just upload `manage369-forms.html` to your server at `/forms/` and you're done!

All submissions go to: **service@manage369.com**