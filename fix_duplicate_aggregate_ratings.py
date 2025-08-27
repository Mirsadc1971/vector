#!/usr/bin/env python3
"""
Fix duplicate aggregate rating schemas that prevent rich results in Google Search
Removes all aggregate ratings and review schemas to clean up duplicate issues
"""

import os
import re
from pathlib import Path

def remove_aggregate_ratings(content):
    """Remove all aggregate rating and review schemas"""
    
    # Pattern 1: Remove aggregateRating blocks
    pattern1 = r',?\s*"aggregateRating"\s*:\s*\{[^}]*?"@type"\s*:\s*"AggregateRating"[^}]*?\}'
    content = re.sub(pattern1, '', content, flags=re.DOTALL)
    
    # Pattern 2: Remove review arrays
    pattern2 = r',?\s*"review"\s*:\s*\[[^\]]*?\]'
    content = re.sub(pattern2, '', content, flags=re.DOTALL)
    
    # Pattern 3: Remove single review objects
    pattern3 = r',?\s*"review"\s*:\s*\{[^}]*?"@type"\s*:\s*"Review"[^}]*?\}'
    content = re.sub(pattern3, '', content, flags=re.DOTALL)
    
    # Pattern 4: Clean up any aggregateRating that might be in a different format
    pattern4 = r'"aggregateRating"[^,}]*?(?:\{[^}]*?\})?[,]?'
    content = re.sub(pattern4, '', content, flags=re.DOTALL)
    
    # Clean up double commas that might result from removal
    content = re.sub(r',\s*,', ',', content)
    content = re.sub(r',\s*\}', '}', content)
    content = re.sub(r'\{\s*,', '{', content)
    
    return content

def process_file(file_path):
    """Process a single HTML file to remove duplicate ratings"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Count how many aggregate ratings exist
        rating_count = len(re.findall(r'"aggregateRating"', content, re.IGNORECASE))
        review_count = len(re.findall(r'"review"', content, re.IGNORECASE))
        
        if rating_count > 0 or review_count > 0:
            # Remove all aggregate ratings and reviews
            content = remove_aggregate_ratings(content)
            
            # Save the cleaned content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return rating_count, review_count
        
        return 0, 0
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return -1, -1

def main():
    print("Fixing Duplicate Aggregate Rating Schemas")
    print("=" * 60)
    print("\nThis will remove ALL aggregate ratings and reviews to fix")
    print("Google Search Console validation errors.\n")
    
    # Process main index
    print("Processing homepage...")
    ratings, reviews = process_file('index.html')
    if ratings > 0 or reviews > 0:
        print(f"  Removed {ratings} aggregate ratings and {reviews} review sections")
    
    # Process all HTML files in property-management directory
    property_dir = Path('property-management')
    if property_dir.exists():
        print("\nProcessing property management pages...")
        total_ratings = 0
        total_reviews = 0
        
        for location_dir in property_dir.iterdir():
            if location_dir.is_dir():
                index_file = location_dir / 'index.html'
                if index_file.exists():
                    ratings, reviews = process_file(index_file)
                    if ratings > 0 or reviews > 0:
                        print(f"  {location_dir.name}: Removed {ratings} ratings, {reviews} reviews")
                        total_ratings += ratings
                        total_reviews += reviews
        
        print(f"\nTotal removed from property pages: {total_ratings} ratings, {total_reviews} reviews")
    
    # Process service pages
    services_dir = Path('services')
    if services_dir.exists():
        print("\nProcessing service pages...")
        for service_dir in services_dir.iterdir():
            if service_dir.is_dir():
                index_file = service_dir / 'index.html'
                if index_file.exists():
                    ratings, reviews = process_file(index_file)
                    if ratings > 0 or reviews > 0:
                        print(f"  {service_dir.name}: Removed {ratings} ratings, {reviews} reviews")
    
    # Process other main pages
    print("\nProcessing other pages...")
    other_pages = [
        'contact.html',
        'services.html', 
        'payment-methods.html',
        'forms.html',
        'chicago-property-management-companies.html',
        'property-management-near-me.html',
        'property-management-cost-guide.html',
        'emergency-property-management-chicago.html'
    ]
    
    for page in other_pages:
        if Path(page).exists():
            ratings, reviews = process_file(page)
            if ratings > 0 or reviews > 0:
                print(f"  {page}: Removed {ratings} ratings, {reviews} reviews")
    
    print("\n" + "=" * 60)
    print("\nCleanup Complete!")
    print("\nWhat was fixed:")
    print("- Removed ALL aggregate rating schemas")
    print("- Removed ALL review schemas")
    print("- This eliminates duplicate rating errors in Google Search Console")
    
    print("\nNext steps:")
    print("1. Wait 24-48 hours for Google to recrawl")
    print("2. Check Google Search Console for validation")
    print("3. Consider adding back a SINGLE aggregate rating later if needed")
    print("\nNote: Removing ratings may temporarily affect rich snippets,")
    print("but it's better than having invalid markup that Google rejects.")

if __name__ == "__main__":
    main()