# Stellar Forms System

Professional contact and lead generation forms for Stellar Property Group.

## Features

### Two Form Types
1. **Contact Form** - General inquiries with full validation
2. **Lead Generation Form** - Qualified lead capture with scoring

### Advanced Features
- Real-time form validation
- Phone number formatting
- Email validation
- Lead scoring (0-100)
- Auto-reply emails
- Admin notifications
- Conversion tracking
- Statistics dashboard

## Setup Instructions

### 1. Basic HTML Setup
Simply upload the files to your web server:
- `index.html` - Main forms page
- `forms.js` - JavaScript handler
- `process-form.php` - Backend processor

### 2. Configure Email Settings
Edit `process-form.php` and update:
```php
define('ADMIN_EMAIL', 'your-email@stellarpropertygroup.com');
define('FROM_EMAIL', 'noreply@stellarpropertygroup.com');
```

### 3. Database Setup (Optional)
Create a MySQL table for storing submissions:

```sql
CREATE TABLE form_submissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(50),
    data JSON,
    lead_score INT,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 4. Integration Options

#### Option A: Standalone Page
Use as-is at `https://stellarpropertygroup.com/forms/`

#### Option B: Embed in Existing Site
Copy the form HTML and include the JavaScript:
```html
<script src="forms.js"></script>
```

#### Option C: WordPress Integration
1. Create a new page
2. Add HTML in text mode
3. Include scripts in theme

## Lead Scoring System

Leads are automatically scored based on:
- **Company Size** (up to 50 points)
- **Budget** (up to 25 points)  
- **Timeline** (up to 25 points)
- **Company Name** (+10 points)
- **Detailed Needs** (+10 points)

Scores 70+ are marked as HIGH PRIORITY.

## Email Notifications

### Admin Receives:
- All form submissions instantly
- Lead scores for prioritization
- High-priority alerts for hot leads

### User Receives:
- Auto-confirmation email
- Next steps information
- Company contact details

## API Integration

The forms can integrate with:
- CRM systems (Salesforce, HubSpot)
- Email marketing (Mailchimp, Constant Contact)
- Analytics (Google Analytics, Facebook Pixel)
- Slack notifications
- SMS alerts (Twilio)

## Customization

### Styling
Modify the CSS in `index.html` to match your brand:
- Colors: Change gradient colors
- Fonts: Update font-family
- Layout: Adjust grid columns

### Fields
Add custom fields by editing the HTML and updating validation in `forms.js`

### Validation Rules
Modify validation logic in the `validateContactForm()` and `validateLeadForm()` functions

## Testing

### Local Testing
1. Open `index.html` in a browser
2. Forms will work with localStorage
3. Check console for submissions

### Server Testing
1. Upload all files
2. Ensure PHP is enabled
3. Set email configuration
4. Test form submissions

## Security Features

- Input sanitization
- Email validation
- CSRF protection (add token)
- Rate limiting (implement in PHP)
- Honeypot field (optional)

## Analytics Tracking

The forms track:
- Total submissions
- Daily submissions
- Conversion rates
- Response times

View stats at the bottom of the forms page.

## Support

For issues or customization needs, contact:
- Email: support@stellarpropertygroup.com
- Phone: (312) 555-0100

## License

Property of Stellar Property Group. All rights reserved.