import os
import re
from pathlib import Path

def count_words_in_html(file_path):
    """Count actual text words in HTML file, excluding tags and code"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove script and style sections
        content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
        content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove HTML tags
        content = re.sub(r'<[^>]+>', ' ', content)
        
        # Remove HTML entities
        content = re.sub(r'&[a-z]+;', ' ', content)
        
        # Remove extra whitespace
        content = re.sub(r'\s+', ' ', content)
        
        # Count words (sequences of letters/numbers)
        words = re.findall(r'\b[a-zA-Z0-9]+\b', content)
        
        return len(words)
    except Exception as e:
        return 0

# Check all property-management subdirectories
property_dir = Path('property-management')
results = []

for area_dir in sorted(property_dir.iterdir()):
    if area_dir.is_dir():
        area_name = area_dir.name
        index_file = area_dir / 'index.html'
        
        if index_file.exists():
            word_count = count_words_in_html(index_file)
            
            if word_count < 2500:
                status = "NEEDS CONTENT"
            elif word_count < 3000:
                status = "BORDERLINE"
            else:
                status = "GOOD"
            
            results.append((status, area_name, word_count))
        else:
            results.append(("NO FILE", area_name, 0))

# Print results sorted by status
print("\n=== PROPERTY MANAGEMENT PAGES WORD COUNT VERIFICATION ===\n")

# Print pages needing attention first
print("PAGES NEEDING CONTENT:")
needs_work = [(s, n, w) for s, n, w in results if "NEEDS CONTENT" in s or "NO FILE" in s]
for status, name, words in needs_work:
    print(f"{status}: {name} - {words:,} words")

print("\nBORDERLINE PAGES (under 3000 words):")
borderline = [(s, n, w) for s, n, w in results if "BORDERLINE" in s]
for status, name, words in borderline:
    print(f"{status}: {name} - {words:,} words")

print("\nGOOD PAGES (3000+ words):")
good = [(s, n, w) for s, n, w in results if "GOOD" in s]
for status, name, words in good:
    print(f"{status}: {name} - {words:,} words")

# Summary
print(f"\n=== SUMMARY ===")
print(f"Total areas: {len(results)}")
print(f"Good (3000+ words): {len(good)}")
print(f"Borderline (2500-3000): {len(borderline)}")
print(f"Needs content (<2500): {len(needs_work)}")
print(f"\nAverage word count: {sum(w for _, _, w in results) / len(results):,.0f} words")