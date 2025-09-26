import re

with open('src/pages/locations/suburbs/index.astro', 'r') as f:
    content = f.read()

# Fix all the links - remove leading slashes since we're already in /locations/suburbs/
content = re.sub(r'href="/locations/suburbs/([^"]+)"', r'href="\1"', content)

with open('src/pages/locations/suburbs/index.astro', 'w') as f:
    f.write(content)

print("Fixed all suburb links to be relative")
