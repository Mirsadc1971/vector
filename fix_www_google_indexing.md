# Fix WWW URL Not on Google

## Current Status
✅ Redirect is working: https://www.manage369.com/ → https://manage369.com/ (301)
❌ Google still shows "URL not on Google" for www version

## Solution Steps

### 1. Netlify Domain Configuration
Ensure both domains are configured in Netlify:
- Primary domain: manage369.com
- Domain alias: www.manage369.com

In Netlify Dashboard:
1. Go to Site settings → Domain management
2. Add www.manage369.com as a domain alias
3. Set manage369.com as primary domain

### 2. DNS Configuration
Your DNS should have:
```
Type    Name    Value
CNAME   www     manage369.netlify.app (or your Netlify subdomain)
A       @       75.2.60.5 (Netlify's load balancer)
```

### 3. Update _redirects File (Already Done)
```
# Force www to non-www
https://www.manage369.com/*    https://manage369.com/:splat    301!
http://www.manage369.com/*     https://manage369.com/:splat    301!
```

### 4. Google Search Console Actions

#### A. Add Both Versions to Search Console
1. Add property: https://manage369.com/ (already done)
2. Add property: https://www.manage369.com/
3. Verify both properties

#### B. Set Preferred Domain
1. In Search Console for www version
2. Go to Settings → Change of Address
3. Select https://manage369.com/ as the new site

#### C. Submit URL Removal
1. Go to Google Search Console
2. Select the www version property
3. Click "Removals" → "New Request"
4. Choose "Remove all URLs with this prefix"
5. Enter: https://www.manage369.com/
6. Select "Remove all URLs with this prefix"

#### D. Update Sitemap Submission
1. In the non-www property (https://manage369.com/)
2. Go to Sitemaps
3. Ensure sitemap.xml is submitted
4. It should show as "Success"

### 5. Request Indexing
1. Go to URL Inspection tool
2. Enter: https://manage369.com/
3. Click "Request Indexing"

### 6. Additional Verification File
Create a verification file to confirm redirect is working: