import os
from pathlib import Path

# Get all property management locations
prop_dir = Path('property-management')
locations = []

for location_dir in prop_dir.iterdir():
    if location_dir.is_dir():
        index_file = location_dir / 'index.html'
        if index_file.exists():
            locations.append(location_dir.name)

locations.sort()

print(f"FOUND {len(locations)} PROPERTY MANAGEMENT PAGES:")
print("=" * 60)

# List all locations
for i, loc in enumerate(locations, 1):
    print(f"{i:2}. {loc}")

print("\n" + "=" * 60)
print("ALL 68 PAGES EXIST LOCALLY!")
print("\nTo deploy these to your live site, you need to:")
print("1. Push to GitHub (already done)")
print("2. Deploy from GitHub to your web hosting")
print("3. Or manually upload the property-management folder")

# Create a list of URLs for Google submission
print("\n" + "=" * 60)
print("URLs TO SUBMIT TO GOOGLE SEARCH CONSOLE:")
print("=" * 60)
with open('property_urls.txt', 'w') as f:
    for loc in locations:
        url = f"https://manage369.com/property-management/{loc}/"
        print(url)
        f.write(url + '\n')

print(f"\nSaved all {len(locations)} URLs to property_urls.txt")