import re

# Read the file
with open(r'C:\Users\mirsa\manage369-live\property-management\norridge\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all problematic characters
replacements = {
    '–': '-',  # em dash to hyphen
    '—': '-',  # en dash to hyphen  
    ''': "'",  # smart quote
    ''': "'",  # smart quote
    '"': '"',  # smart quote
    '"': '"',  # smart quote
    '…': '...',  # ellipsis
    '•': '*',  # bullet
    '™': '(TM)',  # trademark
    '®': '(R)',  # registered
    '©': '(C)',  # copyright
    '°': ' degrees',  # degree symbol
    '½': '1/2',  # fraction
    '¼': '1/4',  # fraction
    '¾': '3/4',  # fraction
    '\u2013': '-',  # Unicode em dash
    '\u2014': '-',  # Unicode en dash
    '\u2018': "'",  # Unicode left single quote
    '\u2019': "'",  # Unicode right single quote/apostrophe
    '\u201C': '"',  # Unicode left double quote
    '\u201D': '"',  # Unicode right double quote
    '\u2026': '...',  # Unicode ellipsis
    '\u2022': '*',  # Unicode bullet
}

for old, new in replacements.items():
    content = content.replace(old, new)

# Write the file back
with open(r'C:\Users\mirsa\manage369-live\property-management\norridge\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed encoding issues in Norridge page")