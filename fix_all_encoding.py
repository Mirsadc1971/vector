import os
import re
import glob

# Dictionary of all problematic characters to replace
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

# Find all property management HTML files
pm_files = glob.glob(r'C:\Users\mirsa\manage369-live\property-management\*\index.html')

fixed_count = 0
for file_path in pm_files:
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file needs fixing
        needs_fixing = False
        for char in replacements.keys():
            if char in content:
                needs_fixing = True
                break
        
        if needs_fixing:
            # Apply all replacements
            for old, new in replacements.items():
                content = content.replace(old, new)
            
            # Write the file back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            location = os.path.basename(os.path.dirname(file_path))
            print(f"Fixed encoding in: {location}")
            fixed_count += 1
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

print(f"\nTotal files fixed: {fixed_count}")
print("All property management pages have been checked and fixed for encoding issues.")