import os
import re

def remove_fake_statistics(filepath):
    """Remove fake Units Managed and Years statistics, keep only 24/7 and 100% stats"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    
    # Pattern to find the entire statistics grid section
    pattern = r'(<div class="stats-grid"[^>]*>)(.*?)(</div>\s*</div>)'
    
    def replace_stats(match):
        # Replace with only the two truthful statistics
        new_stats = """<div class="stat-box" style="flex: 1; min-width: 200px; text-align: center; padding: 20px; background: #f8f9fa; border-radius: 8px;">
                        <div style="font-size: 2em; font-weight: bold; color: #4285f4;">24/7</div>
                        <div style="color: #666; margin-top: 10px;">Emergency Response</div>
                    </div>
                    <div class="stat-box" style="flex: 1; min-width: 200px; text-align: center; padding: 20px; background: #f8f9fa; border-radius: 8px;">
                        <div style="font-size: 2em; font-weight: bold; color: #4285f4;">100%</div>
                        <div style="color: #666; margin-top: 10px;">Local Knowledge</div>
                    </div>"""
        return match.group(1) + new_stats + match.group(3)
    
    # Replace the statistics section
    new_content = re.sub(pattern, replace_stats, content, flags=re.DOTALL)
    
    if new_content != content:
        modified = True
        
        # Also remove any references to specific numbers of years or units in the text
        # Pattern for "managing XXX+ units" or "XXX+ units managed"
        new_content = re.sub(r'currently managing \d+\+ units', 'currently managing multiple properties', new_content)
        new_content = re.sub(r'managing \d+\+ units', 'managing multiple properties', new_content)
        
        # Pattern for "over XX years" or "XX+ years"
        new_content = re.sub(r'for over \d+ years', 'for many years', new_content)
        new_content = re.sub(r'over \d+\+ years', 'many years', new_content)
        new_content = re.sub(r'\d+\+ years', 'many years', new_content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"  Removed fake statistics from {filepath}")
        return True
    
    return False

def main():
    """Remove fake statistics from all location pages"""
    
    property_mgmt_dir = 'property-management'
    processed = 0
    
    if os.path.exists(property_mgmt_dir):
        locations = os.listdir(property_mgmt_dir)
        print(f"Processing {len(locations)} location directories...")
        
        for location in locations:
            location_path = os.path.join(property_mgmt_dir, location)
            if os.path.isdir(location_path):
                index_file = os.path.join(location_path, 'index.html')
                if os.path.exists(index_file):
                    if remove_fake_statistics(index_file):
                        processed += 1
    
    print(f"\n[COMPLETE] Removed fake statistics from {processed} pages")
    print("Pages now show only truthful statistics: 24/7 Emergency Response and 100% Local Knowledge")

if __name__ == "__main__":
    main()