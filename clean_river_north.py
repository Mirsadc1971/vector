import re

# Read the file
with open(r'C:\Users\mirsa\manage369-live\property-management\river-north\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the first massive style block (lines ~112-752)
# This is causing all the display issues
content = re.sub(r'<style>.*?</style>', '', content, flags=re.DOTALL, count=1)

# Write back
with open(r'C:\Users\mirsa\manage369-live\property-management\river-north\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Removed the massive inline CSS block that was breaking the page")