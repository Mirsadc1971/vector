#!/usr/bin/env python3
"""
Google Search Console Issue Diagnostic & Fix Script
Identifies and fixes: 404s, redirects, robots.txt blocks, non-indexed pages, duplicates
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import hashlib

class SearchConsoleDiagnostics:
    def __init__(self):
        self.base_url = "https://manage369.com"
        self.issues = {
            '404_errors': [],
            'redirect_errors': [],
            'robots_blocked': [],
            'not_indexed': [],
            'duplicate_content': [],
            'fixes_applied': []
        }
        self.all_pages = []
        self.internal_links = defaultdict(list)
        
    def scan_all_files(self):
        """Scan all HTML files in the project"""
        print("=" * 70)
        print("SCANNING ALL FILES")
        print("=" * 70)
        
        html_files = list(Path('.').glob('**/*.html'))
        
        for file_path in html_files:
            # Skip unwanted directories
            if any(skip in str(file_path) for skip in ['node_modules', '.git', 'stellar-repo']):
                continue
                
            self.all_pages.append(str(file_path).replace('\\', '/'))
            
            # Extract all links from the file
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    links = re.findall(r'href=["\'](.*?)["\']', content, re.IGNORECASE)
                    for link in links:
                        if not link.startswith(('http', 'mailto:', 'tel:', '#')):
                            self.internal_links[str(file_path)].append(link)
            except:
                pass
        
        print(f"Found {len(self.all_pages)} HTML files")
        print(f"Found {sum(len(v) for v in self.internal_links.values())} internal links")
    
    def diagnose_404_errors(self):
        """Find all 404 errors (broken internal links)"""
        print("\n" + "=" * 70)
        print("DIAGNOSING 404 ERRORS")
        print("=" * 70)
        
        broken_links = defaultdict(list)
        
        for source_file, links in self.internal_links.items():
            for link in links:
                # Clean up the link
                link_clean = link.split('?')[0].split('#')[0]
                if not link_clean:
                    continue
                
                # Resolve the link path
                if link_clean.startswith('/'):
                    target_path = link_clean[1:]
                else:
                    # Relative path
                    source_dir = os.path.dirname(source_file)
                    target_path = os.path.normpath(os.path.join(source_dir, link_clean))
                    target_path = target_path.replace('\\', '/')
                
                # Check if target exists
                if not Path(target_path).exists():
                    # Try adding .html
                    if not target_path.endswith('.html'):
                        if not Path(target_path + '.html').exists():
                            # Check if it's a directory with index.html
                            index_path = os.path.join(target_path, 'index.html')
                            if not Path(index_path).exists():
                                broken_links[link].append(source_file)
                    else:
                        broken_links[link].append(source_file)
        
        # Add to issues
        for link, sources in broken_links.items():
            self.issues['404_errors'].append({
                'url': link,
                'found_in': sources[:5],  # First 5 sources
                'occurrences': len(sources)
            })
        
        print(f"Found {len(broken_links)} unique 404 errors")
        
        # Show top 10
        for i, (link, sources) in enumerate(list(broken_links.items())[:10], 1):
            print(f"\n{i}. {link}")
            print(f"   Found in {len(sources)} files")
            print(f"   Example: {sources[0]}")
    
    def diagnose_redirect_errors(self):
        """Find redirect chains and errors"""
        print("\n" + "=" * 70)
        print("DIAGNOSING REDIRECT ERRORS")  
        print("=" * 70)
        
        # Read _redirects file
        redirects = {}
        redirect_chains = []
        
        if Path('_redirects').exists():
            with open('_redirects', 'r') as f:
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        parts = line.split()
                        if len(parts) >= 3:
                            from_url = parts[0]
                            to_url = parts[1]
                            redirects[from_url] = to_url
        
        # Check for redirect chains
        for from_url, to_url in redirects.items():
            if to_url in redirects:
                # This creates a chain
                chain = [from_url, to_url]
                next_url = redirects[to_url]
                while next_url in redirects and next_url not in chain:
                    chain.append(next_url)
                    next_url = redirects[next_url]
                chain.append(next_url)
                
                if len(chain) > 2:
                    redirect_chains.append(chain)
        
        # Check for redirects to 404s
        redirects_to_404 = []
        for from_url, to_url in redirects.items():
            if not to_url.startswith('http'):
                # Check if target exists
                target_path = to_url[1:] if to_url.startswith('/') else to_url
                if not Path(target_path).exists() and not Path(target_path.replace('/', '')).exists():
                    redirects_to_404.append({
                        'from': from_url,
                        'to': to_url,
                        'issue': 'Redirects to non-existent page'
                    })
        
        self.issues['redirect_errors'] = {
            'chains': redirect_chains,
            'to_404': redirects_to_404,
            'total_redirects': len(redirects)
        }
        
        print(f"Total redirects: {len(redirects)}")
        print(f"Redirect chains: {len(redirect_chains)}")
        print(f"Redirects to 404: {len(redirects_to_404)}")
        
        if redirect_chains:
            print("\n[REDIRECT CHAINS FOUND]")
            for chain in redirect_chains[:5]:
                print(f"  {' -> '.join(chain)}")
    
    def diagnose_robots_blocked(self):
        """Find pages blocked by robots.txt"""
        print("\n" + "=" * 70)
        print("DIAGNOSING ROBOTS.TXT BLOCKS")
        print("=" * 70)
        
        blocked_pages = []
        disallow_rules = []
        
        # Parse robots.txt
        if Path('robots.txt').exists():
            with open('robots.txt', 'r') as f:
                for line in f:
                    if line.strip().startswith('Disallow:'):
                        rule = line.replace('Disallow:', '').strip()
                        if rule and rule != '/':
                            disallow_rules.append(rule)
        
        # Check which pages are blocked
        for page in self.all_pages:
            page_url = '/' + page
            
            for rule in disallow_rules:
                if rule.endswith('/'):
                    # Directory block
                    if rule[:-1] in page_url:
                        blocked_pages.append({
                            'page': page,
                            'rule': rule,
                            'url': self.base_url + '/' + page
                        })
                        break
                elif rule.endswith('*'):
                    # Wildcard block
                    pattern = rule[:-1]
                    if pattern in page_url:
                        blocked_pages.append({
                            'page': page,
                            'rule': rule,
                            'url': self.base_url + '/' + page
                        })
                        break
                else:
                    # Exact match
                    if rule == page_url:
                        blocked_pages.append({
                            'page': page,
                            'rule': rule,
                            'url': self.base_url + '/' + page
                        })
                        break
        
        self.issues['robots_blocked'] = blocked_pages
        
        print(f"Disallow rules: {len(disallow_rules)}")
        print(f"Pages blocked: {len(blocked_pages)}")
        
        if blocked_pages:
            print("\n[BLOCKED PAGES] (First 10)")
            for i, blocked in enumerate(blocked_pages[:10], 1):
                print(f"{i}. {blocked['page']}")
                print(f"   Blocked by: {blocked['rule']}")
    
    def diagnose_not_indexed(self):
        """Identify why pages are not indexed"""
        print("\n" + "=" * 70)
        print("DIAGNOSING NON-INDEXED PAGES")
        print("=" * 70)
        
        not_indexed_reasons = defaultdict(list)
        
        for page_path in self.all_pages:
            try:
                with open(page_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                reasons = []
                
                # Check for noindex
                if 'noindex' in content.lower():
                    reasons.append('Has noindex meta tag')
                
                # Check for canonical pointing elsewhere
                canonical_match = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']', content, re.IGNORECASE)
                if canonical_match:
                    canonical_url = canonical_match.group(1)
                    expected_url = self.base_url + '/' + page_path.replace('\\', '/')
                    if canonical_url != expected_url and not page_path.endswith('index.html'):
                        reasons.append(f'Canonical points to: {canonical_url}')
                else:
                    reasons.append('Missing canonical tag')
                
                # Check for thin content
                text_content = re.sub(r'<[^>]+>', '', content)
                text_content = re.sub(r'\s+', ' ', text_content)
                word_count = len(text_content.split())
                
                if word_count < 300:
                    reasons.append(f'Thin content ({word_count} words)')
                
                # Check for meta description
                if not re.search(r'<meta\s+name=["\']description["\']', content, re.IGNORECASE):
                    reasons.append('Missing meta description')
                
                # Check for title
                if not re.search(r'<title>', content, re.IGNORECASE):
                    reasons.append('Missing title tag')
                
                # Check if orphaned (no internal links pointing to it)
                is_linked = False
                for source, links in self.internal_links.items():
                    for link in links:
                        if page_path in link or page_path.replace('.html', '') in link:
                            is_linked = True
                            break
                    if is_linked:
                        break
                
                if not is_linked and page_path != 'index.html':
                    reasons.append('Orphaned page (no internal links)')
                
                if reasons:
                    not_indexed_reasons[page_path] = reasons
                    
            except Exception as e:
                not_indexed_reasons[page_path] = [f'Error reading file: {e}']
        
        self.issues['not_indexed'] = dict(not_indexed_reasons)
        
        print(f"Pages with indexing issues: {len(not_indexed_reasons)}")
        
        # Group by reason
        reason_counts = defaultdict(int)
        for reasons in not_indexed_reasons.values():
            for reason in reasons:
                if 'Canonical points to' in reason:
                    reason_counts['Wrong canonical'] += 1
                else:
                    reason_counts[reason] += 1
        
        print("\n[INDEXING ISSUES BY TYPE]")
        for reason, count in sorted(reason_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {reason}: {count} pages")
    
    def diagnose_duplicate_content(self):
        """Find duplicate content issues"""
        print("\n" + "=" * 70)
        print("DIAGNOSING DUPLICATE CONTENT")
        print("=" * 70)
        
        content_hashes = defaultdict(list)
        title_duplicates = defaultdict(list)
        meta_duplicates = defaultdict(list)
        
        for page_path in self.all_pages:
            try:
                with open(page_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract title
                title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
                if title_match:
                    title = title_match.group(1).strip()
                    title_duplicates[title].append(page_path)
                
                # Extract meta description
                meta_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', content, re.IGNORECASE)
                if meta_match:
                    meta_desc = meta_match.group(1)
                    meta_duplicates[meta_desc].append(page_path)
                
                # Hash main content
                body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.IGNORECASE | re.DOTALL)
                if body_match:
                    body_content = body_match.group(1)
                    # Remove scripts and styles
                    body_content = re.sub(r'<script.*?</script>', '', body_content, flags=re.IGNORECASE | re.DOTALL)
                    body_content = re.sub(r'<style.*?</style>', '', body_content, flags=re.IGNORECASE | re.DOTALL)
                    body_content = re.sub(r'<[^>]+>', '', body_content)
                    body_content = ' '.join(body_content.split())
                    
                    if len(body_content) > 100:  # Only hash substantial content
                        content_hash = hashlib.md5(body_content.encode()).hexdigest()
                        content_hashes[content_hash].append(page_path)
                        
            except:
                pass
        
        # Find duplicates
        duplicate_issues = {
            'identical_content': [],
            'duplicate_titles': [],
            'duplicate_meta': []
        }
        
        for content_hash, pages in content_hashes.items():
            if len(pages) > 1:
                duplicate_issues['identical_content'].append(pages)
        
        for title, pages in title_duplicates.items():
            if len(pages) > 1:
                duplicate_issues['duplicate_titles'].append({
                    'title': title[:80],
                    'pages': pages
                })
        
        for meta, pages in meta_duplicates.items():
            if len(pages) > 1:
                duplicate_issues['duplicate_meta'].append({
                    'meta': meta[:80],
                    'pages': pages
                })
        
        self.issues['duplicate_content'] = duplicate_issues
        
        print(f"Identical content groups: {len(duplicate_issues['identical_content'])}")
        print(f"Duplicate titles: {len(duplicate_issues['duplicate_titles'])}")
        print(f"Duplicate meta descriptions: {len(duplicate_issues['duplicate_meta'])}")
        
        if duplicate_issues['identical_content']:
            print("\n[IDENTICAL CONTENT] (First 5)")
            for i, pages in enumerate(duplicate_issues['identical_content'][:5], 1):
                print(f"{i}. {pages[0]} == {pages[1]}")
                if len(pages) > 2:
                    print(f"   (+{len(pages)-2} more)")
    
    def generate_fixes(self):
        """Generate fixes for all issues"""
        print("\n" + "=" * 70)
        print("GENERATING FIXES")
        print("=" * 70)
        
        fixes = {
            'redirects_to_add': [],
            'robots_to_update': [],
            'canonicals_to_fix': [],
            'content_to_enhance': [],
            'duplicates_to_resolve': []
        }
        
        # Fix 404s with redirects
        print("\n[FIXING 404 ERRORS]")
        for error in self.issues['404_errors'][:20]:  # Fix top 20
            broken_link = error['url']
            
            # Try to find the correct target
            if '.html' not in broken_link:
                # Might be missing extension
                potential_fix = broken_link + '.html'
                fixes['redirects_to_add'].append(f"{broken_link} {potential_fix} 301!")
            elif broken_link.startswith('/property-management-'):
                # Old URL pattern
                location = broken_link.replace('/property-management-', '').replace('.html', '')
                new_url = f"/property-management/{location}/"
                fixes['redirects_to_add'].append(f"{broken_link} {new_url} 301!")
        
        # Fix redirect chains
        print("\n[FIXING REDIRECT CHAINS]")
        if self.issues['redirect_errors'].get('chains'):
            for chain in self.issues['redirect_errors']['chains']:
                # Direct first to last
                fixes['redirects_to_add'].append(f"{chain[0]} {chain[-1]} 301!")
        
        # Fix robots.txt blocks
        print("\n[FIXING ROBOTS.TXT]")
        important_pages = [p for p in self.issues['robots_blocked'] 
                          if 'property-management' in p['page'] or 'services' in p['page']]
        if important_pages:
            fixes['robots_to_update'].append("Add Allow rules for important pages:")
            for page in important_pages[:10]:
                fixes['robots_to_update'].append(f"Allow: /{page['page']}")
        
        # Fix non-indexed pages
        print("\n[FIXING NON-INDEXED PAGES]")
        for page, reasons in list(self.issues['not_indexed'].items())[:20]:
            if 'Thin content' in ' '.join(reasons):
                fixes['content_to_enhance'].append({
                    'page': page,
                    'action': 'Add 300+ words of relevant content'
                })
            if 'Missing canonical tag' in reasons:
                canonical_url = self.base_url + '/' + page.replace('\\', '/')
                if page.endswith('/index.html'):
                    canonical_url = canonical_url.replace('/index.html', '/')
                fixes['canonicals_to_fix'].append({
                    'page': page,
                    'canonical': canonical_url
                })
        
        # Fix duplicates
        print("\n[FIXING DUPLICATE CONTENT]")
        for dup_group in self.issues['duplicate_content']['identical_content'][:10]:
            # Keep first, canonicalize others to it
            primary = dup_group[0]
            for secondary in dup_group[1:]:
                fixes['duplicates_to_resolve'].append({
                    'page': secondary,
                    'canonical_to': self.base_url + '/' + primary.replace('\\', '/')
                })
        
        return fixes
    
    def save_report(self, fixes):
        """Save diagnostic report and fixes"""
        report = {
            'scan_date': datetime.now().isoformat(),
            'summary': {
                '404_errors': len(self.issues['404_errors']),
                'redirect_errors': len(self.issues['redirect_errors'].get('chains', [])),
                'robots_blocked': len(self.issues['robots_blocked']),
                'not_indexed': len(self.issues['not_indexed']),
                'duplicate_content': len(self.issues['duplicate_content']['identical_content'])
            },
            'issues': self.issues,
            'fixes': fixes
        }
        
        # Save JSON report
        with open('search_console_diagnostic_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        # Generate fix scripts
        self.generate_fix_scripts(fixes)
        
        print("\n" + "=" * 70)
        print("REPORT SAVED")
        print("=" * 70)
        print("Files created:")
        print("  - search_console_diagnostic_report.json")
        print("  - fix_redirects.txt")
        print("  - fix_canonicals.py") 
        print("  - fix_robots.txt")
        
    def generate_fix_scripts(self, fixes):
        """Generate executable fix scripts"""
        
        # Generate redirect fixes
        if fixes['redirects_to_add']:
            with open('fix_redirects.txt', 'w') as f:
                f.write("# Add these to _redirects file\n\n")
                f.write("# Fix 404 errors\n")
                for redirect in fixes['redirects_to_add']:
                    f.write(redirect + '\n')
        
        # Generate canonical fix script
        if fixes['canonicals_to_fix'] or fixes['duplicates_to_resolve']:
            script = '''import re
from pathlib import Path

def add_canonical(file_path, canonical_url):
    """Add or update canonical tag"""
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    if '<link rel="canonical"' in html:
        html = re.sub(
            r'<link\\s+rel=["\']canonical["\'].*?>',
            f'<link rel="canonical" href="{canonical_url}">',
            html, flags=re.IGNORECASE
        )
    else:
        html = html.replace('</head>', f'    <link rel="canonical" href="{canonical_url}">\\n</head>')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Fixed: {file_path}")

# Fix missing canonicals
canonicals_to_fix = '''
            
            script += str(fixes['canonicals_to_fix']) + '\n\n'
            script += '''
for fix in canonicals_to_fix:
    if Path(fix['page']).exists():
        add_canonical(fix['page'], fix['canonical'])

# Fix duplicates
duplicates = '''
            script += str(fixes['duplicates_to_resolve']) + '\n\n'
            script += '''
for fix in duplicates:
    if Path(fix['page']).exists():
        add_canonical(fix['page'], fix['canonical_to'])

print("Canonical fixes applied!")
'''
            
            with open('fix_canonicals.py', 'w') as f:
                f.write(script)
        
        # Generate robots.txt fixes
        if fixes['robots_to_update']:
            with open('fix_robots.txt', 'w') as f:
                f.write("# Add these Allow rules before Disallow rules\n\n")
                for rule in fixes['robots_to_update']:
                    f.write(rule + '\n')
    
    def run_diagnostics(self):
        """Run all diagnostics"""
        self.scan_all_files()
        self.diagnose_404_errors()
        self.diagnose_redirect_errors()
        self.diagnose_robots_blocked()
        self.diagnose_not_indexed()
        self.diagnose_duplicate_content()
        fixes = self.generate_fixes()
        self.save_report(fixes)
        
        # Print summary
        print("\n" + "=" * 70)
        print("DIAGNOSTIC SUMMARY")
        print("=" * 70)
        print(f"✗ 404 Errors: {len(self.issues['404_errors'])}")
        print(f"✗ Redirect Chains: {len(self.issues['redirect_errors'].get('chains', []))}")
        print(f"✗ Robots Blocked: {len(self.issues['robots_blocked'])}")
        print(f"✗ Not Indexed: {len(self.issues['not_indexed'])}")
        print(f"✗ Duplicate Content: {len(self.issues['duplicate_content']['identical_content'])}")
        print(f"\n✓ Fixes Generated: {sum(len(v) for v in fixes.values())}")
        
        return self.issues, fixes

if __name__ == "__main__":
    diagnostics = SearchConsoleDiagnostics()
    issues, fixes = diagnostics.run_diagnostics()
    
    print("\n" + "=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    print("1. Review search_console_diagnostic_report.json")
    print("2. Apply redirects from fix_redirects.txt to _redirects")
    print("3. Run: python fix_canonicals.py")
    print("4. Update robots.txt with fix_robots.txt")
    print("5. Re-submit sitemap to Google Search Console")
    print("6. Request re-indexing for fixed pages")