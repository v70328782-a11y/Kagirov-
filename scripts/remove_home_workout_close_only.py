from pathlib import Path

index_path = Path('index.html')
home_path = Path('home-workout.html')
index = index_path.read_text(encoding='utf-8')
home = home_path.read_text(encoding='utf-8')

# Keep fullscreen behavior unchanged; only ensure the cross is never shown.
index = index.replace(
    '.workout-platform-view.fullscreen .home-workout-close{display:grid;place-items:center;opacity:1;transform:scale(1)}',
    '.workout-platform-view.fullscreen .home-workout-close{display:none!important}'
)
index = index.replace(
    '.workout-platform-view.fullscreen .home-workout-close { display: grid; place-items: center; }',
    '.workout-platform-view.fullscreen .home-workout-close { display: none !important; }'
)

# Remove any previously queued extra back button/UI additions.
start = home.find('    .fullscreen-exit-back {')
if start >= 0:
    end = home.find('\n  </style>', start)
    if end >= 0:
        home = home[:start] + home[end:]

home = home.replace('<button id="fullscreenExitBack" class="fullscreen-exit-back" type="button" aria-label="Вернуться в основной сайт">←</button>\n  ', '')

marker = '  <script>\n    (() => {\n      "use strict";\n      const exitBack = document.getElementById("fullscreenExitBack");'
start = home.find(marker)
if start >= 0:
    end = home.find('  </script>', start)
    if end >= 0:
        home = home[:start] + home[end + len('  </script>'):]

index_path.write_text(index, encoding='utf-8')
home_path.write_text(home, encoding='utf-8')
