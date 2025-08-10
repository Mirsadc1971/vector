import re

# Read the file
with open(r'C:\Users\mirsa\manage369-live\property-management\norridge\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the start of the body tag
body_start = content.find('<body>')

if body_start == -1:
    print("Error: Could not find <body> tag")
    exit(1)

# Extract everything before </script> of the schema markup and everything from <body> onwards
# We need to properly close the head tag

# Find the last </script> before body
script_end = content.rfind('</script>', 0, body_start)
if script_end == -1:
    print("Error: Could not find </script> tag")
    exit(1)

# Get the part before the broken styles (up to and including the schema script)
head_part = content[:script_end + len('</script>')]

# Add proper head closing and get body part
body_part = content[body_start:]

# Combine with proper head closing
new_content = head_part + '\n</head>\n' + body_part

# Write back
with open(r'C:\Users\mirsa\manage369-live\property-management\norridge\index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Rebuilt Norridge page - removed all inline styles")