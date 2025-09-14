import re

# List of 40 areas for townhome management
areas = [
    "Gold Coast", "River North", "Streeterville", "Lincoln Park",
    "Lakeview", "Old Town", "Loop", "South Loop",
    "West Loop", "Uptown", "Edgewater", "Andersonville",
    "Rogers Park", "Logan Square", "Bucktown", "Wicker Park",
    "Glenview", "Northbrook", "Highland Park", "Lake Forest",
    "Wilmette", "Winnetka", "Glencoe", "Evanston",
    "Kenilworth", "Lake Bluff", "Deerfield", "Libertyville",
    "Lincolnshire", "Mundelein", "Park Ridge", "Skokie",
    "Wheeling", "Buffalo Grove", "Vernon Hills", "Arlington Heights",
    "Mount Prospect", "Des Plaines", "Niles", "Morton Grove"
]

# Create the HTML for area cards
cards_html = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem;">\n'
for area in areas:
    area_slug = area.lower().replace(' ', '-')
    cards_html += f'<a href="../../property-management-{area_slug}.html" onmouseout="this.style.transform=\'translateY(0)\'" onmouseover="this.style.transform=\'translateY(-2px)\'" style="background: #1f2937; padding: 1rem; border-radius: 8px; text-decoration: none; color: #2c5aa0; font-weight: 600; text-align: center; box-shadow: 0 2px 5px rgba(0,0,0,0.1); transition: transform 0.3s;">{area} Townhome Management</a>\n'
cards_html += '</div>'

# Read the townhome management file
with open('services/townhome-management/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the section where we need to insert the cards
pattern = r'(<h2 class="section-title">Townhome Management Areas We Serve</h2>.*?<div style="text-align: center;">)'
replacement = r'\1\n' + cards_html + '\n<div style="text-align: center;">'

# Replace the section
content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Write back
with open('services/townhome-management/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Added 40 area cards to townhome management page")