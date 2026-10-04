import urllib.request
import re

req = urllib.request.Request('https://tmforgchart.xyz/', headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
    with open('tmforgchart_raw.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Downloaded HTML, size:", len(html))

    # Find all JS script tags
    scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', html)
    print("Scripts:", scripts)

    # Let's download the scripts to find the org chart definitions
    for s in scripts:
        s_url = s if s.startswith('http') else 'https://tmforgchart.xyz' + (s if s.startswith('/') else '/' + s)
        print("Fetching script:", s_url)
        s_req = urllib.request.Request(s_url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(s_req) as s_resp:
                s_js = s_resp.read().decode('utf-8', errors='ignore')
            with open('tmforgchart_app.js', 'w', encoding='utf-8') as f:
                f.write(s_js)
            print("Saved script, size:", len(s_js))
        except Exception as e:
            print("Error fetching script:", e)

except Exception as e:
    print("Error:", e)
