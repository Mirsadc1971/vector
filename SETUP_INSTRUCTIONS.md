# Manage369 Website Setup Instructions

## Critical Setup Tasks

### 1. Google Analytics Configuration
**IMPORTANT**: Replace the placeholder Google Analytics ID with your actual GA4 measurement ID.

1. Go to [Google Analytics](https://analytics.google.com/)
2. Create a new GA4 property for manage369.com
3. Get your Measurement ID (format: G-XXXXXXXXXX)
4. In `index.html`, find and replace both instances of `G-XXXXXXXXXX` with your actual ID:
   - Line 68: `<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>`
   - Line 73: `gtag('config', 'G-XXXXXXXXXX');`

### 2. Contact Form Configuration
The quick contact form uses Formspree for form handling. To activate it:

1. Go to [Formspree.io](https://formspree.io/)
2. Sign up for a free account
3. Create a new form for manage369.com
4. Get your form endpoint ID
5. In `index.html`, line 1715, replace `YOUR_FORM_ID` with your actual Formspree form ID:
   ```html
   <form class="contact-form" action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
   ```

### 3. Completed Optimizations

✅ **Schema Markup**: Comprehensive structured data already implemented including:
   - LocalBusiness/ProfessionalService schema
   - Organization schema
   - FAQ schema
   - BreadcrumbList schema
   - WebSite schema with sitelinks searchbox

✅ **Accessibility**: All images have proper alt tags

✅ **Phone Numbers**: All phone numbers are clickable with `tel:` links

✅ **Quick Contact Form**: Professional lead capture form added before footer

✅ **SEO Enhancements**: 
   - Meta tags optimized
   - Open Graph tags configured
   - Twitter cards implemented
   - Canonical URLs set

## Testing Checklist

1. [ ] Test Google Analytics tracking after adding your ID
2. [ ] Submit a test form to verify Formspree integration
3. [ ] Check all phone number links on mobile devices
4. [ ] Validate schema markup using [Google's Rich Results Test](https://search.google.com/test/rich-results)
5. [ ] Test form on mobile devices for responsive layout

## Notes

- The website is optimized for Chicago & North Shore property management searches
- All critical SEO elements are in place
- Mobile-responsive design is implemented
- The contact form collects: Name, Email, Phone, Property Type, Address, and Message

## Support

For any issues with setup, contact your web developer or refer to:
- [Google Analytics Help](https://support.google.com/analytics)
- [Formspree Documentation](https://help.formspree.io/)
- [Schema.org Documentation](https://schema.org/)