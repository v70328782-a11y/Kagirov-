from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Remove Coral Club entry popup markup and startup script, while keeping the Supplements Coral Club block.
s=re.sub(r'<aside class="coral-pop" id="coralPop">.*?</aside>', '', s, count=1, flags=re.S)
s=re.sub(r'<script>\(\(\)=>\{const b=document\.getElementById\("coralPop"\);.*?</script>', '', s, count=1, flags=re.S)

# Make room for six navigation buttons.
s=s.replace('grid-template-columns: repeat(5,1fr);','grid-template-columns: repeat(6,1fr);',1)
s=s.replace('width: min(690px, calc(100% - 22px));','width: min(780px, calc(100% - 22px));',1)

# Women platform styles.
style_marker='/* WOMEN BODY MODE PLATFORM */'
if style_marker not in s:
    css='''\n\n    /* WOMEN BODY MODE PLATFORM */\n    .women-platform-frame{background:#efe8dc}\n    .women-entry-card{\n      margin-top:13px;\n      padding:19px;\n      display:flex;\n      align-items:center;\n      justify-content:space-between;\n      gap:14px;\n      border:1px solid rgba(103,77,52,.16);\n      border-radius:22px;\n      background:linear-gradient(135deg,#fff8ef,#f3e4d2);\n      box-shadow:0 13px 34px rgba(91,61,35,.09);\n    }\n    .women-entry-card h3{margin:0;color:var(--text);font-size:20px;letter-spacing:-.035em}\n    .women-entry-card p{margin:5px 0 0;color:var(--muted);font-size:11px;line-height:1.5}\n    .women-entry-badge{display:inline-flex;margin-bottom:8px;padding:5px 8px;border-radius:999px;background:#ead6c1;color:#76543b;font-size:9px;font-weight:900;letter-spacing:.08em;text-transform:uppercase}\n    .women-entry-card .btn{flex:0 0 auto}\n    @media(max-width:650px){\n      .bottom-nav{gap:2px;padding:6px}\n      .nav-btn{font-size:8px;gap:2px}\n      .nav-btn svg{width:17px;height:17px}\n      .women-entry-card{align-items:flex-start;flex-direction:column}\n      .women-entry-card .btn{width:100%}\n    }\n'''
    s=s.replace('\n  </style>',css+'\n  </style>',1)

# Add a home entry card directly after the main hero.
hero_end='''        </div>\n\n        <div class="stats-grid">'''
if 'womenHomeEntry' not in s:
    women_card='''        </div>\n\n        <article class="women-entry-card" id="womenHomeEntry">\n          <div>\n            <span class="women-entry-badge">Отдельная программа</span>\n            <h3>BODY MODE · для женщин</h3>\n            <p>Зал и дом, набор и снижение жира, питание, таймер и дневник прогресса в отдельном пространстве.</p>\n          </div>\n          <button class="btn btn-primary" data-go="women">Открыть</button>\n        </article>\n\n        <div class="stats-grid">'''
    if hero_end not in s:
        raise SystemExit('Home hero insertion point not found')
    s=s.replace(hero_end,women_card,1)

# Add iframe view before Progress.
progress_marker='''      <section class="view" data-view="progress">'''
if 'data-view="women"' not in s:
    women_view='''      <section class="view workout-platform-view" data-view="women">\n        <div class="workout-platform-head">\n          <div>\n            <h2>Женщинам · BODY MODE</h2>\n            <p>Отдельная система: тренировки в зале и дома, питание, цели, таймер и дневник прогресса</p>\n          </div>\n        </div>\n        <iframe class="workout-platform-frame women-platform-frame" src="women-body-mode.html?v=1" title="BODY MODE — женский фитнес" loading="eager"></iframe>\n      </section>\n\n'''
    if progress_marker not in s:
        raise SystemExit('Progress insertion point not found')
    s=s.replace(progress_marker,women_view+progress_marker,1)

# Add Women nav item before Progress.
progress_nav='''    <button class="nav-btn" data-view-target="progress"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20V10M10 20V4M16 20v-7M22 20H2"></path></svg><span>Прогресс</span></button>'''
if 'data-view-target="women"' not in s:
    women_nav='''    <button class="nav-btn" data-view-target="women"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"></circle><path d="M12 12v9M8.5 17h7"></path></svg><span>Женщинам</span></button>\n'''
    if progress_nav not in s:
        raise SystemExit('Progress nav insertion point not found')
    s=s.replace(progress_nav,women_nav+progress_nav,1)

# Required checks.
for required in ['data-view="women"','data-view-target="women"','women-body-mode.html?v=1','BODY MODE · для женщин']:
    if required not in s: raise SystemExit('Missing: '+required)
if 'id="coralPop"' in s: raise SystemExit('Coral popup markup still present')
if 'getElementById("coralPop")' in s: raise SystemExit('Coral popup JS still present')

p.write_text(s,encoding='utf-8')
