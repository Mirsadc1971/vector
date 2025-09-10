import os
import re

def update_savings_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update the CTA that mentions 75% in the strategic link section
    content = content.replace("reduced costs by 75%", "reduced costs by 50%")
    
    # Update the bottom CTA that mentions 75%
    content = content.replace("Start Saving 75% on Property Management Today", "Start Saving 50% on Property Management")
    
    # Update any other 75% references
    content = content.replace("Save 75%", "Save 50%")
    content = content.replace("save 75%", "save 50%")
    content = content.replace("75% savings", "50% savings")
    content = content.replace("75% Savings", "50% Savings")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

# Update all area pages
updated_count = 0
for root, dirs, files in os.walk('property-management'):
    if 'node_modules' in root or '.git' in root:
        continue
    
    for file in files:
        if file == 'index.html':
            filepath = os.path.join(root, file)
            if update_savings_in_file(filepath):
                updated_count += 1
                print(f"Updated: {filepath}")

print(f"\nTotal files updated: {updated_count}")
print("\nPromotion updated to:")
print("  Year 1: 35% off")
print("  Year 2: 15% off") 
print("  Year 3: Regular price")
print("  Total savings: 50% over 2 years")