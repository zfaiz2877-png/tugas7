import urllib.request
import re
import json

url = 'https://www.w3schools.com/html/default.asp'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')

# Save html to examine if needed
with open('w3schools_page.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Extract navigation / sections
# Look for leftmenu or sidebar navigation
sections = {}
current_section = "HTML Tutorial"

# Let's find leftmenu
idx_start = html.find('id="leftmenuinnerinner"')
if idx_start == -1:
    idx_start = html.find('id="leftmenuinner"')
if idx_start == -1:
    idx_start = html.find('id="sidenav"')

print(f"Found menu at index {idx_start}")

# Regex to find h2, h3, a within sidebar
# Let's parse all sections and their links in the page
lines = html[idx_start:idx_start+50000].split('\n') if idx_start != -1 else html.split('\n')

for line in lines:
    h2_match = re.search(r'<h2[^>]*>(.*?)</h2>', line, re.IGNORECASE)
    if h2_match:
        current_section = re.sub(r'<[^>]+>', '', h2_match.group(1)).strip()
        sections[current_section] = []
        continue
    
    a_match = re.search(r'<a[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', line, re.IGNORECASE)
    if a_match:
        href = a_match.group(1)
        title = re.sub(r'<[^>]+>', '', a_match.group(2)).strip()
        if href.startswith('html_') or href.startswith('default.asp') or '/html/' in href:
            if current_section not in sections:
                sections[current_section] = []
            sections[current_section].append({'title': title, 'href': href})

for sec, links in sections.items():
    print(f"\n[{sec}] ({len(links)} links)")
    for l in links:
        print(f"  - {l['title']} ({l['href']})")
