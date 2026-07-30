from pathlib import Path

index_path = Path('index.html')
home_path = Path('home-workout.html')
index = index_path.read_text(encoding='utf-8')
home = home_path.read_text(encoding='utf-8')

# 1) Remove the parent-level close button entirely.
parent_button = '        <button class="home-workout-close" id="closeHomeWorkoutFullscreen" type="button" aria-label="Свернуть домашнюю тренировку">×</button>\n\n'
index = index.replace(parent_button, '', 1)

# 2) Parent CSS must never render a close button.
index = index.replace(
    '    .home-workout-close { display:none;position:fixed;top:max(12px,env(safe-area-inset-top));right:12px;z-index:1003;width:46px;height:46px;border:1px solid rgba(103,77,52,.18);border-radius:15px;color:var(--text);background:rgba(255,253,249,.97);box-shadow:0 12px 34px rgba(91,61,35,.20);font-size:23px;cursor:pointer;opacity:0;transform:scale(.92);transition:opacity .2s ease .1s,transform .2s ease .1s}\n',
    '',
    1
)
index = index.replace(
    '    .workout-platform-view.fullscreen.home-screen .home-workout-close{display:grid!important;place-items:center;opacity:1;transform:scale(1)}\n',
    '',
    1
)
index = index.replace(
    '    .workout-platform-view.fullscreen:not(.home-screen) .home-workout-close{display:none!important}\n',
    '',
    1
)

# 3) Parent fullscreen controller no longer depends on a parent close button.
index = index.replace(
    "      const closeButton = document.getElementById('closeHomeWorkoutFullscreen');\n      if (!platform || !closeButton) return;",
    "      if (!platform) return;",
    1
)
index = index.replace("      closeButton.addEventListener('click', closeFullscreen);\n", '', 1)

# Keep screen class logic harmless, but it no longer controls any close UI.

# 4) Add the close button CSS inside the embedded app.
child_css = '''\n    .home-fullscreen-close{\n      display:none;\n      position:fixed;\n      top:max(12px,env(safe-area-inset-top));\n      right:12px;\n      z-index:90;\n      width:46px;\n      height:46px;\n      padding:0;\n      border:1px solid rgba(101,67,47,.15);\n      border-radius:15px;\n      color:var(--accent-dark);\n      background:rgba(255,253,249,.96);\n      box-shadow:0 12px 34px rgba(83,53,34,.18);\n      backdrop-filter:blur(14px);\n      -webkit-backdrop-filter:blur(14px);\n      place-items:center;\n      font-size:25px;\n      line-height:1;\n      cursor:pointer;\n    }\n    body.parent-fullscreen #homeScreen.active .home-fullscreen-close{display:grid}\n'''
if '.home-fullscreen-close{' not in home:
    home = home.replace('\n  </style>', child_css + '\n  </style>', 1)

# 5) Place the button physically inside homeScreen only.
child_button = '      <button id="homeFullscreenClose" class="home-fullscreen-close" type="button" aria-label="Закрыть полноэкранный режим">×</button>\n'
marker = '    <section id="homeScreen" class="screen active">\n'
if 'id="homeFullscreenClose"' not in home:
    if marker not in home:
        raise SystemExit('homeScreen marker not found')
    home = home.replace(marker, marker + child_button, 1)

# 6) Add fullscreen-state sync and close action in the child app.
child_script = '''\n  <script>\n    (()=>{\n      "use strict";\n      const closeButton=document.getElementById("homeFullscreenClose");\n      window.addEventListener("message",event=>{\n        if(event.origin!==window.location.origin)return;\n        if(event.data?.type!=="kagirov-home-workout-fullscreen-state")return;\n        document.body.classList.toggle("parent-fullscreen",Boolean(event.data.fullscreen));\n      });\n      closeButton?.addEventListener("click",()=>{\n        document.body.classList.remove("parent-fullscreen");\n        window.parent.postMessage({type:"kagirov-home-workout-collapse"},window.location.origin);\n      });\n    })();\n  </script>\n'''
if 'kagirov-home-workout-fullscreen-state' not in home:
    home = home.replace('\n</body>', child_script + '\n</body>', 1)

# Make main-card expansion explicitly identify the home screen.
home = home.replace(
    "window.parent.postMessage({ type: 'kagirov-home-workout-expand' }, window.location.origin);",
    "window.parent.postMessage({ type: 'kagirov-home-workout-expand', screen: 'home' }, window.location.origin);"
)

index_path.write_text(index, encoding='utf-8')
home_path.write_text(home, encoding='utf-8')
