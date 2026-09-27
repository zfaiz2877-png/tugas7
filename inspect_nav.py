import re
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

with open('w3schools_page.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('id="leftmenuinnerinner"')
end = html.find('id="main"')
if start != -1 and end != -1:
    menu_chunk = html[start:end]
else:
    menu_chunk = html

# Extract h2 (Sections), a (Links)
items = re.findall(r'(<h2[^>]*>(?:<span[^>]*>)?(.*?)(?:</span>)?</h2>|<a[^>]*href=["\']([^"\']+)["\'][^>]*>(?:<span[^>]*>)?(.*?)(?:</span>)?</a>)', menu_chunk, re.DOTALL)

current_sec = "TOP"
nav_tree = {}

for item in items:
    full_tag = item[0]
    h2_text = item[1]
    a_href = item[2]
    a_text = item[3]
    
    if full_tag.startswith('<h2'):
        clean_h2 = re.sub(r'<[^>]+>', '', h2_text).strip()
        current_sec = clean_h2
        nav_tree[current_sec] = []
    elif a_href:
        clean_text = re.sub(r'<[^>]+>', '', a_text).strip()
        if not a_href.startswith('javascript:') and clean_text:
            if current_sec not in nav_tree:
                nav_tree[current_sec] = []
            nav_tree[current_sec].append((clean_text, a_href))

for sec, links in nav_tree.items():
    print(f"\n[SECTION] {sec}:")
    for txt, href in links:
        if 'exercise' not in href and 'challenge' not in href and 'quiz' not in href:
            print(f"   - {txt} -> {href}")
