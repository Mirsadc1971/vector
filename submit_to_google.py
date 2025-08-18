"""
Google Search Console Indexing API Script
Run this after deployment to request indexing of key pages
"""

# IMPORTANT: This requires Google Search Console API setup
# 1. Go to Google Cloud Console
# 2. Enable Indexing API
# 3. Create service account
# 4. Add service account email to Search Console as owner
# 5. Download credentials JSON

import json
import requests
from oauth2client.service_account import ServiceAccountCredentials
import httplib2

SCOPES = ["https://www.googleapis.com/auth/indexing"]

# Key pages to submit for indexing
URLS = [
    "https://manage369.com/",
    "https://manage369.com/contact.html",
    "https://manage369.com/services.html",
    "https://manage369.com/property-management/glenview/",
    "https://manage369.com/property-management/wilmette/",
    "https://manage369.com/property-management/winnetka/",
    "https://manage369.com/property-management/highland-park/",
    "https://manage369.com/property-management/northbrook/",
    "https://manage369.com/property-management/evanston/",
    "https://manage369.com/property-management/skokie/"
]

def index_url(url, credentials_file="credentials.json"):
    """Submit URL to Google for indexing"""
    
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        credentials_file, scopes=SCOPES
    )
    http = credentials.authorize(httplib2.Http())
    
    content = {
        "url": url,
        "type": "URL_UPDATED"
    }
    
    response, content = http.request(
        "https://indexing.googleapis.com/v3/urlNotifications:publish",
        method="POST",
        body=json.dumps(content),
        headers={"Content-Type": "application/json"}
    )
    
    return response, content

if __name__ == "__main__":
    print("Submitting URLs to Google Indexing API...")
    for url in URLS:
        try:
            response, content = index_url(url)
            print(f"✓ Submitted: {url}")
        except Exception as e:
            print(f"✗ Failed: {url} - {str(e)}")
