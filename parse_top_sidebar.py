import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('w3schools_page.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('id="leftmenuinnerinner"')
end = html.find('id="main"')
if start != -1 and end != -1:
    menu = html[start:end]
else:
    menu = html

# Let's parse all h2 and the subsequent a tags
sections = []
current_sec = None

for line in menu.split('\n'):
    h2 = re.search(r'<h2[^>]*>(.*?)</h2>', line)
    if h2:
        title = re.sub(r'<[^>]+>', '', h2.group(1)).strip()
        current_sec = {'title': title, 'items': []}
        sections.append(current_sec)
    a = re.search(r'<a[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', line)
    if a and current_sec:
        href = a.group(1)
        name = re.sub(r'<[^>]+>', '', a.group(2)).strip()
        if not href.startswith('javascript:') and 'exercise' not in href and 'challenge' not in href and 'quiz' not in href and not href.startswith('http') and not href.startswith('/'):
            if not any(item['href'] == href for item in current_sec['items']):
                current_sec['items'].append({'name': name, 'href': href})

for sec in sections[:10]:
    if sec['items']:
        print(f"\n======================================")
        print(f"KATEGORI: {sec['title']} (Total: {len(sec['items'])})")
        print(f"======================================")
        for it in sec['items']:
            print(f"  * {it['name']} -> {it['href']}")
