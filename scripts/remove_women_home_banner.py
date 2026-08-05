from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
pattern=r'\n\s*<article class="women-entry-card" id="womenHomeEntry">.*?</article>\s*\n'
s2,n=re.subn(pattern,'\n',s,count=1,flags=re.S)
if n!=1:
    raise SystemExit(f'Expected exactly one womenHomeEntry block, found {n}')
for text in ('Отдельная программа','BODY MODE · для женщин','Зал и дом, набор и снижение жира, питание, таймер и дневник прогресса в отдельном пространстве.'):
    if text in s2:
        raise SystemExit('Banner text still present: '+text)
p.write_text(s2,encoding='utf-8')
