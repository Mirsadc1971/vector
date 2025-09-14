#!/usr/bin/env python3
import os

updates = [
    {
        'file': 'roselle/index.html',
        'old_intro': "Roselle combines family-friendly neighborhoods with a strong business district. Boards here face:",
        'new_intro': "Roselle associations face:",
        'old_challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Townhome communities with aging infrastructure</li>
<li style="padding: 10px 0; color: var(--text-light);">• HOAs managing stormwater retention ponds</li>
<li style="padding: 10px 0; color: var(--text-light);">• Capital planning for roofing and siding projects</li>
<li style="padding: 10px 0; color: var(--text-light);">• Boards balancing amenity costs with budgets</li>''',
        'new_challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Shared amenities like pools and playgrounds</li>
<li style="padding: 10px 0; color: var(--text-light);">• Townhome reserves for exterior upkeep</li>
<li style="padding: 10px 0; color: var(--text-light);">• Budget-conscious boards balancing limited reserves</li>
<li style="padding: 10px 0; color: var(--text-light);">• Residents expecting professional digital communication</li>''',
        'old_footer': "With 18+ years serving Chicago's North Shore and Northwest suburbs, Manage369 understands Roselle's unique property management needs. Our certified managers provide the expertise, transparency, and hands-on service your board deserves.",
        'new_footer': "👉 Manage369 delivers hands-on support, proactive planning, and clear reporting for Roselle boards."
    },
    {
        'file': 'bartlett/index.html',
        'old_intro': "Bartlett offers a mix of townhome associations and suburban HOAs. Boards often deal with:",
        'new_intro': "Bartlett boards often manage:",
        'old_challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Reserve planning for large townhome complexes</li>
<li style="padding: 10px 0; color: var(--text-light);">• Shared amenities like pools and playgrounds</li>
<li style="padding: 10px 0; color: var(--text-light);">• Snow removal costs during long winters</li>
<li style="padding: 10px 0; color: var(--text-light);">• Residents expecting consistent board communication</li>''',
        'new_challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Large townhome HOAs with capital projects</li>
<li style="padding: 10px 0; color: var(--text-light);">• Common amenities needing regular upkeep</li>
<li style="padding: 10px 0; color: var(--text-light);">• Snow removal and landscaping costs</li>
<li style="padding: 10px 0; color: var(--text-light);">• Residents demanding financial transparency</li>''',
        'old_footer': "With 18+ years serving Chicago's North Shore and Northwest suburbs, Manage369 understands Bartlett's unique property management needs. Our certified managers provide the expertise, transparency, and hands-on service your board deserves.",
        'new_footer': "👉 Manage369 provides disciplined budgeting, vendor management, and emergency support for Bartlett communities."
    },
    {
        'file': 'streamwood/index.html',
        'old_intro': "Streamwood is home to affordable condos and mid-size HOAs. Local challenges include:",
        'new_intro': "Streamwood challenges include:",
        'old_challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Older condo buildings with deferred maintenance</li>
<li style="padding: 10px 0; color: var(--text-light);">• Boards needing delinquency reduction strategies</li>
<li style="padding: 10px 0; color: var(--text-light);">• Stormwater management for low-lying areas</li>
<li style="padding: 10px 0; color: var(--text-light);">• Tight budgets in cost-sensitive associations</li>''',
        'new_challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Older condo systems needing constant repair</li>
<li style="padding: 10px 0; color: var(--text-light);">• Delinquencies in cost-sensitive communities</li>
<li style="padding: 10px 0; color: var(--text-light);">• Drainage and stormwater issues</li>
<li style="padding: 10px 0; color: var(--text-light);">• Boards requiring strong financial reporting</li>''',
        'old_footer': "With 18+ years serving Chicago's North Shore and Northwest suburbs, Manage369 understands Streamwood's unique property management needs. Our certified managers provide the expertise, transparency, and hands-on service your board deserves.",
        'new_footer': "👉 Manage369 stabilizes Streamwood associations with reserve planning, vendor oversight, and board-focused governance."
    },
    {
        'file': 'hanover-park/index.html',
        'old_intro': "Hanover Park is a diverse suburb with many mid-size associations. Local challenges include:",
        'new_intro': "Hanover Park boards face:",
        'old_challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Older condo HVAC and plumbing systems</li>
<li style="padding: 10px 0; color: var(--text-light);">• Boards needing strict financial controls</li>
<li style="padding: 10px 0; color: var(--text-light);">• HOAs balancing rising vendor costs</li>
<li style="padding: 10px 0; color: var(--text-light);">• Residents expecting clear board communication</li>''',
        'new_challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Townhome communities with deferred maintenance</li>
<li style="padding: 10px 0; color: var(--text-light);">• Budget-conscious HOAs balancing rising costs</li>
<li style="padding: 10px 0; color: var(--text-light);">• Plumbing and HVAC issues in aging condos</li>
<li style="padding: 10px 0; color: var(--text-light);">• Residents expecting quick response and clarity</li>''',
        'old_footer': "With 18+ years serving Chicago's North Shore and Northwest suburbs, Manage369 understands Hanover Park's unique property management needs. Our certified managers provide the expertise, transparency, and hands-on service your board deserves.",
        'new_footer': "👉 Manage369 ensures Hanover Park boards get transparent reporting, governance support, and emergency coverage."
    },
    {
        'file': 'addison/index.html',
        'old_intro': "Addison is home to diverse condos, townhomes, and small HOAs. Boards here face:",
        'new_intro': "Addison associations must manage:",
        'old_challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Older infrastructure in condo associations</li>
<li style="padding: 10px 0; color: var(--text-light);">• HOAs balancing snow removal and landscaping costs</li>
<li style="padding: 10px 0; color: var(--text-light);">• Capital projects for roofing & paving</li>
<li style="padding: 10px 0; color: var(--text-light);">• Boards needing strong financial planning</li>''',
        'new_challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Older infrastructure in garden-style condos</li>
<li style="padding: 10px 0; color: var(--text-light);">• Budget constraints and reserve challenges</li>
<li style="padding: 10px 0; color: var(--text-light);">• Roofing, paving, and siding projects</li>
<li style="padding: 10px 0; color: var(--text-light);">• Residents needing consistent communication</li>''',
        'old_footer': "With 18+ years serving Chicago's North Shore and Northwest suburbs, Manage369 understands Addison's unique property management needs. Our certified managers provide the expertise, transparency, and hands-on service your board deserves.",
        'new_footer': "👉 Manage369 provides Addison boards with financial clarity, cost efficiency, and 24/7 emergency response."
    },
    {
        'file': 'bensenville/index.html',
        'old_intro': "Bensenville combines affordable housing with suburban HOAs near O'Hare. Boards here manage:",
        'new_intro': "Bensenville boards deal with:",
        'old_challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Older condo HVAC & plumbing systems</li>
<li style="padding: 10px 0; color: var(--text-light);">• Snow removal contracts for large communities</li>
<li style="padding: 10px 0; color: var(--text-light);">• Budget challenges in cost-sensitive associations</li>
<li style="padding: 10px 0; color: var(--text-light);">• Residents expecting consistent communication</li>''',
        'new_challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Condos near O'Hare requiring frequent vendor support</li>
<li style="padding: 10px 0; color: var(--text-light);">• High snow removal and utility costs</li>
<li style="padding: 10px 0; color: var(--text-light);">• Small HOAs with limited reserves</li>
<li style="padding: 10px 0; color: var(--text-light);">• Residents expecting bilingual communication</li>''',
        'old_footer': "With 18+ years serving Chicago's North Shore and Northwest suburbs, Manage369 understands Bensenville's unique property management needs. Our certified managers provide the expertise, transparency, and hands-on service your board deserves.",
        'new_footer': "👉 Manage369 partners with Bensenville boards for governance, vendor oversight, and stable financial planning."
    },
    {
        'file': 'bloomingdale/index.html',
        'old_intro': "Bloomingdale features established HOAs and townhome communities. Boards here often manage:",
        'new_intro': "Bloomingdale associations manage:",
        'old_challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Large HOAs with complex governance needs</li>
<li style="padding: 10px 0; color: var(--text-light);">• Reserve planning for aging infrastructure</li>
<li style="padding: 10px 0; color: var(--text-light);">• Stormwater management in retention areas</li>
<li style="padding: 10px 0; color: var(--text-light);">• Boards balancing amenity costs with assessments</li>''',
        'new_challenges': '''<li style="padding: 10px 0; color: var(--text-light);">• Large HOA budgets with shared amenities (pools, clubhouses, green space)</li>
<li style="padding: 10px 0; color: var(--text-light);">• Reserve planning for capital projects</li>
<li style="padding: 10px 0; color: var(--text-light);">• Vendor coordination for landscaping and snow removal</li>
<li style="padding: 10px 0; color: var(--text-light);">• Residents expecting responsive digital tools</li>''',
        'old_footer': "With 18+ years serving Chicago's North Shore and Northwest suburbs, Manage369 understands Bloomingdale's unique property management needs. Our certified managers provide the expertise, transparency, and hands-on service your board deserves.",
        'new_footer': "👉 Manage369 helps Bloomingdale boards maintain property values with proactive management and transparent communication."
    }
]

os.chdir('C:\\Users\\mirsa\\Documents\\manage369-live\\property-management')

for update in updates:
    file_path = update['file']

    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace intro
    content = content.replace(update['old_intro'], update['new_intro'])

    # Replace challenges
    content = content.replace(update['old_challenges'], update['new_challenges'])

    # Replace footer
    content = content.replace(update['old_footer'], update['new_footer'])

    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Updated: {file_path}")