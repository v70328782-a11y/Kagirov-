from pathlib import Path
import re, subprocess, tempfile, sys
from html.parser import HTMLParser

ROOT = Path('.')
FILES = [Path('index.html'), Path('home-workout.html'), Path('women-body-mode.html')]
issues=[]
notes=[]

class Scanner(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids=[]
        self.links=[]
    def handle_starttag(self, tag, attrs):
        d=dict(attrs)
        if 'id' in d: self.ids.append(d['id'])
        for key in ('src','href'):
            if key in d and d[key]: self.links.append((tag,key,d[key]))

for file in FILES:
    if not file.exists():
        issues.append(f'{file}: FILE MISSING')
        continue
    text=file.read_text(encoding='utf-8')
    scan=Scanner()
    try:
        scan.feed(text)
        scan.close()
    except Exception as e:
        issues.append(f'{file}: HTML parser error: {e}')

    seen=set()
    for ident in scan.ids:
        if ident in seen:
            issues.append(f'{file}: duplicate id="{ident}"')
        seen.add(ident)

    for tag,key,value in scan.links:
        v=value.strip()
        if not v or v.startswith(('#','http://','https://','mailto:','tel:','data:','javascript:')):
            continue
        local=v.split('#',1)[0].split('?',1)[0]
        if local and not (file.parent/local).exists():
            issues.append(f'{file}: broken local {key}="{value}"')

    scripts=[]
    for m in re.finditer(r'<script\b([^>]*)>(.*?)</script\s*>', text, flags=re.I|re.S):
        attrs=m.group(1)
        body=m.group(2)
        if re.search(r'\bsrc\s*=', attrs, flags=re.I):
            continue
        t=re.search(r'\btype\s*=\s*["\']([^"\']+)',attrs,flags=re.I)
        if t and t.group(1).lower() not in ('text/javascript','application/javascript','module'):
            continue
        if body.strip(): scripts.append(body)
    for i,js in enumerate(scripts,1):
        with tempfile.NamedTemporaryFile('w',suffix='.js',encoding='utf-8',delete=False) as tmp:
            tmp.write(js); name=tmp.name
        p=subprocess.run(['node','--check',name],capture_output=True,text=True)
        Path(name).unlink(missing_ok=True)
        if p.returncode:
            msg=(p.stderr or p.stdout).strip().replace('\n',' | ')
            issues.append(f'{file}: inline script #{i} syntax error: {msg}')
    notes.append(f'{file}: {len(scan.ids)} ids, {len(scripts)} inline scripts checked')

# Cross-file required integration checks
if Path('index.html').exists():
    idx=Path('index.html').read_text(encoding='utf-8')
    required=[
        'src="home-workout.html',
        'src="women-body-mode.html',
        'data-view="home-workout"',
        'data-view="women"',
        'data-view-target="supplements"'
    ]
    for token in required:
        if token not in idx: issues.append(f'index.html: required integration missing: {token}')
    if 'id="coralPop"' in idx or 'getElementById("coralPop")' in idx:
        issues.append('index.html: Coral Club entry popup still present')
    if '<body class="maintenance-locked"' in idx or 'id="maintenanceScreen"' in idx:
        issues.append('index.html: maintenance lock still present in working branch')

report=[]
report.append('KAGIROV SITE VALIDATION')
report.append('=======================')
report.extend(notes)
report.append('')
if issues:
    report.append(f'FAIL: {len(issues)} issue(s)')
    report.extend('- '+x for x in issues)
else:
    report.append('PASS: no structural, local-link, duplicate-id, or inline-JavaScript syntax errors found.')
Path('validation-report.txt').write_text('\n'.join(report)+'\n',encoding='utf-8')
print('\n'.join(report))
sys.exit(1 if issues else 0)
